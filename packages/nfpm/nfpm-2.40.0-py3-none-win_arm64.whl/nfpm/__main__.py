import os
import platform
import subprocess
import sys
from pathlib import Path

_IS_WINDOWS = platform.system() == "Windows"

def _main():
    binary_path = Path(__file__).parent / "nfpm"
    if _IS_WINDOWS:
        binary_path = binary_path.with_suffix(".exe")

    argv = (binary_path, *sys.argv[1:])
    try:
        if not _IS_WINDOWS:
            os.execv(argv[0], argv)
        else:
            sys.exit(subprocess.call(argv))
    except FileNotFoundError as error:
        raise FileNotFoundError(f"{binary_path} not found.") from error

if __name__ == '__main__':
    _main()
