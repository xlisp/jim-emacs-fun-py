import Pyro5.api

uri = input("Enter the URI of the greeting maker: ")
greeting_maker = Pyro5.api.Proxy(uri)
print(greeting_maker.get_fortune("Alice"))

# Enter the URI of the greeting maker: PYRO:obj_f1ec382ba9c74ab991bc8958432104ca@localhost:50933
# Hello, Alice. This is your fortune.

