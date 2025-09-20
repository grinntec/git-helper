import os
import subprocess
from src.config import (
    QUESTION_TEXT,
    ANSWER_TEXT,
    ERROR_TEXT,
    OUTPUT_TEXT,
    RESET_TEXT,
    print_section_header,
)
from src.create_project import simple_project_init

def prompt_for_origin():
    print_section_header("GitHub Remote Setup")
    while True:
        origin_url = input(f"{QUESTION_TEXT}Enter the GitHub repository URL for origin (or leave blank to skip): {RESET_TEXT}").strip()
        if not origin_url:
            return None
        # Accept SSH and HTTPS URLs only
        if origin_url.startswith('git@github.com:') or origin_url.startswith('https://github.com/'):
            return origin_url
        else:
            print(f"{ERROR_TEXT}Invalid URL format. Please enter a GitHub SSH (git@github.com:...) or HTTPS (https://github.com/...) URL.{RESET_TEXT}")

def init_git_repo(project_path, origin_url=None):
    try:
        if not os.path.isdir(project_path):
            print(f"{ERROR_TEXT}Directory '{project_path}' does not exist.{RESET_TEXT}")
            return
        # Init repo with main as default branch if possible
        # git >=2.28 supports --initial-branch
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        git_version = result.stdout.strip().split()[-1]
        major, minor = map(int, git_version.split('.')[:2])
        if (major > 2) or (major == 2 and minor >= 28):
            subprocess.run(['git', 'init', '--initial-branch=main'], cwd=project_path, check=True)
        else:
            subprocess.run(['git', 'init'], cwd=project_path, check=True)
            subprocess.run(['git', 'checkout', '-b', 'main'], cwd=project_path, check=True)
        subprocess.run(['git', 'add', '.'], cwd=project_path, check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial project structure'], cwd=project_path, check=True)
        print(f"{ANSWER_TEXT}Git repository initialized on 'main' branch and initial commit made.{RESET_TEXT}")
        if origin_url:
            subprocess.run(['git', 'remote', 'add', 'origin', origin_url], cwd=project_path, check=True)
            print(f"{ANSWER_TEXT}Remote 'origin' set to: {origin_url}{RESET_TEXT}")

            # Optionally push to GitHub
            do_push = input(f"{QUESTION_TEXT}Would you like to push the initial commit to GitHub now? (y/N): {RESET_TEXT}").strip().lower()
            if do_push == 'y':
                try:
                    subprocess.run(['git', 'push', '-u', 'origin', 'main'], cwd=project_path, check=True)
                    print(f"{ANSWER_TEXT}Initial commit pushed to 'main' branch on GitHub.{RESET_TEXT}")
                except Exception as e:
                    print(f"{ERROR_TEXT}Failed to push initial commit to 'main': {e}{RESET_TEXT}")
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