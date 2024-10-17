from owly_sdk.common.utils import makerequest
import uuid
import time


class VnfManager:
    """
    The VnfManager class provides the functionality to manage VNFs such as
    onboarding, instantiation, termination, offboarding, listing, and getting logs.
    """
    def __init__(self, domain_orch_url, request_config):
        """
        Initialize the VnfManager class with the domain_orch_url and request_config.
        
        :param domain_orch_url: The URL of the Orchestrator.
        :param request_config: The RequestConfig object to be used for making requests.
        """
        self.domain_orch_url = domain_orch_url
        self.request_config = request_config
        

    def terminate(self, service, vnf):
        """
        Terminate a VNF of a network service
        
        :param service: network service configuration
        :param vnf: name of the VNF to be terminated
        
        :return: Termination status
        """

        terminated = False
        _r,_s = makerequest(_type='get',url=f"{self.domain_orch_url}/list/vnf",params={'name':service['name']})
        if _s == 200 and _r['status'] == 'NOTFOUND':
            raise Exception(f"Service {service['name']} is not found: {_r}")
        elif _s == 200 and _r['status'] in ['INSTANTIATED','TERMINATING']:
            package_id = _r['packageId']
            vim_id = _r['vimId']
            if vnf is not None:
                vnfs = [{'vnfName':v['vnfName'],'vnfDId':v['vnfDId'],'vnfInstanceId':v['vnfInstanceId']} for v in _r['vnfs'] if vnf in v['vnfName'] ]
                _vnfs = [v for v in service['vnfs'] if v['vnfName'] == vnf]
                service.update({'packageId':package_id,'vnfs':_vnfs})
            else:
                vnfs = [{'vnfName':v['vnfName'],'vnfDId':v['vnfDId'],'vnfInstanceId':v['vnfInstanceId']} for v in _r['vnfs']]
            if len(vnfs) == 0 or vnfs is None:
                raise Exception(f"VNF {vnf} is not instantiated")
            body = {'packageId':package_id,'vnfs':vnfs}
            count = 0
            start_time = time.time()
            r,s = makerequest(_type='post',url=f"{self.domain_orch_url}/terminate/vnf",body=body)
            if s == 201 and r['status'] == "TERMINATING":
                while True:
                    if vnf is not None:
                        params = {'packageId':package_id,'vnfInstanceId':vnfs[0]['vnfInstanceId']}
                    else:
                        params = {'packageId':package_id}
                    r,s = makerequest(_type='get',url=f"{self.domain_orch_url}/terminate/vnf",params=params)
                    if s==200 and r['status'] == "TERMINATED":
                        end_time = time.time() - start_time
                        terminated = True
                        break
                    if count == len(vnfs) * 20:
                        raise Exception(f"Time out in terminating the service {service['name']}")
                    count +=1
                    time.sleep(0.5)
            else:
                raise Exception(f"Server replied with {s}, response {r}")

        return terminated


    def termination_status(self, packageId : str, vnfInstanceId : str = None):
        '''
        get the status of the termination process
        
        :param packageId: package id of the network service
        :param vnfInstanceId: instance id of the network function
        
        :return: status of the termination process
        '''
        r, s = makerequest(
            _type = 'get',
            url = f"{self.domain_orch_url}/terminate/vnf",
            params = {
                'packageId':packageId,
                'vnfInstanceId':vnfInstanceId
            }
        )
        
        return r


    def offboard(self, service : dict, vnf : str = None):
        """
        Offboard a VNF of a network service
        
        :param service: network service configuration
        :param vnf: name of the VNF to be offboarded
        
        :return: None
        """
        offboarded = False
        package_id = service['packageId']
        vim_id = service['vimId']
        body = {'packageId':package_id,'vimId':vim_id}
        if vnf is not None:
            vnfDIds = [v['vnfDId'] for v in service['vnfs'] if vnf in v['vnfName']]
            body.update({'vnfDIds':vnfDIds})
        else:
            return None
        count = 0
        start_time = time.time()
        r,s = makerequest(_type='post',url=f"{self.domain_orch_url}/offboard/vnf",body=body)
        if s == 201 and r['status'] == 'OFFBOARDING':
            while True:
                r,s = makerequest(_type='get',url=f"{self.domain_orch_url}/list/vnf",params={'name':service['name'],'vnfName':vnf,'latest':'no'})
                if s==200 and (r == [] or r['status'] == 'NOTFOUND'):
                    end_time = time.time() - start_time
                    offboarded=True
                    break
                if count == 100: #it means timeout is 20 * 0.5 seconds
                    raise Exception(f"Time out in offboarding the vnf {vnf} for service {service['name']} ")
                count +=1
                time.sleep(0.5)
        return offboarded



    def offboarding_status(self, packageId : str):
        '''
        get the status of the offboarding process
        
        :param packageId: package id of the network service
        
        :return: status of the offboarding process
        '''
        r, s = makerequest(_type='get',url=f"{self.domain_orch_url}/offboard/vnf",params={'packageId':packageId})
        return r


    def onboard(self, service : dict, packageId : str):
        '''
        onboard network function to a network service

        :param service: network service configuration
        :param packageId: package id of the service
        
        return: network service configuration
        '''
        service.update({'packageId':packageId})
        [ vnf.update({'vnfDId': str(uuid.uuid4())}) for vnf in service['vnfs'] ]
        service.update({'vimId':[service['vimId']]})
        r, s = makerequest(_type='post',url= f"{self.domain_orch_url}/onboard/vnf",body=service)
        if s != 201:
            raise Exception(f"Encounted an error while posting the request {r}")
        r,s = makerequest(_type='get',url=f"{self.domain_orch_url}/onboard/vnf",params={'packageId':service['packageId']})
        if not (s == 200 and r['status'] == 'ONBOARDED'):
            raise Exception(f"Server replied with status code {s}, response {r}")
        return service


    def onboarding_status(self, packageId : str):
        '''
        get the status of the onboarding process

        :param packageId: package id of the network service
        
        :return: status of the onboarding process
        '''
        r, s = makerequest(_type='get',url=f"{self.domain_orch_url}/onboard/vnf",params={'packageId':packageId})
        return r


    def instantiate(self, name : str, body : dict):
        '''
        instantiate network functions of a network service

        '''
        count = 0
        start_time = time.time()
        r, s = makerequest(_type='post',url=f"{self.domain_orch_url}/instantiate/vnf",body=body)
        print(r, s)
        if s !=201:
            print(f"Encounted an error, details: {r}")
            return None
        print(f"Made a request to instantiate {name} service")
        print(f"Instantiating {name} service")
        while True:
            r,s = makerequest(_type='get',url=f"{self.domain_orch_url}/instantiate/vnf",params={'packageId':body['packageId']})
            if s == 200 and r['status'] != 'INSTANTIATED':
                print(f"Service in state {r['status']}\n{r['reason']}")
            elif s ==200 and r['status'] == 'INSTANTIATED':
                end_time = time.time() - start_time
                print(f"Service {r['status']} in {end_time} seconds")
                break
            else:
                print(f"Encounted an error at the server side, details: {r}")
                break
            if count == len(body['vnfs']) * 10: #it means timeout is 100*len(vnfs) * 0.5 seconds
                break
            count +=1
            time.sleep(0.5)
        if s == 500:
            print(f"Server replied with 500, response {r}")
            raise Exception(f"Server replied with 500, response {r}")
        elif count == len(body['vnfs']) * 100: #it means timeout is 100*len(vnfs) * 0.5 seconds
            print(f"Timeout in instantiating the service {name}")
            print(f"Last response from the server {r}")
            raise Exception(f"Timeout in instantiating the service {name}")
        elif s not in [500,200,201]:
            print(f"Encounted an error at the server side, details: {r['reason']}")
            
            
    def instantiation_status(self, packageId : str):
        '''
        get the status of the network service
        
        :param packageId: package id of the network service
        
        :return: status of the network service
        '''
        r,s = makerequest(_type='get',url=f"{self.domain_orch_url}/instantiate/vnf",params={'packageId':packageId})
        return r


    def get_list(self, name : str, vnfName : str = None, latest : str = 'yes'):
        '''
        list all the network services
        
        :param name: name of the network service
        :param vnfName: name of the network function
        :param latest: get the latest network service
        
        :return: list of network services
        '''
        r,s = makerequest(_type='get',url=f"{self.domain_orch_url}/list/vnf", params={'name':name, 'vnfName':vnfName, 'latest':latest})
        return r


    def logs(
        self,
        vim: str,
        name: str,
        vnf: str,
        containername: str = None,
        lines: int = None
    ):
        """
        Logs of a VNF of a network service NAME VNF_NAME
        
        :param vim: The name or ID of the VIM
        :param name: The name of the network service
        :param vnf: The name of the VNF
        :param containername: The name of the container
        :param lines: The number of lines to output
        
        :return: The logs of the VNF or an error message
        """
        params = {'name':name,'vnfName':vnf, 'vimId': vim, 'containerName':containername,'lines':lines}
        r, s = makerequest(_type='get',url=f"{self.domain_orch_url}/logs/vnf",params=params)

        if s in [200, 404, 400]:
            return r
        else:
            return "Encounted an error in fetching the list of onboarded services"
        

    def metrics(self, vim : str, name : str, vnf : str = None):
        """
        get the metrics of the network service
        
        :param vim: ID or name of the VIM
        :param name: name of the network service
        :param vnf: name of the network function
        
        :return: metrics of the network service
        """
        r, s = makerequest(_type='get',url=f"{self.domain_orch_url}/metrics/vnf",params={'name':name, 'vnfName':vnf, 'vimId':vim})
        
        if s in [200, 404, 400]:
            return r
        else:
            return "Encounted an error in fetching the list of onboarded services"