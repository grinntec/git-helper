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

from display import (
    clear_screen,
    display_title,
    prompt_to_continue,
    log_options,
    log_separator,
    show_error,
    show_warning,
    get_user_choice,
    UserChoice,
    print_repository_info,
    print_status,
)

from utils import (
    print_section_header,
    setup_logging,
    get_repo_root,
    initialize_repository,
    get_org_and_repo_name,
    get_uncommitted_changes,
    compare_with_origin,
)

from git_pull import (
        git_pull,
)

from git_push import (
    git_push,
)

from git_add import (
    git_add,
)

from git_commit import (
    git_commit,
)

from tag import (
    get_user_choice,
    tag_version,
    get_repo_root,
    update_changelog,
)

logger = setup_logging()

def main():
    error_message = None
    warning_message = None

    while True:
        clear_screen()
        display_title(PROGRAM_TITLE, PROGRAM_AUTHOR, PROGRAM_HELP_TEXT, PROGRAM_VERSION, PROGRAM_DATE)

        # Repo info
        try:
            repo, branch_name, latest_tag = initialize_repository()
            print_repository_info(repo, branch_name, latest_tag)
        except Exception as e:
            logger.error(f"Error initializing repository: {e}")
            show_error(f"Error initializing repository: {e}")
            prompt_to_continue()
            continue

        # Status info
        try:
            comparison_result = compare_with_origin(repo, branch_name)
            print_status(comparison_result)
        except Exception as e:
            logger.error(f"Error comparing with origin: {e}")
            show_error(f"Error comparing with origin: {e}")

        log_options()
        log_separator()

        if warning_message:
            show_warning(warning_message)
            logger.warning(warning_message)
            warning_message = None

        if error_message:
            show_error(error_message)
            logger.error(error_message)
            error_message = None

        choice = get_user_choice()
        if choice == UserChoice.REFRESH.value[0]:
            repo, branch_name, latest_tag = initialize_repository()
        
        elif choice == UserChoice.PULL.value[0]:
            git_pull(repo, branch_name)
            prompt_to_continue()
        
        elif choice == UserChoice.PUSH.value[0]:
            git_push(repo, branch_name)
            prompt_to_continue()

        elif choice == UserChoice.ADD.value[0]:
            git_add(repo)
            prompt_to_continue()
        
        elif choice == UserChoice.COMMIT.value[0]:
            git_commit(repo)
            prompt_to_continue()

        elif choice == UserChoice.TAG.value[0]:
            tag_version(repo, latest_tag)
            prompt_to_continue()
        
        elif choice == UserChoice.EXIT.value[0]:
            logger.info("Exiting the application. Goodbye!")
            print("Exiting the application. Goodbye!")
            break


if __name__ == "__main__":
    main()