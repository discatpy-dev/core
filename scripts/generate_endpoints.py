import argparse
import builtins
import contextlib
import json
import pathlib
import types
from typing import Any, Final, Optional, TypeVar, Union, overload

#
#  Constants
#

DEFAULT_SOURCE_DIR = "data/endpoints"
DEFAULT_DEST_DIR = "discatcore/http/endpoints"
VALID_METHODS = ["GET", "HEAD", "POST", "PUT", "DELETE", "PATCH"]
GENERATION_COMMENT = "# this file was auto-generated by scripts/generate_endpoints.py"
IMPORTS = {
    "Any": "from typing import Any",
    "Union": "from typing import Union",
    "Optional": "from typing import Optional",
    "Snowflake": "from discord_typings import Snowflake",
    "discord_typings": "import discord_typings",
    "BasicFile": "from discatcore.file import BasicFile",
    "Unset": "from discatcore.types import Unset",
}
FILE_TEMPLATE = f"""# SPDX-License-Identifier: MIT

{GENERATION_COMMENT}

{{0}}
from discatcore.http.endpoints.core import EndpointMixin
from discatcore.http.route import Route

__all__ = ("{{1}}",)

class {{1}}(EndpointMixin):
{{2}}

"""
INIT_HEADER = f"""\"\"\"
discatcore.http.endpoints
~~~~~~~~~~~~~~~~~~~~~~~~~

The implementations for Discord API endpoints. These are for internal use only, use
`discatcore.http.HTTPClient` instead.
\"\"\"

{GENERATION_COMMENT}

"""
T = TypeVar("T")


class _UnsetDefine:
    pass


Unset: Final[Any] = _UnsetDefine()

#
#  Function Creator
#

# taken from typing
# https://github.com/python/cpython/blob/3.10/Lib/typing.py#L185-L203
def _type_repr(obj: Any):
    """Return the repr() of an object, special-casing types (internal helper).
    If obj is a type, we return a shorter version than the default
    type.__repr__, based on the module and qualified name, which is
    typically enough to uniquely identify a type.  For everything
    else, we fall back on repr(obj).
    """
    if isinstance(obj, types.GenericAlias):
        return repr(obj)
    if isinstance(obj, type):
        if obj.__module__ == "builtins":
            return obj.__qualname__
        return f"{obj.__module__}.{obj.__qualname__}"
    if obj is ...:
        return "..."
    if isinstance(obj, types.FunctionType):
        return obj.__name__
    return repr(obj)


class FunctionArg:
    name: Optional[str]
    annotation: str
    default: str
    pos_and_kw: bool
    pos_modifier: bool
    kw_modifier: bool
    variable_pos: bool
    variable_kw: bool

    def __init__(
        self,
        name: Optional[str] = None,
        *,
        annotation: str = Unset,
        default: str = Unset,
        pos_and_kw: bool = True,
        pos_modifier: bool = False,
        kw_modifier: bool = False,
        variable_pos: bool = False,
        variable_kw: bool = False,
    ):
        self.name = name
        self.annotation = annotation
        self.default = default
        self.pos_and_kw = pos_and_kw
        self.pos_modifier = pos_modifier
        self.kw_modifier = kw_modifier
        self.variable_pos = variable_pos
        self.variable_kw = variable_kw

        if self.pos_modifier and self.kw_modifier:
            raise ValueError(
                f"arg {self.name} cannot be both a positional modifier and a keyword modifier!"
            )
        if self.variable_pos and self.variable_kw:
            raise ValueError(
                f"arg {self.name} cannot be both a variable positional argument and a variable keyword argument!"
            )
        if (self.pos_modifier or self.kw_modifier) and (self.variable_pos or self.variable_kw):
            raise ValueError(f"arg {self.name} cannot be both a modifier and a variable argument!")
        if (self.pos_modifier or self.kw_modifier) and self.name:
            raise ValueError(f"arg {self.name} cannot be a modifier and have a name!")
        elif not (self.pos_modifier or self.kw_modifier) and not self.name:
            raise ValueError(f"non-modifier args require a name!")
        if (self.pos_modifier or self.kw_modifier) and self.annotation is not Unset:
            raise ValueError(f"modifier args cannot have annotations!")


