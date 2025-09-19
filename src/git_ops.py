# git_ops.py
import git
import semver
from git import Repo
from semver import VersionInfo

def initialize_repository():
    repo_path = os.getcwd()
    try:
        repo = git.Repo(repo_path, search_parent_directories=True)
        branch_name = repo.active_branch.name
        latest_tag = max(repo.tags, key=lambda t: semver.VersionInfo.parse(t.name)) if repo.tags else "No tags available"
    except git.InvalidGitRepositoryError:
        raise Exception(f"Invalid Git repository: {repo_path}")
    except Exception as e:
        raise Exception(f"Error initializing repository: {e}")
    return repo, branch_name, str(latest_tag)

# Add other git functions here (pull_origin, push_commits, add_files, commit_changes, tag_version, etc.)