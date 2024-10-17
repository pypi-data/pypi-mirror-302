from owly_sdk.common.utils import makerequest
from pathlib import Path
import time
import yaml


class VimManager:
    """
    The VimManager class provides the functionality to manage VIMs such as listing, adding, describing, and removing VIMs.
    """
    def __init__(self, domain_orch_url, request_config):
        """
        Initialize the VimManager class with the domain_orch_url and request_config.
        
        :param domain_orch_url: The URL of the Orchestrator.
        :param request_config: The RequestConfig object to be used for making requests.
        """
        self.domain_orch_url = domain_orch_url
        self.request_config = request_config

    def _format_vim(self, vims: list, wide: bool = False):
        """
        Format the VIMs to display only the required information.

        :param vims: The list of VIMs to be formatted.
        :param wide: Whether to display more information about the VIMs. Default is False.
        
        :return: The formatted VIMs.
        """
        formatted_vims = []
        for vim in vims:
            keys = ['name', 'status', 'url']
            wide_keys = ['vimType']
            
            formatted_response = {k: vim[k] for k in keys}

            if wide:
                for k in wide_keys:
                    formatted_response[k] = vim[k]
            
            formatted_vims.append(formatted_response)
            
        return formatted_vims

    def list_vims(self, vim_id: str = 'all', wide: bool = False):
        """
        Fetch the list of VIMs registered in the database.

        :param vim_id: ID of the VIM to be listed. If not provided, all VIMs will be listed.
        :param wide: Whether to display more information about the VIMs. Default is False.
        
        :return: List of VIMs registered in the database or a specific VIM if vim_id is provided.
        """
        response, _ = makerequest(
            _type='get',
            url=f"{self.domain_orch_url}/resource/vim",
            params={'vimId': vim_id},
            config=self.request_config
        )
        
        if isinstance(response, dict):
            if 'status' in response and response['status'] == "NOTFOUND":
                return response
            response = [response]
        
        formatted_vims = self._format_vim(response, wide)
        
        if vim_id == 'all':
            return formatted_vims
        
        return formatted_vims[0]

    def add_vim(self, file: Path):
        """
        Add a VIM to the list of registered VIMs.
        Provide the path of the yaml file which
        contains the VIM(s) definition.
        You can add multiple VIMs at the same time if mentioned in the same file.

        :param file: The path of the YAML file containing the VIM(s) definition.

        :return: A string message indicating the success or failure of the registration process.
        """
        start_time = time.time()
        with open(file) as f:
            vims = yaml.safe_load_all(f)
            for vim in vims:
                if 'kind' not in vim.keys() or vim['kind'] != 'vim':
                    return 'Not a valid VIM template, kind is not vim'
                r, s = makerequest(
                    _type='post',
                    url=f"{self.domain_orch_url}/resource/vim",
                    body=vim,
                    config=self.request_config
                )
                if s == 201 and r['status'] == 'REGISTERED':
                    end_time = time.time() - start_time
                    return f"VIM {vim['name']} successfully registered in {end_time} seconds"
                else:
                    return f"VIM {vim['name']} cannot be registered: {r['reason']}"

    def describe_vim(self, name: str):
        """
        Describe the current state of the VIM NAME.
        
        :param name: The name of the VIM to be described.
        
        :return: The response from the API.
        """
        response, _ = makerequest(
            _type='get',
            url=self.domain_orch_url + '/resource/vim',
            params={'vimId': name},
            config=self.request_config
        )
        
        return response

    def remove_vim(self, name: str, forcefully: bool = False):
        """
        Remove the VIM NAME from the list of registered VIMs.
        Normally if there are workloads running on the VIM, 
        it is not possible to remove it. 
        
        :param name: The name of the VIM to be removed.
        :param forcefully: If True, the VIM will be removed forcefully. Default is False.
        
        :return: A string message indicating the success or failure of the removal process.
        """
        response, status_code = makerequest(
            _type='delete',
            url=self.domain_orch_url + '/resource/vim',
            params={'vimId': name, 'forcefully': forcefully, 'wipe': False},
            config=self.request_config
        )

        if status_code == 204:
            return f"VIM {name} successfully removed"      
        else:
            if 'instances' in response.keys():
                return f"VIM {name} could not be removed because {response['reason']} instances {response['instances']}"
            else:
                return f"VIM {name} could not be removed because {response['reason']}"
