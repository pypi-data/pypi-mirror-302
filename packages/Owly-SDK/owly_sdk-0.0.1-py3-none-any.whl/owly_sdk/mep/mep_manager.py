from owly_sdk.common.utils import makerequest, format_response
from owly_sdk.common.constants import DOMAIN_ORCH_BASE_URL
from pathlib import Path
import yaml
import time


class MepManager:
    """
    The MepManager class provides the functionality to manage MEPs such as listing, adding, describing, and removing MEPs.
    """
    def __init__(self, domain_orch_url, request_config):
        """
        Initialize the MepManager class with the domain_orch_url and request_config.
        
        :param domain_orch_url: The URL of the Orchestrator.
        :param request_config: The RequestConfig object to be used for making requests.
        """
        self.mep_url = f"{domain_orch_url}/resource/mep"
        self.request_config = request_config


    def add_mep(self, file: Path):
        """
        Add a mep to the list of registered meps.
        Provide the path of the yaml file which
        contains the mep(s) defination.
        You can add multiple meps at the same time. If mentioned in the same file.
        
        :param file: The path to the yaml file containing the mep(s) defination.
        
        :return: Success message or error message.
        """
        start_time = time.time()
        with open(file) as f:
            meps = yaml.safe_load_all(f)
            for mep in meps:
                r, s = makerequest(_type='post',url=self.mep_url,body=mep)
                if s == 201 and r['status'] == 'REGISTERED':
                    end_time = time.time() - start_time
                    return f"mep {mep['name']} succesfully registered in {end_time} seconds"
                else:
                    if 'reason' in r.keys():
                        return f"mep {mep['name']} can not be registered reason {r['reason']}"
                    return r


    def list_meps(self, output: str = None):
        """
        List of meps registered in the database
        
        :param output: Output format (json/yaml).
        
        :return: List of meps
        """
        response, _ = makerequest(_type='get', url=self.mep_url, params={'mepId':'all'})
        
        formatted_meps = []

        keys = ['name', 'status']
        for mep in response:
            formatted_mep = {key: mep[key] for key in keys}
            
            formatted_meps.append(formatted_mep)
            
        return format_response(formatted_meps, output)


    def describe_mep(self, name: str, output: str = None):
        """
        Describe the current state of the mep NAME. 

        :param name: The name of the mep to describe.
        :param output: Format of the output (json/yaml).
        
        :return: The response from the API or an error message.
        """
        response, _ = makerequest(_type='get', url=self.mep_url, params={'mepId':name})

        return format_response(response, output)


    def remove_mep(self, name: str):
        """
        Remove the mep NAME from the list of registered meps.
        Normally if there are workloads running on the mep 
        it is not possible to remove it.
        
        :param name: The name of the mep to remove.
        
        :return: Response from the API.
        """
        response, _ = makerequest(_type='delete', url=self.mep_url, params={'mepId':name})

        return response