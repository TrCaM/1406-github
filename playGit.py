# Written by: Tri Cao
# Note: This only works for Python3 please install Python3 and pip before use
#       To install PyGithub with pip: pip install PyGithub
# To not typing username and password multiple time consider cache your
# information:
#  git config --global credential.helper 'cache --timeout 7200'
import subprocess, getpass, argparse, os, os.path, json, errno, re
from github import Github
from git import Repo

# print('sys.argv[1] is', sys.argv[1]);

def main():
    """ The main function of the script

    This function run as a starting point of the program
    """
    parser = argparse.ArgumentParser(prog='playGit.py')
    parser.add_argument("-u", "--user", help ="authorize with github username")
    parser.add_argument("-t", "--token", help = "authorize with github token")
    parser.add_argument("-s", "--save", help = "save the provided information \
                        (token or username)",action="store_true")
    parser.add_argument("-c", "--clone", metavar= 'prefix',  help= "clone all \
                        repository in SCS-Carleton beginning with the pattern")
    parser.add_argument("-d", "--dir", metavar= 'directory',  help= "the \
                        directory path to save the clone folder")
    parser.add_argument("-a", "--add", metavar = 'prefix and files ', nargs= '*'
                        ,help = "Commit files to the remote repositories of all \
                        students")
    args = parser.parse_args()
    try:
        with open("./data/data.json", "r") as f:
            data = json.load(f)
    except IOError as e:
        data = {'user': None, 'token' : None, 'dir': None}

    if args.save and not (args.user or args. token or args.dir):
        print("TAtool: no information to save")
        print("TAtool: try 'TAtool --help' for more information")
    elif args.user or args.token or args.dir:
        if args.user:
            data['user'] = args.user
        if args.token:
            data['token'] = args.token
        if args.save:
            with safe_open_w("./data/data.json") as f:
                json.dump(data, f, ensure_ascii = False)
        if args.token == None:
            data['token'] = None



    if args.clone or args.add:
        # get the git with authorization
        if not data['token']:
            git = connect_to_git(login= data['user'])
        else:
            git = connect_to_git(data['token'])
        SCS = git.get_organization("SCS-Carleton")
        count =0
        if args.add:
            print(args.add[1:])
            for path in args.add[1:]:
                if not os.path.isfile:
                    raise Exception
            add_files(args.add[1:], args.add[0], SCS)
        else:
            if args.dir:
                if os.path.isdir(args.dir):
                    data['dir'] = os.path.abspath(args.dir)
                else:
                    raise Exception
            else:
                data['dir'] = './'
            with safe_open_w("./data/data.json") as f:
                json.dump(data, f, ensure_ascii = False)

            # Save the students information
            students = [];
            # Save the inavalid folder (For late or not providing good information)
            invalid_submission = [];
            for repo in SCS.get_repos():
                if repo.name.startswith(args.clone):
                    count+=1
                    clone_repo(repo.name, data['dir'])
                    path = data['dir'] +"submissions/" + repo.name
                    try:
                        with open(path + '/submit-01', 'r') as f:
                            student ={'id'       : f.readline().strip(),
                                      'email'    : f.readline().strip(),
                                      'name'     : f.readline().strip(),
                                      'username' : f.readline().strip(),
                                      'repo_path': os.path.abspath(path)
                                      }
                        check_info(student)
                    except EnvironmentError:
                        error = "Invalid submission: " + repo.name \
                                + "doesn't have submit-01"
                        print()
                        print(error)
                        invalid_submission.append(repo.name)
                    except InvalidError as e:
                        print()
                        print(repo.name+ ": ", e)
                        invalid_submission.append(repo.name)
                    else:
                        print("[GOOD]")
                        students.append(student)
            with safe_open_w("./data/students.json") as f:
                json.dump(students, f, ensure_ascii = False, indent= 4)
            print("There are total ", count," submissions cloned")
            if invalid_submission:
                print("There are ",len(invalid_submission), " invalid submissions:")
                for name_of_invalids in invalid_submission:
                    print(name_of_invalids)

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

def clone_repo(repo_name, dir_path, *org_or_user):
    """Clone a remote repository

    Initiate a subprocess that call git to be launched and clone the specified
    repo_name

    Args:
        repo_name: the name of the repository
        dir_path : the directories that user wants to clone into
        org_or_user: the name of the organization or user that the repo belongs
        to (Default: "SCS-Caleton")

    """
    try:
        print("Cloning ", repo_name, "...", end=""),
        if not org_or_user:
            Repo.clone_from("https://github.com/SCS-Carleton/" + repo_name +
                            ".git", dir_path +"submissions/" + repo_name)
        else:
            Repo.clone_from("https://github.com/"+ "/".join(org_or_user) +
                            "/" + repo_name + ".git", dir_path + "submissions/"
                            + repo_name)
    except Exception as e:
        print("Faile to clone: " + repo_name)

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

def add_files(file_list, prefix, SCS):
    count = 0
    commit_message = 'Added files: ' + ','.join(file_list)
    for repo in SCS.get_repos():
        if repo.name.startswith(prefix):
            count+=1
            gitpy_repo = Repo(repo.name)
            gitpy_repo.index.add(file_list)
            gitpy_repo.index.commit(commit_message)
            origin = gitpy_repo.remote('origin')
            origin.push()
    print("There are total " + str(count) + " commits  done")

class InvalidError(Exception):
    pass

def check_info(student):
    ''' Check the provided information in submit-01 file
    '''
    email_p = re.compile('\w+@cmail.carleton.ca')
    id_p = re.compile('\d{9}')
    name_p = re.compile('^(\w+\s)+\w+$')
    username_p = re.compile('\w+')
    error = []
    if not email_p.match(student['email']):
        error.append('email')
    if not id_p.match(student['id']):
        error.append('id')
    if not name_p.match(student['name']):
        error.append('name')
    if not username_p.match(student['username']):
        error.append('username')
    if error:
        message = "Invalid or lack information: " + ", ".join(error)
        raise InvalidError(message)

if __name__ == '__main__':
    main()
