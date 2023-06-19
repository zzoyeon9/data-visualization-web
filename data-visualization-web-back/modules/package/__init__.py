#-*- coding:utf-8 -*-

"""Packages
"""

__all__ = [
    "Package",
]

#
# Imports Modules
#
import sys
import subprocess
import pkg_resources
from modules.exceptions import *
from modules.types import *

#
# Objects
#
class Package(Namespace):
    """Namespace Package
    """

    # Executable pythonfile
    execuable = sys.executable

    @classmethod
    def installed(namespace) -> DefaultList:
        """get installed packages list

        Returns
        -------
        :List : installed packages list

        """

        inst_pkgs = pkg_resources.working_set
        inst_pkgs_list = []
        for pkg in inst_pkgs:
            pkg_info = {"name": pkg.key, "version": pkg.version}
            inst_pkgs_list.append(pkg_info)
        return inst_pkgs_list

    @classmethod
    def install(
        namespace, 
        pkg_lib: String,
        upgrade: Boolean=False,
        no_deps: Boolean=False,
        force_reinstall: Boolean=False,
    ):
        """install package

        Parameters
        ----------
        pkg_lib: String: Package library name

        upgrade: Boolean: Upgrade all specified packages to the newest available version

        no_deps: Boolean: Don't install package dependencies

        force_reinstall: Boolean: Reinstall all packages even if they are already up-to-date.

        """

        # Setting arguments
        args = [
            namespace.execuable, 
            '-m', 
            'pip', 
            'install', 
        ]
        if upgrade:
            args += ['--upgrade']
        if no_deps:
            args += ['--no-deps']
        if force_reinstall:
            args += ['--force-reinstall']
        args += [pkg_lib]

        # Call the subprocess without stdout.
        namespace._subprocess_call_without_stdout(args)

    @classmethod
    def uninstall(namespace, pkg_lib: String):
        """uninstall package

        Parameters
        ----------
        pkg_lib: String: package library name

        """

        # Setting arguments
        args = [
            namespace.execuable, 
            '-m', 
            'pip', 
            'uninstall', 
            '--y', 
            pkg_lib,
        ]

        # Call the subprocess without stdout.
        namespace._subprocess_call_without_stdout(args)

    @classmethod
    def find_package(namespace, name: String) -> DefaultDict:
        """Find package

        Parameters
        ----------
        name: String: Package name

        Returns
        -------
        :Dict :Package info

        """

        # Search the package: by name
        for int_pkg_info in namespace.installed():
            pkg_name = int_pkg_info["name"]
            if pkg_name == name:
                return int_pkg_info
        
        # Not Fouund Package
        message = "NotFoundError: {0}".format(name)
        raise PackageNotFoundError(message)

    def _subprocess_call_without_stdout(args: DefaultList):
        """Create subprocess without stdout.

        Parameters
        ----------
        args: List: Arguments

        """
        
        subprocess.check_call(args, stdout=subprocess.DEVNULL)
