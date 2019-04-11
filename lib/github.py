from github import Github

# using username and password
g = Github("csmith2", "SweeneyApr2019!")

# Github Enterprise with custom hostname
g = Github(base_url="https://github.west.isilon.com")

org = "isilon" # get from url
pr_number = "546" # get from url

repo = g.get_repo("{}/onefs".format(org))
pr = repo.get_pull(int(pr_number))

num_commits = pr.get_commits().totalCount()
