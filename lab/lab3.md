**Q1. Version number? Logged artifact vs registered model?**
My model got **version 1**.
A logged model artifact is just files saved inside one training run (found by run ID).
A registered model has a name (`food11`), version numbers, aliases and tags, and can be loaded by name instead of run ID.

**Q2. What replaced stages? Why version separately? Why are aliases better?**
**Aliases** (like `champion`) and **tags** replaced the old stages (`Staging`, `Production`).
Versioning the model separately keeps a clean history of only the models worth serving, not every experiment.
An alias can be moved to any version at any time without changing code, and I can choose any names (e.g. `champion`, `challenger`).

**Q3. Why `models:/food11@champion` instead of a `.pth` file? How to serve a newer version?**
The URI asks MLflow which version is `champion` and downloads the full model package (architecture + weights + metadata).
A `.pth` path only works on the machine where that file exists, and it would not exist inside a container.
To serve a newer model: register the new version, move the `champion` alias to it, and restart the API. No code change or rebuild. I did this: `champion` moved from version 1 to version 2.

**Q4. Why copy `pyproject.toml`/`uv.lock` and run `uv sync` before the code? What happens when `serve.py` changes?**
Docker caches layers. If a layer changes, it and all layers after it are rebuilt.
Dependencies change rarely, code changes often, so dependencies go first and code goes last.
- First build: **11,109 s** (`uv sync` alone: 9,600 s)
- After changing one line in `serve.py`: **2.0 s**. Everything was `CACHED` except `COPY src/`.

**Q5. Single-stage vs multi-stage size?**
| Image | Disk size |
|---|---|
| Naive single-stage (`python:3.12`) | 11.1 GB |
| Multi-stage (`python:3.12-slim`) | 9.58 GB |

Multi-stage is about **1.5 GB smaller**.
`docker history`: the biggest layer in both is the venv (**6.2 GB**, mostly PyTorch + CUDA).
The naive image also includes the full Python base image (~1.19 GB, with 695 MB and 202 MB layers of build tools) and `uv` (58.8 MB). The slim base is only ~134 MB.

**Q6. What if I forget `.dockerignore`? Which folder would break the build?**
With `.dockerignore` the build context was **2.30 kB**. Without it, Docker would send about **3.7 GB** (`data/` 1.2 GB, `.dvc/` 1.2 GB, `.venv/` 1.0 GB, `mlruns/` 257 MB…).
That makes every build slower, and with `COPY . .` the image would be much bigger.
**`.venv/`** would break the build: it is a Windows environment, and copying it would overwrite the Linux venv inside the container.

**Q7. Why not `127.0.0.1:5000` inside the container? What is `host.docker.internal`?**
Inside a container, `127.0.0.1` means **the container itself**, not my PC.
`host.docker.internal` is a special Docker Desktop name that points to **the host machine** (my Windows PC).
Extra fixes I needed:
- Start MLflow with `--host 0.0.0.0` and `--allowed-hosts` including `host.docker.internal`.
- The original model files were saved at a Windows path (`file:///C:/.../mlruns/1`), so the container failed with `No such artifact`. I re-logged the model through the server (`mlflow-artifacts:/`) as **version 2** and moved `champion` to it.

**Q8. New container from the same image: does the model still load?**
Yes. A new container from the same image (no rebuild) loaded the model and gave the same prediction (Bread → Fried food, 0.5244).
- **Baked into the image:** Python, dependencies, my code.
- **Fetched at runtime:** the model, downloaded from MLflow at every start.

So I can change the model by moving the alias, but the container needs the MLflow server to be running.

**Q9. What is missing for another machine to run this exact image?**
The code is in Git (commit `ba21f9f`), but the image is only on my PC. Missing:
1. **Push the image to a registry** (Docker Hub / GitHub Container Registry).
2. **An immutable tag** (e.g. Git commit `food11-api:ba21f9f` or a digest). `latest` changes: mine pointed to two different images.
3. **Automatic builds in CI** (e.g. GitHub Actions), with pinned base images.
4. **A reachable MLflow server and shared artifact storage.** `host.docker.internal` only works on my PC.