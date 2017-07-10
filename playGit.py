import subprocess
from github import Github


# print('sys.argv[1] is', sys.argv[1]);

def main():
    g = Github("TrCaM", "01234722581Tri")
    SCS = g.get_organization("SCS-Carleton")
    count =0
    for repo in SCS.get_repos():
        if repo.name.startswith('a0-'):
            count+=1
            clone_repo(repo.name)
    print(count)

def clone_repo(name):
    try:
        print("Cloning ", name, "...")
        subprocess.run(["git", "clone", "https://github.com/SCS-Carleton/" + name + ".git"])
    except Exception as e:
        print(e.message)

if __name__ == '__main__':
    main()
