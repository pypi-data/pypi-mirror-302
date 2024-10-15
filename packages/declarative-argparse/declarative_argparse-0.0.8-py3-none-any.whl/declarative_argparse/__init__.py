from __future__ import annotations

import argparse
from typing import Any, Dict, List, Optional, Sequence, Type, cast

from declarative_argparse.options.abc import IDeclarativeOption
from declarative_argparse.options.bool import BoolArrayDO, BoolDO
from declarative_argparse.options.float import FloatArrayDO, FloatDO
from declarative_argparse.options.int import IntArrayDO, IntDO
from declarative_argparse.options.path import PathArrayDO, PathDO
from declarative_argparse.options.stores import StoreFalseDO, StoreTrueDO
from declarative_argparse.options.str import StrArrayDO, StrDO

__version__ = "0.0.8"

__all__ = [
    "BoolArrayDO",
    "BoolDO",
    "DeclarativeOptionParser",
    "FloatArrayDO",
    "FloatDO",
    "IntArrayDO",
    "IntDO",
    "PathArrayDO",
    "PathDO",
    "StoreFalseDO",
    "StoreTrueDO",
    "StrArrayDO",
    "StrDO",
]


class DeclarativeOptionParser:
    def __init__(self, argp: Optional[argparse.ArgumentParser]) -> None:
        self.argp: argparse.ArgumentParser = argp or argparse.ArgumentParser()
        self.allOpts: List[IDeclarativeOption] = []
        self.allOptsByID: Dict[str, IDeclarativeOption] = {}
        self.subparsers: Dict[str, "DeclarativeOptionParser"] = {}
        self.groups: Dict[str, "DeclarativeOptionParser"] = {}

        self.subp: Optional[argparse._SubParsersAction[argparse.ArgumentParser]] = None
        # self.verbose: BoolDO = self.addBool('quiet', 'q', 'Removes verbosity of output')

    def _bind_to_namespace(self, args: argparse.Namespace) -> None:
        for x in self.allOpts:
            x._bind_to_namespace(args)

        for p in self.subparsers.values():
            p._bind_to_namespace(args)

    def _bind_to_argparser(self) -> None:
        for arg in self.allOpts:
            arg.add_to_argparser(self.argp)
        # Recurse
        for p in self.subparsers.values():
            p._bind_to_argparser()

    def printHelp(self) -> None:
        self._bind_to_argparser()
        self.argp.print_help()

    def printUsage(self) -> None:
        self._bind_to_argparser()
        self.argp.print_usage()

    def parseArguments(self, args: Optional[Sequence[str]] = None) -> None:
        self._bind_to_argparser()
        ns = self.argp.parse_args(args)
        self._bind_to_namespace(ns)

    def addSubparser(
        self,
        name: str,
        aliases: Sequence[str] = [],
        description: Optional[str] = None,
    ) -> "DeclarativeOptionParser":
        if self.subp is None:
            self.subp = self.argp.add_subparsers()
        p = self.subp.add_parser(name, help=description, aliases=aliases)
        dop = DeclarativeOptionParser(p)
        self.subparsers[name] = dop
        return dop

    def addOptionGroup(
        self,
        title: str,
        description: Optional[str] = None,
    ) -> "DeclarativeOptionParser":
        g = self.argp.add_argument_group(title=title, description=description)
        dog = DeclarativeOptionParser(g)  # type: ignore
        self.groups[title] = dog
        return dog

    def setDefaults(self, **kwargs: Any) -> None:
        self.argp.set_defaults(**kwargs)

    def add(
        self,
        t: Type[IDeclarativeOption],
        *flags: str,
        description: Optional[str] = None,
    ) -> IDeclarativeOption:
        do = t(self, *flags, description=description)
        self.allOpts.append(do)
        self.allOptsByID[do.id] = do
        return do

    def addStoreTrue(
        self,
        *flags: str,
        description: Optional[str] = None,
    ) -> StoreTrueDO:
        return cast(StoreTrueDO, self.add(StoreTrueDO, *flags, description=description))

    def addStoreFalse(
        self,
        *flags: str,
        description: Optional[str] = None,
    ) -> StoreFalseDO:
        return cast(StoreFalseDO, self.add(StoreFalseDO, *flags, description=description))

    def addBool(
        self,
        *flags: str,
        description: Optional[str] = None,
    ) -> BoolDO:
        return cast(BoolDO, self.add(BoolDO, *flags, description=description))

    def addBoolArray(
        self,
        *flags: str,
        nargs: str,
        description: Optional[str] = None,
    ) -> BoolArrayDO:
        return cast(BoolArrayDO, self.add(BoolArrayDO, *flags, description=description)).setNArgs(nargs)  # type: ignore

    def addFloat(
        self,
        *flags: str,
        description: Optional[str] = None,
    ) -> FloatDO:
        return cast(FloatDO, self.add(FloatDO, *flags, description=description))

    def addFloatArray(
        self,
        *flags: str,
        nargs: str,
        description: Optional[str] = None,
    ) -> FloatArrayDO:
        return cast(FloatArrayDO, self.add(FloatArrayDO, *flags, description=description)).setNArgs(nargs)  # type: ignore

    def addInt(
        self,
        *flags: str,
        description: Optional[str] = None,
    ) -> IntDO:
        return cast(IntDO, self.add(IntDO, *flags, description=description))

    def addIntArray(
        self,
        *flags: str,
        nargs: str,
        description: Optional[str] = None,
    ) -> IntArrayDO:
        return cast(IntArrayDO, self.add(IntArrayDO, *flags, description=description)).setNArgs(nargs)  # type: ignore

    def addStr(
        self,
        *flags: str,
        description: Optional[str] = None,
    ) -> StrDO:
        return cast(StrDO, self.add(StrDO, *flags, description=description))

    def addStrArray(
        self,
        *flags: str,
        nargs: str,
        description: Optional[str] = None,
    ) -> StrArrayDO:
        return cast(StrArrayDO, self.add(StrArrayDO, *flags, description=description)).setNArgs(nargs)  # type: ignore

    def addPath(
        self,
        *flags: str,
        description: Optional[str] = None,
    ) -> PathDO:
        return cast(PathDO, self.add(PathDO, *flags, description=description))

    def addPathArray(
        self,
        *flags: str,
        nargs: str,
        description: Optional[str] = None,
    ) -> PathArrayDO:
        return cast(PathArrayDO, self.add(PathArrayDO, *flags, description=description)).setNArgs(nargs)  # type: ignore
