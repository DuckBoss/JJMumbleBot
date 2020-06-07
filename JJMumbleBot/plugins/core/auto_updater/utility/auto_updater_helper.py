from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.lib.resources.strings import L_DEPENDENCIES
from requests import get
from subprocess import call
import pkg_resources


def check_pypi_version(package_name):
    resp = get(f"https://pypi.org/pypi/{package_name}/json")
    if resp is not None:
        data = resp.json()
        return data['info']['version']
    return None


def update_package(package_name, pip_cmd):
    cmd = f'{pip_cmd}'
    param = f'install --upgrade {package_name}'
    if call([cmd, param]) == 0:
        return True
    return False


def update_available(package_name):
    packages = [dist.project_name for dist in pkg_resources.working_set]
    if package_name not in packages:
        dprint(f"The package: [{package_name}] is not a dependency of this software.", origin=L_DEPENDENCIES)
        return None
    vers = check_pypi_version(package_name)
    if vers is not None:
        dprint(f"{package_name} available: {vers}", origin=L_DEPENDENCIES)
        dprint(f"{package_name} current: {pkg_resources.get_distribution(package_name).version}", origin=L_DEPENDENCIES)
        if vers != pkg_resources.get_distribution(package_name).version:
            dprint(f"There is a newer version of: [{package_name}({vers})] available.", origin=L_DEPENDENCIES)
            return True
    return False


def check_and_update(package_name, pip_cmd):
    vers = check_pypi_version(package_name)
    if vers != pkg_resources.get_distribution(package_name).version:
        dprint(f"There is a newer version of: [{package_name}({vers})] available. Updating...", origin=L_DEPENDENCIES)
        if update_package(package_name, pip_cmd):
            return vers
    return None

