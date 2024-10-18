import asyncio
import logging
from pysnmp.hlapi.v1arch.asyncio import *


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def make_oid(val:str)->ObjectType:
    if "." in val:
        return ObjectType(ObjectIdentity((val)))
    return ObjectType(ObjectIdentity('SNMPv2-MIB', val, 0))
                                        

async def get(snmpDispatcher:SnmpDispatcher,ip:str,oid:str,version:str="v1",community:str="public",port:int=161)->str|None:
    oid_obj=make_oid(oid)
    mpModel=1 if version =="v2" else 0
    iterator = await get_cmd(
        snmpDispatcher,
        CommunityData(community, mpModel=mpModel),
        await UdpTransportTarget.create((ip, port),timeout=1,retries=0),
        oid_obj
    )

    errorIndication, errorStatus, errorIndex, varBinds = iterator

    if errorIndication:
        logger.error(errorIndication)

    elif errorStatus:
        logger.error(
            "{} at {}".format(
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
            )
        )
    else:
        return varBinds[0].prettyPrint()


async def get_next(snmpDispatcher:SnmpDispatcher,ip:str,oid:str,version:str="v1",community:str="public",port:int=161)->str|None:
    oid_obj = make_oid(oid)
    mpModel=1 if version =="v2" else 0
    iterator = await next_cmd(
        snmpDispatcher,
        CommunityData(community, mpModel=mpModel),
        await UdpTransportTarget.create((ip, port),timeout=1,retries=0),
        oid_obj
    )

    errorIndication, errorStatus, errorIndex, varBinds = iterator

    if errorIndication:
        logger.error(errorIndication)

    elif errorStatus:
        logger.error(
            "{} at {}".format(
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
            )
        )
    else:
        return varBinds[0].prettyPrint()
    

async def get_oids(snmpDispatcher:SnmpDispatcher,ip:str,oids:list[str],version="v1",community:str="public",port:int=161)->list[str]:
    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(get(snmpDispatcher,ip,oid,version,community,port)) for oid in oids]

    return [t.result() for t in tasks]


async def get_oid_devices(snmpDispatcher:SnmpDispatcher,ips:list[str],oid:str,version="v1",community:str="public",port:int=161)->list[str]:
    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(get(snmpDispatcher,ip,oid,version,community,port)) for ip in ips]

    return [t.result() for t in tasks]
    

def snmp_poll(ips:list[str],oid:str,version="v1",community:str="public",port:int=161):
    return asyncio.run(get_oid_devices(SnmpDispatcher(),ips,oid,version,community,port))


def snmp_device_details(ip,version:str="v1",community:str="public",port:int=161)->list[str]:
    oids=["sysObjectID","sysDescr","sysUpTime","sysName","sysContact","sysLocation"]

    return asyncio.run(get_oids(SnmpDispatcher(),ip,oids,version,community,port))


def snmp_get(ip:str,oids:list[str],version="v1",community:str="public",port:int=161):
    return asyncio.run(get_oids(SnmpDispatcher(),ip,oids,version,community,port))



