import pytest
from click.testing import CliRunner
from csrgen import cli
import os

curfilePath = os.path.abspath(__file__)

# this will return current directory in which python file resides.
curDir = os.path.abspath(os.path.join(curfilePath, os.pardir))

# this will return parent directory.
parentDir = os.path.abspath(os.path.join(curDir, os.pardir))

@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner):
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert not result.exception
    assert result.output.strip() == 'Please provide a domain or seek --help. Exiting'


def test_cli_with_option(runner):
    try:
        os.remove('./csrgen-template.yaml')
    except:
        pass
    result = runner.invoke(cli.main, ['--generate-template'])
    assert not result.exception
    assert result.exit_code == 0
    assert result.output.strip() == 'Tempalte written to ./csrgen-template.yaml. Exiting'
    assert os.path.exists('./csrgen-template.yaml')

def test_cli_with_args(runner):
    result = runner.invoke(cli.main, [
        'bacon.lol', 
        '-c US', 
        '-s AZ', 
        '-l Tucson',
        '-o "Hayden"', 
        '-u "Bacon"', 
        '-e "noreply@bacon.lol"',
        '--key-file',
        parentDir+'/test.key',
        '--csr-file',
        parentDir+'/test.csr'
    ])
    assert result.exit_code == -1
    try:
        os.remove(parentDir+'/test.key')
        os.remove(parentDir+'/test.csr')
    except:
        pass

def test_cli_with_test_file(runner):
    result = runner.invoke(cli.main, ['--generate-template'])
    result = runner.invoke(cli.main, [
        'bacon.lol',
        '--from-template',
        '/csrgen-template.yaml'
    ])
    assert result.exit_code == 0
    try:
        os.remove('./bacon.lol*.*')
        os.remove('./csrgen-template.yaml')
    except:
        pass
    
