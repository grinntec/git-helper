# git_add.py

from git import Repo, exc
from utils import (
    setup_logging,
    get_uncommitted_changes,
)

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

logger = setup_logging()



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
