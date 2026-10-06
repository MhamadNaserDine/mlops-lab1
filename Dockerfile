# =========================================================
# Stage 1: builder
# Full Python image + uv, used only to build the virtual env
# =========================================================
FROM python:3.12 AS builder

# Install uv
RUN pip install --no-cache-dir uv

WORKDIR /app

# Copy ONLY the dependency files first (better layer caching)
COPY pyproject.toml uv.lock ./

# Build the virtual environment (.venv) from the lock file
#   --frozen             : use uv.lock exactly, don't update it
#   --no-dev             : skip development dependencies
#   --no-install-project : install dependencies only, not our own package
RUN uv sync --frozen --no-dev --no-install-project


# =========================================================
# Stage 2: runtime
# Small slim image that only RUNS the app
# =========================================================
FROM python:3.12-slim AS runtime

WORKDIR /app

# Copy the ready-made virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Use the venv's Python and packages by default
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

# Copy the application source code (changes most often -> last)
COPY src/ ./src/

# The API listens on port 8000
EXPOSE 8000

# Start the FastAPI app with uvicorn
ENTRYPOINT ["uvicorn", "src.food11.serve:app", "--host", "0.0.0.0", "--port", "8000"]