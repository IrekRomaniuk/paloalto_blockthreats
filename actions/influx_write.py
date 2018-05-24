from influxdb import InfluxDBClient

from st2actions.runners.pythonrunner import Action


class influx_write(Action):
       
    def run(self, payload): #, tags
        """
        '{''10.41.2.20'': {u''dp2:3'': 3, u''dp2:2'': 3, u''dp0:7'': 4}}'
        """
        _db = self.config['db']
        _user = self.config['username']
        _pass = self.config['password']
        _base_url, _port = self.config['base_url'].split(":")
        client = InfluxDBClient(_base_url, _port, _user, _pass, _db)
        # print(_db,_user,_pass,_base_url, _port)
        client.close()
        return payload