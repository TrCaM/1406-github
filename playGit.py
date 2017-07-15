# Written by: Tri Cao
# Note: This only works for Python3 please install Python3 and pip before use
#       To install PyGithub with pip: pip install PyGithub
# To not typing username and password multiple time consider cache your
# information:
#  git config --global credential.helper 'cache --timeout 7200'
#  to Create token: need to install curl
import subprocess
import getpass
import argparse
import os
import os.path
import json
import errno
import re
import time
from github import Github, GithubException
from tqdm import tqdm
from git import Repo


def main():
    """ The main function of the script

    This function run as a starting point of the program
    """
    parser = argparse.ArgumentParser(prog='playGit.py')
    parser.add_argument("-u", "--user", help="authorize with github username")
    parser.add_argument("-t", "--token", action="store_true",
                        help="authorize by creating OAuth token")
    parser.add_argument("-c", "--clone", metavar='prefix',  help="clone all \
                        repository in SCS-Carleton beginning with the pattern")
    parser.add_argument("-d", "--dir", metavar='directory',  help="the \
                        directory path to save the clone folder")
    parser.add_argument("-a", "--add", metavar='prefix and files ', nargs='*', help="Commit files to the remote repositories of all \
                        students")
    parser.add_argument("-dl", "--deadline", metavar="YYYY-MM-DD-H:M",
                        help="specify the deadline for current assignment")
    args = parser.parse_args()

    try:
        with open("./data/data.json", "r") as f:
            data = json.load(f)
        assert data
    except Exception as e:
        data = {'user': None, 'token': None, 'dir': None, 'deadline': None}

    if args.user:
        data['user'] = args.user
    if args.token:
        try:
            data['token'] = create_token(data['user'])
        except TokenCreateException as e:
            print("You already have a token, consider deleting it")
            return
        except ValidationException as e:
            print(e)
            return
    if args.deadline:
        try:
            data['deadline'] = time.mktime(time.strptime(args.deadline,
                                                         "%Y-%m-%d-%H-%M"))
        except ValueError as e:
            print(e)
    with safe_open_w("./data/data.json") as f:
        json.dump(data, f, ensure_ascii=False, sort_keys=True, indent=4 )

    if args.clone or args.add:
        print("Conecting with github...", end="", flush = True)
        # get the git with authorization
        if not data['token']:
            git = connect_to_git(login=data['user'])
        else:
            git = connect_to_git(data['token'])

        try:
            SCS = git.get_organization("SCS-Carleton")
        except GithubException:
            print("Error: Bad (expired) token or wrong username|password")
            return
        ''' Set up some counters
        '''
        count = 0  # Counter for cloned repositories
        late = 0  # Counter for late submissions
        invalid = 0
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
                json.dump(data, f, ensure_ascii=False)

            # Save the students information
            students = []
            # Save the inavalid folder (For late or not providing good information)
            invalid_submission = []
            names = []

            for repo in SCS.get_repos():
                if repo.name.startswith(args.clone):
                    names.append(repo.name)
            print("Done")
            print("Cloning ...")
            for name in tqdm(names):
                clone_repo(name, data['dir'])
                count += 1
                path = os.path.abspath(data['dir'] + "submissions/" + name)

                ''' Get the time stamp of the last commit
                '''
                # Time in epoc-unix (integer)
                cloned_repo = Repo(path)
                epoc_unix = cloned_repo.head.commit.committed_date
                submitted_time = time.localtime(epoc_unix)

                ''' Write student information by reading the submit-01 file
                '''
                try:
                    with open(path + '/submit-01', 'r') as f:
                        student = {'id': f.readline().strip(),
                                   'email': f.readline().strip(),
                                   'name': f.readline().strip(),
                                   'username': f.readline().strip(),
                                   'repo_path': path,
                                   'submit-time': time.strftime(
                            "%H:%M %d %b %Y",
                            submitted_time),
                        }
                    check_info(student)
                    if check_time(epoc_unix, data['deadline']):
                        student['status'] = "OK"
                    else:
                        student['status'] = "LATE"
                        late += 1
                except EnvironmentError:
                    error = "Invalid submission: " + name \
                            + "doesn't have submit-01"
                    invalid_submission.append(name)
                    invalid += 1
                except InvalidError as e:
                    invalid_submission.append(name)
                    invalid += 1
                else:
                    students.append(student)

            with safe_open_w("./data/students.json") as f:
                json.dump(students, f, ensure_ascii=False, indent=4)
            print("There are total ", count, " submissions cloned (", late,
                  " late submissions, ",   invalid, " invalid submissions)")

            if invalid_submission:
                print("There are ", len(invalid_submission),
                      " invalid submissions")
                with safe_open_w("./data/invalids") as f:
                    f.write("\n".join(invalid_submission))


def connect_to_git(token='35c547fc11e88ffbf1d9a2e50b7055a0688ee2d5', login=None):
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
        if not login:
            login = input("Enter your user name: ")
        password = getpass.getpass()
        return Github(login, password)


class TokenCreateException(Exception):
    pass


class ValidationException(Exception):
    pass


def create_token(login):
    """ Create the OAuth token for authorization
        "IMPORTANT": having curl installed
    """
    if not login:
        login = input("Please enter your username: ")
    completed_process = subprocess.run(['curl', '-u', login, '-d',
                                        '{"scopes": ["repo", "user"], "note": "getting-started"}',
                                        'https://api.github.com/authorizations'],
                                       stdout=subprocess.PIPE, universal_newlines=True)

    result = json.loads(completed_process.stdout)
    if 'token' in result:
        print(result['token'])
        return result['token']
    else:
        if result['errors']:
            raise TokenCreateException("You already have a token")
        else:
            raise ValidationException("Wrong username|password")


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
        if not org_or_user:
            cloned_repo = Repo.clone_from("https://github.com/SCS-Carleton/" + repo_name +
                                          ".git", dir_path + "submissions/" + repo_name)
        else:
            cloned_repo = Repo.clone_from("https://github.com/" + "/".join(org_or_user) +
                                          "/" + repo_name + ".git", dir_path + "submissions/"
                                          + repo_name)
    except Exception as e:
        pass
    return clone_repo

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
            count += 1
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


def check_time(current, deadline):
    ''' Check if the submit time of the assignment (last commit time) is before
        the deadline
    '''
    if not deadline:
        return True
    return current <= deadline


if __name__ == '__main__':
    main()
