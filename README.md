# GitHub - hbkdal/theScore: 

This is a simple solution to theScore qa challenge.

It finds leagues, teams and players based on data files and verifies they load

I have used python and appium as I am more familiar with that than the java stack



## Prerequisite

Clone the repository

Connect an android device

### dependencies

Appium @ 2.5.1

Appium driver uiautomator2 @ 2.45.1

python @ 3.11 

Android studio with cmd line tools

theScore android app @ 24.5.0

### Python modules
Appium-Python-Client @ 4.0 

pytest @ 8.1.1

selenium @ 4.19.0

## Installation



python: follow instructions on https://www.python.org/downloads/

Android studio: follow instructions from https://developer.android.com/studio/ be sure to install 
the cmd line tools and get adb in your path

npm i --location=global appium

appium driver install uiautomator2

for the python requirements Run: pip install -r requirements.txt

## Running

start appium in a terminal window 

from cmd line: pytest --no-header -v


## results

* pytest --no-header -v
* ======================================================================== test session starts ========================================================================
* collected 9 items                                                                                                                                                    
* 
* test_theScore.py::test_League[NHL] PASSED                                                                                                                      [ 11%]
* test_theScore.py::test_League[NBA] PASSED                                                                                                                      [ 22%]
* test_theScore.py::test_League[NFL] PASSED                                                                                                                      [ 33%]
* test_theScore.py::test_Team[Seattle Seahawks] PASSED                                                                                                           [ 44%]
* test_theScore.py::test_Team[Seattle Kraken] PASSED                                                                                                             [ 55%]
* test_theScore.py::test_Player[Geno Smith] PASSED                                                                                                               [ 66%]
* test_theScore.py::test_Player[Henrik Lundqvist] PASSED                                                                                                         [ 77%]
* test_theScore.py::test_Player[Philipp Grubauer] PASSED                                                                                                         [ 88%]
* test_theScore.py::test_Player[Connor McDavid] PASSED                                                                                                           [100%]

## adding leagues, teams, players

The data folder has 3 json files, edit them to add tests