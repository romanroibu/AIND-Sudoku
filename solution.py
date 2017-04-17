assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def remove_value(values, box, remove_value):
    new_value = values[box]

    for char in remove_value:
        new_value = new_value.replace(char, '')

    return assign_value(values, box, new_value)

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [ a + b for a in A for b in B ]

ROWS  = 'ABCDEFGHI'
COLS  = '123456789'
BOXES = cross(ROWS, COLS)

ROW_UNITS = [ cross(r, COLS) for r in ROWS ]
COL_UNITS = [ cross(ROWS, c) for c in COLS ]
SQUARE_UNITS = [ cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789') ]

DIAGONAL_UNIT1 = [ r + c for r, c in zip(ROWS, COLS) ]
DIAGONAL_UNIT2 = [ r + c for r, c in zip(ROWS, reversed(COLS)) ]
DIAGONAL_UNITS = [ DIAGONAL_UNIT1, DIAGONAL_UNIT2 ]

UNIT_LIST = ROW_UNITS + COL_UNITS + SQUARE_UNITS + DIAGONAL_UNITS
UNITS = dict( (box, [ unit for unit in UNIT_LIST if box in unit ]) for box in BOXES)
PEERS = dict( (box, set(sum(UNITS[box],[])) - set([box])) for box in BOXES)

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = [ cell if cell != '.' else '123456789' for cell in grid ]

    return dict(zip(BOXES, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max( len(values[box]) for box in BOXES )

    def printable_row(row):
        digits = [ values[ row + col ].center(width) for col in COLS ]
        digits.insert(+3, '|') # Add first separator
        digits.insert(-3, '|') # Add last  separator
        return ''.join(digits)

    def horizontal_separator():
        item   = '-' * width
        group  = item * 3
        groups = [ group ] * 3
        return '+'.join(groups)

    rows = list(map(printable_row, ROWS))
    rows.insert(+3, horizontal_separator()) # Add first separator
    rows.insert(-3, horizontal_separator()) # Add last  separator

    board = "\n".join(rows)
    print(board)

def eliminate(values):
    pass

def only_choice(values):
    pass

def reduce_puzzle(values):
    halt = False

    # Function for counting boxes with `value_count` number of values
    def count_boxes(values, value_count=1):
        return len([ box for box, value in values.items() if len(value) == value_count ])

    while not halt:
        # Check how many boxes have a determined value
        solved_values_before = count_boxes(values)

        # TODO: Enforce constarints here...

        # Check how many boxes have a determined value, to compare
        solved_values_after = count_boxes(values)

        # If no new values were added, stop the loop
        halt = solved_values_before == solved_values_after

        # Sanity check, return False if there is a box with zero available values
        if count_boxes(values, value_count=0):
            return False

    return values

def search(values):
    pass

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
