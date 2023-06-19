#-*- coding:utf-8 -*-

"""Dependency
"""

__all__ = [
    "check_dependencies",
    "PackageNotFoundError",
]

#
# Imports Modules
#
from modules.config import Config
from modules.package import Package
from modules.exceptions import *
from modules.types import *

#
# Functions
#
def check_dependencies():
    """Check package dependencies
    """

    # Get dependencies
    dependencies = Config().dependencies

    # Check package dependencies
    for pkg_info in dependencies:

        # Get pkg name
        new_pkg_name: String=pkg_info["name"]

        # Get pkg version
        if "version" in pkg_info:
            new_pkg_version: String=pkg_info["version"]
        else:
            new_pkg_version = ""

        # Get pkg install commnad
        if "install" in pkg_info:
            new_pkg_install: String=pkg_info["install"]
        else:
            new_pkg_install: String=new_pkg_name
        
        try:
            old_pkg_info = Package.find_package(new_pkg_name)
        
        except PackageNotFoundError:
            # In the case, Not exist package
            # Sets the command to install libraries
            if len(new_pkg_version) > 0:
                pkg_lib: String="{INSTALL}=={VERSION}".format(INSTALL=new_pkg_install, VERSION=new_pkg_version)
            else:
                pkg_lib: String="{INSTALL}".format(INSTALL=new_pkg_install)

            # Try to install the package
            Package.install(pkg_lib)

        except Exception:
            # In other Exceptions, Skip
            continue

        else:
            # In the case, Already installed package.
            if not len(new_pkg_version):
                continue

            # Get old version
            old_pkg_version: String=old_pkg_info["version"]

            # Try to compare teh version.
            if new_pkg_version.split(".") == old_pkg_version.split("."):
                continue

            # Sets the command to install libraries
            pkg_lib: String="{INSTALL}=={VERSION}".format(INSTALL=new_pkg_install, VERSION=new_pkg_version)

            # Try to install the package
            Package.install(
                pkg_lib, 
                upgrade=True, 
                no_deps=True, 
                force_reinstall=True,
            )
