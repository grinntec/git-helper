import os
import logging
from git import Repo, exc
import semver
import re

from config import (
    BOLD_TEXT,
    UNDERLINE_TEXT,
    QUESTION_TEXT,
    ANSWER_TEXT,
    ERROR_TEXT,
    OUTPUT_TEXT,
    HELP_TEXT,
    WARNING_TEXT,
    RESET_TEXT,
    print_section_header,
    PROGRAM_TITLE,
    PROGRAM_AUTHOR,
    PROGRAM_HELP_TEXT,
    PROGRAM_VERSION,
    PROGRAM_DATE,
)

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
                latest_tag_str = str(sorted(repo.tags, key=lambda t: t.name)[-1])
        else:
            latest_tag_str = "No tags available"
    except exc.InvalidGitRepositoryError:
        raise Exception(f"Invalid Git repository: {repo_path}")
    except Exception as e:
        raise Exception(f"Error initializing repository: {e}")
    return repo, branch_name, latest_tag_str

def get_org_and_repo_name(remote_url):
    remote_url = remote_url.replace('.git', '')
    match = re.search(r'[:/](?P<org>[^/]+)/(?P<repo>[^/]+)$', remote_url)
    if match:
        return match.group('org'), match.group('repo')
    return None, None

# --- Get uncommited changes --- #
def get_uncommitted_changes(repo):
    messages = ""

    # Get modified but not staged files
    unstaged_files = repo.git.diff('--name-only').splitlines()

    # Get staged but not yet committed files
    staged_files = repo.git.diff('--cached', '--name-only').splitlines()

    # Get newly added (untracked) files
    untracked_files = repo.untracked_files

    if staged_files:
        formatted_staged_files = '\n'.join([f"{OUTPUT_TEXT}  Modified (staged): {file}{RESET_TEXT}" for file in staged_files])
        messages += f"\n{ANSWER_TEXT}{UNDERLINE_TEXT}Changes ready to be committed:{RESET_TEXT}\n{formatted_staged_files}{RESET_TEXT}\n\n"
        messages += f"{HELP_TEXT}Guidance: Consider {WARNING_TEXT}(4.)COMMITTING{RESET_TEXT} your changes.{RESET_TEXT}\n"
        messages += f"{HELP_TEXT}>    These files have been added to the staging area and are ready for your next commit.{RESET_TEXT}\n"
        messages += f"{HELP_TEXT}>    You shouldn't change these files any further until you commit them.{RESET_TEXT}\n"
        messages += f"{HELP_TEXT}>    Once committed, these files can be pushed to the origin repository.{RESET_TEXT}\n\n"

    if unstaged_files:
        formatted_unstaged_files = '\n'.join([f"{OUTPUT_TEXT}  Modified (not staged): {file}{RESET_TEXT}" for file in unstaged_files])
        messages += f"\n{ANSWER_TEXT}{UNDERLINE_TEXT}Files not yet added to staging:{RESET_TEXT}\n{formatted_unstaged_files}{RESET_TEXT}\n\n"
        messages += f"{HELP_TEXT}Guidance: Consider {WARNING_TEXT}(3.)ADDING{RESET_TEXT} the changed files to staging.{RESET_TEXT}\n"
        messages += f"{HELP_TEXT}>    These files have been changed since the last commit, but are not yet staged.{RESET_TEXT}\n"
        messages += f"{HELP_TEXT}>    Only add files that are ready to be staged and then committed to the repository.{RESET_TEXT}\n"
        messages += f"{HELP_TEXT}>    When added, the files will be staged and ready to commit.{RESET_TEXT}\n\n"

    if untracked_files:
        formatted_untracked_files = '\n'.join([f"{OUTPUT_TEXT}  New file (untracked): {file}{RESET_TEXT}" for file in untracked_files])
        messages += f"\n{ANSWER_TEXT}{UNDERLINE_TEXT}Untracked files not yet added to staging:{RESET_TEXT}\n{formatted_untracked_files}{RESET_TEXT}\n\n"
        messages += f"{HELP_TEXT}Guidance: Consider {WARNING_TEXT}(3.)ADDING{RESET_TEXT} the new files to staging.{RESET_TEXT}\n"
        messages += f"{HELP_TEXT}>    These files are recognized by Git, but are not yet part of version control.{RESET_TEXT}\n"
        messages += f"{HELP_TEXT}>    Only add files that are ready to be staged and then committed to the repository.{RESET_TEXT}\n"
        messages += f"{HELP_TEXT}>    When added, the files will be staged and ready to commit.{RESET_TEXT}\n\n"
    
    return messages

#--- Compare the local repository with the remote origin ---#
def compare_with_origin(repo, branch_name):
    try:
        # Fetch the latest changes from the remote origin
        repo.remotes.origin.fetch()

        # Initialize a string for the messages
        messages = ''

        # Check if the local branch is ahead of or behind the remote branch
        behind_commits = list(repo.iter_commits(f'{branch_name}..origin/{branch_name}'))
        ahead_commits = list(repo.iter_commits(f'origin/{branch_name}..{branch_name}'))

        # If the local branch is behind, show the number and guidance
        if behind_commits:
            messages += f"\n{ANSWER_TEXT}{UNDERLINE_TEXT}Local branch {branch_name} is behind the remote origin by {len(behind_commits)} commits.{RESET_TEXT}\n"
            # List files that are changed in the commits the local branch is behind
            files_to_pull = []
            for commit in behind_commits:
                for modified_file in commit.stats.files:
                    files_to_pull.append(modified_file)
            files_to_pull = list(set(files_to_pull))  # Remove duplicates
            messages += f"{ANSWER_TEXT}Files on remote to be pulled:\n"
            for file in files_to_pull:
                messages += f"{OUTPUT_TEXT}  - {file}{RESET_TEXT}\n\n"
            messages += f"{HELP_TEXT}Guidance: Consider {WARNING_TEXT}(1.)PULLING{RESET_TEXT}{HELP_TEXT} the changes from the remote repository.{RESET_TEXT}\n"
            messages += f"{HELP_TEXT}>    Files exist on the remote repository that you do not have locally.{RESET_TEXT}\n"
            messages += f"{HELP_TEXT}>    Pulling the files will update your local copy of the repository to match the remote one.{RESET_TEXT}\n\n"

        # If the local branch is ahead, show the commits and guidance
        if ahead_commits:
            messages += f"\n{ANSWER_TEXT}{UNDERLINE_TEXT}Local branch {branch_name} is ahead of the remote origin by {len(ahead_commits)} commits.{RESET_TEXT}\n"
            messages += f"{ANSWER_TEXT}Commits waiting to be pushed:{RESET_TEXT}\n"
            for commit in ahead_commits:
                messages += f"{OUTPUT_TEXT}{commit.hexsha[:7]} - {commit.author.name}: {commit.summary}{RESET_TEXT}\n\n"
            messages += f"{HELP_TEXT}Guidance: Consider {WARNING_TEXT}(2.)PUSHING{RESET_TEXT}{HELP_TEXT} your commits to synchronize with the remote repository.{RESET_TEXT}\n"
            messages += f"{HELP_TEXT}>    Files exist on the local repository that do not exist on the remote one.{RESET_TEXT}\n"
            messages += f"{HELP_TEXT}>    Pushing the files will update the remote repository to match the local one.{RESET_TEXT}\n\n"

        # Get the messages for uncommitted changes and untracked files
        messages += get_uncommitted_changes(repo)

        return messages
        
    except Exception as e:
        # Return an error message if any exception occurs during the comparison
        return f"{ERROR_TEXT}Error comparing with the origin: {e}{RESET_TEXT}"
