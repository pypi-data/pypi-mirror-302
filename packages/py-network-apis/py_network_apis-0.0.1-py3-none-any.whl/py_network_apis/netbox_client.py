import pynetbox
import pynetbox.models
import pynetbox.models.dcim
import pynetbox.models.ipam
from slugify import slugify
import logging

class netbox:
    def __init__(self,url:str=None,token:str=None):
        self.api=pynetbox.api(url=url,token=token)
        self.log = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        
    
    def get_or_add_site(self,name:str)->pynetbox.models.dcim.Record:
        site=self.api.dcim.sites.get(name=name)
        if site is None:
            return self.api.dcim.sites.create(name=name,status="active",slug=slugify(name))
        return site
        
    def get_or_add_ip_address(self,ip:str,descr:str)->pynetbox.models.ipam.IpAddresses:
        ip_address = self.api.ipam.ip_addresses.get(address=ip)
        if ip_address is None:
            return self.api.ipam.ip_addresses.create(address=ip,status="active",description=descr)
        return ip_address


    def get_or_add_role(self,name:str)->pynetbox.models.dcim.Record:
        role = self.api.dcim.device_roles.get(name=name)
        if role is None:
            return self.api.dcim.device_roles.create(name=name,slug=slugify(name),color="00ff00")
        return role


    def get_or_add_location(self,site:str,loc:str)->pynetbox.models.dcim.Record:
        site=self.api.dcim.sites.get(name=site)
        locs = list(self.api.dcim.locations.filter(site_id=site.id,name=loc))
        if len(locs)==0:
            return self.api.dcim.locations.create(site=site.id,status="active",name=loc,slug=slugify(loc))
        return locs[0]
    

    def get_or_add_manufacturer(self,name:str)->pynetbox.models.dcim.Record:
        manufacturer=self.api.dcim.manufacturers.get(name=name)
        if manufacturer is None:
            return self.api.dcim.manufacturers.create(name=name,slug=slugify(name))
        return manufacturer

    
    def get_device_type(self,device_type:str)->pynetbox.models.dcim.DeviceTypes|None:
        return self.api.dcim.device_types.get(model=device_type)
    

    def add_device_type(self,device_type:str,manufacturer_id:int,height:int=1)->pynetbox.models.dcim.DeviceTypes:
        return self.api.dcim.device_types.create(model=device_type,manufacturer=manufacturer_id,slug=slugify(device_type),u_height=height)


    def get_or_add_mgmt(self,device:pynetbox.models.dcim.Devices)->pynetbox.models.dcim.Interfaces:
        interfaces = self.api.dcim.interfaces.filter(device_id=device.id,name="mgmt")
        if len(interfaces)>0:
            return interfaces[0]
        return self.api.dcim.interfaces.create(device=device.id,name="mgmt",type="other")
    

    def get_device_by_ip(self,ip)->pynetbox.models.dcim.Devices|None:
        ip_resp = self.api.ipam.ip_addresses.get(address=ip)
        if ip_resp is None:
            return
    
        if ip_resp.assigned_object is None or ip_resp.assigned_object.device is None:
            return
        return ip_resp.assigned_object.device
    

    def add_device(self,name:str,role:int,manufacturer:int,device_type:int,site:int,
                   status:str="active",location:str=None,lat:float=None,long:float=None)->pynetbox.models.dcim.Devices:
        
        return self.api.dcim.devices.create(name=name,role=role,manufacturer=manufacturer,device_type=device_type,site=site,
                                            status=status,location=location,lat=lat,long=long)
    

    def assign_ip(self,device:pynetbox.models.dcim.Devices,ip:pynetbox.models.ipam.IpAddresses,
                  interface:pynetbox.models.dcim.Interfaces)->None:
        ip.assigned_object_type='dcim.interface'
        ip.assigned_object_id=interface.id
        ip.save()

        device.primary_ip4=ip
        device.primary_ip=ip
        device.save()


    def add_device_full(self,ip_cidr:str,name:str,model:str,site:str,role="Switch",
                        manufacturer:str=None,loc:str=None)->pynetbox.models.dcim.Devices|None:
        ip = ip_cidr.split("/")[0]
        nb_device = self.get_device_by_ip(ip)
        if nb_device is not None:
            self.log.info(f"Device already exists with ip {ip}")
            return nb_device

        nb_device_type=self.get_device_type(model)
        if nb_device_type is None:
            if manufacturer is None:
                self.log.info(f"Manufacturer name required to add device type")
                return
            nb_manufacturer= self.get_or_add_manufacturer(manufacturer)
            nb_device_type = self.add_device_type(model,nb_manufacturer.id)
           
        nb_site = site=self.api.dcim.sites.get(name=name)
        if site is None:
            self.log.warning(f"Site not found")
            return
        nb_role= self.get_or_add_role(role)
        nb_device = self.add_device(name=name,manufacturer=nb_device_type.manufacturer.id,device_type=nb_device_type.id,
                                role=nb_role.id,site=nb_site.id)
        
        if loc is not None:
            nb_location =self.get_or_add_location(site,loc)
            nb_device.location = nb_location
            nb_device.save()

        nb_interface=self.get_or_add_mgmt(nb_device)
        nb_ip= self.get_or_add_ip_address(ip_cidr,f"{nb_device.device_type.model}- {nb_site.name}")
        self.assign_ip(nb_device,nb_ip,nb_interface)

        self.log.info(f"Created device: id: {nb_device.id}, {nb_device.device_type.model} {nb_device.site.name} {nb_device.role.name} {nb_device.primary_ip.address}")
        return nb_device

    def has_device_type(self,device:str,manufacturer:str)->None:
        nb_manufacturer=self.get_or_add_manufacturer(manufacturer)


        results = self.api.dcim.device_types.filter(model=device,manufacturer_id=nb_manufacturer.id)
        return len(list(results))>0
    


    def add_power_outlet_template(self,outlet_dict:dict)->None:
        if "power_port" in outlet_dict:
            nb_power_ports= list(self.api.dcim.power_port_templates.filter(device_type_id=outlet_dict["device_type"],name=outlet_dict["power_port"]))
            if len(nb_power_ports)>0:
                outlet_dict["power_port"]=nb_power_ports[0].id

        self.api.dcim.power_outlet_templates.create(outlet_dict)

        
    def add_front_port_template(self,port_dict:dict)->None:
        if "rear_port" in port_dict:
            nb_rear_ports = list(self.api.dcim.rear_port_templates.filter(device_type_id=port_dict["device_type"],name=port_dict["rear_port"]))
            if len(nb_rear_ports)>0:
                port_dict["rear_port"]=nb_rear_ports[0].id

        self.api.dcim.front_port_templates.create(port_dict)

    def add_inventory_item_template(self,item_dict:dict)->None:
        if "manufacturer" in item_dict:
            manufacturer= self.get_or_add_manufacturer(item_dict["manufacturer"])
            item_dict["manufacturer"]=manufacturer.id
        self.api.dcim.inventory_item_templates.create(item_dict)


    def has_duplicate(self,site_id:int,device_name:str)->bool:
        return len(list(self.api.dcim.devices.filter(site_id=site_id,name=device_name)))>0
    
