import os
import sys
import git
from git import Repo
import logging
import semver
from semver import VersionInfo
import datetime
import tempfile
import shutil


# utils.py
import logging

# Configure the basic settings for logging
# Set the logging level to INFO, so it will capture Info, Warning, Error, and Critical messages
# Format the log messages to display only the actual log message
logging.basicConfig(level=logging.INFO, format='%(message)s')








#--- Prompt the user to enter their choice and return the entered choice ---#
def get_user_choice():
    # Display a prompt to the user asking them to enter the number corresponding to their choice
    # The prompt is highlighted using a specific text style for better visibility
    # The function then returns the user’s input as a string
    return input(f"\n{QUESTION_TEXT}Enter the number of your choice: {RESET_TEXT}")

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
        messages += f"\n{ANSWER_TEXT}{UNDERLINE_TEXT}There are uncommited changes:{RESET_TEXT}\n{formatted_staged_files}{RESET_TEXT}\n\n"
        messages += f"{HELP_TEXT}Guidance: Consider {WARNING_TEXT}(3.)COMMITTING{RESET_TEXT} your changes.{RESET_TEXT}\n"
        messages += f"{HELP_TEXT}>    Files that have been marked for inclusion in the next commit.{RESET_TEXT}\n"
        messages += f"{HELP_TEXT}>    You shouldn't change these files any further.{RESET_TEXT}\n"
        messages += f"{HELP_TEXT}>    Once staged, the files will be pushed to the origin.{RESET_TEXT}\n\n"

    if unstaged_files:
        formatted_unstaged_files = '\n'.join([f"{OUTPUT_TEXT}  Modified (not staged): {file}{RESET_TEXT}" for file in unstaged_files])
        messages += f"\n{ANSWER_TEXT}{UNDERLINE_TEXT}There are changes to existing files which aren't yet added to staging:{RESET_TEXT}\n{formatted_unstaged_files}{RESET_TEXT}\n\n"
        messages += f"{HELP_TEXT}Guidance: Consider {WARNING_TEXT}(4.)ADDING{RESET_TEXT} the changed files to staging.{RESET_TEXT}\n"
        messages += f"{HELP_TEXT}>    Already existing files that have been changed since the last commit, but not yet staged.{RESET_TEXT}\n"
        messages += f"{HELP_TEXT}>    Only add files that are ready to be staged and then committed to the origin repository.{RESET_TEXT}\n"
        messages += f"{HELP_TEXT}>    When added, the files will be staged where you will then commit them.{RESET_TEXT}\n\n"

    if untracked_files:
        formatted_untracked_files = '\n'.join([f"{OUTPUT_TEXT}  New file (untracked): {file}{RESET_TEXT}" for file in untracked_files])
        messages += f"\n{ANSWER_TEXT}{UNDERLINE_TEXT}There are new (untracked) files which aren't yet added to staging:{RESET_TEXT}\n{formatted_untracked_files}{RESET_TEXT}\n\n"
        messages += f"{HELP_TEXT}Guidance: Consider {WARNING_TEXT}(4.)ADDING{RESET_TEXT} the new files to staging.{RESET_TEXT}\n"
        messages += f"{HELP_TEXT}>    New files that are recognized by Git, but they have not yet been added to staging in preparation for a commit.{RESET_TEXT}\n"
        messages += f"{HELP_TEXT}>    Only add files that are ready to be staged and then committed to the origin repository.{RESET_TEXT}\n"
        messages += f"{HELP_TEXT}>    When added, the files will be staged where you will then commit them.{RESET_TEXT}\n\n"

    return messages

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

