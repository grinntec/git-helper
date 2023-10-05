
## 11.0.0 - 2023-10-05
- added exit to tag function

### Diff:
```
diff --git a/fromGE/current/git-helper-17.py b/fromGE/current/git-helper-17.py
index a5c2edf..6611df6 100644
--- a/fromGE/current/git-helper-17.py
+++ b/fromGE/current/git-helper-17.py
@@ -440 +440,6 @@ def tag_version(repo, latest_tag):
-    version_choices = ["1. Increment major version", "2. Increment minor version", "3. Increment patch version"]
+    version_choices = [
+        "1. Increment major version",
+        "2. Increment minor version",
+        "3. Increment patch version",
+        "4. Exit without tagging"
+    ]
@@ -451,0 +457,3 @@ def tag_version(repo, latest_tag):
+    elif version_choice == '4':
+        logger.info(f"{ANSWER_TEXT}Exiting without tagging.{RESET_TEXT}")
+        return
@@ -453 +461 @@ def tag_version(repo, latest_tag):
-        logger.error(f"{ERROR_TEXT}Invalid choice. Please enter a number between 1 and 3.{RESET_TEXT}")
+        logger.error(f"{ERROR_TEXT}Invalid choice. Please enter a number between 1 and 4.{RESET_TEXT}")
@@ -476,0 +485 @@ def tag_version(repo, latest_tag):
+
```


## 10.0.0 - 2023-10-05
- this works

### Diff:
```
diff --git a/fromGE/current/git-helper-17.py b/fromGE/current/git-helper-17.py
index a00098c..cd8c14b 100644
--- a/fromGE/current/git-helper-17.py
+++ b/fromGE/current/git-helper-17.py
@@ -344,2 +344,3 @@ def commit_changes(repo):
-    commit_message_input = input(f"{QUESTION_TEXT}Enter a commit message (separate lines with ';', or 'exit' to quit): {RESET_TEXT}").strip()
-    if commit_message_input.lower() == 'exit':
+    commit_message = input(f"{QUESTION_TEXT}Enter a single-line commit message (or 'exit' to quit): {RESET_TEXT}").strip()
+
+    if commit_message.lower() == 'exit':
@@ -349,2 +349,0 @@ def commit_changes(repo):
-    commit_message = commit_message_input.replace(";", "\n")
-
@@ -352,2 +351,2 @@ def commit_changes(repo):
-        commit_message_input = input(f"{ERROR_TEXT}Commit message can't be empty! Please enter a valid commit message (separate lines with ';', or 'exit' to quit): {RESET_TEXT}").strip()
-        if commit_message_input.lower() == 'exit':
+        commit_message = input(f"{ERROR_TEXT}Commit message can't be empty! Please enter a valid single-line commit message (or 'exit' to quit): {RESET_TEXT}").strip()
+        if commit_message.lower() == 'exit':
@@ -356,6 +354,0 @@ def commit_changes(repo):
-        commit_message = commit_message_input.replace(";", "\n")
-
-    # Write commit message to temporary file and commit
-    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp_file:
-        tmp_file.write(commit_message)
-        tmp_filename = tmp_file.name
@@ -364,2 +357 @@ def commit_changes(repo):
-        repo.git.commit('-F', tmp_filename)
-        os.remove(tmp_filename)  # Clean up the temporary file
+        repo.git.commit('-m', commit_message)
@@ -368 +359,0 @@ def commit_changes(repo):
-        os.remove(tmp_filename)  # Clean up the temporary file
@@ -371 +361,0 @@ def commit_changes(repo):
-        os.remove(tmp_filename)  # Clean up the temporary file
@@ -373,0 +364 @@ def commit_changes(repo):
+
```


## 9.0.0 - 2023-10-05
- fixed a load of comment
- looks great now

### Diff:
```
diff --git a/fromGE/current/git-helper-16.py b/fromGE/current/git-helper-16.py
index cae8b22..3bd618c 100644
--- a/fromGE/current/git-helper-16.py
+++ b/fromGE/current/git-helper-16.py
@@ -211 +211 @@ def compare_with_origin(repo, branch_name):
-            messages += f"{ANSWER_TEXT}{UNDERLINE_TEXT}Local branch {branch_name} is ahead of the remote origin by {len(ahead_commits)} commits.{RESET_TEXT}\n"
+            messages += f"\n{ANSWER_TEXT}{UNDERLINE_TEXT}Local branch {branch_name} is ahead of the remote origin by {len(ahead_commits)} commits.{RESET_TEXT}\n"
```


