# git_commit.py
from git import Repo, exc
from src.utils import (
    setup_logging,
    get_uncommitted_changes,
)

from src.config import (
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



