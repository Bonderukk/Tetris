from typing import List, Tuple
import random

Block = List[Tuple[int, int]]

BLOCK_I, BLOCK_J, BLOCK_L, BLOCK_S, BLOCK_Z, BLOCK_T, BLOCK_O = range(7)

LEFT, RIGHT, ROTATE_CW, ROTATE_CCW, DOWN, DROP, QUIT = range(7)

WALL = "##"
SQUARE = "[]"
EMPTY = "  "

Arena = List[List[bool]]


def coords(block_type: int) -> Block:
    if block_type == BLOCK_I:
        return [(0, -1), (0, 0), (0, 1), (0, 2)]
    if block_type == BLOCK_J:
        return [(0, -1), (0, 0), (0, 1), (-1, 1)]
    if block_type == BLOCK_L:
        return [(0, -1), (0, 0), (0, 1), (1, 1)]
    if block_type == BLOCK_S:
        return [(-1, 1), (0, 1), (0, 0), (1, 0)]
    if block_type == BLOCK_Z:
        return [(-1, 0), (0, 0), (0, 1), (1, 1)]
    if block_type == BLOCK_T:
        return [(-1, 0), (0, 0), (0, 1), (1, 0)]
    if block_type == BLOCK_O:
        return [(0, 0), (1, 0), (0, 1), (1, 1)]

    return [(0, 0), (0, 0), (0, 0), (0, 0)]


def find_pivot(block: Block) -> int:
    for point in range(len(block)):
        if block[point] == (0, 0):
            return point


def rotate_cw(coords: Block, anchor: int) -> Block:
    anchor_x, anchor_y = coords[anchor]
    new_block = []
    for point in coords:
        if point != coords[anchor]:
            x, y = point
            x -= anchor_x
            y -= anchor_y
            new_block.append((anchor_x - y, anchor_y + x))
        else:
            new_block.append(coords[anchor])

    return new_block


def rotate_ccw(coords: Block, anchor: int) -> Block:
    anchor_x, anchor_y = coords[anchor]
    new_block = []
    for point in coords:
        if point != coords[anchor]:
            x, y = point
            x -= anchor_x
            y -= anchor_y
            new_block.append((anchor_x + y, anchor_y - x))
        else:
            new_block.append(coords[anchor])
    return new_block


def new_arena(cols: int, rows: int) -> Arena:
    table = []
    row = []

    for e in range(rows):
        for i in range(cols):
            row.append(False)

        table.append(row)
        row = []

    return table


def is_occupied(arena: Arena, x: int, y: int) -> bool:
    n_of_rows = len(arena[0])
    n_of_cols = len(arena)
    pos_x = 0
    pos_y = 0

    for row in arena:
        for point in row:

            if (pos_x, pos_y) == (x, y) and point is True:
                return True
            pos_x += 1

        pos_x = 0
        pos_y += 1

    if 0 <= x < n_of_rows and 0 <= y < n_of_cols:
        return False

    else:
        return True


def set_occupied(arena: Arena, x: int, y: int, occupied: bool) -> None:
    len_row = len(arena[0])
    len_cols = len(arena)

    if 0 <= x < len_row and 0 <= y < len_cols:
        row = arena[y]
        row[x] = occupied


def insert_block(arena: Arena, block: Block) -> bool:
    for point in block:
        x, y = point
        if is_occupied(arena, x, y):
            return False

    for point in block:
        x, y = point
        set_occupied(arena, x, y, True)

    return True


