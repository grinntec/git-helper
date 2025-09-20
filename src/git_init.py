import os
import subprocess
from config import (
    QUESTION_TEXT,
    ANSWER_TEXT,
    ERROR_TEXT,
    OUTPUT_TEXT,
    RESET_TEXT,
    print_section_header,
)
from create_project import simple_project_init

def prompt_for_origin():
    print_section_header("GitHub Remote Setup")
    origin_url = input(f"{QUESTION_TEXT}Enter the GitHub repository URL for origin (or leave blank to skip): {RESET_TEXT}").strip()
    return origin_url if origin_url else None

def init_git_repo(project_path, origin_url=None):
    try:
        subprocess.run(['git', 'init'], cwd=project_path, check=True)
        subprocess.run(['git', 'add', '.'], cwd=project_path, check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial project structure'], cwd=project_path, check=True)
        print(f"{ANSWER_TEXT}Git repository initialized and initial commit made.{RESET_TEXT}")
        if origin_url:
            subprocess.run(['git', 'remote', 'add', 'origin', origin_url], cwd=project_path, check=True)
            print(f"{ANSWER_TEXT}Remote 'origin' set to: {origin_url}{RESET_TEXT}")
    except Exception as e:
        print(f"{ERROR_TEXT}Error initializing git repo: {e}{RESET_TEXT}")

def main():
    print_section_header("New Project + Git Initializer")
    # Run the project scaffold and get the project path
    project_path = simple_project_init()  # <- Return the full path from your scaffold

    if not project_path or not os.path.isdir(project_path):
        print(f"{ERROR_TEXT}The directory {project_path} does not exist. Please check your input and run again.{RESET_TEXT}")
        return

    origin_url = prompt_for_origin()
    init_git_repo(project_path, origin_url)
    print(f"{OUTPUT_TEXT}Project and git setup complete!{RESET_TEXT}")

if __name__ == "__main__":
    main()