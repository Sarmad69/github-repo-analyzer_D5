# GitHub Repository Analyzer

## Project Overview
What the API does.

## Features
- GitHub repository metadata
- language percentages
- popularity level
- activity status
- repository age
- open issue ratio
- health score
- GitHub authentication through .env
- async HTTP requests

## Tech Stack
FastAPI
HTTPX
Pydantic
python-dotenv

## Endpoint
GET /repos/{owner}/{repo}

Example:
GET /repos/fastapi/fastapi

## Environment Variables
GITHUB_TOKEN=your_token_here

Never commit .env.

## Run Locally
uv sync
uv run uvicorn main:app --reload

## Error Handling
404 → repository not found
502 → GitHub API/network failure

## Project Structure
main.py
github_client.py
schemas.py
.env
.gitignore
README.md