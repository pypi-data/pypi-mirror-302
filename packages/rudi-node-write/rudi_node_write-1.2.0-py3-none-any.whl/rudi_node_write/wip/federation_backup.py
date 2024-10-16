from concurrent.futures import as_completed, ThreadPoolExecutor
from os import cpu_count
from time import sleep, time
from urllib.request import urlopen

from rudi_node_write.connectors.io_rudi_manager_write import RudiNodeManagerConnector
from rudi_node_write.connectors.rudi_node_auth import RudiNodeAuth
from rudi_node_write.rudi_node_writer import RudiNodeWriter
from rudi_node_write.utils.file_utils import check_is_dir, check_is_file, read_json_file, write_json_file
from rudi_node_write.utils.log import log_d, log_e, log_w
from rudi_node_write.utils.str_utils import slash_join
from rudi_node_write.utils.type_date import Date

federation_data = {}


MAX_WORKERS = 0
DEFAULT_WAIT_TIME = 0.3


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
    if not pm_url.startswith("http"):
        pm_url = "https://" + pm_url

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
    here = "RudiNodeFederation backup"

    test_dir = check_is_dir("../dwnld")
    data_dir = check_is_dir("../data")
    creds_file = check_is_file("../creds/test_creds_manager.json")
    servers_file = check_is_file("../creds/servers.json")

    servers_list = read_json_file(servers_file)
    nodes = servers_list.get("nodes")

    # nodes = {"exatow": nodes["exatow"]}

    nb_nodes = len(nodes.keys())

    rudi_node_creds = read_json_file(creds_file)
    auth = RudiNodeAuth.from_json(rudi_node_creds)
    url = rudi_node_creds["url"]
    pm_url = url if url.endswith("prodmanager") else slash_join(url, "prodmanager")
    assert isinstance(auth, RudiNodeAuth)
    errors = {}
    if MAX_WORKERS:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(backup_node, node_name, nodes[node_name]): node_name for node_name in nodes}
            for future in as_completed(futures, timeout=120):
                try:
                    future_result = future.result()
                except Exception as err:
                    node_name = futures[future]
                    log_e(here, "Backup failed for node:", futures[future])
                    future_result = {}
                    errors[node_name] = err
                node_name = futures[future]
                future_result["node_name"] = None
                federation_data[node_name] = future_result
    else:
        # federation_info = {nodes[node_name] for node_name in nodes}

        for node_name in nodes:
            log_d(here, "----- node_name", node_name)
            node_info = nodes[node_name]
            try:
                node_data = backup_node(node_name, node_info)
                federation_data[node_name] = node_data

                write_json_file(destination_file_path=slash_join(data_dir, node_name + ".json"), json_dict=node_data)
            except Exception as e:
                errors[node_name] = e
                node_data = None

            federation_data[node_name] = node_data

    write_json_file(destination_file_path=slash_join(data_dir, "_federation.json"), json_dict=federation_data)
    if len(errors.keys()) > 0:
        log_e(here, "Backup failed for some nodes:", errors)
    else:
        log_d(here, "All nodes were successfully backed up")

    log_d(here, "exec. time", time() - begin)

# urls = [
#     # "http://www.foxnews.com/",
#     "http://www.cnn.com/",
#     "http://europe.wsj.com/",
#     "http://www.bbc.co.uk/",
#     "http://some-made-up-domain.com/",
# ]

# url_dict = {url + "r": url for url in urls}
# print(url_dict)


# def load_url(url, timeout):
#     with urlopen(url, timeout=timeout) as conn:
#         return conn.read()


# with ThreadPoolExecutor(max_workers=5) as executor:
#     future_to_url = {executor.submit(load_url, url, 60): url for url in urls}
#     for future in as_completed(future_to_url):
#         url = future_to_url[future]
#         try:
#             data = future.result()
#         except Exception as exc:
#             print("%r generated an exception: %s" % (url, exc))
#         else:
#             print("%r page is %d bytes" % (url, len(data)))

# print(cpu_count() * 5)
# pool = ThreadPoolExecutor()
# print(pool._max_workers)
