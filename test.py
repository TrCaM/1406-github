import subprocess, getpass, argparse, os, os.path, json, errno, re, time
from github import Github
from git import Repo

import ./GiTandMarK
# cloned_repo = Repo("./")
# print(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))
# print(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(cloned_repo.head.commit.committed_date)))
# print(time.mktime(time.localtime()))

# Result = subprocess.run(['curl', '-u', 'TrCaM', '-d', '{"scopes": ["repo", "user"], "note": "getting-started"}',
#                          'https://api.github.com/authorizations'], stdout=subprocess.PIPE, universal_newlines=True)
#
#
# print(json.loads(Result.stdout))
clone_repo("rrrtrt","./", "TrCaM")


@authorize_user
def send_feedback(orgs, data, args):
    ''' Send the graded rubik to students remote repo

    - TODO Create new "graded" branch
    - TODO Delete readme, change rubik into readme
    - 


    '''
