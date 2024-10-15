# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Show Create Node

This is a SQL Query Execution Plan Node.
"""

from typing import Generator

import pyarrow

from opteryx.exceptions import DatasetNotFoundError
from opteryx.exceptions import UnsupportedSyntaxError
from opteryx.models import QueryProperties
from opteryx.operators import BasePlanNode
from opteryx.operators import OperatorType


class ShowCreateNode(BasePlanNode):
    operator_type = OperatorType.PRODUCER

    def __init__(self, properties: QueryProperties, **config):
        super().__init__(properties=properties)

        self.object_type = config.get("object_type")
        self.object_name = config.get("object_name")

    @classmethod
    def from_json(cls, json_obj: str) -> "BasePlanNode":  # pragma: no cover
        raise NotImplementedError()

    @property
    def name(self):  # pragma: no cover
        return "Show"

    @property
    def config(self):  # pragma: no cover
        return ""

    def execute(self) -> Generator:
        if self.object_type == "VIEW":
            from opteryx.planner.views import is_view
            from opteryx.planner.views import view_as_sql

            if is_view(self.object_name):
                view_sql = view_as_sql(self.object_name)
                buffer = [{self.object_name: view_sql}]
                table = pyarrow.Table.from_pylist(buffer)
                yield table
                return

            raise DatasetNotFoundError(self.object_name)

        raise UnsupportedSyntaxError("Invalid SHOW statement")
