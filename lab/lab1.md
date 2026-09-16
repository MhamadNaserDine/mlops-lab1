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

