from rich import print as richprint
from owly_sdk.common.constants import *
from owly_sdk.common.request_config import RequestConfig
import requests
import time
import json
import yaml


def makerequest(_type,url,params=None,body=None,https_verify=False,header=None, config: RequestConfig = RequestConfig()):
    connection_try = config.connection_retry
    while True:
        try:
            if _type == 'post':
                r = requests.post(url, json=body, verify=https_verify)
            elif _type == 'get':
                r = requests.get(url, verify=https_verify,params=params,headers=header)
            elif _type == 'delete':
                r = requests.delete(url,verify=https_verify,params=params,headers=header)
            elif _type == 'put':
                if body is not None:
                    r = requests.put(url,verify=https_verify,json=body,headers=header)
                if params is not None:
                    r = requests.put(url,verify=https_verify,params=params,headers=header)
            status_code = r.status_code
            if status_code!=204:
                response = r.json()
            else:
                response = {}
            break
        except Exception as e:
            richprint(str(e))
            if connection_try>0:
                connection_try -=1
                time.sleep(config.connection_retry_time)
            else:
                response = {'status': 'error','reason':e}
                status_code = 500
                break
    return response, status_code


def format_response(response, output : str = None):
    """
    Format the response in the given format.
    
    :param response: The response to be formatted.
    :param output: The format of the output (json/yaml).
    
    :return: The formatted response
    """
    if output == 'yaml':
        return yaml.dump(response)
    if output == 'json':
        return json.dumps(response)
    return response