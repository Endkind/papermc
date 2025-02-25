import os

class GithubConfig:
    TOKEN = os.getenv('GITHUB_TOKEN', 'github_')
    REPO = os.getenv('REPO')
    
    if REPO:
        REPO_OWNER, REPO_NAME = REPO.split('/', 1)
    else:
        REPO_OWNER = os.getenv('REPO_OWNER', 'Endkind')
        REPO_NAME = os.getenv('REPO_NAME', 'papermc')

    REPO_OWNER = REPO_OWNER
    REPO_NAME = REPO_NAME
