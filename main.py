

from fastapi import FastAPI, HTTPException
from github_client import build_git_api
from schemas import RepositoryAnalysis


app = FastAPI() 

@app.get("/repos/{owner}/{repo}", response_model=RepositoryAnalysis)
async def get_repo(owner: str, repo: str):

    try:
        response = await build_git_api(owner, repo)

    except RuntimeError:
        raise HTTPException(status_code=502, detail="GitHub API Request Failed")
    if response is None:
        raise HTTPException(status_code=404, detail="Repo Not Found")


    return response