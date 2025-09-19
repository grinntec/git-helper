from cli import (
    clear_screen,
    display_title,
    prompt_to_continue,
    PROGRAM_TITLE,
    PROGRAM_AUTHOR,
    PROGRAM_HELP_TEXT,
    PROGRAM_VERSION,
    PROGRAM_DATE,
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
    setup_logging,
    get_repo_root,
    initialize_repository,
    get_org_and_repo_name,
)

def main():
    error_message = None
    warning_message = None

    while True:
        clear_screen()
        display_title(PROGRAM_TITLE, PROGRAM_AUTHOR, PROGRAM_HELP_TEXT, PROGRAM_VERSION, PROGRAM_DATE)
        
        # Repo info
        repo, branch_name, latest_tag = initialize_repository()
        print_repository_info(repo, branch_name, latest_tag)

        # Status info
        comparison_result = compare_with_origin(repo, branch_name)
        print_status(comparison_result)

        log_options()
        log_separator()

        if warning_message:
            show_warning(warning_message)
            warning_message = None

        if error_message:
            show_error(error_message)
            error_message = None

        choice = get_user_choice()
        if choice == UserChoice.EXIT.value[0]:
            print("Exiting the application. Goodbye!")
            break

        # In a real app, set error/warning after actual git actions
        if choice == UserChoice.PULL.value[0]:
            warning_message = "Remote branch is ahead, consider pulling."
        elif choice == UserChoice.COMMIT.value[0]:
            error_message = "No staged changes to commit."

        prompt_to_continue()

if __name__ == "__main__":
    main()