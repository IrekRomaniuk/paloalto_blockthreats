import sys

from st2actions.runners.pythonrunner import Action

class MyEchoAction(Action):
    def run(self, source):
        print(source,self.config)

        if source == '1.1.1.1':
            return (True, source)
        return (False, source)