import sys
import os
import subprocess
from tqdm import tqdm

def main():
    process_args = sys.argv[1:] if sys.argv[1] != "-s" else sys.argv[2:]
    # subprocess.run(process_args)
    errors = []
    for dir_name in tqdm(os.listdir()):
        if os.path.isdir(dir_name):
            try:
                cur_dir = os.path.abspath(r"./%s" % (dir_name))

                complete = subprocess.run(process_args, cwd=cur_dir,
                                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True,
                                          universal_newlines=True, encoding='utf-8')
                if complete.returncode == 1:
                    errors.append(dir_name)
                elif complete.returncode == 0 and sys.argv[1] == '-s':
                    with open('%s/submit-03' % cur_dir, 'a') as file:
                        file.write(complete.stdout)




            except subprocess.SubprocessError:
                errors.append(dir_name)
    print("ERRORS:")
    print("\n".join(errors))

if __name__ == "__main__":
    main()
