# tag.py

from semver import VersionInfo
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