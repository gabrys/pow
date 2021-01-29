#!/usr/bin/env python3

import importlib.util
import os
import re
import sys
from pathlib import Path


class PowEnv:
    BASENAME = 'pow'
    CWD = os.getcwd()
    HOME = os.path.expanduser("~")
    POW_FILE_GLOBS = [
        "pow_file.py",
        ".pow_file.py",
        "pow_files/pow_*.py",
        ".pow_files/pow_*.py",
    ]
    TERM = os.getenv("TERM")
    UID = os.getenv("UID")
    USER = os.getenv("USER")


class PowPlugins:
    pass


class PowUtils:
    @staticmethod
    def get_cwd_and_parents():
        return [Path(PowEnv.CWD)] + list(Path(PowEnv.CWD).parents)

    @staticmethod
    def print_error(msg):
        print(
            "{}: {}".format(PowEnv.BASENAME, msg), file=sys.stderr,
        )

    @staticmethod
    def print_usage():
        usage = [
            "\nUsage: {} [options] <command> [command parameters]\n".format(
                PowEnv.BASENAME
            )
        ]
        names = sorted(Pow.commands.keys())
        longest_name_len = max((len(name) for name in names), default=0)
        line_template = "  {} {{:{}}}   {{}}".format(PowEnv.BASENAME, longest_name_len)
        for name in names:
            usage.append(line_template.format(name, Pow.commands[name].__doc__ or ""))
        print("\n".join(usage) + "\n", file=sys.stderr)

    @staticmethod
    def to_kabob_case(name):
        return name.replace("_", "-")

    @staticmethod
    def to_snake_case(name):
        return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


class Pow:
    # Helpers
    env = PowEnv()
    utils = PowUtils()

    # For pow debugging
    _command_origins = {}
    _plugin_origins = {}
    _pow_files = []

    # pow_files fill these
    commands = {}
    plugins = PowPlugins()


class PowDefaultCommands:
    @staticmethod
    def pow__h(args):
        """Alias for --help"""
        PowUtils.print_usage()

    @staticmethod
    def pow___help(args):
        """Print pow's usage and available commands"""
        PowUtils.print_usage()

    @staticmethod
    def pow_inspect_pow(args):
        """Inspect loaded pow files"""
        inventory = {}

        for file in Pow._pow_files:
            inventory[file] = {
                "plugins": [],
                "commands": [],
            }

        for plugin, origin in Pow._plugin_origins.items():
            inventory[origin]["plugins"].append((plugin, getattr(Pow.plugins, plugin)))

        for cmd, origin in Pow._command_origins.items():
            inventory[origin]["commands"].append((cmd, Pow.commands[cmd]))

        for file in Pow._pow_files:
            plugins = sorted(inventory[file]["plugins"])
            commands = sorted(inventory[file]["commands"])
            print(
                "* {}".format(
                    "pow internal" if file == "__pow__" else "from {}".format(file)
                )
            )
            print("  * plugins: {}".format(len(plugins)))
            for plugin_name, _ in plugins:
                print("    * {}".format(plugin_name))
            print("  * commands: {}".format(len(commands)))
            for cmd_name, _ in commands:
                print("    * {}".format(cmd_name))
            print("")


def main(args):
    register_pow_module(PowDefaultCommands, file_path="__pow__")
    files_to_load = []
    for path in reversed(PowUtils.get_cwd_and_parents()):
        for glob in PowEnv.POW_FILE_GLOBS:
            for pow_path in path.glob(glob):
                if os.path.isfile(pow_path):
                    files_to_load.append(pow_path.as_posix())
    for file in files_to_load:
        mod = load_pow_module(file)
        register_pow_module(mod, file_path=file)

    if not len(args):
        PowUtils.print_usage()
        return

    cmd = PowUtils.to_kabob_case(args.pop(0))
    fn = Pow.commands.get(cmd)
    if fn is None:
        PowUtils.print_error('command "{}" not found'.format(cmd))
        return

    return fn(args)


def load_pow_module(path):
    # load module
    spec = importlib.util.spec_from_file_location(path, path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except:
        PowUtils.print_error("error loading pow file {}".format(path))
        raise

    mod.Pow = Pow
    return mod


def register_pow_module(mod, file_path):
    # Register the file path itself
    Pow._pow_files.append(file_path)

    # Register commands
    cmd_prefix = "pow_"
    cmd_prefix_len = len(cmd_prefix)
    for name in dir(mod):
        if name.startswith(cmd_prefix):
            fn = getattr(mod, name)
            cmd_name = PowUtils.to_kabob_case(name[cmd_prefix_len:])
            Pow.commands[cmd_name] = fn
            Pow._command_origins[cmd_name] = file_path

    # Register plugins
    plugin_prefix = "PowPlugin"
    plugin_prefix_len = len(plugin_prefix)
    for name in dir(mod):
        if name.startswith(plugin_prefix):
            plugin = getattr(mod, name)()
            plugin_name = PowUtils.to_snake_case(name[plugin_prefix_len:])
            setattr(Pow.plugins, plugin_name, plugin)
            Pow._plugin_origins[plugin_name] = file_path


if __name__ == "__main__":
    main(sys.argv[1:])
