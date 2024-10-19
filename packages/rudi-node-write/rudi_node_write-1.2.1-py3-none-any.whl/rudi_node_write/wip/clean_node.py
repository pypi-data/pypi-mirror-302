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

if __name__ == "__main__":  # pragma: no cover
    begin = time()
    here = "RudiNodeClean"

    test_dir = check_is_dir("../dwnld")
    data_dir = check_is_dir("../data")
    creds_file = read_json_file("../creds/creds_release.json")
    auth = RudiNodeAuth(b64url_auth=creds_file["b64auth"])
    node = RudiNodeWriter(creds_file["pm_url"], auth, keep_connection=True)

    for meta in node.metadata_list:
        changed = False
        print(meta["global_id"], ":", meta["access_condition"]["confidentiality"]["gdpr_sensitive"])
        if meta["access_condition"]["confidentiality"]["gdpr_sensitive"] == None:
            meta["access_condition"]["confidentiality"]["gdpr_sensitive"] = False
            changed = True
        # try:
        #     if meta["geography"]["geographic_distribution"]["geometry"] == None:
        #         del meta["geography"]["geographic_distribution"]["geometry"]
        #         changed = True
        # except:
        #     pass
        # try:
        #     if meta["metadata_info"]["metadata_dates"]["published"] == None:
        #         del meta["metadata_info"]["metadata_dates"]["published"]
        #         changed = True
        # except:
        #     pass
        if changed:
            node.put_metadata(meta)
