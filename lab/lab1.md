# Lab 1 - Git/DVC and Data Preparation

## Question 1

After running `uv init`, the project was initialized successfully. It created `.python-version`, `pyproject.toml`, `README.md`, and the `src` folder.

- `.python-version` stores the Python version used by the project.
- `pyproject.toml` contains the project configuration and dependency information.
- `README.md` is used for project documentation.
- `src` is where the Python source code is placed.

## Question 2

After running `dvc init`, DVC created the `.dvc` folder and the `.dvcignore` file.

Inside `.dvc` I found:

- `cache/`: stores cached copies of data managed by DVC.
- `tmp/`: stores temporary DVC files.
- `.gitignore`: prevents Git from tracking DVC cache and temporary files.
- `config`: contains the project DVC configuration.
- `config.local`: contains local configuration that should stay only on my machine, such as local credentials and local remote settings.

The root `.dvcignore` file tells DVC which files or folders it should ignore.

The files that should be pushed to Git are the non-secret DVC configuration files such as `.dvc/config`, `.dvc/.gitignore`, and `.dvcignore`.

`config.local`, the cache folder, temporary files, and credentials should not be pushed to GitHub.

## Question 3

In my setup, the non-secret DVC remote configuration is stored in `.dvc/config`.

Local authentication and local configuration are stored in `.dvc/config.local` because I used the `--local` option.

Other configuration options include:

- `--global`: stores the configuration for the current user and can be used across repositories.
- `--local`: stores private configuration only for the current repository.
- Without these options, DVC stores repository-level configuration in `.dvc/config`.

Credentials should never be pushed to GitHub. Only non-secret configuration should be committed.

## Question 4

After running:

`dvc add data`

DVC added `/data` to the root `.gitignore`.

This means Git ignores the actual `data` folder and does not upload the large image datasets to GitHub.

Instead, Git tracks the small `data.dvc` pointer file, while DVC manages the actual data.

## Question 5

Yes. DVC created a file named `data.dvc`.

In my final setup, it contained information such as:

- An MD5 hash that identifies the exact version of the data.
- Dataset size.
- Number of files.
- Hash type: `md5`.
- Path: `data`.

Before creating the processed datasets, the tracked data contained 16,643 files and had a size of 1,188,442,712 bytes.

The `data.dvc` file acts as a pointer to the real dataset, while the actual dataset files are managed by DVC.

## Question 6

On GitHub, I can see the project code, configuration files, processing script, and the `data.dvc` pointer file.

The actual Food-11 image dataset is not stored directly in GitHub because the `data` folder is ignored by Git.

I first tried to use DagsHub as the DVC remote, but the upload produced authentication and network errors.

Because the lab allows using a local DVC remote when uploading the full dataset to DagsHub is difficult, I used a local remote instead.

The actual DVC data is stored outside the Git repository in:

`C:\Users\HPI\dvc-storage\mlops-lab1`

GitHub therefore stores the code and DVC pointer files, while the actual data versions are stored in the DVC remote.

## Question 7

I cloned the GitHub repository into a completely new temporary folder.

The Git clone contained the project files and the DVC pointer information, but the actual Food-11 dataset was not downloaded automatically.

The DVC command used to retrieve tracked data is:

`dvc pull`

In my first test, `dvc pull` could not retrieve the dataset because no default remote was configured in the cloned repository.

This shows that Git retrieves the code and DVC metadata, while DVC is responsible for retrieving the actual dataset from its configured remote.

## Question 8

I listed the commits that modified `data.dvc` using:

`git log --oneline -- data.dvc`

I found:

- `239a626` - Add processed Food-11 datasets and local DVC storage
- `cc57708` - Track data folder with DVC

I checked out the older commit:

`git checkout cc57708`

Then I ran:

`dvc checkout`

At this point, `food11_processed` and `food11_processed_mini` disappeared and only `food11_raw` remained.

After switching back to the main branch using:

`git checkout main`

and running:

`dvc checkout`

the folders `food11_processed` and `food11_processed_mini` were restored.

This demonstrates that Git and DVC can work together to switch between different versions of both the code and the data.

## DVC Storage Solution

Because pushing the full Food-11 dataset to DagsHub caused authentication and network problems, I used the local DVC remote option allowed by the lab.

The local DVC remote is stored outside the Git repository at:

`C:\Users\HPI\dvc-storage\mlops-lab1`

I configured it as the default DVC remote.

After running:

`dvc push`

DVC successfully pushed 32,034 files to the local remote.

GitHub stores the code and DVC pointer files, while the actual dataset versions are stored in the local DVC remote.

## Data Preparation

I created the script:

`src/food11/data.py`

The script processes the original Food-11 dataset and creates:

- `data/food11_processed`
- `data/food11_processed_mini`

The processed images are resized to `128x128` pixels and organized into folders according to their food categories.

For example:

`data/food11_processed/training/Bread/`

`data/food11_processed/training/Dairy product/`

`data/food11_processed/training/Dessert/`

The mini dataset has the same structure but contains at most 100 images per category.

The script successfully processed:

- Training: 9,866 images
- Evaluation: 3,347 images
- Validation: 3,430 images

