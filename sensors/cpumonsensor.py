from st2reactor.sensor.base import PollingSensor
import requests
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
    curl -k "https://1.1.1.1/esp/restapi.esp?type=op&cmd=<show><running><resource-monitor><seurce-monitor></running></show>&key="    
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


    def poll(self):        
        self._logger.debug('#### PanCpuMonitorSensor dispatching trigger...')
        payload = {}
        ips = self._ips.split(',')
        self._logger.debug('#### Addresses: {}'.format(ips))
        for ip in ips:
            # self._logger.debug('url: {}'.format('https://' + ip + self._url + self._key))
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            response = requests.get('https://' + ip + self._url + self._key, verify=False)
            # self._logger.debug('response {}'.format(response.text))
            payload[ip]=response.status_code
        #requests.get("https://hchk.io/")
        self.sensor_service.dispatch(trigger="pan.cpu_mon_trigger", payload=payload)     

    def cleanup(self):
        pass

    # Methods required for programmable sensors.
    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass