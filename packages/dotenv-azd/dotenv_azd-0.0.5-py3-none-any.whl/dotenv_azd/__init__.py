import subprocess
from os import PathLike
from typing import Optional, TypeAlias

from dotenv import load_dotenv

StrOrBytesPath: TypeAlias = str | bytes | PathLike

def _azd_env_get_values(cwd: Optional[StrOrBytesPath] = None) -> str:
    result = subprocess.run(['azd', 'env', 'get-values'], capture_output=True, text=True, cwd=cwd, check=False)
    if result.returncode:
        raise Exception("Failed to get azd environment values because of: " + result.stdout.strip())
    return result.stdout

def load_azd_env(cwd: Optional[StrOrBytesPath] = None) -> None:
    from io import StringIO
    env_values = _azd_env_get_values(cwd)
    config = StringIO(env_values)
    load_dotenv(stream=config)
