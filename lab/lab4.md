\# Lab 4 – Orchestrating the app with Docker Compose



\## What I did

1\. Containerized MLflow (`mlflow/Dockerfile`) with its data in `/mlflow-data`.

2\. Created a Streamlit frontend (`frontend/app.py`, `frontend/Dockerfile`).

3\. Wired `mlflow`, `inference` (Lab 3 image) and `frontend` together in `docker-compose.yml`, with a named volume `mlflow-data`.

4\. The new MLflow started empty, so I exported my champion model from my PC's MLflow (`export\_champion.py`) and registered it in the container (`register\_in\_compose.py`).

5\. Tested: frontend → inference → MLflow model gave \*\*Soup (99.5%)\*\* for `9\_0.jpg`.



Note: the lab says "Staging", but stages are deprecated. I used the alias \*\*`champion`\*\* (`models:/food11@champion`).



\### Changes to the lab's `mlflow/Dockerfile`

| Change | Why |

|---|---|

| `mlflow==3.16.1` | Same version as the inference client |

| `RUN mkdir -p /mlflow-data` | So SQLite works even without a volume (Q1 test) |

| `--artifacts-destination` instead of `--default-artifact-root` | Model files go through the server (`mlflow-artifacts:/`), so other containers can download them (Lab 3 lesson) |

| `--allowed-hosts` with `mlflow:5000` | MLflow's security check would otherwise reject requests from the inference container |



\## Main commands

```powershell

docker build -t food11-mlflow ./mlflow

docker compose up --build

uv run python register\_in\_compose.py

docker compose restart inference

docker compose ps

docker compose logs inference

docker compose down        # keeps the volume

docker compose down -v     # deletes the volume

```



\---



\## Answers



\*\*Q1. What happens to `/mlflow-data` without a volume?\*\*

It is lost when the container is removed. I created experiment `q1-test`, ran `docker stop` + `docker rm`, and started a new container from the same image. `q1-test` was gone; only a new `Default` experiment existed.



\*\*Q2. Named volume vs bind mount?\*\*

A named volume is managed by Docker and doesn't depend on a host path, so it works the same on any machine. It's faster and safer for SQLite on Windows, and keeps the database out of Git.

A bind mount would also work for local dev (easy to see files), but it ties the setup to my folder, is slower on Windows, can cause SQLite/permission issues, and must be git-ignored.



\*\*Q3. Why does `http://mlflow:5000` resolve now?\*\*

Compose puts all services on one private network with an \*\*embedded DNS\*\* that maps service names to containers. In Lab 3 the API ran alone and MLflow was on my PC, so I needed `host.docker.internal`.

Evidence: inference reached `http://mlflow:5000` and got `RESOURCE\_DOES\_NOT\_EXIST` (the server answered).



\*\*Q4. Why read `INFERENCE\_URL` from an environment variable?\*\*

The name `inference` only exists inside the Compose network. If hardcoded, the frontend image would fail when run alone. With an environment variable, the same image works everywhere; only the configuration changes.



\*\*Q5. Why doesn't `inference` publish a port?\*\*

Only services humans open in the browser are published (MLflow 5000, frontend 8501). The frontend reaches inference \*\*inside the network\*\* at `http://inference:8000`. Not publishing it is also safer.



\*\*Q6. What if MLflow isn't ready (or has no model) when inference starts?\*\*

`serve.py` loads the model at startup. If that fails, the container \*\*exits with code 1\*\* and is not restarted.

My first `up`: `RESOURCE\_DOES\_NOT\_EXIST: Registered Model with name=food11 not found` → `inference-1 exited with code 1` (the new volume was empty). If MLflow had been slower, it would be \*connection refused\*. `depends\_on` only waits for the container to start, not for readiness.

Fixes: `restart: on-failure`, a retry loop, or a healthcheck + `depends\_on: condition: service\_healthy`.



\*\*Q7. `docker compose ps`: which services publish ports?\*\*

| Service | PORTS |

|---|---|

| mlflow | `0.0.0.0:5000->5000/tcp` |

| frontend | `0.0.0.0:8501->8501/tcp` |

| inference | `8000/tcp` (internal only) |



This matches the compose file: only `mlflow` and `frontend` have `ports:`.



\*\*Q8. After promoting a new version, which model answers?\*\*

The \*\*old\*\* one. The model is loaded once at startup. After moving `champion` to version 2, a new prediction caused \*\*no request\*\* to MLflow (its log was empty).

The command `docker compose restart inference` fixed it: MLflow's log then showed the inference container asking for `alias=champion`, then `version=2`, and downloading `model.pth`.



\*\*Q9. Why does `restart` work without a rebuild?\*\*

The image only contains Python, dependencies and code. The \*\*model is downloaded from MLflow at every startup\*\*, using the current `champion` alias. So code lives in the image (Git), and the model lives in the registry (MLflow).



\*\*Q10. `down`/`up` vs `down -v`/`up`?\*\*

\- `down` + `up`: containers were recreated, but `food11` (version 2, `@champion`) was \*\*still there\*\*, because the volume was kept.

\- `down -v` + `up`: output showed `Volume mlops-lab1\_mlflow-data Removed`, then `Created`. The registry was \*\*empty\*\*, and inference crashed with `RESOURCE\_DOES\_NOT\_EXIST`. I restored it with `register\_in\_compose.py` + `restart inference`.



`-v` deletes the named volume, the only place the data lives.



\*\*Q11. What can't Compose give us?\*\*

Compose runs on \*\*one machine\*\*. For 3 inference replicas behind a load balancer and for surviving a machine failure we need:

1\. An \*\*orchestrator\*\* (Kubernetes / Swarm) to run replicas on several machines and restart or move them.

2\. A \*\*load balancer with health checks\*\* (Kubernetes Service/Ingress, readiness probes).

3\. \*\*Rolling updates\*\* and autoscaling.

4\. For MLflow: a replicated \*\*database\*\* (PostgreSQL) instead of SQLite, and \*\*object storage\*\* (S3/MinIO) for artifacts instead of a local volume.

5\. A \*\*container registry\*\* for the images, and managed secrets/config.

