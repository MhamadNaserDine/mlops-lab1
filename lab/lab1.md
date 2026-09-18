\# Lab 1 - Git/DVC and Data Preparation



\## Question 1



After running `uv init`, the project was initialized successfully. It created `.python-version`, `pyproject.toml`, `README.md`, and the `src` folder.



\- `.python-version` stores the Python version used by the project.

\- `pyproject.toml` contains the project configuration and dependency information.

\- `README.md` is used for project documentation.

\- `src` is where the Python source code will be placed.



\## Question 2



After running `dvc init`, DVC created the `.dvc` folder and the `.dvcignore` file.



Inside `.dvc` I found:

\- `cache/`: stores cached copies of data managed by DVC.

\- `tmp/`: stores temporary DVC files.

\- `.gitignore`: prevents Git from tracking DVC cache and temporary files.

\- `config`: contains the project DVC configuration, such as the configured remote.

\- `config.local`: contains local configuration that should stay only on my machine, for example local credentials.



The root `.dvcignore` file tells DVC which files or folders it should ignore.



The files that should be pushed to Git are the non-secret DVC configuration files such as `.dvc/config`, `.dvc/.gitignore`, and `.dvcignore`.



`config.local`, the cache folder, and temporary files should not be pushed to Git.









\## Question 3



In my setup, the DVC remote URL is stored in `.dvc/config`.



The authentication information is stored in `.dvc/config.local` because I configured the credentials using the `--local` option.



Other options include:

\- `--global`: stores the configuration for the current user and makes it available across repositories.

\- `--local`: stores repository-specific private configuration in `.dvc/config.local`.

\- Without these options, DVC stores the repository configuration in `.dvc/config`.



Credentials should never be pushed to GitHub. The `.dvc/config.local` file should remain local because it may contain sensitive authentication information. Only the non-secret `.dvc/config` should be committed.





\## Question 4



After running DVC on the dataset, DVC added `/food11 dataset` to `data/.gitignore`.



This means Git will ignore the real Food-11 dataset folder and will not upload all of the image files to GitHub. Instead, Git tracks the small `.dvc` metadata file, while DVC manages the actual dataset.





\## Question 5



Yes, I have a `.dvc` file named `data/food11 dataset.dvc`.



It contains metadata about the tracked dataset, including:



\- MD5 hash: identifies the exact dataset version.

\- Size: `1188442712` bytes.

\- Number of files: `16643`.

\- Hash type: `md5`.

\- Path: `food11 dataset`.



This `.dvc` file acts as a pointer to the real dataset, while the actual dataset files are managed by DVC instead of Git.









\## Question 6



On GitHub, I can see the project code and the DVC pointer file, but I do not see the actual Food-11 image dataset.



The file `data/food11 dataset.dvc` points to the tracked dataset version.



The actual dataset is supposed to be stored in the DVC remote on DagsHub after running `dvc push`.



In my current run, the DagsHub upload did not complete successfully because of authentication errors, so the full dataset is not yet available there.









\## Question 7



After cloning the GitHub repository into a new temporary folder, I could see the `data` folder, but the actual Food-11 dataset was not there.



Inside `data`, I only found:

\- `.gitignore`

\- `food11 dataset.dvc`



This shows that GitHub contains the DVC pointer file, not the real dataset.



The command needed to retrieve the dataset is:



`dvc pull`



In my test, `dvc pull` did not download the dataset because no default DVC remote was configured in the cloned repository.









## DVC Storage Solution

Because pushing the full Food-11 dataset to DagsHub caused authentication and network problems, I used the local DVC remote option allowed by the lab.

The local DVC remote is outside the Git repository at:

`C:\Users\HPI\dvc-storage\mlops-lab1`

After running `dvc push`, the data was successfully pushed to the local DVC remote.

GitHub stores the code and DVC pointer files, while the actual dataset versions are stored in the local DVC remote.


