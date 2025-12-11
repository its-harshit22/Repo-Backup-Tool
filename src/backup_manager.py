import os
import json
import shutil
import requests
from datetime import datetime
from .custom_exceptions import GitHubAPIError, FileOperationError

class RepoBackupManager:
    def __init__(self, username, output_dir="backups"):
        self.username = username
        self.output_dir = output_dir
        self.api_url = f"https://api.github.com/users/{username}/repos"
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def fetch_repos(self):
        print(f"[*] Fetching repositories for user: {self.username}...")
        try:
            response = requests.get(self.api_url)
            if response.status_code != 200:
                raise GitHubAPIError(f"API status {response.status_code}: {response.reason}")
            
            data = response.json()
            if not data:
                print("[-] No repositories found.")
                return []
            
            print(f"[+] Successfully fetched {len(data)} repositories.")
            return data
        except requests.exceptions.RequestException as e:
            raise GitHubAPIError(f"Network error: {str(e)}")

    def save_to_json(self, data):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"repos_{self.username}_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            print(f"[+] Data saved to JSON: {filepath}")
            return filepath
        except IOError as e:
            raise FileOperationError(f"Failed to write JSON: {e}")

    def archive_backup(self):
        archive_name = f"backup_archive_{self.username}"
        try:
            print(f"[*] Archiving folder '{self.output_dir}'...")
            shutil.make_archive(archive_name, 'zip', self.output_dir)
            print(f"[+] Archive created: {archive_name}.zip")
        except Exception as e:
            raise FileOperationError(f"Archiving failed: {e}")