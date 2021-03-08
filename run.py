# -*- coding: utf-8 -*-

import logging

from jils.facade.compare import Compare
from jils.facade.stats import TCStat

# from jils.facade.tceuler import TCEuler
from jils.facade.tcbfs import TCBFS
from jils.facade.tcbruteforce import TCBruteForce
from jils.facade.tcdfs import TCDFS
from jils.facade.updatedb import UpdateDB
from jils.logger import logger

logger = logging.getLogger(__name__)


def main(args):

    if args.updatedb:
        instanceUpdate = UpdateDB(file=args.opendrive, delta=args.delta)
        instanceUpdate.Run()

    elif args.bfs:
        instanceTCBFS = TCBFS(id=args.id)
        instanceTCBFS.Run()

    elif args.dfs:
        logger.error(f"ignore at the moment ..., modify database")
        # instanceTCBFS = TCDFS(id=args.id)
        # instanceTCBFS.Run()

    elif args.brute:
        instanceBrute = TCBruteForce(id=args.id, time=args.time)
        instanceBrute.Run()

    elif args.stat:
        instanceTCStat = TCStat(id=args.id)
        instanceTCStat.Run()

    elif args.compare:
        instanceCompare = Compare(oldid=args.id, newid=args.delta)
        instanceCompare.Run()
