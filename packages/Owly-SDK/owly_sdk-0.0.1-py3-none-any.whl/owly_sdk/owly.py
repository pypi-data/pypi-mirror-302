from owly_sdk.common.request_config import RequestConfig
from owly_sdk.vim.vim_manager import VimManager
from owly_sdk.ns.ns_manager import NsManager
from owly_sdk.mep.mep_manager import MepManager

class Owly:
    def __init__(self, domain_orch_url : str, request_config : RequestConfig = RequestConfig()):
        self.domain_orch_url = domain_orch_url
        self.request_config = request_config

        self.vim = VimManager(domain_orch_url, request_config)
        self.ns = NsManager(domain_orch_url, request_config)
        self.mep = MepManager(domain_orch_url, request_config)