# --- Commit changes --- #
def commit_changes(repo):

    def get_changed_files():
        untracked = repo.untracked_files
        changed = [item.a_path for item in repo.index.diff(None)]
        staged = [item.a_path for item in repo.index.diff('HEAD')]
        return untracked, changed, staged

    untracked_files, changed_files, staged_files = get_changed_files()

    if not staged_files:
        logger.info(f"{ANSWER_TEXT}No staged changes to commit.{RESET_TEXT}")
        return

    # Display the files
    for category, files in [("Staged files", staged_files)]:
        print(f"{QUESTION_TEXT}{category}:{RESET_TEXT}")
        for file in files:
            print(file)

    commit_message = input(f"{QUESTION_TEXT}Enter a single-line commit message (or 'exit' to quit): {RESET_TEXT}").strip()

    if commit_message.lower() == 'exit':
        logger.info(f"{ANSWER_TEXT}Exiting commit process.{RESET_TEXT}")
        return

    while not commit_message.strip():
        commit_message = input(f"{ERROR_TEXT}Commit message can't be empty! Please enter a valid single-line commit message (or 'exit' to quit): {RESET_TEXT}").strip()
        if commit_message.lower() == 'exit':
            logger.info(f"{ANSWER_TEXT}Exiting commit process.{RESET_TEXT}")
            return

    try:
        repo.git.commit('-m', commit_message)
        logger.info(f"{ANSWER_TEXT}Staged changes have been committed.{RESET_TEXT}")
    except git.exc.GitCommandError as e:
        logger.error(f"{ERROR_TEXT}Error committing changes: {e}{RESET_TEXT}")
    except Exception as e:
        logger.error(f"{ERROR_TEXT}An unexpected error occurred: {e}{RESET_TEXT}")

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
        user_decision = input(f"{QUESTION_TEXT}Would you like to add all files? (yes/no/exit): {RESET_TEXT}").strip().lower()
        
        if user_decision == 'yes':
            try:
                repo.git.add('-A')
                logger.info(f"{ANSWER_TEXT}All files added successfully!{RESET_TEXT}")
                break
            except git.exc.GitCommandError as e:
                # Handle specific Git errors
                logger.error(f"{ERROR_TEXT}Error adding files: {e}{RESET_TEXT}")

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
                    try:
                        repo.git.add(file)
                        added_any = True
                    except git.exc.GitCommandError as e:
                        # Handle specific Git errors
                        logger.error(f"{ERROR_TEXT}Error adding file {file}: {e}{RESET_TEXT}")
                else:
                    logger.warning(f"{WARNING_TEXT}File {file} was not in the list and was skipped.{RESET_TEXT}")

            # If we added any files, log success and break out
            if added_any:
                logger.info(f"{ANSWER_TEXT}Selected files have been added.{RESET_TEXT}")
                break

        elif user_decision == 'exit':
            logger.info(f"{ANSWER_TEXT}Exiting file addition process.{RESET_TEXT}")
            return

        else:
            logger.warning(f"{WARNING_TEXT}Invalid input. Please enter 'yes', 'no', or 'exit'.{RESET_TEXT}")

# --- Create the tag ---#
def tag_version(repo, latest_tag):
    if repo.is_dirty():
        logger.error(f"{ERROR_TEXT}Uncommitted changes detected. Please commit your changes before tagging a new version.{RESET_TEXT}")
        return

    current_version = VersionInfo.parse(latest_tag if latest_tag != "No tags available" else '0.0.0')
    logger.info(f"{OUTPUT_TEXT}Current version: {ANSWER_TEXT}{current_version}{RESET_TEXT}")

    version_choices = [
        "1. Increment major version",
        "2. Increment minor version",
        "3. Increment patch version",
        "4. Exit without tagging"
    ]
    for choice in version_choices:
        logger.info(f"{OUTPUT_TEXT}{choice}{RESET_TEXT}")

    version_choice = input(f"{QUESTION_TEXT}Enter the number of your choice: {RESET_TEXT}")

    if version_choice == '1':
        new_version = current_version.bump_major()
    elif version_choice == '2':
        new_version = current_version.bump_minor()
    elif version_choice == '3':
        new_version = current_version.bump_patch()
    elif version_choice == '4':
        logger.info(f"{ANSWER_TEXT}Exiting without tagging.{RESET_TEXT}")
        return
    else:
        logger.error(f"{ERROR_TEXT}Invalid choice. Please enter a number between 1 and 4.{RESET_TEXT}")
        return

    diff = repo.git.diff('HEAD~1', '--unified=0')

    # Create the tag locally without a message
    repo.create_tag(str(new_version))

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




#--- Define the main function to execute the program --- #
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

        
         
if __name__ == "__main__":
    main()