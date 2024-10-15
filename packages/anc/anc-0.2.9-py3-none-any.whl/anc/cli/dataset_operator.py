from .util import is_valid_source_path, get_file_or_folder_name, convert_to_absolute_path
from anc.conf.remote import remote_server, remote_storage_prefix, repo_url
from anc.api.connection import Connection
import subprocess
import os
import sys
import json
from requests.exceptions import RequestException
from tabulate import tabulate

from .util import get_enviroment


class DatasetOperator:
    def __init__(self):
        self.conn = Connection(url=remote_server)

    def download_dataset(self, name, version, dest, cache_policy):
        dest = os.path.abspath(dest)
        if remote_storage_prefix in dest:
            return self.remote_download(name, version, dest, cache_policy)
        git_commit_id = self.get_commit_id(name, version)
        if git_commit_id is None:
            print("Not found a git commit id for the dataset, can't do download.")
            return
        self.local_download(git_commit_id, name, dest)

    # for training job use.
    def add_dataset(self, dataset_name, version, source_path, message):
        if remote_storage_prefix in source_path:
            return self.remote_add(dataset_name, version, source_path, message)
        self.local_add(dataset_name, version, source_path, message)

    def remote_add(self, version, source_path, message):
        project, cluster, peronsal = get_enviroment()
        source_path = os.path.abspath(source_path)
        if not is_valid_source_path(source_path):
            sys.exit(1)
        abs_path = convert_to_absolute_path(source_path)
        dataset_name = get_file_or_folder_name(abs_path)
        conn = Connection(url=remote_server)
        data = {
            "dataset_name": dataset_name,
            "version": version,
            "source_path": abs_path,
            "dest_path": "local",
            "project": project,
            'cluster': cluster,
            'personal': peronsal,
            "message": message
        }
        try:
            response = conn.post("/add", json=data)

            # Check if the status code is in the 2xx range
            if 200 <= response.status_code < 300:
                response_data = response.json()
                task_id = response_data.get('task_id')
                if task_id:
                    print(f"Task added successfully. Your task ID is: {task_id}")
                    print(f"You can check the status later by running: anc ds list -n {dataset_name}")
                    print(f"You can check the task status: anc ds task status {task_id}")
                    print(f"If your task has been pending a long time, please check the queue with: anc ds queue status")
                else:
                    print("Task added successfully, but no task ID was returned.")
            else:
                print(f"Error: Server responded with status code {response.status_code}")
                print(f"{response.text}")
  
        except RequestException as e:
            print(f"Error occurred while communicating with the server: {e}")
        except json.JSONDecodeError:
            print("Error: Received invalid JSON response from server")
        except KeyboardInterrupt:
            print(f"Operation interrupted. The dataset add operation may still be processing on the backend.")
            print(f"You can check its status later by running: anc ds list -n {dataset_name}")
            sys.exit(0)
        except Exception as e:
            print(f"Remote add got an unexpected error: {e}")

    # TODO
    def local_add(self, dataset_name, version, source_path, message):
        if os.getenv("AWS_ACCESS_KEY_ID", None) is None or os.getenv("AWS_SECRET_ACCESS_KEY", None) is None or os.getenv("GIT_TOKEN", None) is None:
            print("!!!! Hey, are you sure you want to upload it to remote? if yes, please set environment for <AWS_ACCESS_KEY_ID> and <AWS_SECRET_ACCESS_KEY> and <GIT_TOKEN>, so we can continue !!!!")
            sys.exit(1)
        print("sorry, this featur not proviede")
        # git_token = os.environ["GIT_TOKEN"]
        # repo_url_with_token = repo_url.replace("https://", f"https://{git_token}@")
        # with tempfile.TemporaryDirectory() as temp_dir:
        #     subprocess.run(['git', 'clone', '-b', 'main', repo_url_with_token, temp_dir], check=True)
        #     subprocess.run(["dvc", "import-url", "--force", source_path, "local"], cwd=temp_dir, check=True)

        #     print(f"download success and copy {temp_dir}/{source_path} to {dest_path}")
        #     subprocess.run(['cp', '-ar', source_path, dest_path],cwd=temp_dir, check=True)


    def remote_download(self, name, version, dest, cache_policy):
        abs_path = convert_to_absolute_path(dest)
        project, cluster, personal = get_enviroment()
        data = {
            "dataset_name": name,
            "version": version,
            "dest_path": abs_path,
            "cache_policy": cache_policy,
            "project": project,
            "cluster": cluster,
            "personal": personal,
        }
        try:
            response = self.conn.post("/get", json=data)

            # Check if the status code is in the 2xx range
            if 200 <= response.status_code < 300:
                response_data = response.json()
                task_id = response_data.get('task_id')
                if task_id:
                    print(f"Dataset get operation initiated. Your task ID is: {task_id}")
                    print(f"You can check the status later by running: anc ds task status {task_id}")
                    print(f"If your task has been pending a long time, please check the queue with: anc ds queue status")
                    print(f"please don't do any directory change along with {abs_path}")
                else:
                    print("Dataset get operation initiated, but no task ID was returned.")
            else:
                print(f"Error: Server responded with status code {response.status_code}")
                print(f"{response.text}")

        except RequestException as e:
            print(f"Error occurred while communicating with the server: {e}")
        except json.JSONDecodeError:
            print("Error: Received invalid JSON response from server")
        except KeyboardInterrupt:
            print(f"Operation interrupted. The dataset get operation may still be processing on the backend.")
            print(f"You can check its status later by running: anc ds list")
            print(f"Once completed, you can verify the dataset with: ls {data.get('abs_path', 'path_not_provided')}")
            sys.exit(0)
        except Exception as e:
            print(f"Remote download got an unexpected error: {e}")

    def list_dataset(self, dataset_name):
        response = self.conn.get("/query_datasets", params={"dataset_name": dataset_name})
        if response.status_code == 200:
            data = response.json()
            headers = [
                "Created At", "Dataset Name", 
                "Dataset Version",  "Message"
            ]
            table = [
                [
                    item["created_at"], item["dataset_name"],
                    item["dataset_version"],
                    item["message"]
                ] for item in data
            ]
            print(tabulate(table, headers=headers, tablefmt="grid", disable_numparse=True))
        else:
            print("Failed to retrieve datasets. Status code:", response.status_code)


    def get_commit_id(self, dataset_name, dataset_version):
        data = {
            "dataset_name": dataset_name,
            "version": dataset_version,
        }
        try:
            response = self.conn.get("/query_datasets", params={"dataset_name": dataset_name, "dataset_version": dataset_version})
            data = response.json()
            return data[0]["git_commit_id"] if len(data) > 0 and "git_commit_id" in data[0] else None
        except Exception as e:
            print(f"Error occurred: {e}")


    def local_download(self, git_commit_id, dataset_name, dest_path):
        print("<<This is a local download operation>>")
        if os.getenv("AWS_ACCESS_KEY_ID", None) is None or os.getenv("AWS_SECRET_ACCESS_KEY", None) is None or os.getenv("GIT_TOKEN", None) is None:
            print("!!!! Hey, are you sure you want to download it to your local? if yes, please set environment for <AWS_ACCESS_KEY_ID> and <AWS_SECRET_ACCESS_KEY> and <GIT_TOKEN>, so we can continue !!!!")
            sys.exit(1)
        url = repo_url
        git_token = os.environ["GIT_TOKEN"]
        repo_url_with_token = url.replace("https://", f"https://{git_token}@")
        source_path = 'local/' +  dataset_name
        command = ["dvc", "get", repo_url_with_token, source_path, "--rev", git_commit_id, "-o", dest_path]

        try:
            subprocess.run(command, check=True)
            print(f"Successfully downloaded {source_path} from {repo_url} to {dest_path}.")
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Failed to download {source_path}: {e}")