def indent(text: str, *, level: int = 1):
    return "    " * level + text


class FunctionCreator:
    """A class that can dynamically create a function in a nice, OOP styled fashion.

    Args:
        name (str): The name of this function.
        decorators (Optional[List[:class:`str`]]): The list of decorators for this function. Defaults to None.
        is_async (bool): Whether or not this function is asynchronous. Defaults to False.

    Attributes:
        func_args (List[:class:`FunctionArg`]): The list of arguments for this function.
    """

    def __init__(
        self, name: str, *, decorators: Optional[list[str]] = None, is_async: bool = False
    ):
        self.func_name: str = name
        self.func_async: bool = is_async
        self.func_args: list[FunctionArg] = []
        self.func_return_anno: Union[str, types.EllipsisType] = ...
        self.func_decorators: Optional[list[str]] = decorators
        self.func_body: list[str] = []
        self.func_indent_level: int = 1

    def insert_arg(self, arg: FunctionArg, index: int):
        self.func_args.insert(index, arg)

    def append_arg(self, arg: FunctionArg):
        self.func_args.append(arg)

    def remove_arg(self, index: int):
        del self.func_args[index]

    @contextlib.contextmanager
    def indent(self):
        self.func_indent_level += 1
        try:
            yield
        finally:
            self.func_indent_level -= 1

    def print(self, *args: str):
        if not args:
            self.func_body.append("")
        else:
            self.func_body.extend([indent(arg, level=self.func_indent_level) for arg in args])

    def print_block(self, lines: str):
        for line in lines.splitlines():
            self.print(line)

    def _convert_arg_to_str(self, arg: FunctionArg):
        str_arg: str = ""

        if (arg.variable_pos or arg.variable_kw or arg.pos_and_kw) and arg.name:
            if arg.variable_pos or arg.variable_kw:
                str_arg += "*" * (arg.variable_pos or arg.variable_kw * 2)
            str_arg += arg.name

            if arg.annotation is not Unset:
                str_arg += f": {arg.annotation}"
            if arg.default is not Unset:
                str_arg += f" = {arg.default}"
        else:
            str_arg += "*" if arg.kw_modifier else "/"

        return str_arg

    def generate_raw(self):
        func_str = ""
        if self.func_async:
            func_str += "async "

        str_args = ", ".join([self._convert_arg_to_str(arg) for arg in self.func_args])
        func_str += f"def {self.func_name}({str_args})"
        if self.func_return_anno is not ...:
            func_str += f" -> {self.func_return_anno}"
        func_str += ":\n" + "\n".join(self.func_body)

        return func_str

    def generate(
        self, *, globals: dict[str, Any] = {}, locals: dict[str, Any] = {}
    ) -> types.FunctionType:
        if "BUILTINS" not in locals:
            locals["BUILTINS"] = builtins

        func_str = "\n".join([indent(line) for line in self.generate_raw().splitlines()])
        local_vars = ", ".join(locals.keys())
        func_creator_str = (
            f"def __create_fn__({local_vars}):\n{func_str}\n    return {self.func_name}"
        )

        ns = {}
        exec(func_creator_str, globals, ns)

        # since pyright is a static type checker, it doesn't know the type of what was generated
        # in the ns
        func = ns["__create_fn__"](**locals)  # type: ignore
        if not isinstance(func, types.FunctionType):
            raise TypeError(
                f"the generated object was of type {type(func)!r}, not types.FunctionType!"  # type: ignore
            )
        return func


#
#  JSON Parsing
#


@overload
def _dict_type_check(d: dict[Any, Any], key: Any, expected_type: type[T]) -> T:
    ...


@overload
def _dict_type_check(
    d: dict[Any, Any], key: Any, expected_type: type[T], *, is_required: bool = ...
) -> Union[T, Any]:
    ...


