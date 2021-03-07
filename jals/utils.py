# -*- coding: utf-8 -*-
#type:ignore

import hashlib
import json
import re
from typing import DefaultDict, Dict, Iterable, List, Tuple, Union

def Chunks(lst:Union[List, Tuple], n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def FilenameFromPath(path:str)->str:
    return re.findall(r"[^\W]+|\d+", path)[-2]


def TokenizeParseString(string:str)->List[str]:
    return string.split('_')


def LinkToDict(t: Iterable[Tuple]) -> DefaultDict[str, List[str]]:
    default_ = DefaultDict()
    for lanes in t:
        default_.setdefault(lanes[0], []).append(lanes[1])
    return default_


def HashDict(graphOne: DefaultDict)-> str:

    hash = hashlib.md5()
    hash.update(json.dumps(graphOne, sort_keys=True).encode())
    return hash.hexdigest()


def HashString(string: str)-> str:

    hash = hashlib.md5()
    hash.update(string.encode())
    return hash.hexdigest()
