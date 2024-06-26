# remote_binding_client.py
import Pyro5.api

uri = input("Enter the URI of the remote binding server: ")
remote_binding = Pyro5.api.Proxy(uri)

# Execute code remotely
remote_binding.exec_code('a = 10')
remote_binding.exec_code('b = 20')

# Evaluate an expression remotely
result = remote_binding.eval_expression('a + b')
print(f"Result of a + b: {result}")

# Get a variable value remotely
a_value = remote_binding.get_variable('a')
print(f"Value of a: {a_value}")

# Change a variable remotely
remote_binding.exec_code('a = 30')
new_a_value = remote_binding.get_variable('a')
print(f"New value of a: {new_a_value}")

# =>
# Enter the URI of the remote binding server: PYRO:obj_4d56b5a612934b31b4d20e085cbf1601@localhost:52038
# Result of a + b: 30
# Value of a: 10
# New value of a: 30
