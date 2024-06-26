# remote_binding_server.py
import Pyro5.api

class Binding:
    def __init__(self, context):
        self.context = context
    
    def exec(self, code):
        exec(code, self.context)
    
    def eval(self, expression):
        return eval(expression, self.context)
    
    def get(self, varname):
        return self.context.get(varname, None)

@Pyro5.api.expose
class RemoteBinding:
    def __init__(self):
        self.binding = Binding(globals())
    
    def exec_code(self, code):
        self.binding.exec(code)
    
    def eval_expression(self, expression):
        return self.binding.eval(expression)
    
    def get_variable(self, varname):
        return self.binding.get(varname)

def main():
    daemon = Pyro5.api.Daemon()
    uri = daemon.register(RemoteBinding)
    print(f"Ready. Object URI = {uri}")
    daemon.requestLoop()

if __name__ == "__main__":
    main()

# => 
# Ready. Object URI = PYRO:obj_4d56b5a612934b31b4d20e085cbf1601@localhost:52038

