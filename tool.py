import os
import argparse
from util import get_submodules, lazy_import

tool_modules = lazy_import("tools")
available_tools = get_submodules(tool_modules)

cli_parser = argparse.ArgumentParser(prog="yt-download",
                                     description="Youtube download"
                                     " utility tool")
cli_subparser = cli_parser.add_subparsers(title="Tools",
                                          dest="tool_name",
                                          required=True)

for tool_name in available_tools:
    tool_mod = lazy_import("tools."+tool_name)
    subparser = cli_subparser.add_parser(tool_name, **tool_mod.ARG_PARSER)

    for arg, arg_prop in tool_mod.ARGS.items():
        arg_splitted = arg.split(';')
        subparser.add_argument(*arg_splitted, **arg_prop)

args = cli_parser.parse_args()

if not os.path.exists("data"):
    os.mkdir("data")

tool_mod = lazy_import("tools."+args.tool_name)
tool_mod.run(args)
