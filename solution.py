assignments = []

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

#Following variable are used through out project to make iterations simple.
rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
#Diagonal started from left top.
left_diagonal = [[rows[i]+cols[i] for i in range(0, len(rows))]]
#Diagonal started from right top.
right_diagonal = [[rows[i]+cols[len(rows) - i - 1] for i in range(0, len(rows))]]
diagonalunits = left_diagonal + right_diagonal
updatedunitlist = row_units + column_units + square_units + left_diagonal + right_diagonal

unitlist = row_units + column_units + square_units
units = dict((s, [u for u in updatedunitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
#print(type(peers['A1']))

def assign_value(values, box, value):
    """
    This function updates your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        box(string): a string with the cell value.

    Returns:
        the values dictionary after assigning updated values. 
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins_elimination(box1, box2, values):
    """
    This function eliminates the individuals characters of naked twins from other cells of the unit.
    Args:
        box1(string): a string with the cell value.
        box2(string): a string with the cell value.
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from unitlist.

    """
    for each_unit in updatedunitlist:
        if box2 in each_unit and box1 in each_unit:
            for each_cell in each_unit:
                if each_cell != box2 and each_cell != box1 and len(values[each_cell]) > 2:
                    nt1, nt2 = values[box1][0], values[box1][1]
                    values[each_cell] = values[each_cell].replace(nt1, '')
                    values[each_cell] = values[each_cell].replace(nt2, '')

    return values

def naked_twins(values):
    """
    
    Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    
    """
    dboxes = list()
    for box in values:
        if len(values[box]) == 2:
            dboxes.append(box)

    #Find all Naked Twins
    naked_twins = list()
    for i in range(0, len(dboxes)):
        for j in range(i+1, len(dboxes)):
            if values[dboxes[i]] == values[dboxes[j]]:
                if dboxes[j] in peers[dboxes[i]]:
                    nt = (dboxes[i], dboxes[j])
                    naked_twins.append(nt)
    
    #Find common peers
    for each in naked_twins:
        box1 = each[0]
        box2 = each[1]
        common_peers = list(peers[box1].intersection(peers[box2]))
        for cell in common_peers:
            #print(values[box1], values[box2], values[cell])
            #Sanity Check. Really don't have any importance to if statement
            if len(values[box1]) == 2 and len(values[box2]) == 2:
                #Elimination of Individual digits
                nt1, nt2 = values[box1][0], values[box1][1]
                if nt1 in values[cell] and len(values[cell]) > 1:
                    values = assign_value(values, cell, values[cell].replace(nt1, ''))
                if nt2 in values[cell] and len(values[cell]) > 1:
                    values = assign_value(values, cell, values[cell].replace(nt2, ''))
            
    return values

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
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    
    """

    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """

    Implements the Elimination strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary after eliminating already assigned values from peers.

    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]

    for solved_val in solved_values:
        digit = values[solved_val]
        peers_solv = peers[solved_val]
        for peer in peers_solv:
            values = assign_value(values, peer, values[peer].replace(digit,''))
    return values
   

def only_choice(values):
    """
    
    Implements only choice strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary after updating only choice values in peers.

    """
    number_of_choices = list()
    for each_unit in updatedunitlist:
        for char in '123456789':
            for cell in each_unit:
                if char in values[cell]:
                    number_of_choices.append(cell)
            if len(number_of_choices) == 1:
                #values[number_of_choices[0]] = char
                values = assign_value(values, number_of_choices[0], char)
            number_of_choices = list()
                
    return values

def reduce_puzzle(values):
    """
    This function reduces puzzle after applying Eliminate and Only Choice strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary after updating only choice values in peers.

    """

    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Eliminate Strategy
        values = eliminate(values)
                    
        # Only Choice Strategy
        values = only_choice(values)

        # Naked Twins
        values = naked_twins(values)
        
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
        

    return values

def search(values):
    """
    Implements the DFS strategy in recursion.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary after checking all possible cell values. 
    """
    values = reduce_puzzle(values)
                
    
    if values is False:
        return False

    #if check_diagonal_sudoku(values) is False:
     #   return False
    if all(len(values[s]) == 1 for s in boxes):
        return values
    
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def check_diagonal_sudoku(values):
    if values is not False:
        ld = [values[s] for s in left_diagonal[0]]
        rd = [values[s] for s in right_diagonal[0]]
        if len(ld) == len(set(ld)) and len(rd) == len(set(rd)):
            return values
        else:
            return False
    else:
        return False

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    #values = check_diagonal_sudoku(values)
    #reduce_puzzle(values)
    return values

if __name__ == '__main__':
    diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        #visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
