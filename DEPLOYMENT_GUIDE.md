# Deployment Guide

This guide covers how to deploy the Stock Analysis Application to Hugging Face Spaces, Vercel, and GitHub.

## 1. Hugging Face Spaces Deployment (Recommended for Full Features)

Hugging Face Spaces supports Docker, which is perfect for this app.

1.  Create a new Space on [Hugging Face](https://huggingface.co/spaces).
2.  Select **Docker** as the SDK.
3.  Choose a name (e.g., `stock-analysis`).
4.  In your local project, initialize Git if you haven't already:
    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    ```
5.  Add the Hugging Face remote (replace `USERNAME` and `SPACE_NAME`):
    ```bash
    git remote add hf https://huggingface.co/spaces/USERNAME/SPACE_NAME
    ```
6.  Push to Hugging Face:
    ```bash
    git push hf main
    ```
    *Note: If you have large files (like `stock_analysis.db`), you might need to use `git-lfs` or exclude them via `.gitignore`.*

## 2. GitHub Actions Automation & Keep Alive

We've included a GitHub Action that:
- Automatically syncs your code to Hugging Face when you push to GitHub.
- Pings your app every 12 hours to prevent it from sleeping (if on a free tier).

### Setup:
1.  Push your code to a GitHub repository.
2.  Go to **Settings** > **Secrets and variables** > **Actions**.
3.  Add the following Repository Secrets:
    - `HF_TOKEN`: Your Hugging Face Access Token (Write permissions).
    - `HF_USERNAME`: Your Hugging Face username.
    - `HF_SPACE_NAME`: The name of your Space.

The workflow file is located at `.github/workflows/deploy_and_keep_alive.yml`.

## 3. Vercel Deployment

Vercel is great for the frontend, but requires specific configuration for Python backends (serverless).

1.  Install Vercel CLI: `npm i -g vercel`
2.  Login: `vercel login`
3.  Deploy:
    ```bash
    vercel
    ```
4.  The `vercel.json` configuration file handles the routing to the Python backend.

## 4. Local "Keep Alive" Script

If you prefer to run a keep-alive script from your own machine:

1.  Edit `keep_alive.py` and set your URL.
2.  Run it:
    ```bash
    python keep_alive.py
    ```
    It will ping your server every 12 hours.

## Important Notes

- **Database**: The SQLite database (`stock_analysis.db`) is file-based. On Hugging Face Spaces (Docker), it will reset if the container restarts unless you set up persistent storage (Hugging Face "Persistent Storage" dataset or upgrade the space). For production, consider using an external database (PostgreSQL/Supabase).
- **Environment Variables**: Make sure to set any secrets (like database URLs or API keys) in the Settings tab of your deployment platform.
