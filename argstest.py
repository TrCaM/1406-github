# import argparse
# parser = argparse.ArgumentParser()
# parser.parse_args()

from github import Github

git = Github('1944d85c58233a0a8822ac8c1c82898b5b777b42')
repos = git.get_organization("SCS-Carleton")

for user in repos.get_repos():
    print(user.name)
