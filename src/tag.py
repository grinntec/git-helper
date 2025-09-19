# tag.py

from semver import VersionInfo
from git import Repo, exc
import os

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

#--- Prompt the user to enter their choice and return the entered choice ---#
def get_user_choice():
    # Display a prompt to the user asking them to enter the number corresponding to their choice
    # The prompt is highlighted using a specific text style for better visibility
    # The function then returns the user’s input as a string
    return input(f"\n{QUESTION_TEXT}Enter the number of your choice: {RESET_TEXT}")

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

# --- Update the change log ---#
def get_repo_root():
    """Get the root directory of the git repository."""
    repo = Repo(os.getcwd(), search_parent_directories=True)
    return repo.git.rev_parse("--show-toplevel")

# --- Add a diff and comment to the change log --- #
def update_changelog(version, diff):
    repo_root = get_repo_root()
    changelog_path = os.path.join(repo_root, 'CHANGELOG.md')
    temp_file = os.path.join(repo_root, "CHANGELOG_TEMP.md")
    
    try:
        with open(temp_file, 'w') as temp:
            # Check if CHANGELOG.md exists in the repo root
            if os.path.exists(changelog_path):
                with open(changelog_path, 'r') as original:
                    # Write the new changelog entry at the top
                    temp.write(f"\n## {version} - {datetime.datetime.now().strftime('%Y-%m-%d')}\n")
                    
                    # Ask for changes with a semicolon delimiter
                    changes_input = input(f"{QUESTION_TEXT}Enter the changes included in this version (separate multiple changes with ';'): {RESET_TEXT}")
                    changes = changes_input.split(';')
                    
                    for change in changes:
                        temp.write(f"- {change.strip()}\n")
                    temp.write(f"\n### Diff:\n```\n{diff}\n```\n\n")
                    
                    # Copy the rest of the original changelog
                    temp.write(original.read())
            else:
                print(f"{ANSWER_TEXT}CHANGELOG.md not found in the repository root. Creating a new one.{RESET_TEXT}")
                temp.write(f"\n## {version} - {datetime.datetime.now().strftime('%Y-%m-%d')}\n")
        
        # Replace the original changelog with the temporary one
        shutil.move(temp_file, changelog_path)
        print(f"{ANSWER_TEXT}CHANGELOG.md in the repository root has been updated with version {version} and associated changes.{RESET_TEXT}")
    except Exception as e:
        print(f"Error updating CHANGELOG.md: {e}")
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