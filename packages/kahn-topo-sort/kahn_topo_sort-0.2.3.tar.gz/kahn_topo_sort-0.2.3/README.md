# Topological Sort Package

This package helps with sorting arrays based on the info a 2d-array provides.

## Example

from kahn-topo-sort import Topo_Sort as ToSo

2d_Array = [
    ['B', 'A', 'D', 'F'],
    ['D', 'F'],
    ['A', 'E', 'D', 'C'],
    ['F', 'C'],
]
Array = [
    'B', 'C', 'D', 'F'
]

graph, in_degree = ToSo.createGraph(2d_Array)
sorted_list = ToSo.sort(graph=graph, in_degree=in_degree)
result = ToSo.filterList(sorted_list, Array)

print(result)

result = [
    'B', 'D', 'F', 'C'
]
