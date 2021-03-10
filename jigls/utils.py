# -*- coding: utf-8 -*-
# type:ignore

import hashlib
import json
import re
from typing import DefaultDict, Dict, Iterable, List, Tuple, Union


def Chunks(lst: Union[List, Tuple], n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def FilenameFromPath(path: str) -> str:
    return re.findall(r"[^\W]+|\d+", path)[-2]


def TokenizeParseString(string: str) -> List[str]:
    return string.split("_")


def IterableToDict(t: Iterable[Tuple]) -> DefaultDict[str, List[str]]:
    default_ = DefaultDict()
    for ix in t:
        default_.setdefault(ix[0], []).append(ix[1])
    return default_