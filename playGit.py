# Written by: Tri Cao
# Note: This only works for Python3 please install Python3 and pip before use
#       To install PyGithub with pip: pip install PyGithub
# To not typing username and password multiple time consider cache your information:
#  git config --global credential.helper 'cache --timeout 7200'
import subprocess, getpass, argparse, os, os.path, json, errno
from github import Github


# print('sys.argv[1] is', sys.argv[1]);

def main():
    """ The main function of the script

    This function run as a starting point of the program
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", help ="authorize with github username")
    parser.add_argument("-t", "--token", help = "authorize with github token")
    parser.add_argument("-s", "--save", help = "save the provided information (token or username)",
                         action="store_true")
    parser.add_argument("-c", "--clone", help= "clone all repository in SCS-Carleton beginning with the pattern")
    args = parser.parse_args()
    try:
        with open("./data/data.json", "r") as f:
            data = json.load(f)
    except IOError as e:
        data = {'user': None, 'token' : None}

    if args.save and not (args.user or args. token):
        print("TAtool: no information to save")
        print("TAtool: try 'TAtool --help' for more information")
    elif args.user or args.token:
        if args.user:
            data['user'] = args.user
        if args.token:
            data['token'] = args.token
        if args.save:
            with safe_open_w("./data/data.json") as f:
                json.dump(data, f, ensure_ascii = False)
        if args.token == None:
            data['token'] = None
    if args.clone:
        # get the git with authorization
        if not data['token']:
            git = connect_to_git(login= data['user'])
        else:
            git = connect_to_git(data['token'])
        print("get here")
        SCS = git.get_organization("SCS-Carleton")
        count =0
        # Set up credential helper
        for repo in SCS.get_repos():
            if repo.name.startswith(args.clone):
                count+=1
                clone_repo(repo.name)
        print("There are total " + str(count) + " submissions cloned")

def connect_to_git(token=None, login=None):
    """ Get the github object that connect to the github account

    User should provide token or username to authorize:
    if username is provided then program will prompt to write the password

    Args:
        token: The token that can be used to access github
        login: the username if token is not provided
    """
    if token:
        return Github(token)
    else:
        password = getpass.getpass()
        return Github(login, password)

def clone_repo(repo_name, *org_or_user):
    """Clone a remote repository

    Initiate a subprocess that call git to be launched and clone the specified repo_name

    Args:
        repo_name: the name of the repository

        org_or_user: the name of the organization or user that the repo belongs to (Default: "SCS-Caleton")

    """
    try:
        print("Cloning ", repo_name, "...")
        if not org_or_user:
            subprocess.run(["git", "clone", "https://github.com/SCS-Carleton/" + repo_name + ".git", "./submissions/" + repo_name])
        else:
            subprocess.run(["git", "clone", "https://github.com/"+ "/".join(org_or_user) + "/" + repo_name + ".git", "./submissions/" + repo_name])

    except Exception as e:
        print(e.message)

# Taken from https://stackoverflow.com/a/600612/119527
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

# Taken from https://stackoverflow.com/questions/23793987/python-write-file-to-directory-doesnt-exist
def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    mkdir_p(os.path.dirname(path))
    return open(path, 'w')


if __name__ == '__main__':
    main()
