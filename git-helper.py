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

#--- Define an enumeration class named UserChoice ---#
class UserChoice(Enum):
    # Each member of this enumeration represents a user choice in the application
    # PUSH represents the choice to push changes to the remote repository
    PUSH = '1'    
    # COMMIT represents the choice to commit changes to the local repository
    COMMIT = '2'
    # ADD represents the choice to add changes to the staging area
    ADD = '3'    
    # TAG represents the choice to tag a specific commit
    TAG = '4'    
    # EXIT represents the choice to exit the application
    EXIT = '5'

#--- Define a function to initialize the git repository --- #
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


#--- Define a function to compare the local repository with the remote origin ---#
def compare_with_origin(repo, branch_name):
    try:
        # Fetch the latest changes from the remote origin
        repo.remotes.origin.fetch()
        
        # Check if there are any uncommitted changes in the working directory
        uncommitted_changes = repo.is_dirty()
        
        # Get a list of untracked files in the working directory
        untracked_files = repo.untracked_files
        
        # Get the latest commit in the local branch
        local_commit = repo.commit(branch_name)
        
        # Get the latest commit in the remote branch
        remote_commit = repo.commit(f'origin/{branch_name}')
        
        # If the local and remote commits are the same, and there are no uncommitted changes or untracked files,
        # return a message indicating that the working directory and local branch are up to date with the origin
        if local_commit.hexsha == remote_commit.hexsha and not uncommitted_changes and not untracked_files:
            return f"{ANSWER_TEXT}The working directory and the local branch {branch_name} are up to date with the origin.{RESET_TEXT}"
        
        # Initialize lists to store messages about differences and guidance
        differences, guidance = [], []
        
        # If the local and remote commits are different, list the unpushed commits and provide guidance
        if local_commit.hexsha != remote_commit.hexsha:
            unpushed_commits = list(repo.iter_commits(f'origin/{branch_name}..{branch_name}'))
            formatted_unpushed_commits = '\n'.join([f"{OUTPUT_TEXT}  - {commit.message.strip()}{RESET_TEXT}" for commit in unpushed_commits])
            differences.append(f"{ERROR_TEXT}There are unpushed commits:{RESET_TEXT}\n{formatted_unpushed_commits}")
            guidance.append("Consider pushing your commits to synchronize with the remote repository.")
        
        # If there are uncommitted changes, list the modified files and provide guidance
        if uncommitted_changes:
            modified_files = repo.git.diff('--name-only').splitlines()
            formatted_modified_files = '\n'.join([f"{OUTPUT_TEXT}  - {file}{RESET_TEXT}" for file in modified_files])
            differences.append(f"{ERROR_TEXT}There are uncommitted changes in the working directory:{RESET_TEXT}\n{formatted_modified_files}")
            guidance.append("Consider committing or stashing your changes before synchronizing with the remote repository.")
        
        # If there are untracked files, list them and provide guidance
        if untracked_files:
            formatted_untracked_files = '\n'.join([f"{OUTPUT_TEXT}  - {file}{RESET_TEXT}" for file in untracked_files])
            differences.append(f"{ERROR_TEXT}There are untracked files:{RESET_TEXT}\n{formatted_untracked_files}")
            guidance.append("Consider adding new files to the repository or updating the .gitignore file if these files should not be tracked.")
        
        # Join the differences and guidance messages and return them
        differences_str = '\n'.join(differences)
        guidance_str = '\n'.join(guidance)
        return f"{ERROR_TEXT}{differences_str}{RESET_TEXT}\n\n{HELP_TEXT}Guidance:\n{guidance_str}{RESET_TEXT}"
        
    except Exception as e:
        # Return an error message if any exception occurs during the comparison
        return f"{ERROR_TEXT}Error comparing with the origin: {e}{RESET_TEXT}"

#--- Define a function to log information about the repository, branch, and latest tag ---#
def log_repository_info(repo, branch_name, latest_tag):
    # Log a header for the repository information section
    logger.info(f"\n{BOLD_TEXT}--- Repository Information ---{RESET_TEXT}")
    
    # Log the current working directory of the repository, the active branch name, and the latest tag
    # The information is highlighted using different text styles for better visibility
    logger.info(f"{OUTPUT_TEXT}You are working in the {ANSWER_TEXT}{repo.working_tree_dir}{OUTPUT_TEXT} repository on the {ANSWER_TEXT}{branch_name}{OUTPUT_TEXT} branch. The latest tag (version) is {ANSWER_TEXT}{latest_tag}{RESET_TEXT}\n")


#--- Define a function to log the status of the repository by displaying the comparison result ---#
def log_status(comparison_result):
    # Log a header for the status section to separate it visually in the log output
    logger.info(f"{BOLD_TEXT}--- Status ---{RESET_TEXT}")
    
    # Log the result of the comparison between the local and remote repository
    # The comparison_result is expected to contain messages about the state of the repository, 
    # such as differences between local and remote, uncommitted changes, untracked files, etc.
    logger.info(comparison_result)

#--- Define a function to log the available options that a user can choose from--- #
def log_options():
    # Log a header for the options section to visually separate it in the log output
    logger.info(f"\n{BOLD_TEXT}--- Options ---{RESET_TEXT}")
    
    # Iterate over each member of the UserChoice enumeration
    for choice in UserChoice:
        # For each choice, log its value and name, with the name capitalized and spaces replacing underscores
        # The name is also converted to lowercase after capitalization to maintain a consistent format
        logger.info(f"{OUTPUT_TEXT}{choice.value}. {choice.name.capitalize().replace('_', ' ').lower()}{RESET_TEXT}")


#--- Define a function to prompt the user to enter their choice and return the entered choice ---#
def get_user_choice():
    # Display a prompt to the user asking them to enter the number corresponding to their choice
    # The prompt is highlighted using a specific text style for better visibility
    # The function then returns the user’s input as a string
    return input(f"\n{QUESTION_TEXT}Enter the number of your choice: {RESET_TEXT}")

#--- Define a function to log a visual separator in the console ---#
def log_separator():
    # Log a series of dashes as a visual separator to organize the console output
    # The separator is highlighted using a specific text style for better visibility
    logger.info(f"{BOLD_TEXT}-----------------------------{RESET_TEXT}\n")

#--- Define a function to push commits from the local branch to the remote origin ---#
def push_commits(repo, branch_name):
    try:
        # Attempt to push commits from the specified local branch to the corresponding remote branch on the origin
        repo.git.push('origin', branch_name)
        
        # Push tags to the remote repository
        repo.git.push('origin', '--tags')
        
        # Log a success message if the push operation is successful
        logger.info(f"{ANSWER_TEXT}Unpushed commits and tags have been pushed to the origin.{RESET_TEXT}")
        
    except Exception as e:
        # Log an error message if any exception occurs during the push operation
        logger.error(f"{ERROR_TEXT}Error pushing commits or tags: {e}{RESET_TEXT}")


#--- Define a function to commit all staged changes in the local repository ---#
def commit_changes(repo):
    # Prompt the user to enter a commit message and store the input
    commit_message = input(f"{QUESTION_TEXT}Enter a commit message: {RESET_TEXT}")
    
    try:
        # Attempt to stage all changes in the working directory
        repo.git.add('.')  # Stage all changes
        
        # Attempt to commit the staged changes with the provided commit message
        repo.git.commit('-m', commit_message)
        
        # Log a success message if the commit operation is successful
        logger.info(f"{ANSWER_TEXT}Uncommitted changes have been committed.{RESET_TEXT}")
        
    except Exception as e:
        # Log an error message if any exception occurs during the commit operation
        logger.error(f"{ERROR_TEXT}Error committing changes: {e}{RESET_TEXT}")

#--- Define a function to add all untracked files in the local repository to the staging area ---#
def add_files(repo):
    try:
        # Attempt to add all untracked files in the working directory to the staging area
        repo.git.add('.')
        
        # Log a success message if the add operation is successful
        logger.info(f"{ANSWER_TEXT}Untracked files have been added.{RESET_TEXT}")
        
    except Exception as e:
        # Log an error message if any exception occurs during the add operation
        logger.error(f"{ERROR_TEXT}Error adding files: {e}{RESET_TEXT}")

#--- Define a function to tag a new version of the code in the local repository ---#
def tag_version(repo, latest_tag):
    # Parse the latest tag to get the current version, or set it to '0.0.0' if no tags are available
    current_version = VersionInfo.parse(latest_tag if latest_tag != "No tags available" else '0.0.0')
    
    # Log the current version and the options to increment major, minor, or patch version
    logger.info(f"{OUTPUT_TEXT}Current version: {ANSWER_TEXT}{current_version}{RESET_TEXT}")
    logger.info(f"{OUTPUT_TEXT}1. Increment major version{RESET_TEXT}")
    logger.info(f"{OUTPUT_TEXT}2. Increment minor version{RESET_TEXT}")
    logger.info(f"{OUTPUT_TEXT}3. Increment patch version{RESET_TEXT}")
    
    # Prompt the user to choose an option to increment the version
    version_choice = input(f"{QUESTION_TEXT}Enter the number of your choice: {RESET_TEXT}")
    
    # Determine the new version based on the user's choice
    if version_choice == '1':
        new_version = current_version.bump_major()
    elif version_choice == '2':
        new_version = current_version.bump_minor()
    elif version_choice == '3':
        new_version = current_version.bump_patch()
    else:
        # Log an error message and return if the user enters an invalid choice
        logger.error(f"{ERROR_TEXT}Invalid choice. Please enter a number between 1 and 3.{RESET_TEXT}")
        return
    
    # Get the diff of the repository and create a new tag with the new version
    diff = repo.git.diff()
    repo.create_tag(str(new_version))
    
    # Open the CHANGELOG.md file and append the new version, date, and changes made in this version
    with open('CHANGELOG.md', 'a') as f:
        f.write(f"\n## {new_version} - {datetime.datetime.now().strftime('%Y-%m-%d')}\n")
        changes = input(f"{QUESTION_TEXT}Enter the changes included in this version (separate multiple changes with commas): {RESET_TEXT}")
        f.write(', '.join(changes.split(',')) + f"\n\n### Diff:\n```\n{diff}\n```\n")
    
    # Log a success message indicating that a new version has been tagged and the changelog has been updated
    logger.info(f"{ANSWER_TEXT}A new version {new_version} has been tagged and the changelog has been updated.{RESET_TEXT}")


# Define the main function to execute the program
def main():
    # Initialize the repository and log the repository information
    repo, branch_name, latest_tag = initialize_repository()
    log_repository_info(repo, branch_name, latest_tag)
    
    # Enter into an infinite loop to continuously prompt the user for choices until the user chooses to exit
    while True:
        # Log the status of the repository by comparing with the origin and log the available options to the user
        log_status(compare_with_origin(repo, branch_name))
        log_options()
        
        # Prompt the user to enter their choice
        user_choice = get_user_choice()
        
        # Execute the corresponding function based on the user's choice
        if user_choice == UserChoice.PUSH.value:
            push_commits(repo, branch_name)
        elif user_choice == UserChoice.COMMIT.value:
            commit_changes(repo)
        elif user_choice == UserChoice.ADD.value:
            add_files(repo)
        elif user_choice == UserChoice.TAG.value:
            tag_version(repo, latest_tag)
        elif user_choice == UserChoice.EXIT.value:
            # Exit the program if the user chooses to exit
            sys.exit(0)
        else:
            # Log an error message if the user enters an invalid choice
            logger.error(f"{ERROR_TEXT}Invalid choice. Please enter a valid number.{RESET_TEXT}")
        
        # Log a separator to organize the console output
        log_separator()


if __name__ == "__main__":
    main()
