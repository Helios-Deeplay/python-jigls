# -*- coding: utf-8 -*-
# https://docs.python.org/3/library/logging.html

import logging
import logging.config
logger = logging.config.fileConfig(fname=r'./config/log.conf')

def NotTrace(func):
    def wrapper(self, *args, **kwargs):
        if func.__name__ not in self.nTrace:
            self.nTrace.append(func.__name__)
            print(f"trace functioncall {func.__name__} added to ignore list !!")
        return func(self, *args, **kwargs)
    return wrapper