import os
import subprocess
import uuid

TEMPLATE = '''
from locust import HttpUser, task, between

class UserBehavior(HttpUser):
    wait_time = between(1, 2)

    @task
    def my_task(self):
        self.client.{method}("{path}")
'''

def generate_locust_file(test_run):
    method = test_run.request_type.lower()
    url_path = test_run.target_url.split("/", 3)[-1]  # extract path
    script = TEMPLATE.format(method=method, path="/" + url_path)

    locust_dir = "locust_scripts"
    os.makedirs(locust_dir, exist_ok=True)
    file_path = os.path.join(locust_dir, f"test_{uuid.uuid4().hex}.py")
    with open(file_path, "w") as f:
        f.write(script)
    return file_path

def run_locust(test_run, script_path):
    log_path = f"logs/locust_{uuid.uuid4().hex}.log"
    os.makedirs("logs", exist_ok=True)

    cmd = [
        "locust",
        "-f", script_path,
        "--headless",
        "-u", str(test_run.num_users),
        "-r", str(test_run.spawn_rate),
        "--run-time", test_run.duration,
        "--host", test_run.target_url,
        "--csv", log_path.replace(".log", ""),
        "--only-summary"
    ]
    subprocess.run(cmd, stdout=open(log_path, "w"), stderr=subprocess.STDOUT)
    return log_path