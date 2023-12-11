import requests
import json
import wandb
import psutil
import os
import signal
import time

def wait_for_process(process_name, check_interval=5, max_wait=60):
    process_found = False
    start_time = time.time()
    while not process_found:
        for proc in psutil.process_iter(['pid', 'name']):
            if process_name.lower() in proc.info['name'].lower():
                print(f'Process {proc.info["name"]} with PID {proc.info["pid"]} found.')
                process_found = True
                break
        
        if time.time() - start_time > max_wait:
            raise ValueError("Not started")
        if not process_found:
            print(f'Process "{process_name}" not found. Checking again in {check_interval} seconds.')
            time.sleep(check_interval)

def kill_process_by_name(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        # Check if process name contains the given name string.
        if process_name.lower() in proc.info['name'].lower():
            print(f'Killing process {proc.info["name"]} with PID {proc.info["pid"]}')
            os.kill(proc.info['pid'], signal.SIGTERM)  # or signal.SIGKILL



def send_example_to_model(model_server_url, example, run):
    """Sends an example to the TensorFlow model server for inference."""
    headers = {"content-type": "application/json"}
    response = requests.post(model_server_url, data=json.dumps(example), headers=headers)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
wait_for_process("tensorflow_model_server", 5, 60)
# Example usage
model_server_url = "http://localhost:8501/v1/models/saved_model:predict"
example = {
    "signature_name": "serving_default",
    "instances": [[1.0, 2.0, 3.0, 4.0, 5.0]]  # Example input data
}

try:
    run = wandb.init()
    prediction = send_example_to_model(model_server_url, example, run)
    wandb.log({"prediction": prediction, "example": example})
    print("Prediction:", prediction)
except Exception as e:
    print("Error:", e)
finally:
    kill_process_by_name("tensorflow_model_server")