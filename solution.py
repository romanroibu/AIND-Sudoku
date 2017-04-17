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
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the value eliminated from peers.
    """

    # Get a list of all solved boxes and their values
    solved_boxes = [ (box, value) for box, value in values.items() if len(value) == 1 ]

    # For every solved box
    for box, value in solved_boxes:
        # Remove the box's value from every peer of the box
        for peer in PEERS[box]:
            values = remove_value(values, peer, value)

    return values

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

        # Use the Eliminate Strategy
        values = eliminate(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = count_boxes(values)

        # If no new values were added, stop the loop
        halt = solved_values_before == solved_values_after

        # Sanity check, return False if there is a box with zero available values
        if count_boxes(values, value_count=0):
            return False

    return values

def search(values):
    """Using depth-first search and propagation, create a search tree and solve the sudoku.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the naked twins eliminated from PEERS.
    """

    # Reduce the puzzle the search space by enforcing constraints
    values = reduce_puzzle(values)

    # If the solution is invalid, return False
    if values is False:
        return False

    # If all boxes are solved, return the values
    if all(len(values[box]) == 1 for box in BOXES):
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    unsolved_values = [ item for item in values.items() if len(item[1]) > 1 ]
    box, choices = min(unsolved_values, key=lambda item: len(item[1]))

    # For every possibile value of box
    for value in choices:
        # Create a new sudoku game by picking that value for the box
        new_values = values.copy()
        new_values[box] = value

        # Recursively search the game with picked value
        solution = search(new_values)

        # If picked value yelds a solution
        # Return that solution
        if solution:
            return solution

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    # Parse grind string into a sudoku grid dictionary representation
    sudoku = grid_values(grid)

    # Solve the sudoku by searching for a solution
    solution = search(sudoku)

    return solution

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
