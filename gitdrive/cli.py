import argparse
import subprocess
import sys
import os

from typing import List, Optional as Opt, Union as U
from utils import linux_package_manager as get_linux_pm, print_exit
from config import GIT_CRYPT_REPO as GCURL,


def cmd_available(cmd: list) -> bool:
    """Check if a command is available"""
    try:
        subprocess.run(
            cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return True
    except FileNotFoundError:
        return False


def linux_package_manager() -> U[str, None]:
    """Detect the package manager based on the Linux distribution"""
    if os.path.exists('/etc/debian_version'):
        return 'apt-get'
    elif os.path.exists('/etc/redhat-release'):
        return 'yum'
    elif os.path.exists('/etc/arch-release'):
        return 'pacman'
    return None


def install_git_crypt():
    if cmd_available(['git-crypt', '--version']):
        print("git-crypt is already installed.")
        return

    sudo_cmd = ['sudo'] if cmd_available(['sudo', '--version']) else []

    if sys.platform.startswith('linux'):
        package_manager = linux_package_manager()
        if package_manager == 'apt-get':
            subprocess.run(sudo_cmd + ['apt-get', 'update'], check=True)
            subprocess.run(
                sudo_cmd + ['apt-get', 'install', '-y', 'git-crypt'],
                check=True,
            )
        elif package_manager == 'yum':
            subprocess.run(
                sudo_cmd + ['yum', 'install', '-y', 'git-crypt'], check=True
            )
        elif package_manager == 'pacman':
            subprocess.run(
                sudo_cmd + ['pacman', '-S', '--noconfirm', 'git-crypt'],
                check=True,
            )
        else:
            print_exit(
                "Unsupported Linux distribution. ",
                "Please install git-crypt manually.",
            )
    elif sys.platform.startswith('darwin'):
        subprocess.run(['brew', 'install', 'git-crypt'], check=True)
    elif sys.platform.startswith('win'):
        print_exit(f"Manual installation required, please see: {GCURL}")
    else:
        print_exit(
            f"Unsupported OS: {sys.platform}. Please see: {GCURL} for "
            "installation instructions."
        )
    print("git-crypt installed successfully.")


def init_repo(private):
    subprocess.run(['git', 'init'])
    if private:
        subprocess.run(
            ['git', 'config', '--local', 'core.sharedRepository', 'group']
        )


def main():
    parser = argparse.ArgumentParser(
        description='Manage encrypted GitHub storage.'
    )
    parser.add_argument(
        '--init',
        action='store_true',
        help='Initialize the GitDrive with optional encryption.',
    )
    parser.add_argument(
        '--private',
        action='store_true',
        help='Set repository visibility to private.',
    )
    args = parser.parse_args()

    if args.init:
        install_git_crypt()
        init_repo(args.private)


if __name__ == '__main__':
    main()
