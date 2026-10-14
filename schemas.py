from pydantic import BaseModel
from datetime import date

class RepositoryAnalysis(BaseModel):

    name: str
    full_name: str
    owner: str
    description: str | None
    language: str | None
    stars: int
    forks: int
    open_issues: int
    is_fork: bool
    html_url: str
    open_issue_ratio: float
    popularity_level: str
    created_at: date
    updated_at: date
    repo_age_days: int
    activity_status: str
    languages: dict[str, float]
    health_score: int