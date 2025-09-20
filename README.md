[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/grinntec/git-helper?sort=semver)](https://github.com/grinntec/git-helper/tags)

# Git Helper

`git-helper` is a user-friendly tool for guided Git operations, designed to simplify everyday workflows for both beginners and experienced developers.

---

## Features

- **Initialize a Git Repository**: Set up a new Git repository with essential configuration, using `main` as the default branch.
- **Add Files**: Stage new or modified files interactively.
- **Commit Changes**: Commit staged changes with a custom message.
- **Push/Pull Changes**: Synchronize your local repository with the remote.
- **Clone a Repository**: Clone remote repositories to your machine.
- **Check Status**: View status, uncommitted changes, and branch differences.
- **Tag and Release**: Create semantic version tags and update changelogs.
- **Project Creation**: Scaffold a new Python project structure.

---

## Installation

### Option 1: Run from Source (Python 3.10+)

1. **Clone the repository**
    ```sh
    git clone https://github.com/grinntec/git-helper.git
    cd git-helper
    ```

2. **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```

3. **Run the helper**
    ```sh
    python main.py
    ```

---

### Option 2: Install the Prebuilt Binary (Windows 11)

You do **not** need Python or any extra dependencies!

1. **Download the binary**
    - Visit [GitHub Releases](https://github.com/grinntec/git-helper/releases)
    - Download `git-helper.exe` from the latest release.

2. **(Optional) Move to a convenient folder**
    - E.g. `C:\Program Files\git-helper\`

3. **(Optional) Add to your system PATH**
    - Open "Edit environment variables for your account"
    - Add the folder (e.g. `C:\Program Files\git-helper\`) to the `Path` variable.
    - Click OK and restart your terminal.

4. **Run the binary**
    - From anywhere in CMD/PowerShell (if on PATH):
        ```sh
        git-helper.exe
        ```
    - Or navigate to the folder and run:
        ```sh
        cd "C:\Program Files\git-helper"
        .\git-helper.exe
        ```

**Uninstall:**  
Delete `git-helper.exe` and remove its folder from PATH if added.

---

## Building the Binary Yourself (Advanced)

1. **Install PyInstaller**
    ```sh
    pip install pyinstaller
    ```

2. **Build the binary**
    ```sh
    pyinstaller --onefile main.py --name git-helper
    ```
    The binary will be created in the `dist/` folder.

3. **Distribute or install as above!**

---

## Usage

Start the tool and follow the on-screen prompts to perform common Git operations interactively.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Support & Feedback

If you have issues or feature requests, please [open an issue](https://github.com/grinntec/git-helper/issues).