def _dict_type_check(
    d: dict[Any, Any], key: Any, expected_type: type[T], *, is_required: bool = True
) -> Union[T, Any]:
    val = d.get(key, ...)
    if val is ... and is_required:
        raise KeyError(key)
    elif val is ...:
        return Unset

    if isinstance(val, expected_type):
        return val
    raise TypeError(f"the value at key {key} is not of type {_type_repr(expected_type)}!")


def _generate_func_args_json_query(
    func_gen: FunctionCreator,
    params: dict[str, Union[str, list[Any]]],
):
    for param_name, param in params.items():
        default = Unset
        if isinstance(param, str):
            anno = param
        elif isinstance(param, list) and len(param) == 2:  # type: ignore
            anno, default = param
        else:
            raise TypeError(f"Invalid type {_type_repr(param)} for JSON/Query parameter values")

        func_gen.append_arg(FunctionArg(param_name, annotation=anno, default=default))


def _generate_func_args(
    func_gen: FunctionCreator,
    url_params: dict[Any, Any],
    json_params: dict[Any, Any],
    query_params: dict[Any, Any],
    extra_params: dict[Any, Any],
):
    if url_params is not Unset:
        for param_name, param_anno in url_params.items():
            func_gen.append_arg(FunctionArg(param_name, annotation=param_anno))

    if json_params is not Unset or query_params is not Unset or extra_params is not Unset:
        func_gen.append_arg(FunctionArg(kw_modifier=True))

        if json_params is not Unset:
            _generate_func_args_json_query(func_gen, json_params)

        if query_params is not Unset:
            _generate_func_args_json_query(func_gen, query_params)

        if extra_params is not Unset:
            _generate_func_args_json_query(func_gen, extra_params)


def parse_endpoint_func(name: str, func: dict[str, Any]):
    method = _dict_type_check(func, "method", str)
    if method not in VALID_METHODS:
        raise ValueError(f"Invalid method {method}!")
    url = _dict_type_check(func, "url", str)
    url_params: dict[str, str] = _dict_type_check(func, "url-parameters", dict, is_required=False)
    json_params: dict[str, Union[str, list[str]]] = _dict_type_check(
        func, "json-parameters", dict, is_required=False
    )
    query_params: dict[str, Union[str, list[str]]] = _dict_type_check(
        func, "query-parameters", dict, is_required=False
    )
    extra_params: dict[str, Union[str, list[str]]] = _dict_type_check(
        func, "extra-parameters", dict, is_required=False
    )
    extra_request_params: dict[str, str] = _dict_type_check(
        func, "extra-request-parameters", dict, is_required=False
    )
    extra_code: list[str] = list(func.get("extra-code", []))
    supports_reason = bool(func.get("supports-reason"))
    supports_files = bool(func.get("supports-files"))

    func_generator = FunctionCreator(name, is_async=False)

    # generate arguments
    func_generator.append_arg(FunctionArg("self"))
    _generate_func_args(func_generator, url_params, json_params, query_params, extra_params)

    if supports_reason:
        func_generator.append_arg(FunctionArg("reason", annotation="Optional[str]", default="None"))
    if supports_files:
        func_generator.append_arg(
            FunctionArg("files", annotation="list[BasicFile]", default="Unset")
        )

    # generate body
    fmted_url_params = ""
    if url_params is not Unset:
        fmted_url_params += ", " + ", ".join([f"{name}={name}" for name in url_params])

    fmted_extra_params = ""
    if json_params is not Unset:
        fmted_extra_params += ", json_params={"
        fmted_extra_params += ",".join(
            [f'"{param_name}":{param_name}' for param_name in json_params]
        )
        fmted_extra_params += "}"
    if query_params is not Unset:
        fmted_extra_params += ", query_params={"
        fmted_extra_params += ",".join(
            [f'"{param_name}":{param_name}' for param_name in query_params]
        )
        fmted_extra_params += "}"
    if extra_request_params is not Unset:
        fmted_extra_params += ", " + ", ".join(
            [
                f"{param_name}={param_value}"
                for param_name, param_value in extra_request_params.items()
            ]
        )

    if supports_reason:
        fmted_extra_params += ", reason=reason"
    if supports_files:
        fmted_extra_params += ", files=files"

    if extra_code:
        func_generator.print(*extra_code)
    func_generator.print(
        f'return self.request(Route("{method}", "{url}"{fmted_url_params}){fmted_extra_params})'
    )

    return func_generator.generate_raw()


