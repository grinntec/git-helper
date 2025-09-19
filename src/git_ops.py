from git import Repo, exc
from utils import (
    setup_logging,
    get_uncommitted_changes,
)

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

# Section header function
def print_section_header(text, color=BOLD_TEXT):
    """
    Print a visually strong section header with underline and color.
    
    # Example usage in your CLI script:
        print_section_header("Repository Information", color=QUESTION_TEXT)
        print_section_header("Options", color=WARNING_TEXT)
        print_section_header("Differences between local and origin", color=OUTPUT_TEXT)
        print_section_header("Error", color=ERROR_TEXT)
        print_section_header("Guidance", color=HELP_TEXT)

    """
    line_length = max(32, len(text) + 6)
    print(f"{color}{'=' * line_length}{RESET_TEXT}")
    print(f"{color}{text.center(line_length)}{RESET_TEXT}")
    print(f"{color}{'=' * line_length}{RESET_TEXT}")

logger = setup_logging()

# --- Pull from origin --- #
def git_pull(repo, branch_name):
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
def git_push(repo, branch_name):
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

def git_add(repo):
    """
    Interactive function to add files to the Git staging area.

    This function helps you select which files (untracked or modified) you want to stage.
    You can add all files at once, or select specific files by number or name.
    """

    # Gather all untracked (new) and modified-but-not-staged files
    untracked_files = repo.untracked_files
    modified_not_staged_files = repo.git.diff('--name-only').splitlines()
    files_to_display = untracked_files + modified_not_staged_files

    # If there are no files to add, inform the user and exit early
    if not files_to_display:
        logger.info(f"{ANSWER_TEXT}No untracked or modified files found.{RESET_TEXT}")
        return

    # Print the list of files that can be staged, with index and status
    print(f"{QUESTION_TEXT}Files ready for staging:{RESET_TEXT}")
    for idx, file in enumerate(files_to_display, 1):
        status = "Untracked" if file in untracked_files else "Modified (not staged)"
        print(f"{idx}. {file} ({status})")

    # Loop until the user makes a valid decision
    while True:
        # Ask the user if they want to add all files, just some, or exit
        user_decision = input(f"{QUESTION_TEXT}Would you like to add all files? (yes/no/exit): {RESET_TEXT}").strip().lower()
        if user_decision == 'yes':
            # Add all changes found (new and modified) to the staging area
            try:
                repo.git.add('-A')
                logger.info(f"{ANSWER_TEXT}All files added successfully!{RESET_TEXT}")
                print(f"{ANSWER_TEXT}Staged files:\n" + '\n'.join(files_to_display) + RESET_TEXT)
                break
            except git.exc.GitCommandError as e:
                # Handle git errors (e.g., permission issues)
                logger.error(f"{ERROR_TEXT}Error adding files: {e}{RESET_TEXT}")

        elif user_decision == 'no':
            # Let the user select specific files to add by number or name
            files_input = input(f"{QUESTION_TEXT}Enter the number for each files of the files you'd like to add, separated by spaces: {RESET_TEXT}").split()
            files_to_add = []
            for entry in files_input:
                # If input is a number, map it to the corresponding file
                if entry.isdigit() and 1 <= int(entry) <= len(files_to_display):
                    files_to_add.append(files_to_display[int(entry)-1])
                # If input is a filename, use it directly
                elif entry in files_to_display:
                    files_to_add.append(entry)
                else:
                    # Warn about invalid entries
                    logger.warning(f"{WARNING_TEXT}Entry '{entry}' was not in the list and was skipped.{RESET_TEXT}")

            # If nothing valid was entered, warn and repeat
            if not files_to_add:
                logger.warning(f"{WARNING_TEXT}No valid files provided. Please specify files to add or choose 'yes' to add all.{RESET_TEXT}")
                continue

            # Try to add each selected file, handling errors per file
            added_any = False
            for file in files_to_add:
                try:
                    repo.git.add(file)
                    added_any = True
                except git.exc.GitCommandError as e:
                    logger.error(f"{ERROR_TEXT}Error adding file {file}: {e}{RESET_TEXT}")

            # If any files were successfully added, confirm and exit loop
            if added_any:
                logger.info(f"{ANSWER_TEXT}Selected files have been added:{RESET_TEXT}\n" + '\n'.join(files_to_add))
                break

        elif user_decision == 'exit':
            # User chooses to quit the add process
            logger.info(f"{ANSWER_TEXT}Exiting file addition process.{RESET_TEXT}")
            return

        else:
            # Any other response is invalid; user is prompted again
            logger.warning(f"{WARNING_TEXT}Invalid input. Please enter 'yes', 'no', or 'exit'.{RESET_TEXT}")

# --- Commit changes --- #
def git_commit(repo):

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



