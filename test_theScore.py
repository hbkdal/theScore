"""Simple tests to for theScore app"""
import json
import os
import random
from json import JSONDecodeError
from pathlib import Path
from framework.Android_app import Mobile_app
import pytest

from framework.leauge import verify_league
from framework.player import verify_player
from framework.team import verify_team

mobile_app: Mobile_app


def pytest_generate_tests(metafunc):
    """ This allows us to load tests from external files by
    parametrizing tests with each test case found in a data_X
    file """
    for fixture in metafunc.fixturenames:
        if fixture.startswith('players') or fixture.startswith('teams') or fixture.startswith('leagues'):
            # Load associated test data, may want to generate the lists....
            tests = load_tests(fixture)
            metafunc.parametrize(fixture, tests)


def load_tests(name):
    """load the data from files"""
    # Load test data
    dataset = getlist(name)
    # shuffle to get random order
    random.shuffle(dataset)
    # we can also sort alphabetically, or reverse alphabetically
    # dataset.sort(key=str.lower, reverse=True)
    tests_module = dataset
    # Tests are to be found in the variable `tests` of the module
    for test in tests_module:
        yield test


def getlist(name):
    # get the [path to the data files
    current_directory = Path().absolute()
    json_name = name + ".json"
    filename = current_directory / 'data' / json_name
    names = []
    if os.path.isfile(filename):
        try:
            names = load_json(filename)
        except JSONDecodeError:
            print('Error loading datafile')
    return names


def load_json(filename: str):
    """Load the book list from the specified json file"""
    exists = os.path.isfile(filename)
    if exists:
        not_zero_size = os.stat(filename).st_size > 0
        if not_zero_size:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
    data = []
    return data


@pytest.fixture(scope="session")
def appium_driver(request):
    global mobile_app
    mobile_app = Mobile_app()
    driver = mobile_app.initialize_appium_driver()

    def fin():
        driver.quit()

    request.addfinalizer(fin)
    return driver


def test_League(leagues, appium_driver):
    """Test the leagues"""
    result = verify_league(leagues, appium_driver)
    if result == "FAIL":
        pytest.fail(msg=result.Error)


def test_Team(teams, appium_driver):
    """Test the teams"""
    result = verify_team(teams, appium_driver)
    if result == "FAIL":
        pytest.fail(msg=result.Error)


def test_Player(players, appium_driver):
    """Test the players"""
    result = verify_player(players, appium_driver)
    if result == "FAIL":
        pytest.fail(msg=result.Error)
