import logging
import os
from git import Repo, exc
import semver
import sys
import re

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    return logging.getLogger(__name__)

def get_repo_root():
    try:
        repo = Repo(os.getcwd(), search_parent_directories=True)
        return repo.git.rev_parse("--show-toplevel")
    except Exception as e:
        raise Exception(f"Error finding Git repository root: {e}")

def initialize_repository():
    repo_path = os.getcwd()
    try:
        repo = Repo(repo_path, search_parent_directories=True)
        branch_name = repo.active_branch.name
        if repo.tags:
            try:
                latest_tag = max(
                    repo.tags,
                    key=lambda t: semver.VersionInfo.parse(t.name)
                )
                latest_tag_str = str(latest_tag)
            except Exception:
                # fallback: use last tag alphabetically if not semver
                latest_tag_str = str(sorted(repo.tags, key=lambda t: t.name)[-1])
        else:
            latest_tag_str = "No tags available"
    except exc.InvalidGitRepositoryError:
        raise Exception(f"Invalid Git repository: {repo_path}")
    except Exception as e:
        raise Exception(f"Error initializing repository: {e}")
    return repo, branch_name, latest_tag_str

def get_org_and_repo_name(remote_url):
    # Remove .git if present
    remote_url = remote_url.replace('.git', '')
    # Match HTTPS or SSH style
    match = re.search(r'[:/](?P<org>[^/]+)/(?P<repo>[^/]+)$', remote_url)
    if match:
        return match.group('org'), match.group('repo')
    return None, None