import httpx
import os
from datetime import datetime, date
from dotenv import load_dotenv

load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")

headers = {
    "Accept": "application/vnd.github+json"
}

if github_token is not None:
    headers["Authorization"] = f"Bearer {github_token}"

async def build_git_api(owner: str, repo: str):

    url_repo = f"https://api.github.com/repos/{owner}/{repo}"
    url_repo_lang = f"https://api.github.com/repos/{owner}/{repo}/languages"

    try:
        async with httpx.AsyncClient(
            timeout=10.0, 
            follow_redirects=True
        ) as client:
   
            repo_data = await client.get(url_repo, headers=headers)
            repo_lang = await client.get(url_repo_lang, headers=headers)

    except httpx.RequestError:
        raise RuntimeError("GitHub API Request Failed")


    if repo_data.status_code == 404 or repo_lang.status_code == 404:
        return None

    if repo_data.status_code != 200 or repo_lang.status_code != 200:
        raise RuntimeError("GitHub API Request Failed")

    #print(repo_lang.json())

    response = repo_data.json()
    lang_response = repo_lang.json()

    return analyze_repo(response, lang_response)

def analyze_repo(response: dict, lang_response: dict):

    stars = response["stargazers_count"]
    health_score = 0

    if response["archived"] is False:
        health_score += 10

    if stars == 0:
        open_issue_ratio = 0.00
        health_score += 1
    else:
        open_issue_ratio = round(response["open_issues_count"] / stars, 4)
        if open_issue_ratio < 0.01:
            health_score += 20
        elif open_issue_ratio < 0.05:
            health_score += 15
        elif open_issue_ratio < 0.10:
            health_score += 10
        else:
            health_score += 5

    if stars < 100:
        popularity_level = "Low"
        health_score += 5
    elif stars < 1000:
        popularity_level = "Moderate"
        health_score += 10
    elif stars < 10000:
        popularity_level = "Popular"
        health_score += 20
    else:
        popularity_level = "Very Popular"
        health_score += 30

    created_at = response["created_at"].replace("Z", "+00:00")
    created_datetime = datetime.fromisoformat(created_at).date()

    updated_at = response["updated_at"].replace("Z", "+00:00")
    updated_datetime = datetime.fromisoformat(updated_at).date()

    today = date.today()

    repo_age = today - created_datetime
    repo_age_days = repo_age.days

    days_since_update = (today - updated_datetime).days

    if days_since_update <= 30:
        activity_status = "Active"
        health_score += 40
    elif days_since_update <= 180:
        activity_status = "Moderately Active"
        health_score += 25
    else:
        activity_status = "Inactive"
        health_score += 5
    
    total_bytes = 0
    languages = {}

    for lang in lang_response.values():
        total_bytes += lang
        
    if total_bytes > 0:
        for lang_name, lang_bytes in lang_response.items():
            languages[lang_name] = round((lang_bytes / total_bytes) * 100, 2)
    
    data = {
        "name": response["name"],
        "full_name": response["full_name"],
        "owner": response["owner"]["login"],
        "description": response["description"],
        "language": response["language"],
        "stars": response["stargazers_count"],
        "forks": response["forks_count"],
        "open_issues": response["open_issues_count"],
        "is_fork": response["fork"],
        "html_url": response["html_url"],
        "open_issue_ratio": open_issue_ratio,
        "popularity_level": popularity_level,
        "created_at": created_datetime,
        "updated_at": updated_datetime,
        "repo_age_days": repo_age_days,
        "activity_status": activity_status,
        "languages": languages,
        "health_score": health_score
    }

    return data