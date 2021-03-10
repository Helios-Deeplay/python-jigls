# from __future__ import annotations

# import logging
# from typing import List, Optional, Union

# from jils.concrete.base import Base
# from jils.concrete.edge import Edge
# from jils.concrete.node import Node

# from jils.logger import logger

# logger = logging.getLogger(__name__)


# class StateNode(Node):

#     __type__ = "StateNode"

#     def __init__(
#         self,
#         parent: Base,
#         name: str,
#         dirty: bool = False,
#         enable: bool = True,
#         debug: bool = True,
#     ):
#         super().__init__(
#             parent, name, dirty=dirty, enable=enable, debug=debug
#         )
#         self.value: Optional[bool] = None

#     def Set(self, value: Optional[bool]):
#         if self.value == value:
#             return

#         pvalue = self.value
#         self.value = value

#         if self.debug:
#             logger.debug(
#                 f"[P:{self.parent.name}] [N:{self.name}] value change {pvalue} - {self.value}"
#             )

#         if isinstance(self.parent, Edge):
#             if self.debug:
#                 logger.debug(
#                     f"[N:{self.name}] triggered [P:{self.parent.name}]"
#                 )
#             self.parent.Evaluate()

#         for connection in self.connections:
#             if self.debug:
#                 logger.debug(
#                     f"[P:{self.parent.name}] [N:{self.name}] connection to N:{connection.name} value set {value}"
#                 )
#             connection.Set(value)