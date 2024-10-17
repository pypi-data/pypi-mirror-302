from owly_sdk.common.utils import makerequest
from pathlib import Path
import yaml
import json
import time
import typer
import uuid
import base64


class MecnsManager:
    """
    The MecnsManager class provides the functionality to manage MEC Application Services such as
    creating, listing, describing, and deleting MEC Application Services.
    """
    def __init__(self, domain_orch_url, request_config):
        self.domain_orch_url = domain_orch_url
        self.request_config = request_config
        

    def format_mecns(mecns):
        """
        Format the mecns response.
        
        :param mecns: The list of mecns
        
        :return: The list of formatted mecns
        """
        formatted_mecns = []

        keys = ['name', 'status', 'apps']
        app_keys = ['appName', 'status']
        for mecsn in mecns:
            formatted_apps = []
            
            for app in mecsn['apps']:
                formatted_app = {key: app[key] for key in app_keys}
                
                if app['status'] == 'INSTANTIATED':
                    formatted_app['interfaces'] = [
                        f"{networkDetail['ipaddress']}({networkDetail['interface']})"
                        for networkDetail in app['networkDetail']
                    ]
                formatted_apps.append(formatted_app)
                
            
            mecsn['apps'] = formatted_apps   
            formatted_mecsn = {key: mecsn[key] for key in keys}
            formatted_mecns.append(formatted_mecsn)
            
        return formatted_mecns


    def list_mecns(self, output: str = None):
        """
        List of mecsns registered in the database
        
        :param output: Output format (json/yaml)
        
        :return: List of mecsns
        """
        r, _ = makerequest(_type='get',url=f"{self.domain_orch_url}/list/app",params={'name':'all','latest':'yes'})
        
        formatted_mecsns = self.format_mecns(r)

        if output == 'yaml':
            return yaml.dump(formatted_mecsns)
        if output == 'json':
            json.dumps(formatted_mecsns)
        return formatted_mecsns

    def mecappservicecreate(self, service, file):
        '''
        onboard network functions of a mec application service
        
        :param service: mec application service configuration
        :param file: path to the yaml file containing the mec application service configuration
        
        :return: The mec application service configuration
        '''
        if 'packageId' not in service.keys():
            service.update({'packageId':str(uuid.uuid4())})
        for app in service['apps']:
            for container in app['osContainerDesc']:
                if 'bootData' in container.keys():
                    for data in container['bootData']:
                        data.update({'data': (base64.b64encode((open(Path(file.parent) / data['file']).read()).encode('ascii'))).decode('ascii')})
        [ app.update({'appDId': str(uuid.uuid4())}) for app in service['apps'] ]
        if not isinstance(service['vimId'],list):
            service.update({'vimId':[service['vimId']]})
        if 'mepId' in service.keys() and not isinstance(service['mepId'],list):
            service.update({'mepId':[service['mepId']]})
        r, s = makerequest(_type='post',url= f"{self.domain_orch_url}/create/mecs",body=service)
        if s!=201:
            raise typer.Exit(code=1)
        return service


    def create_mecns(self, file: Path):
        """
        Create a mec application service.
        Provide the path of the yaml file which 
        contains the mec application service defination, its apps.

        :param file: The path to the yaml file containing the mec application service defination.
        
        :return: Success message or error message.
        """
        try:
            with open(file) as f:
                services = yaml.safe_load_all(f)
                for service in services:
                    service = self.mecappservicecreate(service=service,file=file)        
        except Exception as e:
            return e


    def describe_mecns(self, name: str, output: str = 'json'):
        """
        Describe a MEC Application NAME

        :param name: The name of the MEC Application
        :param output: Output format (json/yaml). Default is 'json'
        
        :return: The MEC Application description
        """
        r,s = makerequest(_type='get',url=f"{self.domain_orch_url}/list/app",params={'name':name})
        if s==200:
            if output == 'yaml':
                return yaml.dump(r)
            return json.dumps(r)
        else:
            return "Encounted an error in fetching the list of onboarded services"


    def top_mecns(self, vim: str, name: str, app: str = None, output: str = 'json'):
        """
        Performs top on MEC Application VIM_NAME NAME.
        Provides information related to computational 
        resources consumed by the MEC Application 

        :param vim: The name of the VIM
        :param name: The name of the MEC Application
        :param app: The name of the MEC Application Service
        :param output: Output format (json/yaml). Default is 'json'
        
        :return: None
        """
        r,s = makerequest(
            _type='get',
            url=f"{self.domain_orch_url}/metrics/app",
            params={'name':name,'appName':app,'vimId':vim}
        )
        if s in [200,404,400]:
            if output == 'yaml':
                return yaml.dump(r)
            return json.dumps(r)
        else:
            return "Encounted an error in fetching the list of onboarded services"


    def app_logs(
        self,
        vim: str,
        name: str,
        app: str,
        containername: str = None,
        lines: int = None
    ):
        """
        Logs of a MEC Application NAME app_NAME
        
        :param vim: The VIM ID
        :param name: The name of the MEC Application
        :param app: The name of the MEC Application Service
        :param containername: The name of the container
        :param lines: The number of lines to output
        
        :return: The logs of the MEC Application Service or an error message
        """
        params = {'name':name,'appName':app, 'vimId': vim, 'containerName':containername,'lines':lines}
        r,s = makerequest(_type='get',url=f"{self.domain_orch_url}/logs/app",params=params)
        if s in [200,404,400]:
            return r
        else:
            return "Encounted an error in fetching the list of onboarded services"

        
    def delete_mecns(self, name: str):
        """
        Delete the mec application service
        
        :param name: The name of the mec application service
        
        :return: None
        """
        terminated = False
        r,s = makerequest(_type='get',url=f"{self.domain_orch_url}/list/app",params={'name':name,'latest':'no'})
        if s == 200 and r['status'] == 'NOTFOUND':
            raise typer.Exit(code=1)
        elif s == 200 and r['status'] in ['INSTANTIATED','TERMINATING']:
            package_id = r['packageId']
            vim_id = r['vimId']
            apps = [{'appName':app['appName'],'appDId':app['appDId'],'appInstanceId':app['appInstanceId']} for app in r['apps']]
            body = {'packageId':package_id,'apps':apps}
            count = 0
            start_time = time.time()
            r,s = makerequest(_type='post',url=f"{self.domain_orch_url}/terminate/app",body=body)
            if s == 201 and r['status'] == "TERMINATING":
                while True:
                    r,s = makerequest(_type='get',url=f"{self.domain_orch_url}/terminate/app",params={'packageId':package_id})
                    if s==200 and r['status']=='TERMINATED':
                        end_time = time.time() - start_time
                        terminated = True
                        break
                    if count == len(apps) * 4:
                        raise typer.Exit(code=1)
                    count +=1
                    time.sleep(0.5)
            elif s == 500:
                raise typer.Exit(code=1)
        elif s == 200 and r['status'] in ['ONBOARDED','PARTIAL','INSTANTIATING','FAILED']:
            package_id = r['packageId']
            vim_id = r['vimId']
            terminated = True
        #OFFBOARD
        if terminated:
            body = {'packageId':package_id,'vimId':vim_id}
            count = 0
            start_time = time.time()
            r,s = makerequest(_type='post',url=f"{self.domain_orch_url}/offboard/app",body=body)
            if s == 201 and r['status'] == 'OFFBOARDING':
                while True:
                    r,s = makerequest(_type='get',url=f"{self.domain_orch_url}/offboard/app",params={'packageId':package_id})
                    if s==200 and r['status']=='OFFBOARDED':
                        end_time = time.time() - start_time
                        break
                    if count == 100: #it means timeout is 20 * 0.5 seconds
                        raise typer.Exit(code=1)
                    count +=1
                    time.sleep(0.5)