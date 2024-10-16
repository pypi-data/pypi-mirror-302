from nodeflow.adapters import Adapter
from typing import Iterable, Type, Optional, List, Dict
from nodeflow.node import Variable
from collections import deque


class Converter:
    def __init__(self, adapters: Iterable[Adapter]):
        self.graph = {}
        self.add_adapters(adapters)

    def add_adapter(self, adapter: Adapter):
        # Resolve source type
        source_type = adapter.get_type_of_source_variable().__name__
        if source_type not in self.graph:
            self.graph[source_type] = {}

        # Resolve target type
        target_type = adapter.get_type_of_target_variable().__name__
        self.graph[source_type][target_type] = adapter

    def add_adapters(self, adapters: Iterable[Adapter]):
        for adapter in adapters:
            self.add_adapter(adapter)

    def is_support_variable(self, variable_type: Type[Variable]) -> bool:
        return variable_type in self.graph

    def convert(self, variable: Variable, to_type: Type[Variable]) -> Optional[Variable]:
        pipeline = self._get_converting_pipeline(source=variable.__class__, target=to_type)
        assert pipeline is not None, "Could not convert variable"

        for i in range(1, len(pipeline)):
            variable = self.graph[pipeline[i-1]][pipeline[i]].convert(variable)

        return variable

    def _get_converting_pipeline(self, source: Type[Variable], target: Type[Variable]) -> Optional[List[Variable]]:
        # ---------
        # BFS
        # ---------
        visited = set()
        queue   = deque()
        queue.append([source.__name__, [source.__name__]])

        while len(queue) > 0:
            root_type, type_road = queue.popleft()
            visited.add(root_type)
            for child in self.graph[root_type]:
                if child in visited:
                    continue
                if child == target.__name__:
                    return type_road + [child]
                queue.append([child, type_road + [child]])


__all__ = [
    "Converter"
]