def draw(arena: Arena, score: int) -> None:
    graphic_row = ""
    n_column = 1
    len_row = len(arena[0])

    for row in arena:

        for point in row:
            if point is True:
                graphic_row += SQUARE
            else:
                graphic_row += EMPTY

        print(WALL + graphic_row + WALL)
        graphic_row = ""
        n_column += 1

    print(WALL * (len_row + 2))

    score_len = (len(str(score)) // 2)
    check_even_length = (len(str(score)) % 2)
    # Rest of space znamená že odčítam dĺžku slova Score:, ktorá zaberá 3 EMPTY
    rest_of_space = len_row - 3

    if check_even_length == 0:
        rest_of_space -= score_len
        print(EMPTY + "Score:" + (rest_of_space * EMPTY) + str(score))
    else:
        rest_of_space -= score_len + 1
        print(EMPTY + "Score:" + (rest_of_space * EMPTY)
              + " " + str(score), "\n")


def next_block() -> Block:
    # change this function as you wish
    random_block = random.randint(0, 6)
    coordinates = coords(random_block)
    return coordinates


def align_center(arena: Arena, block: Block) -> Block:
    y_coords = []
    x_coords = []

    for point in block:
        x, y = point
        x_coords.append(x)
        y_coords.append(y)

    min_y = min(y_coords)
    modified_y_coords = []

    for y in y_coords:
        y -= min_y
        modified_y_coords.append(y)

    block_width = abs(min(x_coords)) + abs(max(x_coords)) + 1
    modified_x_coords = []

    columns = len(arena[0])
    possible_new_x = columns // 2 - block_width // 2

    if columns % 2 == 0 and block_width % 2 == 1:
        dist_X_NewX = abs(min(x_coords)) + abs(possible_new_x) - 1

    else:
        dist_X_NewX = abs(min(x_coords)) + abs(possible_new_x)

    for x in x_coords:
        modified_x_coords.append(x + dist_X_NewX)

    res = list(zip(modified_x_coords, modified_y_coords))

    return res


def poll_event() -> int:
    return int(input("Event number (0-6): "))


def movement(arena: Arena, move: int, block: Block, cords: Block) -> Block:
    old_block = block
    new_block = []

    for point in old_block:
        x, y = point
        set_occupied(arena, x, y, False)

    if move == LEFT:
        for point in old_block:
            x, y = point
            if is_occupied(arena, x - 1, y):
                return old_block

            new_block.append((x - 1, y))

    if move == RIGHT:
        for point in old_block:
            x, y = point
            if is_occupied(arena, x + 1, y):
                return old_block

            new_block.append((x + 1, y))

    if move == DOWN:
        for point in old_block:
            x, y = point
            if is_occupied(arena, x, y + 1):
                return old_block

            new_block.append((x, y + 1))

    if move == ROTATE_CW:
        anchor = find_pivot(cords)
        new_block = rotate_cw(old_block, anchor)

        for point in new_block:
            x, y = point
            if is_occupied(arena, x, y):
                return old_block

        return new_block

    if move == ROTATE_CCW:
        anchor = find_pivot(cords)
        new_block = rotate_ccw(old_block, anchor)

        for point in new_block:
            x, y = point
            if is_occupied(arena, x, y):
                return old_block

        return new_block

    if move == DROP:
        while True:
            new_block = []
            for point in old_block:
                x, y = point

                if is_occupied(arena, x, y + 1):
                    return old_block

                set_occupied(arena, x, y + 1, False)
                new_block.append((x, y + 1))

            old_block = new_block

    if move == QUIT:
        quit()

    return new_block


def iter_pos_y(arena: Arena, y):
    pos_x = 0
    pos_y = y - 1

    for row in arena:
        for point in row:

            if is_occupied(arena, pos_x, pos_y):
                set_occupied(arena, pos_x, pos_y, False)
                set_occupied(arena, pos_x, pos_y + 1, True)

            pos_x += 1

        pos_x = 0
        pos_y -= 1
        if pos_y < 0:
            break


def play(arena: Arena) -> int:
    game = ""
    score = 0
    while game != QUIT:

        count_occupied_pos = 0
        pos_x = 0
        pos_y = 0

        curr_row = []
        deleted_rows = 0

        # Check if there is full row
        for row in arena:
            for point in row:
                if is_occupied(arena, pos_x, pos_y):
                    count_occupied_pos += 1

                curr_row.append((pos_x, pos_y))
                pos_x += 1

            if count_occupied_pos == len(arena[0]):
                for point in curr_row:
                    x, y = point
                    set_occupied(arena, x, y, False)

                iter_pos_y(arena, pos_y)
                deleted_rows += 1

            curr_row = []
            count_occupied_pos = 0

            pos_x = 0
            pos_y += 1

        score += deleted_rows ** 2

        new_block = next_block()
        aligned_block = align_center(arena, new_block)

        draw(arena, score)
        insert = insert_block(arena, aligned_block)
        if not insert:
            game = QUIT

        # Move block until it cant
        round = "Go on"
        while round != QUIT:
            draw(arena, score)

            poll = poll_event()

            moved_block = movement(arena, poll, aligned_block, new_block)
            if moved_block == aligned_block and (poll == DOWN or poll == DROP):
                round = QUIT
            insert_block(arena, moved_block)
            aligned_block = moved_block

    return score