## 8.0.0 - 2023-10-05
- fixed repo > Repo

### Diff:
```
diff --git a/fromGE/current/git-helper-15.py b/fromGE/current/git-helper-15.py
index b1a8d3d..5d8ee73 100644
--- a/fromGE/current/git-helper-15.py
+++ b/fromGE/current/git-helper-15.py
@@ -4 +4 @@ import git
-from git import repo
+from git import Repo
```


## 0.0.1 - 2023-10-02
initial version

### Diff:
```
diff --git a/grinntec-terraform-aws/terraform-aws-aws_instance b/grinntec-terraform-aws/terraform-aws-aws_instance
index a629b77..f03269e 160000
--- a/grinntec-terraform-aws/terraform-aws-aws_instance
+++ b/grinntec-terraform-aws/terraform-aws-aws_instance
@@ -1 +1 @@
-Subproject commit a629b777e9dbfc921e06e012dab7cfafeabd2ef5
+Subproject commit f03269e5ef31c4521c04003a884fddab79667675
diff --git a/grinntec-terraform-aws/terraform-aws-aws_internet_gateway b/grinntec-terraform-aws/terraform-aws-aws_internet_gateway
index b712c5b..6b1c3d1 160000
--- a/grinntec-terraform-aws/terraform-aws-aws_internet_gateway
+++ b/grinntec-terraform-aws/terraform-aws-aws_internet_gateway
@@ -1 +1 @@
-Subproject commit b712c5bd66fcd5852dce131354ccb66927576e68
+Subproject commit 6b1c3d1d5be0bef29bb759175ba2bd594c9d8e3a
diff --git a/grinntec-terraform-aws/terraform-aws-aws_route_table_association b/grinntec-terraform-aws/terraform-aws-aws_route_table_association
index db768e1..06cfdaf 160000
--- a/grinntec-terraform-aws/terraform-aws-aws_route_table_association
+++ b/grinntec-terraform-aws/terraform-aws-aws_route_table_association
@@ -1 +1 @@
-Subproject commit db768e1567639ada36758519961d04657c3fcbbc
+Subproject commit 06cfdaf4bb7b2cdfeadd23ca9141430a8c6e8c53
diff --git a/grinntec-terraform-aws/terraform-aws-aws_route_table_igw b/grinntec-terraform-aws/terraform-aws-aws_route_table_igw
index b64ce96..bee3520 160000
--- a/grinntec-terraform-aws/terraform-aws-aws_route_table_igw
+++ b/grinntec-terraform-aws/terraform-aws-aws_route_table_igw
@@ -1 +1 @@
-Subproject commit b64ce96ab445de7b9b4a0e82713e3c4d585c8a64
+Subproject commit bee352042415992113e529e328da9eba3ed86589
diff --git a/grinntec-terraform-aws/terraform-aws-aws_subnet b/grinntec-terraform-aws/terraform-aws-aws_subnet
index a1791be..2252ab6 160000
--- a/grinntec-terraform-aws/terraform-aws-aws_subnet
+++ b/grinntec-terraform-aws/terraform-aws-aws_subnet
@@ -1 +1 @@
-Subproject commit a1791be139c7c34e1c8793358255ff38b4d9cdb7
+Subproject commit 2252ab656e4104013f044174c5c967e8ba9c7587
diff --git a/grinntec-terraform-aws/terraform-aws-aws_vpc b/grinntec-terraform-aws/terraform-aws-aws_vpc
index de61809..8810aa8 160000
--- a/grinntec-terraform-aws/terraform-aws-aws_vpc
+++ b/grinntec-terraform-aws/terraform-aws-aws_vpc
@@ -1 +1 @@
-Subproject commit de61809b3f4c97173d93248c07746e032d91ecc1
+Subproject commit 8810aa8fb988970e9c5e0eaf37e9c7d1c7c2f4cb
diff --git a/grinntec-terraform-azure/terraform-azurem-linux_virtual_machine_scale_set b/grinntec-terraform-azure/terraform-azurem-linux_virtual_machine_scale_set
deleted file mode 160000
index 1eeb0c9..0000000
--- a/grinntec-terraform-azure/terraform-azurem-linux_virtual_machine_scale_set
+++ /dev/null
@@ -1 +0,0 @@
-Subproject commit 1eeb0c9adc5d7b38985a1747e3cd9fb52df62988
diff --git a/grinntec-terraform-azure/terraform-azurerm-container_registry b/grinntec-terraform-azure/terraform-azurerm-container_registry
index 42dfc0e..c5ba380 160000
--- a/grinntec-terraform-azure/terraform-azurerm-container_registry
+++ b/grinntec-terraform-azure/terraform-azurerm-container_registry
@@ -1 +1 @@
-Subproject commit 42dfc0e4b97e0c53ffa57c3827890fe4e269eb6f
+Subproject commit c5ba380af087fb2206bf89d9af4ab4a51f7ff709
diff --git a/grinntec-terraform-azure/terraform-azurerm-key_vault b/grinntec-terraform-azure/terraform-azurerm-key_vault
index 3bc23b9..250ef22 160000
--- a/grinntec-terraform-azure/terraform-azurerm-key_vault
+++ b/grinntec-terraform-azure/terraform-azurerm-key_vault
@@ -1 +1 @@
-Subproject commit 3bc23b922e41bf0451cdef87e1920e968dd65cbe
+Subproject commit 250ef228c821c54cded8dd7cff99bdb2a2dd4aed-dirty
diff --git a/grinntec-terraform-azure/terraform-azurerm-linux_virtual_machine b/grinntec-terraform-azure/terraform-azurerm-linux_virtual_machine
index 71defdd..62a3ea9 160000
--- a/grinntec-terraform-azure/terraform-azurerm-linux_virtual_machine
+++ b/grinntec-terraform-azure/terraform-azurerm-linux_virtual_machine
@@ -1 +1 @@
-Subproject commit 71defdda1e46dd2cbe7e74678a0ed0ec07291540
+Subproject commit 62a3ea9388c78c4307776992d67a7d55936a96af
diff --git a/grinntec-terraform-azure/terraform-azurerm-load_balancer_public b/grinntec-terraform-azure/terraform-azurerm-load_balancer_public
index 551c4ab..04338ea 160000
--- a/grinntec-terraform-azure/terraform-azurerm-load_balancer_public
+++ b/grinntec-terraform-azure/terraform-azurerm-load_balancer_public
@@ -1 +1 @@
-Subproject commit 551c4ab21a2c615e5402a0a66477504522d819ec
+Subproject commit 04338ea6456e3238e4e20f83a1adf47e0a5a1799
diff --git a/grinntec-terraform-azure/terraform-azurerm-network_security_group b/grinntec-terraform-azure/terraform-azurerm-network_security_group
index 179d3c3..cc8bc5b 160000
--- a/grinntec-terraform-azure/terraform-azurerm-network_security_group
+++ b/grinntec-terraform-azure/terraform-azurerm-network_security_group
@@ -1 +1 @@
-Subproject commit 179d3c32effaa3b22cf53de8925616bde2e16386
+Subproject commit cc8bc5b2ed10b7ea13d221046764fe020cee08f9
diff --git a/grinntec-terraform-azure/terraform-azurerm-resource_group b/grinntec-terraform-azure/terraform-azurerm-resource_group
index 1b10305..722b653 160000
--- a/grinntec-terraform-azure/terraform-azurerm-resource_group
+++ b/grinntec-terraform-azure/terraform-azurerm-resource_group
@@ -1 +1 @@
-Subproject commit 1b103052df36115c06090f0a442a94f89929fa54
+Subproject commit 722b6537eb9967099b9bbc9a2264770b3b5574dd
diff --git a/grinntec-terraform-azure/terraform-azurerm-storage_account b/grinntec-terraform-azure/terraform-azurerm-storage_account
index 5e1989d..40ac89a 160000
--- a/grinntec-terraform-azure/terraform-azurerm-storage_account
+++ b/grinntec-terraform-azure/terraform-azurerm-storage_account
@@ -1 +1 @@
-Subproject commit 5e1989d1f2b8d8db6a6af58451072b82d38ebd05
+Subproject commit 40ac89a4b52c7f750217532f3c8b0eb85979a799
diff --git a/grinntec-terraform-azure/terraform-azurerm-virtual_network b/grinntec-terraform-azure/terraform-azurerm-virtual_network
index 1fdc561..6e56f44 160000
--- a/grinntec-terraform-azure/terraform-azurerm-virtual_network
+++ b/grinntec-terraform-azure/terraform-azurerm-virtual_network
@@ -1 +1 @@
-Subproject commit 1fdc561ebdc8152a2e35e7f8c6edbddf18ef3572
+Subproject commit 6e56f443f6d49ad6fb902fb823082431a0a235f5
diff --git a/grinntec-terraform-azure/terraform-azurerm_subnet b/grinntec-terraform-azure/terraform-azurerm_subnet
deleted file mode 160000
index 27a6409..0000000
--- a/grinntec-terraform-azure/terraform-azurerm_subnet
+++ /dev/null
@@ -1 +0,0 @@
-Subproject commit 27a6409df30eadba00d7f50765580ed510bf5bae
diff --git a/grinntec/.github b/grinntec/.github
index 28ad47a..0774527 160000
--- a/grinntec/.github
+++ b/grinntec/.github
@@ -1 +1 @@
-Subproject commit 28ad47a2ee3f81ccf0b32914c92d6c7a0c3e5ba7
+Subproject commit 0774527059dc20fa3fc5596f4880b86e2a1f2576
diff --git a/grinntec/azure b/grinntec/azure
index ea6064a..0fd86f2 160000
--- a/grinntec/azure
+++ b/grinntec/azure
@@ -1 +1 @@
-Subproject commit ea6064acc7740c11ff8f1ef8f607c778f1d16602
+Subproject commit 0fd86f2981fce703363a3f79b86e0ea488dccf25
diff --git a/grinntec/azure-cloud-resume-challenge b/grinntec/azure-cloud-resume-challenge
deleted file mode 160000
index 7dd7263..0000000
--- a/grinntec/azure-cloud-resume-challenge
+++ /dev/null
@@ -1 +0,0 @@
-Subproject commit 7dd72634fe225893fc923f8d7a1f4daebacb9562
diff --git a/grinntec/azure-grinntec-sandbox b/grinntec/azure-grinntec-sandbox
deleted file mode 160000
index 077eb73..0000000
--- a/grinntec/azure-grinntec-sandbox
+++ /dev/null
@@ -1 +0,0 @@
-Subproject commit 077eb73141795778cfa1e0c94f51cdd4f60d4432
diff --git a/grinntec/build-grinntec-spoke01-eu b/grinntec/build-grinntec-spoke01-eu
deleted file mode 160000
index 93dd615..0000000
--- a/grinntec/build-grinntec-spoke01-eu
+++ /dev/null
@@ -1 +0,0 @@
-Subproject commit 93dd615c92a96a04466f29aa26c56649d0ac217b
diff --git a/grinntec/docker b/grinntec/docker
index f6a8608..e6f5723 160000
--- a/grinntec/docker
+++ b/grinntec/docker
@@ -1 +1 @@
-Subproject commit f6a86080343b5f8dc83e4a6763391715aadab28d
+Subproject commit e6f5723db2f8a406b96794a512ffda07601a6820
diff --git a/grinntec/github-actions b/grinntec/github-actions
index e9f6c3a..ef15763 160000
--- a/grinntec/github-actions
+++ b/grinntec/github-actions
@@ -1 +1 @@
-Subproject commit e9f6c3a7a6f379e0066a20ddf635febe3345e746
+Subproject commit ef157631f5bd4a43b8a345962818295615b1a427
diff --git a/grinntec/grinntec-sandbox b/grinntec/grinntec-sandbox
deleted file mode 160000
index 7193ae7..0000000
--- a/grinntec/grinntec-sandbox
+++ /dev/null
@@ -1 +0,0 @@
-Subproject commit 7193ae76a5e986497f6727d2e2d5b5e067871137
diff --git a/grinntec/project-aws-grinntec-sandbox b/grinntec/project-aws-grinntec-sandbox
index 61ce6a4..052da19 160000
--- a/grinntec/project-aws-grinntec-sandbox
+++ b/grinntec/project-aws-grinntec-sandbox
@@ -1 +1 @@
-Subproject commit 61ce6a4b69260a5e189ff6dada464f6d6ed78308
+Subproject commit 052da19e57afa097964e082d01b6e4bc822e04f2-dirty
diff --git a/grinntec/project-azure-grinntec-sandbox b/grinntec/project-azure-grinntec-sandbox
index b1531e0..427ca3a 160000
--- a/grinntec/project-azure-grinntec-sandbox
+++ b/grinntec/project-azure-grinntec-sandbox
@@ -1 +1 @@
-Subproject commit b1531e0c58c170d44a6ba8bd2606b41f92c05a36
+Subproject commit 427ca3ad01d46be902680189ef71abc9ac8daf19-dirty
diff --git a/grinntec/terraform b/grinntec/terraform
index 7491927..77dfa22 160000
--- a/grinntec/terraform
+++ b/grinntec/terraform
@@ -1 +1 @@
-Subproject commit 74919271710358f0af6ffc12252a36f961056ec6
+Subproject commit 77dfa22b66a0c7e96f8cc6d7adb8972c931c9d48
diff --git a/grinntec/terraform-bootstrap-azure b/grinntec/terraform-bootstrap-azure
deleted file mode 160000
index 97060c8..0000000
--- a/grinntec/terraform-bootstrap-azure
+++ /dev/null
@@ -1 +0,0 @@
-Subproject commit 97060c89a37ca3adb509b453f8a9919532006afc
diff --git a/grinntec/terraform-modules b/grinntec/terraform-modules
deleted file mode 160000
index f195a51..0000000
--- a/grinntec/terraform-modules
+++ /dev/null
@@ -1 +0,0 @@
-Subproject commit f195a517624ddfac9c78d2d37b9b72b48c120dda
diff --git a/neilgri/cloudresumechallenge b/neilgri/cloudresumechallenge
index c773816..b3417d3 160000
--- a/neilgri/cloudresumechallenge
+++ b/neilgri/cloudresumechallenge
@@ -1 +1 @@
-Subproject commit c7738163561b85cc6247e10973b0d0539f49e3d5
+Subproject commit b3417d3bac0d071135dd2a57f609fa5535393cd5-dirty
diff --git a/neilgri/stapp-grinntec-geekdocs b/neilgri/stapp-grinntec-geekdocs
index baa5a0e..e4150e7 160000
--- a/neilgri/stapp-grinntec-geekdocs
+++ b/neilgri/stapp-grinntec-geekdocs
@@ -1 +1 @@
-Subproject commit baa5a0e6c3cd70f743a32617d3ad99caba18d31d
+Subproject commit e4150e7de025bc053c2e80ef863b9f169c9f8cd7
```

