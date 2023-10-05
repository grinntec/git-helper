import os
import sys
import git
import logging
import semver
from semver import VersionInfo
import datetime
from enum import Enum

# Configure the basic settings for logging
# Set the logging level to INFO, so it will capture Info, Warning, Error, and Critical messages
# Format the log messages to display only the actual log message
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Get a logger object for the module
# __name__ is a built-in variable which evaluates to the name of the current module
# Thus, logger is configured for the current module
logger = logging.getLogger(__name__)

# ANSI escape codes for text colors and reset
BOLD_TEXT = '\033[1m'
UNDERLINE_TEXT = '\033[4m'
QUESTION_TEXT = '\033[96m\033[1m'  # Bold Cyan
ANSWER_TEXT = '\033[92m'  # Green
ERROR_TEXT = '\033[91m\033[1m'  # Bold Red
OUTPUT_TEXT = '\033[97m'  # White
HELP_TEXT = '\033[90m'  # Grey
RESET_TEXT = '\033[0m'  # Reset

# Constants
PROGRAM_TITLE = "Git Helper"
PROGRAM_AUTHOR = "Neil Grinnall"
PROGRAM_HELP_TEXT = "A guided method to using Git"
PROGRAM_VERSION = "1.0.0"
PROGRAM_DATE = "2023-10-04"

#--- Define an enumeration class named UserChoice ---#
class UserChoice(Enum):
    # Each member of this enumeration represents a user choice in the application
    # REFRESH checks and displays the current status with no actions taken
    REFRESH = '0'    
    # PULL represents the choice to pull changes from the remote repository
    PULL = '1'    
    # PUSH represents the choice to push changes to the remote repository
    PUSH = '2'    
    # COMMIT represents the choice to commit changes to the local repository
    COMMIT = '3'
    # ADD represents the choice to add changes to the staging area
    ADD = '4'    
    # TAG represents the choice to tag a specific commit
    TAG = '5'    
    # EXIT represents the choice to exit the application
    EXIT = '6'
#############################################################################################################
# --- Display a title card --- #
def display_title(title, author, help_text, version, date):
    """
    Display a professional-looking title in the console.

    Args:
    - title (str): The title of the program.
    - author (str): The author's name.
    - help_text (str): A brief description of what the program does.
    - version (str): The version of the program.
    - date (str): The release or update date.
    """    
    # Determine the maximum length for proper formatting
    max_length = max(len(title), len(author), len(help_text), len(version) + len("Version: "), len(date) + len("Date: "))
    
    # Print the top border
    print("+" + "-" * (max_length + 2) + "+")
    
    # Print the title, centered
    print("| " + title.center(max_length) + " |")
    print("| " + ("Version: " + version).center(max_length) + " |")
    print("| " + ("Date: " + date).center(max_length) + " |")
    print("| " + ("Author: " + author).center(max_length) + " |")
    print("| " + "-" * max_length + " |")
    
    # Print the help text, centered
    print("| " + help_text.center(max_length) + " |")
    
    # Print the bottom border
    print("+" + "-" * (max_length + 2) + "+")
