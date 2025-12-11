class GitHubAPIError(Exception):
    """Custom exception raised when GitHub API fails."""
    pass

class FileOperationError(Exception):
    """Custom exception for file system errors."""
    pass