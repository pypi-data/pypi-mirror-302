## rowfind
Find points that make an equally spaced row on a 2D plane.

Fast and simple, finds rows by walking in 4 directions `1,0  0,1  1,1  1,-1` to n steps from a point and checking if the next point exists.

### All possible rows
`find_all` finds all rows that satisfy the given lengths and steps.
```python
coords = [
    (0, 0), (1, 1), (2, 2), (3, 3), (3, 4),
    (3, 5), (12, 3), (12, 4), (11, 3), (11, 2),
    (11, 1), (10, 3), (5, 3), (6, 2), (7, 1),
    (7, 0), (8, 1), (8, 5), (9, 5), (4, 4)
]
lengths = 3
steps = 1
rows = rowfind.find_all(coords, lengths, steps)

# The return value is a tuple of tuples, where each
# tuple is a group of points that form a row.

print("\n".join(map(str, rows)))
print(rowfind.draw_graph(coords, rows))

"""
((5, 3), (6, 2), (7, 1))
((1, 1), (2, 2), (3, 3))
((11, 1), (11, 2), (11, 3))
((3, 3), (3, 4), (3, 5))
((0, 0), (1, 1), (2, 2))
((2, 2), (3, 3), (4, 4))
((4, 4), (5, 3), (6, 2))
((3, 5), (4, 4), (5, 3))
((10, 3), (11, 3), (12, 3))
 . . . X . . . . O O . . .
 . . . X X . . . . . . . O
 . . . X . X . . . . X X X
 . . X . . . X . . . . X .
 . X . . . . . X O . . X .
 X . . . . . . O . . . . .
"""
```
`steps` dictates the gap between points in a row.

If `steps` is set to 1, only immediate neighbors will be matched.
```
. x x x .
o . . x .
. . x . x
. x . . o
```
If it's set to 2, only gaps of 1 will be matched.
```
x . x . x
. . . . o
. . x . o
. o . . .
x . x . .
```

`lengths` dictates the row lengths that will be matched.

Both `steps` and `lengths` can be an integer, a tuple/list of integers (multiple constraints) or None.

If they're set to None, all possible steps or lengths that fit into the plane's bounds will be matched. This can be slow if the min and max are far apart.

### Unique rows
`find_unique` finds all rows that satisfy the given steps and minimum length. Sub-rows will not be considered as distinct, so no overlaps.
```python
coords = [
    (0, 0), (1, 1), (2, 2), (3, 3), (3, 4),
    (3, 5), (12, 3), (12, 4), (11, 3), (11, 2),
    (11, 1), (10, 3), (5, 3), (6, 2), (7, 1),
    (7, 0), (8, 1), (8, 5), (9, 5), (4, 4)
]
min_length = 3
steps = 1
rows = rowfind.find_unique(coords, min_length, steps)

print("\n".join(map(str, rows)))
print(rowfind.draw_graph(coords, rows))

"""
((11, 1), (11, 2), (11, 3))
((3, 5), (4, 4), (5, 3), (6, 2), (7, 1))
((3, 3), (3, 4), (3, 5))
((0, 0), (1, 1), (2, 2), (3, 3), (4, 4))
((10, 3), (11, 3), (12, 3))
 . . . X . . . . O O . . .
 . . . X X . . . . . . . O
 . . . X . X . . . . X X X
 . . X . . . X . . . . X .
 . X . . . . . X O . . X .
 X . . . . . . O . . . . .
"""
```

## License
rowfind is licensed under the [MIT License](LICENSE).
