import subprocess

def _azd_env_new(name, cwd):
    result = subprocess.run(['azd', 'env', 'new', name], capture_output=True, text=True, cwd=cwd)
    if result.returncode:
        raise Exception("Failed to create azd env because of: " + result.stderr)
    return result.stdout


def test_load_azd_env(tmp_path):
    from dotenv_azd import load_azd_env
    from os import getenv

    with open(tmp_path / "azure.yaml", "w") as config:
        config.write("name: dotenv-azd-test\n")

    _azd_env_new("test", tmp_path)
    load_azd_env(cwd=tmp_path)
    assert getenv('AZURE_ENV_NAME') is not None