#############################################################################################################
# --- Clear the console screen --- #
def clear_screen():
    """
    Clear the console screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
#############################################################################################################
def prompt_to_continue():
    input("Press enter to continue...")
#############################################################################################################
#--- Initialize the git repository --- #
def initialize_repository():
    # Get the current working directory and set it as the repository path
    repo_path = os.getcwd()
    
    try:
        # Try to create a Repo object for the given repository path
        # search_parent_directories=True allows searching for a git repository in parent directories
        repo = git.Repo(repo_path, search_parent_directories=True)
        
        # Get the name of the active branch of the repository
        branch_name = repo.active_branch.name
        
        # Get the latest tag in the repository, if available, using semantic versioning
        # If no tags are available, set to "No tags available"
        latest_tag = max(repo.tags, key=lambda t: semver.VersionInfo.parse(t.name)) if repo.tags else "No tags available"
        
    except git.InvalidGitRepositoryError:
        # Log an error message and exit if the given path is not a valid git repository
        logger.error(f"{ERROR_TEXT}Invalid Git repository: {repo_path}{RESET_TEXT}")
        sys.exit(1)
        
    except Exception as e:
        # Log any other errors encountered during initialization and exit
        logger.error(f"{ERROR_TEXT}Error initializing repository: {e}{RESET_TEXT}")
        sys.exit(1)
        
    # Return the Repo object, active branch name, and the latest tag as a string
    return repo, branch_name, str(latest_tag)
#############################################################################################################
#--- Log information about the repository, branch, and latest tag ---#
def log_repository_info(repo, branch_name, latest_tag):
    # Log a header for the repository information section
    logger.info(f"\n{BOLD_TEXT}--- Repository Information ---{RESET_TEXT}")
    
    # Log the current working directory of the repository, the active branch name, and the latest tag
    # The information is highlighted using different text styles for better visibility
    logger.info(f"{OUTPUT_TEXT}You are working in the {ANSWER_TEXT}{repo.working_tree_dir}{OUTPUT_TEXT} repository on the {ANSWER_TEXT}{branch_name}{OUTPUT_TEXT} branch. The latest tag (version) is {ANSWER_TEXT}{latest_tag}{RESET_TEXT}\n")
#############################################################################################################
#--- Log the status of the repository by displaying the comparison result ---#
def log_status(comparison_result):
    # Log a header for the status section to separate it visually in the log output
    logger.info(f"{BOLD_TEXT}--- Status ---{RESET_TEXT}")
    
    # Log the result of the comparison between the local and remote repository
    # The comparison_result is expected to contain messages about the state of the repository, 
    # such as differences between local and remote, uncommitted changes, untracked files, etc.
    logger.info(comparison_result)
#############################################################################################################
#--- Log the available options that a user can choose from--- #
def log_options():
    # Log a header for the options section to visually separate it in the log output
    logger.info(f"\n{BOLD_TEXT}--- Options ---{RESET_TEXT}")
    
    # Iterate over each member of the UserChoice enumeration
    for choice in UserChoice:
        logger.info(f"{OUTPUT_TEXT}{choice.value}. {choice.name.capitalize().replace('_', ' ')}{RESET_TEXT}")
#############################################################################################################
#--- Log a visual separator in the console ---#
def log_separator():
    # Log a series of dashes as a visual separator to organize the console output
    # The separator is highlighted using a specific text style for better visibility
    logger.info(f"{BOLD_TEXT}-----------------------------{RESET_TEXT}\n")
#############################################################################################################
#--- Prompt the user to enter their choice and return the entered choice ---#
def get_user_choice():
    # Display a prompt to the user asking them to enter the number corresponding to their choice
    # The prompt is highlighted using a specific text style for better visibility
    # The function then returns the user’s input as a string
    return input(f"\n{QUESTION_TEXT}Enter the number of your choice: {RESET_TEXT}")
#############################################################################################################
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
            messages += f"{ANSWER_TEXT}Local branch {branch_name} is behind the remote origin by {len(behind_commits)} commits.{RESET_TEXT}\n"

            # List files that are changed in the commits the local branch is behind
            files_to_pull = []
            for commit in behind_commits:
                for modified_file in commit.stats.files:
                    files_to_pull.append(modified_file)
            files_to_pull = list(set(files_to_pull))  # Remove duplicates
            messages += f"{ANSWER_TEXT}Files on remote to be pulled:\n"
            for file in files_to_pull:
                messages += f"{OUTPUT_TEXT}  - {file}{RESET_TEXT}\n"

            messages += f"{HELP_TEXT}Guidance: Consider (1.)PULLING the changes from the remote repository.{RESET_TEXT}\n\n"

        # If the local branch is ahead, show the commits and guidance
        if ahead_commits:
            messages += f"{ANSWER_TEXT}Local branch {branch_name} is ahead of the remote origin by {len(ahead_commits)} commits.{RESET_TEXT}\n"
            messages += f"{ANSWER_TEXT}Commits waiting to be pushed:{RESET_TEXT}\n"
            for commit in ahead_commits:
                messages += f"{OUTPUT_TEXT}{commit.hexsha[:7]} - {commit.author.name}: {commit.summary}{RESET_TEXT}\n"
            messages += f"{HELP_TEXT}Guidance: Consider (2.)PUSHING your commits to synchronize with the remote repository.{RESET_TEXT}\n\n"

        # If there are uncommitted changes, list the modified files and provide guidance
        uncommitted_changes = repo.is_dirty()
        if uncommitted_changes:
            modified_files = repo.git.diff('--name-only').splitlines()
            formatted_modified_files = '\n'.join([f"{OUTPUT_TEXT}  - {file}{RESET_TEXT}" for file in modified_files])
            messages += f"{ANSWER_TEXT}There are uncommitted changes in the working directory:\n{formatted_modified_files}{RESET_TEXT}\n"
            messages += f"{HELP_TEXT}Guidance: Consider (3.)COMMITTING your changes before synchronizing with the remote repository.{RESET_TEXT}\n\n"

        # If there are untracked files, list them and provide guidance
        untracked_files = repo.untracked_files
        if untracked_files:
            formatted_untracked_files = '\n'.join([f"{OUTPUT_TEXT}  - {file}{RESET_TEXT}" for file in untracked_files])
            messages += f"{ANSWER_TEXT}There are untracked files:\n{formatted_untracked_files}{RESET_TEXT}\n"
            messages += f"{HELP_TEXT}Guidance: Consider (4.)ADDING untracked files to the repository or updating the .gitignore file if these files should not be tracked.{RESET_TEXT}\n\n"

        return messages
        
    except Exception as e:
        # Return an error message if any exception occurs during the comparison
        return f"{ERROR_TEXT}Error comparing with the origin: {e}{RESET_TEXT}"
#############################################################################################################
# --- Pull from origin --- #
def pull_origin(repo, branch_name):
    try:
        # Fetch the latest changes from the remote origin
        repo.remotes.origin.fetch()

        # Check if there are any new commits on the remote branch that aren't on the local branch
        commits_behind = list(repo.iter_commits(f'{branch_name}..origin/{branch_name}'))
        
        if commits_behind:
            # Merge the changes from the remote branch into the local branch
            repo.git.pull('origin', branch_name)
            
            # Log a success message if the pull operation is successful
            logger.info(f"{ANSWER_TEXT}Successfully pulled changes from the remote origin to the local {branch_name} branch.{RESET_TEXT}")
        else:
            # Log a message indicating the local branch is already up to date with the remote branch
            logger.info(f"{ANSWER_TEXT}The local {branch_name} branch is already up to date with the remote origin.{RESET_TEXT}")

    except git.exc.GitCommandError as e:
        # Handle specific Git errors, like merge conflicts
        if 'fix conflicts' in str(e):
            logger.error(f"{ERROR_TEXT}Merge conflict detected! Please resolve the conflicts manually and then commit the changes.{RESET_TEXT}")
        else:
            logger.error(f"{ERROR_TEXT}Error pulling changes from the origin: {e}{RESET_TEXT}")

    except Exception as e:
        # Log an error message if any other exception occurs during the pull operation
        logger.error(f"{ERROR_TEXT}An unexpected error occurred: {e}{RESET_TEXT}")
#############################################################################################################
# --- Push commits from the local branch to the remote origin ---#
def push_commits(repo, branch_name):
    try:
        # Check for unpushed commits
        commits_ahead = list(repo.iter_commits(f'origin/{branch_name}..{branch_name}'))

        # If there are unpushed commits, push them to the remote
        if commits_ahead:
            # Attempt to push commits from the specified local branch to the corresponding remote branch on the origin
            repo.git.push('origin', branch_name)
            logger.info(f"{ANSWER_TEXT}Unpushed commits have been pushed to the origin.{RESET_TEXT}")
        else:
            # Log a message indicating there were no unpushed commits
            logger.info(f"{ANSWER_TEXT}No unpushed commits to push to the origin.{RESET_TEXT}")

    except git.exc.GitCommandError as e:
        # Handle specific Git errors, suggesting pull if push is rejected
        if 'rejected' in str(e):
            logger.error(f"{ERROR_TEXT}Push was rejected. Consider pulling changes first and then try pushing again.{RESET_TEXT}")
        else:
            logger.error(f"{ERROR_TEXT}Error pushing commits: {e}{RESET_TEXT}")

    except Exception as e:
        # Log an error message if any other exception occurs during the push operation
        logger.error(f"{ERROR_TEXT}An unexpected error occurred: {e}{RESET_TEXT}")
#############################################################################################################
# --- Push commits from the local branch to the remote origin ---#
def push_tags(repo):
    try:
        # Push tags to the remote repository
        repo.git.push('origin', '--tags')
        logger.info(f"{ANSWER_TEXT}Tags have been pushed to the origin.{RESET_TEXT}")

    except git.exc.GitCommandError as e:
        # Handle specific Git errors
        logger.error(f"{ERROR_TEXT}Error pushing tags: {e}{RESET_TEXT}")

    except Exception as e:
        # Log an error message if any other exception occurs during the push operation
        logger.error(f"{ERROR_TEXT}An unexpected error occurred: {e}{RESET_TEXT}")
#############################################################################################################
# --- Commit changes --- #
def commit_changes(repo):
    # Fetches both the untracked files and the modified ones.
    def get_changed_files():
        untracked = repo.untracked_files
        changed = [item.a_path for item in repo.index.diff(None)]
        return untracked, changed

    def stage_files(stage_all, files_to_stage=None):
        if stage_all:
            repo.git.add('.')
        elif files_to_stage:
            for file in files_to_stage:
                if file in untracked_files or file in changed_files:
                    repo.git.add(file)
                else:
                    logger.warning(f"{WARNING_TEXT}File '{file}' does not exist or has no changes. Skipping...{RESET_TEXT}")

    untracked_files, changed_files = get_changed_files()
    
    if not untracked_files and not changed_files:
        logger.info(f"{ANSWER_TEXT}No changes to commit.{RESET_TEXT}")
        return

    # Before the user is prompted to stage files, the untracked and modified files are displayed.
    print(f"{QUESTION_TEXT}Untracked files:{RESET_TEXT}")
    for file in untracked_files:
        print(file)
    
    print(f"{QUESTION_TEXT}Modified files:{RESET_TEXT}")
    for file in changed_files:
        print(file)

    stage_decision = input(f"{QUESTION_TEXT}Would you like to stage all changes for commit? (yes/no/exit): {RESET_TEXT}")
    if stage_decision.lower() == 'exit':
        logger.info(f"{ANSWER_TEXT}Exiting commit process.{RESET_TEXT}")
        return

    if stage_decision.lower() == 'no':
        files_to_stage = input(f"{QUESTION_TEXT}Enter the names of the files you'd like to stage, separated by spaces (or 'exit' to quit): {RESET_TEXT}").split()
        if 'exit' in files_to_stage:
            logger.info(f"{ANSWER_TEXT}Exiting commit process.{RESET_TEXT}")
            return
        stage_files(False, files_to_stage)
    else:
        stage_files(True)

    commit_message = input(f"{QUESTION_TEXT}Enter a commit message (or 'exit' to quit): {RESET_TEXT}").strip()
    if commit_message.lower() == 'exit':
        logger.info(f"{ANSWER_TEXT}Exiting commit process.{RESET_TEXT}")
        return

    while not commit_message:
        commit_message = input(f"{ERROR_TEXT}Commit message can't be empty! Please enter a valid commit message (or 'exit' to quit): {RESET_TEXT}").strip()
        if commit_message.lower() == 'exit':
            logger.info(f"{ANSWER_TEXT}Exiting commit process.{RESET_TEXT}")
            return

    try:
        # Attempt to commit the staged changes with the provided commit message
        repo.git.commit('-m', commit_message)
        # Log a success message if the commit operation is successful
        logger.info(f"{ANSWER_TEXT}Uncommitted changes have been committed.{RESET_TEXT}")
    except git.exc.GitCommandError as e:
        # Handle specific Git errors
        logger.error(f"{ERROR_TEXT}Error committing changes: {e}{RESET_TEXT}")
    except Exception as e:
        # Log an error message if any other exception occurs during the commit operation
        logger.error(f"{ERROR_TEXT}An unexpected error occurred: {e}{RESET_TEXT}")






#############################################################################################################
#############################################################################################################
#############################################################################################################
# Define the main function to execute the program
def main():
    
    while True:
        clear_screen()

        display_title(PROGRAM_TITLE, PROGRAM_AUTHOR, PROGRAM_HELP_TEXT, PROGRAM_VERSION, PROGRAM_DATE)

        repo, branch_name, latest_tag = initialize_repository()
        log_repository_info(repo, branch_name, latest_tag)

        comparison_result = compare_with_origin(repo, branch_name)
        log_status(comparison_result)
        log_options()

        choice = get_user_choice()

        if choice == UserChoice.REFRESH.value:
            repo, branch_name, latest_tag = initialize_repository()
        elif choice == UserChoice.PULL.value:
            pull_origin(repo, branch_name)
        elif choice == UserChoice.PUSH.value:
            push_commits(repo, branch_name)
        elif choice == UserChoice.COMMIT.value:
            commit_changes(repo)
        elif choice == UserChoice.ADD.value:
            add_files(repo)
        elif choice == UserChoice.TAG.value:
            tag_version(repo, latest_tag)
            # Re-fetch the latest tag after a new tag has been created
            latest_tag = str(max(repo.tags, key=lambda t: semver.VersionInfo.parse(t.name)) if repo.tags else "No tags available")
        elif choice == UserChoice.EXIT.value:
            logger.info(f"{ANSWER_TEXT}Exiting the program. Goodbye!{RESET_TEXT}")
            sys.exit(0)
        else:
            logger.error(f"{ERROR_TEXT}Invalid choice! Please select a valid option.{RESET_TEXT}")
        
        # Only prompt to continue if choice wasn't "Refresh" or "Exit"
        if choice != UserChoice.REFRESH.value and choice != UserChoice.EXIT.value:
            prompt_to_continue()

if __name__ == "__main__":
    main()