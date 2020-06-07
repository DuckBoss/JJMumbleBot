from JJMumbleBot.lib.utils.print_utils import rprint, dprint


def check_pypi_version(package_name):
    import requests
    resp = requests.get(f"https://pypi.org/pypi/{package_name}/json")
    data = resp.json()
    return data['info']['version']


def update_package(package_name, pip_cmd):
    from subprocess import call
    call(f"{pip_cmd} install --upgrade {package_name}", shell=True)


def update_available(package_name):
    import pkg_resources
    packages = [dist.project_name for dist in pkg_resources.working_set]
    print(packages)
    if package_name not in packages:
        dprint(f"The package: [{package_name}] is not a dependency of this software.")
        return None
    vers = check_pypi_version(package_name)
    print(f"protobuf_avail: {vers}")
    print(f"protobuf_cur: {pkg_resources.get_distribution(package_name).version}")
    print(pkg_resources.get_distribution(package_name).location)
    if vers != pkg_resources.get_distribution(package_name).version:
        dprint(f"There is a newer version of: [{package_name}] available.")
        return True
    return False


def check_and_update(package_name, pip_cmd):
    import pkg_resources
    vers = check_pypi_version(package_name)
    if vers != pkg_resources.get_distribution(package_name).version:
        dprint(f"There is a newer version of: [{package_name}] available. Updating...")
        update_package(package_name, pip_cmd)
        return vers
    return None

