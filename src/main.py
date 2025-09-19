from cli import clear_screen, display_title, prompt_to_continue, PROGRAM_TITLE, PROGRAM_AUTHOR, PROGRAM_HELP_TEXT, PROGRAM_VERSION, PROGRAM_DATE,get_user_choice

def main():
    while True:
        clear_screen()
        display_title(PROGRAM_TITLE, PROGRAM_AUTHOR, PROGRAM_HELP_TEXT, PROGRAM_VERSION, PROGRAM_DATE)

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
    
if __name__ == "__main__":
    main()