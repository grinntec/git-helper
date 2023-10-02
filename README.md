# Git Automation Tool

This tool automates various Git operations such as pushing commits, committing changes, adding files, tagging versions, and more. It provides a user-friendly interface to perform these operations with ease.

## Code Overview

The code is structured into several functions, each performing a specific task related to Git operations. Here's a brief overview of the main functions:

- `initialize_repository()`: Initializes the Git repository and sets the current working directory as the repository path.
- `compare_with_origin(repo, branch_name)`: Compares the local branch with the remote branch and logs the differences.
- `log_repository_info(repo, branch_name, latest_tag)`: Logs information about the repository, including the working directory, branch name, and the latest tag.
- `log_status(comparison_result)`: Logs the status of the repository by comparing it with the origin.
- `log_options()`: Logs the available options to the user.
- `get_user_choice()`: Prompts the user to enter their choice and returns the input.
- `push_commits(repo, branch_name)`: Pushes the unpushed commits to the origin.
- `commit_changes(repo)`: Commits the uncommitted changes in the local repository.
- `add_files(repo)`: Adds all untracked files in the local repository to the staging area.
- `tag_version(repo, latest_tag)`: Tags a new version of the code in the local repository.
- `main()`: The main function that executes the program and contains the main loop to continuously prompt the user for choices until the user chooses to exit.

  ![image](https://github.com/grinntec/git-helper/assets/40019507/52835528-47c8-4cdc-b59f-a9a047f93315)

## Compiling the Python File into a Binary using PyInstaller

To compile the Python file into a binary, you can use PyInstaller. PyInstaller bundles a Python application and all its dependencies into a single package. Follow the steps below to compile the Python file:

Install PyInstaller:
```sh
pip install pyinstaller
```

Navigate to the directory containing your Python file and run the following command:

```sh
pyinstaller --onefile your_python_file.py
```

After running the command, PyInstaller will create a dist directory in the same folder as your Python file. Inside the dist directory, you will find the compiled binary file.

You can now run the binary file without needing a Python interpreter or any dependencies.

## Usage
Run the compiled binary or the Python file directly, and follow the on-screen prompts to perform Git operations.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.
