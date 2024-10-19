from abc import ABC
from concurrent.futures import as_completed, ThreadPoolExecutor
from dataclasses import dataclass
from os import cpu_count
from time import sleep, time
from typing import Callable
from urllib.request import urlopen

from rudi_node_write.connectors.io_connector import HTTP_REQUEST_METHODS
from rudi_node_write.connectors.io_rudi_api_write import RudiNodeApiConnector
from rudi_node_write.connectors.io_rudi_jwt_factory import RudiNodeJwtFactory
from rudi_node_write.connectors.io_rudi_manager_write import RudiNodeManagerConnector
from rudi_node_write.connectors.rudi_node_auth import RudiNodeAuth
from rudi_node_write.rudi_node_writer import RudiNodeWriter
from rudi_node_write.utils.file_utils import check_is_dir, check_is_file, read_json_file, write_json_file
from rudi_node_write.utils.log import log_d, log_e, log_w
from rudi_node_write.utils.str_utils import slash_join
from rudi_node_write.utils.type_date import Date
from rudi_node_write.utils.url_utils import ensure_http, ensure_url_startswith

federation_data = {}

DEFAULT_WAIT_TIME = 0.3

NO_PORTAL = "No portal connected"


def ensure_url_startswith_api(url):
    return ensure_url_startswith(url, "api")


class Module:
    MANAGER = "manager"
    CATALOG = "catalog"
    STORAGE = "storage"


class HttpMethods:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


@dataclass
class ModuleRequest:
    action_name: str
    module_name: Module = Module.MANAGER
    req_method: HttpMethods = HttpMethods.GET
    url_bit: str = "/"
    post_treatment: Callable = lambda x: x
    can_fail: bool = False
    keep_alive: bool = False
    should_log_request: bool = False
    should_log_response: bool = False


# TODO: envoyer une suite/liste de traitements sur les nœuds:
# - quel connecteur cible (node_write ? catalog ? media ?)
# - quelle URL requête (url_bit )
# - quel post-traitement
#
# => Input: objet à définir
# #
# [{
#     target: Module.MANAGER | Module.CATALOG | MEDIA,
#     url_bit,
#     post_treatment on answer (defaulted to x=>x)
#     opts: keep_alive, log request, log response (defaulted to False)
# }]
class NodeConnector:
    def __init__(
        self,
        node_name,
        catalog_url,
        catalog_auth,
        manager_url,
        manager_auth,
    ):
        self._node_name = node_name
        self._catalog = CatalogConnector(node_name=node_name, module_url=catalog_url, module_auth=catalog_auth)
        self._manager = ManagerConnector(node_name=node_name, module_url=manager_url, module_auth=manager_auth)


class ModuleConnector(ABC):
    def __init__(self, node_name: str, get_connector: Callable, get_headers: Callable):
        self._node_name = node_name
        self._get_connector = get_connector
        self._get_headers = get_headers

    @property
    def node_name(self):
        return self._node_name

    @property
    def module_name(self):
        raise NotImplementedError("This function should be implemented")

    @property
    def connector(self):
        return self._get_connector()

    @property
    def headers(self):
        return self._get_headers()

    @staticmethod
    def create_connector(node_name, module_name, module_url, module_auth):
        if module_name == Module.MANAGER:
            return ManagerConnector(node_name=node_name, module_url=module_url, module_auth=module_auth)
        if module_name == Module.CATALOG:
            return CatalogConnector(node_name=node_name, module_url=module_url, module_auth=module_auth)

    def module_request(
        self,
        request: ModuleRequest,
    ):
        return self.request(
            req_method=request.req_method,
            url_bit=request.url_bit,
            post_treatment=request.post_treatment,
            can_fail=request.can_fail,
            keep_alive=request.keep_alive,
            should_log_request=request.should_log_request,
            should_log_response=request.should_log_response,
        )

    def request(
        self,
        req_method: HttpMethods,
        url_bit: str,
        post_treatment=lambda x: x,
        can_fail: bool = False,
        keep_alive: bool = False,
        should_log_request: bool = False,
        should_log_response: bool = False,
    ):
        try:
            node_res = self.connector.request(
                req_method=req_method,
                relative_url=ensure_url_startswith_api(url_bit),
                headers=self.headers,
                keep_alive=keep_alive,
                should_log_request=should_log_request,
                should_log_response=should_log_response,
            )
            return post_treatment(node_res)
        except Exception as err:
            if can_fail:
                raise err
            return f"ERR: {err}"


