from st2reactor.sensor.base import PollingSensor
import requests
import xmltodict
from requests.packages.urllib3.exceptions import InsecureRequestWarning

class SslDecryptCountSensor(PollingSensor):
    """
    * self.sensor_service
        - provides utilities like
            get_logger() for writing to logs.
            dispatch() for dispatching triggers into the system.
    * self._config
        - contains configuration that was specified as
          config.yaml in the pack.
    * self._poll_interval
        - indicates the interval between two successive poll() calls.
    TESTING:  
    curl -kg "https://10.34.2.20/esp/restapi.esp?type=op&cmd=<show><session><all><filter><ssl-decrypt>yes</ssl-decrypt><count>yes</count></filter></all></session></show>&key="
    op: success
    <response status="success"><result>
        <member>73</member>
        <member>96</member>
        <member>23</member>
    </result></response>
    """
    def __init__(self, sensor_service, config, poll_interval): #sensor_service, config, poll_interval, 
        super(SslDecryptCountSensor, self).__init__(sensor_service=sensor_service,  
                                          config=config,                                 
                                          poll_interval=poll_interval)
        self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)

        
    def setup(self):
        self._key = self._config['api_key'] # or None
        # self._url = self._config['url']
        self._url = "/esp/restapi.esp?type=op&cmd=<show><session><all><filter><ssl-decrypt>yes</ssl-decrypt><count>yes</count></filter></all></session></show>&key="
        self._ips = self._config['ips'] 
        self._dps= ['dp0','dp1','dp2'] 
        # self._mes= self._config['measurement']   
        self._mes= "ssl-decrypt_count"   
        # self._val= self._config['value']  
        self._val= "value"


    def poll(self):        
        self._logger.debug('#### SslDecryptCountSensor dispatching trigger...')                
        ips = [str(ip) for ip in self._ips.split(',')]
        # ['1.1.1.1:pan1:DC1:3', '2.2.2.2:pan2:DC2:3', '3.3.3.3:pan', 'LAB:1']
        self._logger.debug('#### Tags: {}'.format(ips))
        for ip in ips:
            payload = {}                        
            ip = [str(elem) for elem in ip.split(':')]
            self._logger.debug('#### Tag: {}'.format(ip))
            payload['points']=[]
            # ['1.1.1.1', 'pan1', 'DC1', '3']
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            self._logger.debug('#### Request: {}'.format('https://' + ip[0] + self._url + self._key))
            response = requests.get('https://' + ip[0] + self._url + self._key, verify=False)
            self._logger.debug('#### Response: {}'.format(response.text))
            if response.status_code == 200:
                data = xmltodict.parse(response.text)
                for dp in self._dps:
                    ssl=data['response']['result']['member']
                    self._logger.debug('#### Data: {}'.format(ssl))
                    for i in  range(0,len(ssl)): #range(0,len(ssl))
                        # self._logger.debug('#### dsp: {} coreid: {}'.format(dp, i))
                        points={}
                        points['measurement']=self._mes
                        points['fields']={}                           
                        points['tags']= {"site": ip[2],"firewall": ip[1],"dsp": i}                     
                        points['fields'][self._val]=max([int(value) for value in ssl[i]['value'].split(',')])
                        self._logger.debug('#### Points: {}'.format(points))
                        payload['points'].append(points)  
                        self._logger.debug('#### Payload: {}'.format(payload['points']))            
             
            self._logger.debug('#### Dispatching payload of type {} with number of {} points'.format(type(payload),len(payload['points'])))                               
            self.sensor_service.dispatch(trigger="pan.decrypt_count_trigger", payload=payload)               
        #requests.get("https://hchk.io/")
             

    def cleanup(self):
        pass

    # Methods required for programmable sensors.
    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass