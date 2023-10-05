import os
import sys
import git
import logging
import semver
from semver import VersionInfo
import datetime
from enum import Enum
import tempfile

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
WARNING_TEXT = '\033[93m'  # Yellow
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
    REFRESH = ('0', 'REFRESH and display current status')
    
    # PULL represents the choice to pull changes from the remote repository
    PULL = ('1', 'PULL changes from remote repository')  
    
    # PUSH represents the choice to push changes to the remote repository
    PUSH = ('2', 'PUSH changes to remote repository (into MAIN branch)')    
    
    # COMMIT represents the choice to commit changes to the local repository
    COMMIT = ('3', 'COMMIT changes to local repository')
    
    # ADD represents the choice to add changes to the staging area
    ADD = ('4', 'ADD changes/files to staging area')    
    
    # TAG represents the choice to tag a specific commit
    TAG = ('5', 'TAG the repository')    
    
    # EXIT represents the choice to exit the application
    EXIT = ('6', 'Exit the application')
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
    logger.info(f"{BOLD_TEXT}--- Differences ---{RESET_TEXT}")
    
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
        # Extract the number and description from the value
        number, description = choice.value
        logger.info(f"{OUTPUT_TEXT}{number}. {description}{RESET_TEXT}")
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

        # Get the messages for uncommitted changes and untracked files
        messages += get_uncommitted_changes(repo)

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
# --- Commit changes --- #
def commit_changes(repo):

    def get_changed_files():
        untracked = repo.untracked_files
        changed = [item.a_path for item in repo.index.diff(None)]
        staged = [item.a_path for item in repo.index.diff('HEAD')]
        return untracked, changed, staged

    def stage_files(stage_all, files_to_stage=None):
        if stage_all:
            repo.git.add('.')
        elif files_to_stage:
            for file in files_to_stage:
                if file in untracked_files or file in changed_files:
                    repo.git.add(file)
                else:
                    logger.warning(f"{WARNING_TEXT}File '{file}' does not exist or has no changes. Skipping...{RESET_TEXT}")

    untracked_files, changed_files, staged_files = get_changed_files()

    if not untracked_files and not changed_files and not staged_files:
        logger.info(f"{ANSWER_TEXT}No changes to commit.{RESET_TEXT}")
        return

    # Display the files
    for category, files in [("Untracked files", untracked_files), ("Modified files", changed_files), ("Staged files", staged_files)]:
        print(f"{QUESTION_TEXT}{category}:{RESET_TEXT}")
        for file in files:
            print(file)

    while True:
        stage_decision = input(f"{QUESTION_TEXT}Would you like to stage all changes for commit? (yes/no/exit): {RESET_TEXT}").lower()

        if stage_decision == 'yes':
            stage_files(True)
            break
        elif stage_decision == 'no':
            files_to_stage = input(f"{QUESTION_TEXT}Enter the names of the files you'd like to stage, separated by spaces (or 'exit' to quit): {RESET_TEXT}").split()
            if 'exit' in files_to_stage:
                logger.info(f"{ANSWER_TEXT}Exiting commit process.{RESET_TEXT}")
                return
            stage_files(False, files_to_stage)
            break
        elif stage_decision == 'exit':
            logger.info(f"{ANSWER_TEXT}Exiting commit process.{RESET_TEXT}")
            return

    commit_message_input = input(f"{QUESTION_TEXT}Enter a commit message (separate lines with ';', or 'exit' to quit): {RESET_TEXT}").strip()
    commit_message = commit_message_input.replace(";", "\n")

    while not commit_message.strip():
        if commit_message.lower() == 'exit':
            logger.info(f"{ANSWER_TEXT}Exiting commit process.{RESET_TEXT}")
            return
        commit_message_input = input(f"{ERROR_TEXT}Commit message can't be empty! Please enter a valid commit message (separate lines with ';', or 'exit' to quit): {RESET_TEXT}").strip()
        commit_message = commit_message_input.replace(";", "\n")

    # Write commit message to temporary file and commit
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp_file:
        tmp_file.write(commit_message)
        tmp_filename = tmp_file.name

    try:
        repo.git.commit('-F', tmp_filename)
        os.remove(tmp_filename)  # Clean up the temporary file
        logger.info(f"{ANSWER_TEXT}Uncommitted changes have been committed.{RESET_TEXT}")
    except git.exc.GitCommandError as e:
        os.remove(tmp_filename)  # Clean up the temporary file
        logger.error(f"{ERROR_TEXT}Error committing changes: {e}{RESET_TEXT}")
    except Exception as e:
        os.remove(tmp_filename)  # Clean up the temporary file
        logger.error(f"{ERROR_TEXT}An unexpected error occurred: {e}{RESET_TEXT}")
#############################################################################################################
# --- Add files --- #
def add_files(repo):
    # Fetching the list of untracked files
    untracked_files = repo.untracked_files

    # Fetching the list of modified but not staged files
    modified_not_staged_files = repo.git.diff('--name-only').splitlines()

    # Combine the lists for simplicity in further steps
    files_to_display = untracked_files + modified_not_staged_files

    # If there are no files to display, notify the user and return
    if not files_to_display:
        logger.info(f"{ANSWER_TEXT}No untracked or modified files found.{RESET_TEXT}")
        return
    
    # Display the files
    print(f"{QUESTION_TEXT}Files ready for staging:{RESET_TEXT}")
    for file in files_to_display:
        status = "Untracked" if file in untracked_files else "Modified (not staged)"
        print(f"{file} ({status})")

    while True:
        user_decision = input(f"{QUESTION_TEXT}Would you like to add all files? (yes/no): {RESET_TEXT}").strip().lower()
        
        try:
            if user_decision == 'yes':
                repo.git.add('-A')
                logger.info(f"{ANSWER_TEXT}All files added successfully!{RESET_TEXT}")
                break
            elif user_decision == 'no':
                files_to_add = input(f"{QUESTION_TEXT}Enter the names of the files you'd like to add, separated by spaces: {RESET_TEXT}").split()
                
                # Check if user provided any filenames
                if not files_to_add:
                    logger.warning(f"{WARNING_TEXT}No files provided. Please specify files to add or choose 'yes' to add all.{RESET_TEXT}")
                    continue
                
                # Attempt to add specified files
                added_any = False
                for file in files_to_add:
                    if file in files_to_display:
                        repo.git.add(file)
                        added_any = True
                    else:
                        logger.warning(f"{WARNING_TEXT}File {file} was not in the list and was skipped.{RESET_TEXT}")

                # If we added any files, log success and break out
                if added_any:
                    logger.info(f"{ANSWER_TEXT}Selected files have been added.{RESET_TEXT}")
                    break
            else:
                logger.warning(f"{WARNING_TEXT}Invalid input. Please enter 'yes' or 'no'.{RESET_TEXT}")

        except git.exc.GitCommandError as e:
            # Handle specific Git errors
            logger.error(f"{ERROR_TEXT}Error adding files: {e}{RESET_TEXT}")
#############################################################################################################
# --- Get uncommited changes --- #
def get_uncommitted_changes(repo):
    messages = ""

    # Get modified but not staged files
    unstaged_files = repo.git.diff('--name-only').splitlines()

    # Get staged but not yet committed files
    staged_files = repo.git.diff('--cached', '--name-only').splitlines()

    # Get newly added (untracked) files
    untracked_files = repo.untracked_files

    if unstaged_files:
        formatted_unstaged_files = '\n'.join([f"{OUTPUT_TEXT}  Modified (not staged): {file}{RESET_TEXT}" for file in unstaged_files])
        messages += f"{ANSWER_TEXT}There are uncommitted changes in the working directory:\n{formatted_unstaged_files}{RESET_TEXT}\n"

    if staged_files:
        formatted_staged_files = '\n'.join([f"{OUTPUT_TEXT}  Modified (staged): {file}{RESET_TEXT}" for file in staged_files])
        messages += f"{ANSWER_TEXT}There are staged changes not yet committed:\n{formatted_staged_files}{RESET_TEXT}\n"

    if untracked_files:
        formatted_untracked_files = '\n'.join([f"{OUTPUT_TEXT}  New file (untracked): {file}{RESET_TEXT}" for file in untracked_files])
        messages += f"{ANSWER_TEXT}There are new untracked files:\n{formatted_untracked_files}{RESET_TEXT}\n"

    if unstaged_files or staged_files or untracked_files:
        messages += f"{HELP_TEXT}Guidance: Consider actions like (3.)COMMITTING your changes or (4.)ADDING new files before synchronizing with the remote repository.{RESET_TEXT}\n\n"

    return messages
