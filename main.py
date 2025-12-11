from src.backup_manager import RepoBackupManager
from src.custom_exceptions import GitHubAPIError, FileOperationError

def main():
    print("=== GitHub Repo Backup Tool ===")
    user_input = input("Enter GitHub Username to backup: ").strip()

    if not user_input:
        print("[-] Username cannot be empty.")
        return

    manager = RepoBackupManager(user_input)

    try:
        # Step 1: Fetch
        repos = manager.fetch_repos()

        # Step 2: Save & Archive
        if repos:
            manager.save_to_json(repos)
            manager.archive_backup()
        else:
            print("[-] No data to backup.")

    except GitHubAPIError as api_err:
        print(f"[!] API ERROR: {api_err}")
    except FileOperationError as file_err:
        print(f"[!] FILE ERROR: {file_err}")
    except Exception as e:
        print(f"[!] UNEXPECTED ERROR: {e}")
    else:
        print("\n[SUCCESS] Operation completed successfully.")
    finally:
        print("=== End of Program ===")

if __name__ == "__main__":
    main1()