# Use official Python runtime as base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv sync
# --frozen: Use exact versions from uv.lock
# --no-dev: Don't install dev dependencies
RUN uv sync --frozen --no-dev

# Copy application files from streamlit-app
COPY streamlit-app/app.py .
COPY streamlit-app/sharepoint_client.py .
# COPY streamlit-app/local_client.py .
COPY streamlit-app/.streamlit .streamlit

# Expose port 8501 (Streamlit default)
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run Streamlit using uv's managed environment
ENTRYPOINT ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
