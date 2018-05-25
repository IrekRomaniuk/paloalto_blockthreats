from influxdb import InfluxDBClient
import ast
from st2actions.runners.pythonrunner import Action

json_test = [
    {
        "measurement": "cpu_load",
        "tags": {
            "site": "DC1",
            "firewall": "PAN1",
            "dsp": 1,
            "coreid":1
        },
        "fields": {
            "cpu_load": 55
        }
    }
]      

class influx_write(Action):
       
    def run(self, points): #, tags
        """
        Example of payload
        """
        _db = self.config['db']
        _user = self.config['username']
        _pass = self.config['password']
        _base_url, _port = self.config['base_url'].split(":")
        client = InfluxDBClient(_base_url, _port, _user, _pass, _db)
        # print(_db,_user,_pass,_base_url, _port)
        print(ast.literal_eval(points))
        # result=client.write_points(payload)
        client.close()
        # return result
        return type(ast.literal_eval(points))

