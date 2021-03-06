# Advanced Data Structures & Algorithms

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/charlyalizadeh/ESILV_ADSA_Problem/blob/master/LICENSE)
![GitHub contributors](https://img.shields.io/github/contributors/Naereen/StrapDown.js.svg)

## Prerequisites

 * Python 3.8+

## Installation

### Linux/MacOS

Clone this repos
```bash
$ git clone https://github.com/charlyalizadeh/ESILV_ADSA_Problem  
$ cd ESILV_ADSA_Problem/
$ python3 -m venv .venv
$ source .venv/bin/activate # Use the activate script corresponding to your shell
$ pip install -r linux.txt
$ python3 start.py
```

### Windows

To clone a Github repository from windows you can use [Git for Windows](https://gitforwindows.org/)

```bash
$ git clone https://github.com/charlyalizadeh/ESILV_ADSA_Problem  
$ cd ESILV_ADSA_Problem/
$ python3 -m venv .venv
$ .venv/Scripts/activate.bat
$ pip install -r windows.txt
$ python3 start.py
```

## Troubleshooting

When I tested this project on Windows I had some problem importing the matplotlib module. 
Downloading [Visual Studio Community](https://visualstudio.microsoft.com/fr/vs/community/) solved the problem (a little bit overkill I admit). 
[Link to the Stack Overflow discussion about this issue.](https://stackoverflow.com/questions/24251102/from-matplotlib-import-ft2font-importerror-dll-load-failed-the-specified-pro)

## TODO

* [ ] Document the code
* [X] Add `requirements.txt`
* [ ] Restructure the ADSAApp class into multiple smaller classes
* [X] Propose to choose the start and the end for the Hamilton path
* [ ] Add some bonus features
* [ ] Change some bad variable name