## 0.0.1 - 2023-10-02
initial commit

### Diff:
```
diff --git a/README.md b/README.md
index 623bbf0..235d2e7 100644
--- a/README.md
+++ b/README.md
@@ -1 +1,44 @@
-# git-helper
\ No newline at end of file
+# Git Automation Tool

+

+This tool automates various Git operations such as pushing commits, committing changes, adding files, tagging versions, and more. It provides a user-friendly interface to perform these operations with ease.

+

+## Code Overview

+

+The code is structured into several functions, each performing a specific task related to Git operations. Here's a brief overview of the main functions:

+

+- `initialize_repository()`: Initializes the Git repository and sets the current working directory as the repository path.

+- `compare_with_origin(repo, branch_name)`: Compares the local branch with the remote branch and logs the differences.

+- `log_repository_info(repo, branch_name, latest_tag)`: Logs information about the repository, including the working directory, branch name, and the latest tag.

+- `log_status(comparison_result)`: Logs the status of the repository by comparing it with the origin.

+- `log_options()`: Logs the available options to the user.

+- `get_user_choice()`: Prompts the user to enter their choice and returns the input.

+- `push_commits(repo, branch_name)`: Pushes the unpushed commits to the origin.

+- `commit_changes(repo)`: Commits the uncommitted changes in the local repository.

+- `add_files(repo)`: Adds all untracked files in the local repository to the staging area.

+- `tag_version(repo, latest_tag)`: Tags a new version of the code in the local repository.

+- `main()`: The main function that executes the program and contains the main loop to continuously prompt the user for choices until the user chooses to exit.

+

+## Compiling the Python File into a Binary using PyInstaller

+

+To compile the Python file into a binary, you can use PyInstaller. PyInstaller bundles a Python application and all its dependencies into a single package. Follow the steps below to compile the Python file:

+

+Install PyInstaller:

+```sh

+pip install pyinstaller

+```

+

+Navigate to the directory containing your Python file and run the following command:

+

+```sh

+pyinstaller --onefile your_python_file.py

+```

+

+After running the command, PyInstaller will create a dist directory in the same folder as your Python file. Inside the dist directory, you will find the compiled binary file.

+

+You can now run the binary file without needing a Python interpreter or any dependencies.

+

+## Usage

+Run the compiled binary or the Python file directly, and follow the on-screen prompts to perform Git operations.

+

+## License

+This project is licensed under the MIT License - see the LICENSE.md file for details.
\ No newline at end of file
```

## 0.0.2 - 2023-10-03
change diff to only relevant files

### Diff:
```
diff --git a/git-helper.py b/git-helper.py
index 2ab4d65..d74cb1f 100644
--- a/git-helper.py
+++ b/git-helper.py
@@ -251 +251 @@ def tag_version(repo, latest_tag):
-    diff = repo.git.diff()

+    diff = repo.git.diff('--unified=0')

```
