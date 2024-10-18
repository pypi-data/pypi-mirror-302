import requests
import json
import logging
from typing import Tuple

class ipa(object):
    
    def __init__(self,url:str):
        self.ipa_url=url
        self.log = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        self.session = requests.Session()

    def login(self,user:str,password:str):
        login_url = f"https://{self.ipa_url}/ipa/session/login_password" 

        header = {'Content-Type':'application/x-www-form-urlencoded',
                  'Accept':'text/plain'       
        }
        data={'user':user,'password':password}
        resp = self.session.post(login_url,headers=header,data=data,verify=False)   

        if resp.status_code!=200:
            self.log.warning(f"Failed to log {user} into {self.ipa_url}")
            return

        self.log.info(f"Successfully logged in as {user}")


    def make_request(self,data:dict)->dict|None:
        referer=f"https://{self.ipa_url}/ipa"
        req_url=referer+"/session/json"

        header={'referer':referer,'Content-Type': 'application/json',
                  'Accept': 'application/json'}
        

        session_data={'id':0,'method':data['method'],
                'params':[data['item'],data['params']]}
        

        self.log.debug('Making {0} request to {1}'.format(data['method'],req_url))

        resp = self.session.post(
            req_url,headers=header,
            data=json.dumps(session_data),
            verify=False
        )
        results= resp.json()
        if results.get("error") is not None:
            self.log.warning(results['error']['message'])
            return
        return results
    

    @staticmethod
    def reverse_ip(ip:str)->Tuple[str,str]:
        ip_vals=ip.split(".")
        rev_record = ip_vals.pop()
        return ".".join(ip_vals[::-1])+".in-addr.arpa",rev_record


    def dnsrecord_find(self, dnszone:str,record:str)->list|None:
        data={'method': 'dnsrecord_find', 'item': [dnszone], 'params':
             {'criteria':record}}
        resp = self.make_request(data)
        if resp is not None:
            return resp['result']['result']
        

    def dns_arecord_find(self,dnszone:str,ip:str)->list|None:
        data={'method': 'dnsrecord_find', 'item': [dnszone], 'params':
             {'arecord':ip}}
        resp = self.make_request(data)
        if resp is not None:
            return resp['result']['result']


    def dns_ptr_find(self,dnszone:str,ptr:str)->list|None:
        data={'method': 'dnsrecord_find', 'item': [dnszone], 'params':
             {'idnsname':ptr}}
        resp = self.make_request(data)

        if resp is not None:
            ptr_entries = resp['result']['result']
            if len(ptr_entries)==0:
                self.log.warning("Entry {0} not found for zone {1}".format(ptr,dnszone))
                return
            elif len(ptr_entries)>1:
                self.log.warning("Multiple results found for query {0}.{1}".format(ptr,dnszone))
                return
            
            return ptr_entries[0]
     

    def dns_reverse_lookup(self,ip:str)->str|None:
        zone,record = ipa.reverse_ip(ip)
        resp = self.dns_ptr_find(zone,record)
        if resp is not None:
            if len(resp['ptrrecord'])>1:
                self.log.warning("Multiple ptr records for {0}.{1}".format(record,zone))
                return
            return resp['ptrrecord'][0] 
    
    
    def dns_arecord_add(self,dnszone:str,ip:str,dnsname:str):
        data = {'method': 'dnsrecord_add', 'item': [dnszone],'params':
             {'idnsname':dnsname,"arecord":ip}}
        resp = self.make_request(data)
        if resp is not None:
            a_record=resp["result"]["result"]['arecord']
            self.log.info("A-record added: {0}".format(a_record))


    def dns_ptr_add(self,ip:str,dnsname:str):
        dnszone,record=ipa.reverse_ip(ip)
        data = {'method': 'dnsrecord_add', 'item': [dnszone],'params':
             {'idnsname':record,"ptrrecord":dnsname}}
        resp = self.make_request(data)
        if resp is not None:
            record = resp['result']['result']
            self.log.info("PTR added: {0} {1}".format(record['ptrrecord'],record['dn']))

    
    def dnsrecord_delentry(self,dnszone:str,dnsrecord:str):
        data = {'method': 'dnsrecord_delentry', 'item': [dnszone],'params':
             {'idnsname':dnsrecord}}
        resp = self.make_request(data)
        if resp is not None:
            self.log.info("Deleted {0} from dnszone {1}".format(resp['result']['summary'],dnszone))

    
    def dns_arecord_update(self,dnszone:str,old_val:str,new_val:str):
        data = {'method': 'dnsrecord_mod', 'item': [dnszone],'params':
             {'idnsname':old_val,"rename":new_val}}
        resp = self.make_request(data)
        if resp is not None:
            update=resp["result"]["result"]["idnsname"][0]
            self.log.info("{0} updated to {1}".format(old_val,update))


    def dns_ptr_update(self,ip:str,new_val:str):
        dnszone,record=ipa.reverse_ip(ip)
        data = {'method': 'dnsrecord_mod', 'item': [dnszone],'params':
             {'idnsname':record,"ptrrecord":new_val}}
        resp = self.make_request(data)
        if resp is not None:
            update = resp["result"]["result"]["ptrrecord"][0]
            self.log.info("PTR for {0} updated to {1}".format(ip,update))


    def dnsrecord_add_full(self,dnszone:str,ip:str,record:str):
        reverse_zone,rev_record = ipa.reverse_ip(ip)

        forward_zone_resp = self.dnsrecord_find(dnszone,None)
        reverse_zone_resp = self.dnsrecord_find(reverse_zone,None)


        if forward_zone_resp is not None:
            a_records = self.dns_arecord_find(dnszone,ip)
            for a_record in a_records:
                self.dnsrecord_delentry(dnszone,a_record['idnsname'])
        else:
            self.dnszone_add(dnszone)

        if reverse_zone_resp is not None:
            self.dnsrecord_delentry(reverse_zone,rev_record)
        else:
            self.dnszone_add(reverse_zone)

        data = {'method': 'dnsrecord_add', 'item': [dnszone],'params':
             {'idnsname':record,'arecord':ip,'a_extra_create_reverse':True}}
        resp = self.make_request(data)

        if resp is not None:
            dns_entry = resp['result']['result']
            self.log.info("DNS record {0} entry added for ip {1}".format(dns_entry['idnsname'],dns_entry['arecord']))


    def dnsrecord_del_full(self,dnszone:str,ip:str):
        reverse_zone,rev_record = ipa.reverse_ip(ip)

        a_records = self.dns_arecord_find(dnszone,ip)
        for a_record in a_records:
            self.dnsrecord_delentry(dnszone,a_record['idnsname'])

        self.dnsrecord_delentry(reverse_zone,rev_record)
    
    
    def dnszone_add(self,dnszone:str):
        data = {'method': 'dnszone_add', 'item': [dnszone],'params':
             {'skip_overlap_check': False}}
        resp = self.make_request(data)
        if resp is not None:
            self.log.info("DNS zone added {0}".format(resp['result']['result']['idnsname']))


    


