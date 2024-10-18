import yaml
import requests
from py_network_apis.netbox_client import netbox
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def import_device_types(manufacturer:str,device:str)->None:

    with open("config.yaml", 'r') as f:
        netbox_config= yaml.safe_load(f)

    url =netbox_config.get("nb_url")
    token = netbox_config.get("nb_token") 
    if url is None:
        logger.error("Missing Netbox URL")
        return
    if token is None:
        logger.error("Missing Netbox API Token")
        return

    nb = netbox(url,token)
    
    logger.info(f"Fetching device template for device: {device}")
        
    manufacturer_url = manufacturer.replace(" ","%20")
    request_url = "https://raw.githubusercontent.com/netbox-community/devicetype-library/refs/heads/master/device-types"
    resp = requests.get(f"{request_url}/{manufacturer_url}/{device}.yaml")

    if resp.status_code !=200:
        logger.warning(f"Could not find device template: {device}")
        return

    device_dict = yaml.safe_load(resp.content)
    if nb.has_device_type(device_dict["model"],device_dict["manufacturer"]):
        logger.info(f"Template for {device} already exists")
        return

    device_dict["manufacturer"]=nb.get_or_add_manufacturer(manufacturer).id

    device_type = nb.api.dcim.device_types.create(device_dict)
    dict_id={"device_type":device_type.id}

    console_ports=device_dict.get("console-ports")
    if console_ports is not None:
        for port in console_ports:
            port.update(dict_id)
        nb.api.dcim.console_port_templates.create(console_ports)

    console_server_ports=device_dict.get("console-server-ports")
    if console_server_ports is not None:
        for port in console_server_ports:
            port.update(dict_id)   
        nb.api.dcim.console_server_port_templates.create(console_server_ports)

    power_ports=device_dict.get("power-ports")
    if power_ports is not None:
        for port in power_ports:
            port.update(dict_id)
        nb.api.dcim.power_port_templates.create(power_ports)

    power_outlets=device_dict.get("power-outlets")
    if power_outlets is not None:
        for outlet in power_outlets:
            outlet.update(dict_id)
            nb.add_power_outlet_template(outlet)


    interfaces=device_dict.get("interfaces")
    if interfaces is not None:
        for interface in interfaces:
            interface.update(dict_id)   
        nb.api.dcim.interface_templates.create(interfaces)


    rear_ports=device_dict.get("rear-ports")
    if rear_ports is not None:
        for port in rear_ports:
            port.update(dict_id)   
        nb.api.dcim.rear_port_templates.create(rear_ports)


    front_ports=device_dict.get("front-ports")
    if front_ports is not None:
        for port in front_ports:
            port.update(dict_id)   
            nb.add_front_port_template(port)


    module_bays=device_dict.get("module-bays")
    if module_bays is not None:
        for bay in module_bays:
            bay.update(dict_id)   
        
        nb.api.dcim.module_bay_templates.create(module_bays)

    device_bays=device_dict.get("device-bays")
    if device_bays is not None:
        for bay in device_bays:
            bay.update(dict_id)   
        
        nb.api.dcim.device_bay_templates.create(device_bays)

    inventory_items=device_dict.get("inventory-items")
    if inventory_items is not None:
        for item in inventory_items:
            item.update(dict_id)
            nb.add_inventory_item_template(item)

    logger.info(f"Netbox: template succesfully added for {device}")


        
