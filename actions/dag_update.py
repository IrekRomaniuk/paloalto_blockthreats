import sys

from st2actions.runners.pythonrunner import Action

class UpdateDAG(Action):
    def run(self, source):
        print(source, self.config['api_key'], self.config['fws_ips']) 
        if source == '1.1.1.1':
            return (True, source)
        return (False, source)
        
        for firewall in self.config['fws_ips'].split(","):
            print(firewall)
            """    
            url = "https://" + firewall + "/api"
                try:
                    response = requests.post(url + "/?type=user-id&cmd={}&key={}".
                        format(xml.substitute(ip='"{}"'.format(ip), tag=tag), key),verify=False,timeout=5)
                    print("{}\nfirewall {} ip {} tag {}".format(response.text, firewall, ip , tag))                                 
                except requests.exceptions.ConnectionError:
                    print("Post {}: ConnectionError".format(firewall))
                    continue
                doc = json.loads(json.dumps(xmltodict.parse(response.text)))                
                if 'success' in doc['response']['@status']  :
                    result['"{}"'.format(firewall)] = 'success'
                else:
                    result['"{}"'.format(firewall)] = "{} : {} {}".format(doc['response']['@status'], 
                        doc['response']['msg']['line']['uid-response']['payload']['register']['entry']['@ip'],
                        doc['response']['msg']['line']['uid-response']['payload']['register']['entry']['@message'])                       
        print("result {}".format(result))                
            """

    