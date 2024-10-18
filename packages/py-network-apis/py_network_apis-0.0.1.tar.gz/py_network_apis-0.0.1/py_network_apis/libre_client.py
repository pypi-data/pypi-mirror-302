import requests
import logging

class libre(object):
    def __init__(self,api_url:str,token:str):
        self.api_url=api_url
        self.token=token
        self.log = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        self.http_header={'X-Auth-Token': token,}


    def make_request(self,endpoint:str,data:dict=None,method:str="GET")->dict|None:
        req_url=self.api_url+endpoint
        try:
            resp=requests.request(method=method,url=req_url,json=data,headers=self.http_header)
            result = resp.json()
            resp.raise_for_status()
            if 'message' in result:
                self.log.info(result['message'])
            return result
        except requests.exceptions.HTTPError as e:
            self.log.error(e)
            if 'message' in result:
                self.log.error(result['message'])

        except (requests.ConnectionError,requests.Timeout) as e:
            self.log.error(f"Client: could not make connection to: {req_url}")


    def add_device(self,hostname:str)->dict|None:
        resp = self.make_request("/devices",{"hostname":hostname},"POST")
        if resp is not None:
            return resp['devices'][0]
        

    def get_device(self,hostname:str)->dict|None:
        resp = self.make_request(f"/devices/{hostname}")
        if resp is not None:
            return resp['devices'][0]
        

    def get_group_id(self,group_name:str)->int|None:
        resp = self.make_request("/devicegroups")
        if resp is not None:
            if resp["count"]<1:
                self.log.warning("LibreNMS: No device groups found")
                return
            for group in resp["groups"]:
                if group["name"]==group_name:
                    return group["id"]
                
                
    def add_to_group(self,group:int,*devices:int):
        self.make_request(f"/devicegroups/{group}/devices",{"devices":list(devices)},"POST")


    def remove_from_group(self,group:int,*devices:int):
        self.make_request(f"/devicegroups/{group}/devices",{"devices":list(devices)},"DELETE")


    def delete_device(self,id:int):     
        self.make_request(f"/devices/{id}",method="DELETE")


    def update_field(self,device_id:int,field:str,value):
        data = {"field":field,"data":value}
        self.make_request(f"/devices/{device_id}",data,"PATCH")


    def add_location(self,loc:str,lat:float,lng:float)->int|None:
        data = {"location":loc,"lat":lat,"lng":lng}
        resp = self.make_request("/locations",data,"POST")
        if resp is not None and 'message' in resp and 'Location added with id #' in resp['message']:
            return int(resp['message'].split('Location added with id #')[1])

    
    def get_location(self,loc:str)->dict|None:
        resp = self.make_request(f"/location/{loc}")
        if resp is not None:
            return resp["get_location"]
        

    def set_location(self,device_id:int,loc:str,lat:float=None,lng:float=None):
        resp = self.get_location(loc)
        if resp is None:
            loc_id = self.add_location(loc,lat,lng)
        else:
            loc_id = resp['id']

        self.update_field(device_id,"override_sysLocation",1)
        self.update_field(device_id,"location_id",loc_id)


    def get_alerts(self)->list|None:
        resp= self.make_request("/alerts?state=1")
        if resp is not None:
            return resp['alerts']
    

    def get_oxidized_config(self,hostname:str)->list|None:
        resp = self.make_request(f"/oxidized/config/{hostname}")
        if resp is not None:
            return resp["config"]

    def save_oxidize_config(self,hostname:str,file_name:str=None):
        if file_name is None:
            file_name=f"{hostname}.txt"

        resp=self.get_oxidized_config(hostname)
        if resp is not None:

            with open(file_name,"w") as f:
                for val in resp:
                    f.write(val)

    
    def add_parents_to_host(self,device:str|int,*parent_ids:int):
        data = {"parent_ids":','.join(map(str, parent_ids))}
        self.make_request(f"/devices/{device}/parents",data,"POST")


    def del_parents_from_host(self,device:str|int,*parent_ids:int):
        data = {"parent_ids":','.join(map(str, parent_ids))}
        self.make_request(f"/devices/{device}/parents",data,"DELETE")


    def get_device_by_ip(self,ip:str)->dict|None:
        resp = self.make_request("/devices","GET")
        if resp is not None:
            devices = [device for device in resp["devices"] if device["ip"]==ip]
            if len(devices)==1:
                return devices[0]


    def rename_device(self,hostname:str,new_name:str):
        resp = self.make_request(f"/devices/{hostname}/rename/{new_name}",method="PATCH")
