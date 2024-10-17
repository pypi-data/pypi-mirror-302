from dotenv import load_dotenv
import subprocess

def _azd_env_get_values(cwd=None):
    result = subprocess.run(['azd', 'env', 'get-values'], capture_output=True, text=True, cwd=cwd)
    if result.returncode:
        raise Exception("Failed to get azd environment values because of: " + result.stdout.strip())
    return result.stdout

def load_azd_env(cwd=None):
    from io import StringIO
    env_values = _azd_env_get_values(cwd)
    config = StringIO(env_values)
    load_dotenv(stream=config)
