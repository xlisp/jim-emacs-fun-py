import Pyro5.api

@Pyro5.api.expose
class GreetingMaker(object):
    def get_fortune(self, name):
        return f"Hello, {name}. This is your fortune."

daemon = Pyro5.api.Daemon()
uri = daemon.register(GreetingMaker)
print(f"Ready. Object uri = {uri}")
daemon.requestLoop()

# => Ready. Object uri = PYRO:obj_f1ec382ba9c74ab991bc8958432104ca@localhost:50933