def parse_json_file(file: dict[str, Any]):
    funcs: list[str] = []
    name = _dict_type_check(file, "name", str)
    methods: dict[str, Any] = _dict_type_check(file, "methods", dict)
    requires: list[str] = _dict_type_check(file, "requires", list, is_required=False)

    imports = ""
    if requires is not Unset:
        for requirement in requires:
            imports += f"{IMPORTS[requirement]}\n"

    for func_name, func_metadata in methods.items():
        func = parse_endpoint_func(func_name, func_metadata)
        funcs.append("\n".join([indent(line) for line in func.splitlines()]))

    return FILE_TEMPLATE.format(imports, name, "\n\n".join(funcs) if len(funcs) else indent("pass"))


#
#  Main
#


def is_path_legit(p: pathlib.Path):
    return p.exists() and p.is_dir()


def parse_args():
    parser = argparse.ArgumentParser(
        prog="generate_endpoints",
        description="A helper for DisCatCore that processes JSON files into HTTP Endpoint functions.",
    )

    parser.add_argument(
        "-s",
        "--source",
        default=DEFAULT_SOURCE_DIR,
        help="The source directory where the JSON files are located.",
    )
    parser.add_argument(
        "-d",
        "--destination",
        default=DEFAULT_DEST_DIR,
        help="The destination directory where the generated Python files will be stored.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Whether or not the generated files should be stored. This will print the file's contents to STDOUT.",
    )
    parser.add_argument(
        "--no-overwrite",
        action="store_true",
        help="Whether or not a file that already exists in the destination directory should be overwritten.",
    )
    parser.add_argument(
        "--no-init-generation",
        action="store_true",
        help="Whether or not the __init__ file should be generated.",
    )

    gen_args = parser.parse_args()
    gen_args.init_generation = not gen_args.no_init_generation
    gen_args.overwrite = not gen_args.no_overwrite
    return gen_args


def main():
    args = parse_args()
    src_dir = pathlib.Path(args.source)
    dest_dir = pathlib.Path(args.destination)

    if not is_path_legit(src_dir):
        raise ValueError(
            f"Source path {str(src_dir)} is not valid. Please retry with a valid path."
        )
    if not is_path_legit(dest_dir):
        raise ValueError(
            f"Destination path {str(dest_dir)} is not valid. Please retry with a valid path."
        )

    generated_filenames: list[str] = []

    for file in sorted(src_dir.glob("*.json")):
        loaded_file = json.loads(file.read_text())
        if len(loaded_file):
            print("Generating file for JSON metadata", str(file) + "...")

            generated_file = parse_json_file(loaded_file)
            print("Generated file for JSON metadata", str(file) + "!")

            if args.dry_run:
                print(generated_file)
                generated_filenames.append(file.stem)
            else:
                dest_path = dest_dir / f"{file.stem}.py"
                if dest_path.exists() and args.overwrite or not dest_path.exists():
                    if not dest_path.exists():
                        dest_path.touch()
                    with dest_path.open("w") as f:
                        f.write(generated_file)

                    generated_filenames.append(file.stem)
                else:
                    print(
                        "Destination file",
                        str(dest_path),
                        "already exists and overwrite is off! Skipping...",
                    )
                    continue

    if args.init_generation:
        print("Generating file for __init__.py...")
        init_file = INIT_HEADER

        for filename in sorted(generated_filenames):
            init_file += f"from .{filename} import *\n"

        print("Generated file for __init__.py!")
        if args.dry_run:
            print(init_file)
        else:
            dest_path = dest_dir / "__init__.py"
            if dest_path.exists() and args.overwrite or not dest_path.exists():
                if not dest_path.exists():
                    dest_path.touch()
                with dest_path.open("w") as f:
                    f.write(init_file)
            else:
                print(
                    "Destination file __init__.py already exists and overwrite is off! Skipping...",
                )


if __name__ == "__main__":
    main()
