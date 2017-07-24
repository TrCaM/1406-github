#writen by: Trung Dinh

from setuptools import setup

setup(name='gitclassroom',
      version='0.1',
      description="Package supports auto-marking student's assignment on GitHub",
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.x',
      ],
      url='https://github.com/TrCaM/1406-github',
      author='Tri Cao',
      author_email='cmthscb@gmail.com',
      license='MIT',
      packages=['gclr'],
      install_requires=[
        'subprocess',
        'getpass',
        'argparse',
        'os',
        'json', 
        'errno',
        'time',
        're',
        'functools', 
        'github', 
        'tqdm', 
        'git',
        'shutil',
        'markdown'
      ],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      include_package_data=True,
      zip_safe=False)
