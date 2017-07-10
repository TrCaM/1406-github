# import argparse
# parser = argparse.ArgumentParser()
# parser.parse_args()

from github import Github

git = Github('14bd0e85d248f8a39defa2c926a2e9ea684b4e0')
repo = git.get_repo('1406-github')

print(repo.name)
