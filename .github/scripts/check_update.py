from enums import PaperMCAPIProject

from utils import GitHubAPIUtils, PaperMCAPIUtils, VersionUtils


def main():
    all_papermc_api_paper_versions = PaperMCAPIUtils.get_all_versions(
        PaperMCAPIProject.PAPER
    )
    all_local_versions = VersionUtils.get_all_local_versions()
    open_gh_issues = GitHubAPIUtils.get_open_issues().unwrap_or([])
    open_gh_issue_titles = [issue["title"] for issue in open_gh_issues]

    for papermc_api_paper_version in all_papermc_api_paper_versions:
        if papermc_api_paper_version not in all_local_versions:
            issue_title = f"New PaperMC version {papermc_api_paper_version}"
            if not issue_title in open_gh_issue_titles:
                GitHubAPIUtils.create_issue(
                    title=issue_title,
                    body=f"Version {papermc_api_paper_version} is not supported by this repository yet. Please add support for this version.",
                    assignees=["Endkind"],
                    labels=["update"],
                )
                print(papermc_api_paper_version)


if __name__ == "__main__":
    main()
