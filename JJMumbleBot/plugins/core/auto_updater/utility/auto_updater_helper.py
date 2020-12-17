import sys
from subprocess import call

import pkg_resources
from requests import get

from JJMumbleBot.lib.resources.strings import L_DEPENDENCIES
from JJMumbleBot.lib.utils.print_utils import PrintMode
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.resources.strings import INFO, ERROR, DEP_PROCESS_ERR


def check_pypi_version(package_name):
    resp = get(f"https://pypi.org/pypi/{package_name}/json")
    if resp is not None:
        data = resp.json()
        log(
            INFO,
            f"Successfully retrieved PyPi metadata for {package_name}",
            origin=L_DEPENDENCIES,
            print_mode=PrintMode.VERBOSE_PRINT.value
        )
        return data['info']['version']
    return None


def update_package(package_name, pip_cmd):
    if call([sys.executable, '-m', pip_cmd, 'install', '--upgrade', package_name]) == 0:
        log(
            INFO,
            f"Successfully updated dependency package: {package_name}",
            origin=L_DEPENDENCIES,
            print_mode=PrintMode.VERBOSE_PRINT.value
        )
        return True
    return False


def update_available(package_name):
    packages = [dist.project_name for dist in pkg_resources.working_set]
    if package_name not in packages:
        log(
            ERROR,
            f"The package: [{package_name}] is not a dependency of this software.",
            origin=L_DEPENDENCIES,
            error_type=DEP_PROCESS_ERR,
            print_mode=PrintMode.VERBOSE_PRINT.value
        )
        return None
    vers = check_pypi_version(package_name)
    if vers is not None:
        log(
            INFO,
            [
                f"{package_name} version available: {vers}",
                f"{package_name} version current: {pkg_resources.get_distribution(package_name).version}"
            ],
            origin=L_DEPENDENCIES,
            print_mode=PrintMode.VERBOSE_PRINT.value
        )
        if vers != pkg_resources.get_distribution(package_name).version:
            log(
                INFO,
                f"There is a newer version of: [{package_name}({vers})] available.",
                origin=L_DEPENDENCIES,
                print_mode=PrintMode.VERBOSE_PRINT.value
            )
            return True
    return False


def check_and_update(package_name, pip_cmd):
    vers = check_pypi_version(package_name)
    if vers != pkg_resources.get_distribution(package_name).version:
        log(
            INFO,
            f"There is a newer version of: [{package_name}({vers})] available. Updating...",
            origin=L_DEPENDENCIES,
            print_mode=PrintMode.VERBOSE_PRINT.value
        )
        if update_package(package_name, pip_cmd):
            return vers
    return None
