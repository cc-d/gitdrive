import sys
import os.path as op
from typing import List, Optional as Opt, Union as U


def linux_package_manager() -> U[str, None]:
    """Detect the package manager based on the Linux distribution"""
    if op.exists('/etc/debian_version'):
        return 'apt-get'
    elif op.exists('/etc/redhat-release'):
        return 'yum'
    elif op.exists('/etc/arch-release'):
        return 'pacman'
    return None


def print_exit(*args, code: int = 1, **kwargs) -> None:
    """Print and exit"""
    print(*args, **kwargs)
    sys.exit(code)
