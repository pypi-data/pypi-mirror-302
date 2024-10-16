"""
Find points that make an equally spaced row on a 2D plane.
"""


def find_all(coords: tuple[tuple[int, int]] | list[tuple[int, int]],
             lengths: int | tuple[int] | list[int] | None = None,
             steps: int | tuple[int] | list[int] | None = 1) -> tuple[tuple[int, int]]:
    """
    Find all rows of `lengths` points by checking from each point in 4 directions.
    right, top, top-right, and bottom-right. If `lengths` or/and `steps` is None,
    all possible row lengths or/and steps will be tried.
    """
    if not isinstance(coords, tuple | list) or not all(isinstance(x_y, tuple) for x_y in coords):
        raise ValueError("coords should be a tuple/list of tuples [(x1, y1), (x2, y2), ...]")

    if (lengths is not None and not isinstance(lengths, int) and not
       (isinstance(lengths, tuple | list) and all(isinstance(l, int) for l in lengths))):
        raise ValueError("lengths should be an integer, a tuple/list of integers, or None")

    if not lengths:
        lengths = range(2, len(coords) + 1)

    elif isinstance(lengths, int):
        lengths = (lengths,)

    if any(l < 2 for l in lengths):
        raise ValueError("All lengths should be integers greater than 1")

    if (steps is not None and not isinstance(steps, int) and not
       (isinstance(steps, tuple | list) and all(isinstance(s, int) for s in steps))):
        raise ValueError("steps should be an integer, a tuple/list of integers, or None")

    if not steps:
        steps = range(1, len(coords) + 1)

    elif isinstance(steps, int):
        steps = (steps,)

    coords_set = frozenset(coords)
    coords = list(coords_set)
    rows = set()
    walk = ((1, 0), (0, 1), (1, 1), (1, -1))

    # I know the nested loops aren't good practice but
    # they are *marginally* faster than itertools.product
    for x, y in coords:
        for dx, dy in walk:
            for s in steps:
                for l in lengths:
                    if (x + (l - 1) * dx * s, y + (l - 1) * dy * s) not in coords_set:
                        continue

                    row = [(x + i * dx * s, y + i * dy * s) for i in range(l)]
                    if all(point in coords_set for point in row):
                        rows.add(tuple(row))

    return tuple(rows)


def find_unique(coords: tuple[tuple[int, int]] | list[tuple[int, int]],
                min_length: int = 2,
                steps: int | tuple[int] | list[int] | None = 1) -> tuple[tuple[int, int]]:
    """
    Find all unique rows of at least `min_length` points by checking from each
    point in 4 directions. Sub-rows will not be considered as distinct. If `steps`
    is None, all possible steps will be tried.
    """
    if not isinstance(coords, tuple | list) or not all(isinstance(x_y, tuple) for x_y in coords):
        raise ValueError("coords should be a tuple/list of tuples [(x1, y1), (x2, y2), ...]")

    if not isinstance(min_length, int) or min_length < 2:
        raise ValueError("min_length should be an integer greater than 1")

    if (steps is not None and not isinstance(steps, int) and not
       (isinstance(steps, tuple | list) and all(isinstance(s, int) for s in steps))):
        raise ValueError("steps should be an integer, a tuple/list of integers, or None")

    if not steps:
        steps = range(1, len(coords) + 1)

    elif isinstance(steps, int):
        steps = (steps,)

    coords_set = frozenset(coords)
    rows = set()
    walk = ((1, 0), (0, 1), (1, 1), (1, -1))
    visited_pd = {d: set() for d in walk}

    for x, y in coords:
        for idx, (dx, dy) in enumerate(walk):
            visited = visited_pd[(dx, dy)]
            for s in steps:
                if (x, y) in visited:
                    continue

                row = [(x, y)]
                while True:
                    next_point = (row[-1][0] + dx * s, row[-1][1] + dy * s)
                    if next_point not in coords_set:
                        break

                    row.append(next_point)

                if len(row) >= min_length:
                    rows.add(tuple(row))
                    visited.update(row)

    return tuple(rows)


def draw_graph(coords: tuple[tuple[int, int]] | list[tuple[int, int]],
               rows: tuple[tuple[int, int]]) -> str:
    """
    Draw an ASCII graph with the given points. Points that form a row are marked
    with 'X' while the rest are marked with 'O'
    """
    if not isinstance(coords, tuple | list) or not all(isinstance(x_y, tuple) for x_y in coords):
        raise ValueError("coords should be a tuple/list of tuples [(x1, y1), (x2, y2), ...]")

    if not isinstance(rows, tuple) or not all(isinstance(r, tuple) for r in rows):
        raise ValueError("rows should be a tuple of tuples (((x1, y1), (x2, y2)), ...)")

    coords_set = frozenset(coords)
    coords = list(coords_set)
    rows_set = frozenset(coord for row in rows for coord in row)
    min_x, max_x = min(x for x, y in coords), max(x for x, y in coords)
    min_y, max_y = min(y for x, y in coords), max(y for x, y in coords)
    return "\n".join(
        "".join(
            " X" if (x, y) in rows_set else
            " O" if (x, y) in coords_set else
            " ."
            for x in range(min_x, max_x + 1)
        )
        for y in range(max_y, min_y - 1, -1)
    )
