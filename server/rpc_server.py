from xmlrpc.server import SimpleXMLRPCServer


# Define the functions that will be exposed
def add(x, y):
    return x + y


def multiply(x, y):
    return x * y

def ping():
    return "success"


# Create the server
server = SimpleXMLRPCServer(("localhost", 8002))
print("RPC Server is running on port 8002...")

# Register the functions
server.register_function(add, "add")
server.register_function(multiply, "multiply")
server.register_function(ping, "ping")

# Run the server
server.serve_forever()
