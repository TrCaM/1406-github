# import argparse
# parser = argparse.ArgumentParser()
# parser.parse_args()

from github import Github

git = Github('TrCaM', "01234722581Tri")
orgs = git.get_organization("SCS-Carleton")

for user in orgs.get_members():
    print(user.login)
