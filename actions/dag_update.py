import sys

from st2actions.runners.pythonrunner import Action

class UpdateDAG(Action):
    def run(self, source):
        print(source,self.config['api_key'])

        if source == '1.1.1.1':
            return (True, source)
        return (False, source)