#############################################################################################################
# --- Create the tag ---#
def tag_version(repo, latest_tag):
    if repo.is_dirty():
        logger.error(f"{ERROR_TEXT}Uncommitted changes detected. Please commit your changes before tagging a new version.{RESET_TEXT}")
        return

    current_version = VersionInfo.parse(latest_tag if latest_tag != "No tags available" else '0.0.0')
    logger.info(f"{OUTPUT_TEXT}Current version: {ANSWER_TEXT}{current_version}{RESET_TEXT}")

    version_choices = ["1. Increment major version", "2. Increment minor version", "3. Increment patch version"]
    for choice in version_choices:
        logger.info(f"{OUTPUT_TEXT}{choice}{RESET_TEXT}")

    version_choice = input(f"{QUESTION_TEXT}Enter the number of your choice: {RESET_TEXT}")

    if version_choice == '1':
        new_version = current_version.bump_major()
    elif version_choice == '2':
        new_version = current_version.bump_minor()
    elif version_choice == '3':
        new_version = current_version.bump_patch()
    else:
        logger.error(f"{ERROR_TEXT}Invalid choice. Please enter a number between 1 and 3.{RESET_TEXT}")
        return

    diff = repo.git.diff('HEAD~1', '--unified=0')

    tag_message = input(f"{QUESTION_TEXT}Enter a message for this tag (optional): {RESET_TEXT}")

    # Create the tag locally
    repo.create_tag(str(new_version), message=tag_message.strip())

    # Update the changelog
    update_changelog(new_version, diff)

    # Commit changelog update
    if repo.is_dirty():
        repo.git.add('-A')
        repo.git.commit('-m', f"Update changelog for version {new_version}")

    try:
        # Push commits and tags to remote repository
        repo.git.push('origin', 'HEAD')
        repo.git.push('origin', '--tags')
        logger.info(f"{ANSWER_TEXT}Tag {new_version} has been pushed to the remote repository.{RESET_TEXT}")
    except git.exc.GitCommandError as e:
        logger.error(f"{ERROR_TEXT}Error pushing tag to remote: {e}{RESET_TEXT}")
#############################################################################################################
# --- Update the change log ---#
def update_changelog(version, diff):
    temp_file = "CHANGELOG_TEMP.md"
    with open(temp_file, 'w') as temp, open('CHANGELOG.md', 'r') as original:
        # Write the new changelog entry at the top
        temp.write(f"\n## {version} - {datetime.datetime.now().strftime('%Y-%m-%d')}\n")
        changes = input(f"{QUESTION_TEXT}Enter the changes included in this version (separate multiple changes with a new line): {RESET_TEXT}")
        for change in changes.split('\n'):
            temp.write(f"- {change.strip()}\n")
        temp.write(f"\n### Diff:\n```\n{diff}\n```\n\n")
        # Copy the rest of the original changelog
        temp.write(original.read())
    # Replace the original changelog with the temporary one
    os.replace(temp_file, 'CHANGELOG.md')
    logger.info(f"{ANSWER_TEXT}CHANGELOG.md has been updated with version {version} and associated changes.{RESET_TEXT}")
#############################################################################################################
def get_user_choice():
    choice = input("\nEnter the number of your choice: ")
    return choice
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

        if choice == UserChoice.REFRESH.value[0]:
            repo, branch_name, latest_tag = initialize_repository()
        elif choice == UserChoice.PULL.value[0]:
            pull_origin(repo, branch_name)
        elif choice == UserChoice.PUSH.value[0]:
            push_commits(repo, branch_name)
        elif choice == UserChoice.COMMIT.value[0]:
            commit_changes(repo)
        elif choice == UserChoice.ADD.value[0]:
            add_files(repo)
        elif choice == UserChoice.TAG.value[0]:
            tag_version(repo, latest_tag)
            latest_tag = str(max(repo.tags, key=lambda t: semver.VersionInfo.parse(t.name)) if repo.tags else "No tags available")
        elif choice == UserChoice.EXIT.value[0]:
            logger.info(f"{ANSWER_TEXT}Exiting the program. Goodbye!{RESET_TEXT}")
            sys.exit(0)
        else:
            logger.error(f"{ERROR_TEXT}Invalid choice! Please select a valid option.{RESET_TEXT}")
        
        # Only prompt to continue if choice wasn't "Refresh" or "Exit"
        if choice != UserChoice.REFRESH.value[0] and choice != UserChoice.EXIT.value[0]:
            prompt_to_continue()

#############################################################################################################         
if __name__ == "__main__":
    main()