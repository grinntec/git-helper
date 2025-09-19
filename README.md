[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/grinntec/git-helper?sort=semver)](https://github.com/grinntec/git-helper/tags)

# Git Helper

`git-helper.py` is a Python script designed to assist with common Git operations.

## Overview

The script provides a set of functions to automate and simplify various Git tasks. It's designed to be user-friendly and can be easily integrated into any development workflow.

## Features

- **Initialize a Git Repository**: Quickly set up a new Git repository with essential configurations.
- **Add Files**: Add specific files or all changes to the staging area.
- **Commit Changes**: Commit the staged changes with a custom message.
- **Push Changes**: Push the committed changes to the remote repository.
- **Pull Changes**: Fetch and merge changes from the remote repository.
- **Clone a Repository**: Clone a remote Git repository to your local machine.
- **Check Status**: View the current status of your Git repository, including changes not yet staged or committed.

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
