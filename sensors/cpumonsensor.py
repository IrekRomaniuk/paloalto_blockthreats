from st2reactor.sensor.base import PollingSensor
import requests
import xmltodict
from requests.packages.urllib3.exceptions import InsecureRequestWarning

class PanCpuMonitorSensor(PollingSensor):
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
    curl -k "https://1.1.1.1/esp/restapi.esp?type=op&cmd=<show><running><resource-monitor><second></second></resource-monitor></running></show>&key="  
    """
    def __init__(self, sensor_service, config, poll_interval): #sensor_service, config, poll_interval, 
        super(PanCpuMonitorSensor, self).__init__(sensor_service=sensor_service,  
                                          config=config,                                 
                                          poll_interval=poll_interval)
        self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)

        
    def setup(self):
        self._key = self._config['api_key'] # or None
        self._url = self._config['url']
        self._ips = self._config['ips'] 
        self._dps= ['dp0','dp1','dp2'] 
        self._mes= self._config['measurement']      
        self._val= self._config['value']  


    def poll(self):        
        self._logger.debug('#### PanCpuMonitorSensor dispatching trigger...')
        payload = {}
        
        ips = [str(ip) for ip in self._ips.split(',')]
        # ['1.1.1.1:pan1:DC1:3', '2.2.2.2:pan2:DC2:3', '3.3.3.3:pan', 'LAB:1']
        self._logger.debug('#### Tags: {}'.format(ips))
        for ip in ips:
            points={}
            payalod[ip]=[]
            points['measurement']=self._mes
            points['fields']={}
            ip = [str(elem) for elem in ip.split(':')]
            self._logger.debug('#### Tag: {}'.format(ip))
            # ['1.1.1.1', 'pan1', 'DC1', '3']
            points['tags']= {"site": ip[2],"firewall": ip[1],"dsp": 99,"coreid": 99}
            # self._logger.debug('url: {}'.format('https://' + ip + self._url + self._key))
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            response = requests.get('https://' + ip[0] + self._url + self._key, verify=False)
            if response.status_code == 200:
                data = xmltodict.parse(response.text)
                for dp in self._dps:
                    cpu=data['response']['result']['resource-monitor']['data-processors'][dp]['second']['cpu-load-average']['entry']
                    for i in  range(0,len(cpu)):
                        #payload[ip][dp+':'+cpu[i]['coreid']]=max([int(value) for value in cpu[i]['value'].split(',')])
                        points['tags']['dsp']=dp
                        points['tags']['coreid']=i
                        points['fields'][self._val]=max([int(value) for value in cpu[i]['value'].split(',')])
                        self._logger.debug('#### Payload: {}'.format(payload))
                        payload[ip].append(points)              
             
            self._logger.debug('#### Dispatching payload of type {} with number of {} points'.format(type(payload),len(payload[ip])))                               
            self.sensor_service.dispatch(trigger="pan.cpu_mon_trigger", payload=payload)               
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