class ManagerConnector(ModuleConnector):
    def __init__(self, node_name, module_url, module_auth):
        self._node_name = node_name
        self._node_writer = RudiNodeWriter(pm_url=module_url, auth=module_auth, headers_user_agent="ManagerConnector")
        super().__init__(
            node_name=node_name,
            get_connector=lambda: self._node_writer._pm_connector,
            get_headers=lambda: self._node_writer._pm_connector._pm_headers,
        )


class CatalogConnector(ModuleConnector):
    def __init__(self, node_name, module_url, module_auth):
        self._node_name = node_name
        self._catalog_connector = RudiNodeApiConnector(
            server_url=module_url, jwt_factory=module_auth, headers_user_agent="CatalogConnector"
        )
        super().__init__(
            node_name=node_name,
            get_connector=lambda: self._catalog_connector,
            get_headers=lambda: self._catalog_connector._headers,
        )


class RudiNodeFederation:
    def __init__(self, config_file_path, credentials_file_path, local_jwt_factory):
        self.jwt_factory = local_jwt_factory
        self.load_federation_conf(config_file_path, credentials_file_path)

    def load_federation_conf(self, config_file_path, credentials_file_path):
        self._conf = read_json_file(config_file_path)
        self._creds = read_json_file(credentials_file_path)
        self._connectors = {}

        # self._conf["nodes"] = {"exatow": self._conf["nodes"]["exatow"], "rm": self._conf["nodes"]["rm"]}

        for node_name, node_conf in self.nodes_conf.items():
            print(node_name)
            node_url = ensure_http(node_conf["url"])

            pm_url = ensure_http(
                node_conf["pmback"] if node_conf.get("pmback") is not None else slash_join(node_url, "prodmanager")
            )

            self._connectors[node_name] = {
                Module.MANAGER: ManagerConnector(
                    node_name=node_name,
                    module_url=pm_url,
                    module_auth=RudiNodeAuth(b64url_auth=self.get_creds(node_name).get("b64auth")),
                ),
                Module.CATALOG: CatalogConnector(
                    node_name=node_name, module_url=node_url, module_auth=self.jwt_factory
                ),
            }

    @property
    def nodes_conf(self):
        return self.get_node_conf()

    def get_node_conf(self, node_name=None):
        if node_name is None:
            return self._conf["nodes"]
        return self._conf["nodes"].get(node_name)

    def get_creds(self, node_name):
        if self._creds.get(node_name):
            return self._creds[node_name]
        return self._creds["defaults"]

    def request(
        self,
        node_name,
        module_name,
        req_method,
        url_bit,
        post_treatment=lambda x: x,
        can_fail=False,
        keep_alive=False,
        should_log_request=False,
        should_log_response=False,
    ):
        if module_name == Module.MANAGER:
            connector = self._managers[node_name]
            headers = connector._pm_headers
            url_bit = ensure_url_startswith_api(url_bit)
        elif module_name == Module.CATALOG:
            connector = self._catalogs[node_name]
            headers = connector._headers
            url_bit = ensure_url_startswith_api(url_bit)
        else:
            raise NotImplementedError("Not yet available")
        try:
            node_res = connector.request(
                req_method=req_method,
                relative_url=url_bit,
                headers=headers,
                keep_alive=keep_alive,
                should_log_request=should_log_request,
                should_log_response=should_log_response,
            )
            return post_treatment(node_res)
        except Exception as err:
            if can_fail:
                raise err
            return f"ERR: {err}"

    def batch_request_node(self, connectors, request_list, max_workers=0):
        res = {}
        err = {}
        for request in request_list:
            if isinstance(request, ModuleRequest):
                res[request.action_name] = connectors[request.module_name].module_request(request)
            else:
                (action_name, module_name, req_method, url_bit, post_treatment) = request
                res[action_name] = connectors[module_name].request(
                    req_method=req_method,
                    url_bit=url_bit,
                    post_treatment=post_treatment,
                )
        return res

    def batch_requests(self, request_list, max_workers=0):
        """
        @param request_dict: a dict with module names as keys and a list of actions {action_name: (module_name, req_method , url_bit , post_treatment)}}
        """
        res = {}
        err = {}
        if not max_workers:
            for node_name, connectors in self._connectors.items():
                res[node_name] = self.batch_request_node(connectors, request_list)
        else:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {
                    executor.submit(connectors[request.module_name].module_request, request): request
                    for request in request_list
                }
                for future in as_completed(futures, timeout=120):
                    try:
                        future_result = future.result()
                    except Exception as err:
                        node_name = futures[future]
                        log_e(here, "Request failed:", futures[future])
                        future_result = {}
                        errors[request.node_name] = err
                    node_name = futures[future]
                    future_result["node_name"] = None
                    federation_data[node_name] = future_result
        return res

    def try_request(req, wait_time=DEFAULT_WAIT_TIME, quit_on_fail=True):
        fun = "try_request"
        sleep(wait_time)
        try:
            return req
        except Exception as err:
            if quit_on_fail:
                return "FAIL"
            # Let's try one more time
            return try_request(req, wait_time, True)

    def backup_node(node_name, node_info):
        node_url = node_info["url"]
        pm_url = node_info["pmback"] if node_info.get("pmback") is not None else (slash_join(node_url, "prodmanager"))
        ensure_http(pm_url)

        node = RudiNodeWriter(pm_url=pm_url, auth=auth, keep_connection=True)

        node_data = {"node_name": node_name, "pm_url": node.pm_url}
        node_data["media_url"] = try_request(node.media_url)
        node_data["init_data"] = try_request(node.init_data)
        node_data["organization_list"] = try_request(node.organization_list)
        node_data["contact_list"] = try_request(node.contact_list)
        node_data["metadata_list"] = try_request(node.metadata_list)
        node_data["enums"] = try_request(node.enums)
        node_data["media_list"] = try_request(node.media_list)

        node.close_connection()
        return node_data


if __name__ == "__main__":  # pragma: no cover
    begin = time()
    here = "RudiNodeFederation"

    test_dir = check_is_dir("../dwnld")
    data_dir = check_is_dir("../data")
    creds_file = check_is_file("../creds/federation_creds.json")
    servers_file = check_is_file("../creds/servers.json")

    try:
        local_jwt_factory = RudiNodeJwtFactory("http://localhost:4040", {"sub": "rudi_api_pm"})
    except:
        raise ConnectionError("Local crypto module is apparently not launched!")

    rudi_federation = RudiNodeFederation(
        config_file_path=servers_file, credentials_file_path=creds_file, local_jwt_factory=local_jwt_factory
    )

    def get_token(x):
        if x == NO_PORTAL:
            return NO_PORTAL
        try:
            return x["access_token"].replace(r"[\w-]+(\.[\w-]+){2}", "valid_jwt")
        except:
            return x

    res = rudi_federation.batch_requests(
        [
            ModuleRequest(
                action_name="portal_url",
                module_name=Module.MANAGER,
                url_bit="front/portal-url",
                can_fail=True,
                should_log_request=True,
            ),
            ModuleRequest(
                action_name="portal_token",
                module_name=Module.CATALOG,
                url_bit="admin/portal/token",
                post_treatment=get_token,
            ),
        ]
    )
    portal_connections_file = "rudi_node_write/wip/portal_connect.json"
    reworked_portal_connect_file = "rudi_node_write/wip/portal_connect_final.json"
    # res = read_json_file("rudi_node_write/wip/portal_connect.json")
    print(res)
    write_json_file(destination_file_path=portal_connections_file, json_dict=res)
    final_res = {}
    for node_name, node_res in res.items():
        portal_url = node_res["portal_url"]
        print(portal_url)
        portal_connection = (
            node_res["portal_token"]
            if not node_res["portal_token"].startswith("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9")
            else "OK"
        )
        if final_res.get(portal_url) is None:
            final_res[portal_url] = {node_name: portal_connection}
        final_res[portal_url][node_name] = portal_connection
    # print(res)
    # portal_urls = rudi_federation.manager_get("front/portal-url")
    # node_catalog_url = rudi_federation.manager_get("front/ext-api-url")
    # catalog_portal_token = rudi_federation.catalog_get("portal/token", extract_token_from_http_res)
    # node_portals = {}
    # for node_name, portal_url in portal_urls.items():
    #     node_info = {"catalog_url": node_catalog_url[node_name], "portal_token": catalog_portal_token}
    #     if node_portals.get(portal_url) is None:
    #         node_portals[portal_url] = {node_name: node_info}
    #     else:
    #         node_portals[portal_url][node_name] = node_info

    # print(node_portals)
    print(final_res)
    write_json_file(destination_file_path=reworked_portal_connect_file, json_dict=final_res)

print()

# print(chr(sum(range(ord(min(str(not ())))))))
