import tkinter as tk
from tkinter import ttk
import threading
import subprocess
from mqtt_client import MQTTClient
from request_response import RequestResponseApp
from rpc_client import RPCClientApp
from benchmark import BenchmarkApp  # Import BenchmarkApp

# Variable to hold the process of the running servers
http_process = None
rpc_process = None


# Function to run the HTTP server
def run_http_server(python_path):
    global http_process
    http_process = subprocess.Popen([python_path, "server/http_server.py"])
    http_process.wait()  # Wait for the server to finish


# Function to run the RPC server
def run_rpc_server(python_path):
    global rpc_process
    rpc_process = subprocess.Popen([python_path, "server/rpc_server.py"])
    rpc_process.wait()  # Wait for the server to finish


# Start/Stop HTTP Server
def toggle_http_server():
    global http_process
    python_path = python_entry.get()  # Get the Python path from input
    if http_process is None:  # If server is not running
        http_thread = threading.Thread(target=run_http_server, args=(python_path,))
        http_thread.start()
        http_button.config(text="Stop HTTP Server")
        http_status_label.config(text="HTTP Server is running...")
    else:  # If server is running
        http_process.terminate()  # Stop the server
        print("HTTP Server has been stopped.")  # Print message to terminal
        http_process = None
        http_button.config(text="Start HTTP Server")
        http_status_label.config(text="HTTP Server not running")


# Start/Stop RPC Server
def toggle_rpc_server():
    global rpc_process
    python_path = python_entry.get()  # Get the Python path from input
    if rpc_process is None:  # If server is not running
        rpc_thread = threading.Thread(target=run_rpc_server, args=(python_path,))
        rpc_thread.start()
        rpc_button.config(text="Stop RPC Server")
        rpc_status_label.config(text="RPC Server is running...")
    else:  # If server is running
        rpc_process.terminate()  # Stop the server
        print("RPC Server has been stopped.")  # Print message to terminal
        rpc_process = None
        rpc_button.config(text="Start RPC Server")
        rpc_status_label.config(text="RPC Server not running")


# Function to terminate all processes and exit the application
def exit_application():
    global http_process, rpc_process
    if http_process is not None:
        http_process.terminate()  # Terminate HTTP server
    if rpc_process is not None:
        rpc_process.terminate()  # Terminate RPC server
    print("All servers have been stopped.")  # Print message to terminal
    root.quit()  # Close the application


# Create main application window
root = tk.Tk()
root.title("Multi-Protocol Application")
root.geometry("800x900")

# Create tabs for different protocols
tab_control = ttk.Notebook(root)

# Server Management Tab
server_tab = ttk.Frame(tab_control)
tab_control.add(server_tab, text="Server Management")

# MQTT Tab
mqtt_tab = ttk.Frame(tab_control)
tab_control.add(mqtt_tab, text="MQTT")
tab_control.pack(expand=1, fill="both")

mqtt_client = MQTTClient(mqtt_tab)

# Request-Response Tab
request_tab = ttk.Frame(tab_control)
tab_control.add(request_tab, text="Request-Response")
request_response_app = RequestResponseApp(request_tab)

# RPC Tab
rpc_tab = ttk.Frame(tab_control)
tab_control.add(rpc_tab, text="RPC")
rpc_app = RPCClientApp(rpc_tab)

# Benchmark Latency Tab
benchmark_tab = ttk.Frame(tab_control)
tab_control.add(benchmark_tab, text="Benchmark Latency")
benchmark_app = BenchmarkApp(benchmark_tab)

# Input for Python executable path
tk.Label(server_tab, text="Python Path:").pack(pady=5)
python_entry = tk.Entry(server_tab, width=50)
python_entry.pack(pady=5)
python_entry.insert(0, "C:/Users/Dian/anaconda3/envs/py310/python.exe")  # Default value

# Button to start/stop the HTTP server
http_button = tk.Button(
    server_tab, text="Start HTTP Server", command=toggle_http_server
)
http_button.pack(pady=10)

# Label to show HTTP server status
http_status_label = tk.Label(server_tab, text="HTTP Server not running")
http_status_label.pack(pady=5)

# Button to start/stop the RPC server
rpc_button = tk.Button(server_tab, text="Start RPC Server", command=toggle_rpc_server)
rpc_button.pack(pady=10)

# Label to show RPC server status
rpc_status_label = tk.Label(server_tab, text="RPC Server not running")
rpc_status_label.pack(pady=5)

# Button to exit the application
exit_button = tk.Button(server_tab, text="Exit", command=exit_application)
exit_button.pack(pady=20)

# Pack the tab control
tab_control.pack(expand=1, fill="both")

# Run the Tkinter main loop
root.mainloop()
