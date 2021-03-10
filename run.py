# -*- coding: utf-8 -*-

import logging

from jigls.facade.compare import Compare
from jigls.facade.stats import TCStat

# from jigls.facade.tceuler import TCEuler
from jigls.facade.tcbfs import TCBFS
from jigls.facade.tcbruteforce import TCBruteForce
from jigls.facade.tcdfs import TCDFS
from jigls.facade.updatedb import UpdateDB
from jigls.logger import logger

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
