import os
import subprocess
import sys
import requests
import json

def clone_repo(repo_url):
    # Clone the repository
    subprocess.call(["git", "clone", repo_url])

def change_directory_and_list_files():
    # Get the name of the repository
    repo_name = os.path.basename(os.getcwd())
    # List the files and folders in the repository
    print("Files and folders in the repository:")
    for item in os.listdir("."):
        print(item)

# Change to the home directory
os.chdir(os.path.expanduser("~"))

def get_data():
    url = "https://cat-fact.herokuapp.com/facts"
    response = requests.get(url)
    data = json.loads(response.content)
    print(data)

# Clone the repository
repo_url = "https://github.com/tiacloudconsult/hello_st2.git"
print(repo_url)
clone_repo(repo_url)

# # Change directory to the repository and list the files and folders
repo_name = os.path.basename(repo_url).replace(".git", "")
os.chdir(repo_name)



change_directory_and_list_files()
get_data()