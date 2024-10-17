import typer
import yaml
import time
import uuid
import base64
import yaml
from pathlib import Path
from owly_sdk.common.utils import makerequest, format_response


class NsManager:
    """
    The NsManager class provides the functionality to manage Network Services (NS) such as creating, listing, describing, and deleting NS.
    """
    def __init__(self, domain_orch_url, request_config):
        """
        Initialize the NsManager class with the domain_orch_url and request_config.
        
        :param domain_orch_url: The URL of the Orchestrator.
        :param request_config: The RequestConfig object to be used for making requests.
        """
        self.domain_orch_url = domain_orch_url
        self.request_config = request_config
        
        
    def _nscreate(self, service,file):
        '''
        onboard network functions of a network service
        
        :param service: The network service description
        :param file: The path to the yaml file
        
        :return: The network service description
        '''
        if 'packageId' not in service.keys():
            service.update({'packageId':str(uuid.uuid4())})
        for vnf in service['vnfs']:
            for container in vnf['osContainerDesc']:
                if 'bootData' in container.keys():
                    for data in container['bootData']:
                        data.update({'data': (base64.b64encode((open(Path(file.parent) / data['file']).read()).encode('ascii'))).decode('ascii')})
        [ vnf.update({'vnfDId': str(uuid.uuid4())}) for vnf in service['vnfs'] ]
        if not isinstance(service['vimId'],list):
            service.update({'vimId':[service['vimId']]})
        r, s = makerequest(_type='post',url= f"{self.domain_orch_url}/create/ns",body=service)
        if s!=201:
            raise typer.Exit(code=1)
        return service


    def create_ns(self, file):
        """
        Creates a Network Service (NS) from a YAML file.
        
        :param file: The path to the YAML file containing the NS description.
        
        :return: None
        """
        
        try:
            # Convert to Path object if it's a string
            if isinstance(file, str):
                file = Path(file)

            with open(file) as f:
                services = yaml.safe_load_all(f)
                for service in services:
                    service = self._nscreate(service=service,file=file)
        except Exception as e:
            return e


    def _format_ns(self, list_ns, wide=False):
        """
        Formats the network service details for display.
        
        :param list_ns: The list of network services.
        :param wide: Indicates whether to display more details. Default is False.
        
        :return: The formatted network service details.
        """
        formatted_ns = []
        
        for ns in list_ns:
            vnfs = []
            duration = 0
        
            for vnf in ns['vnfs']:
                formatted_vnf = {
                    'vnfName': vnf['vnfName'],
                    'status': vnf['status'],
                }
                
                if vnf['status'] == 'INSTANTIATED':
                    formatted_vnf['interfaces'] = [
                        f"{networkDetail['ipaddress']}({networkDetail['interface']})"
                        for networkDetail in vnf['networkDetail']
                    ]
                    
                    onboarding_duration = float(vnf['onboardingDuration'])
                    instance_creation_duration = float(vnf['instanceCreationDuration'][:-1]) # Remove the 's' at the end
                    duration += onboarding_duration + instance_creation_duration

                    
                vnfs.append(formatted_vnf)

            ns = {
                'name': ns['name'],
                'status': ns['status'],
                'vnfs': vnfs
            }
            
            if wide:
                ns['duration'] = duration
                
            formatted_ns.append(ns)
        
        return formatted_ns


    def list_nss(self, name="all",vf_name="", latest="yes", wide=False):
        """
        Fetches the list of Network Functions (NF) from the API.
        
        :param name: The name of the NF to search for. Default is "all".
        :param vf_name: The name of the VF to search for. Default is "". NOT WORKING
        :param latest: Indicates whether only the latest NFs should be returned. Default is "yes". NOT WORKING
        :param wide: Indicates whether to display more details. Default is False.

        :return: The response from the API.
        """
        try:
            res, status_code = makerequest(
                _type='get',
                url=f'{self.domain_orch_url}/list/vnf',
                params={'name': name, 'vfName': vf_name, 'latest': latest}
            )
            
            if (isinstance(res, list) or isinstance(res, dict)) and status_code == 200:
                if 'status' in res and res['status'] == "NOTFOUND":
                    return res
                if name != "all":
                    res = [res]

                formatted_ns = self._format_ns(res, wide)
                if name == "all":
                    return formatted_ns
                return formatted_ns[0]
            
            return "Encountered an error in fetching the list of onboarded services"
        
        except Exception as e:
            return e


    def describe_ns(self, name: str, output: str = None):
        """
        Describe a network service NAME.

        :param name: The name of the network service to describe.
        :param output: Format of the output (json/yaml).
        
        :return: The response from the API or an error message.
        """
        try:
            response, status_code = makerequest(
                _type='get',
                url=f"{self.domain_orch_url}/list/vnf",
                params={'name': name}
            )

            if status_code == 200:
                return format_response(response, output)
            else:
                return Exception(response.get('message', 'Unknown error'))

        except Exception as e:
            return e


    def top(
        self,
        vim: str,
        name: str,
        vnf: str = None,
        output: str = None,
    ):
        """
        Performs top on network service VIM_NAME NAME.
        Provides information related to computational 
        resources consumed by the network service
        
        :param vim: The VIM ID
        :param name: The name of the network service
        :param vnf: The name of the VNF
        :param output: The format of the output (json/yaml). Default is 'json'.
        """
        r,s = makerequest(_type='get',url=f"{self.domain_orch_url}/metrics/vnf",params={'name':name, 'vnfName':vnf, 'vimId':vim})
        if s in [200,404,400]:        
            return format_response(r, output)
        else:
            return "Encounted an error in fetching the list of onboarded services"
        

    def delete_ns(self, name: str):
        """
        Deletes a Network Function (NF) from the API.

        :param name: The name of the NF to delete.
        
        :return: None if the NF is deleted successfully, else an error message.
        """
        
        # Check if the NF exists
        r, s = makerequest(
                _type='get',
                url=f"{self.domain_orch_url}/list/vnf",
                params={'name':name,'latest':'no'}
            )
        
        if s == 200 and r['status'] == 'NOTFOUND':
            return r

        elif s == 200 and r['status'] in ['INSTANTIATED','TERMINATING']:
            package_id = r['packageId']
            vim_id = r['vimId']
            vnfs = [{'vnfName':vnf['vnfName'],'vnfDId':vnf['vnfDId'],'vnfInstanceId':vnf['vnfInstanceId']} for vnf in r['vnfs']]
            body = {'packageId':package_id,'vnfs':vnfs}
            count = 0
            start_time = time.time()
            r, s = makerequest(_type='post',url=f"{self.domain_orch_url}/terminate/vnf", body=body)
            if s == 201 and r['status'] == "TERMINATING":
                while True:
                    r,s = makerequest(_type='get',url=f"{self.domain_orch_url}/terminate/vnf",params={'packageId':package_id})
                    if s==200 and r['status']=='TERMINATED':
                        end_time = time.time() - start_time
                        terminated = True
                        break
                    if count == len(vnfs) * 4:
                        raise typer.Exit(code=1)
                    count +=1
                    time.sleep(0.5)
            elif s == 500:
                raise typer.Exit(code=1)
            else:
                return r
        elif s == 200 and r['status'] in ['ONBOARDED','PARTIAL','INSTANTIATING','FAILED']:
            package_id = r['packageId']
            vim_id = r['vimId']
            terminated = True
        #OFFBOARD
        if terminated:
            body = {'packageId':package_id,'vimId':vim_id}
            count = 0
            r,s = makerequest(_type='post',url=f"{self.domain_orch_url}/offboard/vnf",body=body)
            if s == 201 and r['status'] == 'OFFBOARDING':
                while True:
                    r,s = makerequest(_type='get',url=f"{self.domain_orch_url}/offboard/vnf",params={'packageId':package_id})
                    if s==200 and r['status']=='OFFBOARDED':
                        break
                    if count == 100: #it means timeout is 20 * 0.5 seconds
                        raise typer.Exit(code=1)
                    count +=1
                    time.sleep(0.5)