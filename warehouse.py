######################################################################
# This file copyright the Georgia Institute of Technology
#
# Permission is given to students to use or modify this file (only)
# to work on their assignments.
#
# You may NOT publish this file or make it available to others not in
# the course.
#
######################################################################

import math
from heapq import heappush, heappop

# If you see different scores locally and on Gradescope this may be an indication
# that you are uploading a different file than the one you are executing locally.
# If this local ID doesn't match the ID on Gradescope then you uploaded a different file.
OUTPUT_UNIQUE_FILE_ID = False
if OUTPUT_UNIQUE_FILE_ID:
    import hashlib, pathlib

    file_hash = hashlib.md5(pathlib.Path(__file__).read_bytes()).hexdigest()
    print(f'Unique file ID: {file_hash}')


class DeliveryPlanner_PartA:
    """
    Note: All print outs must be conditioned on the debug parameter.

    Required methods in this class are:

      plan_delivery(self, debug = False):
       Stubbed out below.  You may not change the method signature
        as it will be called directly by the autograder but you
        may modify the internals as needed.

      __init__:
        Required to initialize the class.  Signature can NOT be changed.
        Basic template starter code is provided.  You may choose to
        use this starter code or modify and replace it based on
        your own solution.
    """

    def __init__(self, warehouse_viewer, dropzone_location, todo, box_locations):

        self.warehouse_viewer = warehouse_viewer
        self.dropzone_location = dropzone_location
        self.todo = todo
        self.box_locations = box_locations
        self.count = 0

        # list of locations of each box to treat as a wall
        # self.box_as_walls = box_locations
        self.box_as_walls = []

        for key in box_locations.keys():
            self.box_as_walls.append(box_locations.get(key))

        self.direction = {
            (-1, -1): 'move nw',
            (-1, 0): 'move n',
            (-1, 1): 'move ne',
            (0, -1): 'move w',
            (0, 1): 'move e',
            (1, -1): 'move sw',
            (1, 1): 'move se',
            (1, 0): 'move s'
        }

        self.opposite = {
            'move nw': 'move se',
            'move w': 'move e',
            'move sw': 'move ne',
            'move n': 'move s',
            'move s': 'move n',
            'move ne': 'move sw',
            'move se': 'move nw',
            'move e': 'move w'
        }

        self.move_to_coord = {
            'move nw': (-1, -1),
            'move n': (-1, 0),
            'move ne': (-1, 1),
            'move w': (0, -1),
            'move e': (0, 1),
            'move sw': (1, -1),
            'move se': (1, 1),
            'move s': (1, 0)
        }

        # You may use these symbols indicating direction for visual debugging
        # ['^', '<', 'v', '>', '\\', '/', '[', ']']
        # or you may choose to use arrows instead
        # ['🡑', '🡐', '🡓', '🡒',  '🡔', '🡕', '🡖', '🡗']

    def plan_delivery(self, debug=False):
        """
        plan_delivery() is required and will be called by the autograder directly.
        You may not change the function signature for it.
        All print outs must be conditioned on the debug flag.
        """
        moves = []

        start = self.dropzone_location

        while self.count < len(self.todo):
            moves_to_add, goal_loc = self.a_star(start)
            moves += moves_to_add

            rtn_to_drop, curr = self.backtrack(moves_to_add, goal_loc, start)
            moves += rtn_to_drop

            start = curr
            self.count += 1
            
            # upon delivery, remove one box from set of walls
            self.box_as_walls = self.box_as_walls[1:]

        if debug:
            for i in range(len(moves)):
                print(moves[i])

        return moves
    
    def backtrack(self, moves, curr, start):
        # 1. remove last move (always a pick up)
        rev = moves[:-1]

        # 2. if no movement was used to get to a box, move to the box picked up
        if len(rev) == 0 and curr == self.dropzone_location:
            box_loc = self.box_locations[self.todo[self.count]]
            by, bx = box_loc
            cy, cx = curr
            
            dy = by - cy
            dx = bx - cx
            move = self.direction.get((dy, dx))

            curr = box_loc
            
            # drop off box
            drop = 'down {}'.format(self.opposite.get(move)[5:])

            return [move, drop], curr
        # 3. no movement to get to box not on dropzone implies adjacent to dropzone
        elif len(rev) == 0:
            dry, drx = self.dropzone_location
            cy, cx = curr

            dy = dry - cy
            dx = drx - cx
            drop = 'down {}'.format(self.direction.get((dy, dx))[5:])

            return [drop], curr
        else:
            moves.reverse()
            rtn = []

            if start == self.dropzone_location:
                end = len(moves) - 1
            else:
                end = len(moves)
            
            for i in range(1, end):
                adj, _, _ = self.is_drop_adj(curr, self.dropzone_location)
                if adj:
                    break
                
                move = self.opposite.get(moves[i])
                rtn.append(move)
                y, x = curr
                dy, dx = self.move_to_coord.get(move)
                x += dx
                y += dy
                curr = (y, x)

            # added enough moves to be adjacent to dropzone
            dry, drx = self.dropzone_location
            cy, cx = curr

            dy = dry - cy
            dx = drx - cx
            drop = 'down {}'.format(self.direction.get((dy, dx))[5:])
            rtn.append(drop)
            
            return rtn, curr
        
    def is_drop_adj(self, curr, goal):
        cy, cx = curr
        
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    ax = cx + j
                    ay = cy + i
                
                    if (ay, ax) == goal:
                        return True, (cy, cx), (i, j)
        return False, (0, 0), (0, 0)
    
    def dir_to_try(self, count):
        i = 0
        j = 0
        # im sorry for committing this sin
        if count == 0:
            j = -1
        elif count == 1:
            j = 1
        elif count == 2:
            i = -1
        elif count == 3:
            i = 1
        elif count == 4:
            j = -1
            i = -1
        elif count == 5:
            j = 1
            i = -1
        elif count == 6:
            j = -1
            i = 1
        elif count == 7:
            j = 1
            i = 1
            
        return self.direction.get((i, j)), i, j
            
    def get_succ(self, curr, curr_cost):
        y, x = curr
        cost = 0
        rtn = []

        count = 0

        while count < 8:
            move, i, j = self.dir_to_try(count)

            if i == 0 or j == 0:
                cost = 2
            else:
                cost = 3
            
            loc = (y+i, x+j)
            if loc in self.box_as_walls:
                count += 1
                continue
            
            try:
                succ = self.warehouse_viewer[y+i][x+j]
                if succ == '#':
                    count += 1
                    continue

                rtn.append((cost + curr_cost, (y+i, x+j), move))
            except:
                count += 1
                continue
            count += 1
            
        return rtn

    def a_star(self, start):
        nodes = []

        # just marks places we have already been
        visited = []
        visited.append(start)

        # keep track of goal location
        goal_loc = None
        
        # add start to prioq
        heappush(nodes, [0, 0, start])

        # each node has a list of moves used to access it
        actions_by_node = {start: []}

        goals = self.get_goals()
        
        count = 1
        while not len(nodes) == 0:
            node_entry = heappop(nodes)
            total_cost = node_entry[0]
            curr = node_entry[2]

            # print('curr', curr)
            # get list of actions
            actions = actions_by_node.get(curr)

            if curr in goals:
                goal_loc = curr
                goal = self.box_locations[self.todo[self.count]]
                
                lift = 'lift {}'.format(self.todo[self.count])
                temp = actions + [lift]

                actions_by_node.update({curr: temp})
                break
                
            # get successors to continue search
            succs = self.get_succ(curr, total_cost)
            for i in range(len(succs)):
            # for succ in succs:
                succ = succs[i]
                count += 1
                cost, pos, move = succ
                # add to prioq if not visited
                if pos not in visited:
                    h = self.heuristic(pos)
                    cost += h

                    # entry based on, breaks ties by horizontal/vertical movement first:
                    # https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
                    entry = [cost, count, pos]
                    heappush(nodes, entry)

                    # visiting
                    visited.append(pos)

                    # add new move to running list of actions
                    temp = actions + [move]
                    actions_by_node.update({pos: temp})

        # print(actions_by_node.get(goal_loc), goal_loc)
        return actions_by_node.get(goal_loc), goal_loc

    def get_goals(self):
        y, x = self.box_locations[self.todo[self.count]]
        goals = []
        
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    ax = x + j
                    ay = y + i
                    goals.append((ay, ax))
        return goals

    def heuristic(self, curr):
        goals = self.get_goals()
        h_list = [self.heuristic_pick(curr, goals[i]) for i in range(8)]

        # print(h_list)
        return min(h_list)
    
    def heuristic_pick(self, curr, goal):
        y, x = curr
        v, u = goal
        
        dy = abs(y-v)
        dx = abs(x-u)
        
        man = dy + dx
        
        # http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html#a-starx27s-use-of-the-heuristic
        dia = 2 * (man) + (3 - 2 * 2) * min(dy, dx)
        
        return 3*dia
    
class DeliveryPlanner_PartB:
    """
    Note: All print outs must be conditioned on the debug parameter.

    Required methods in this class are:

        generate_policies(self, debug = False):
         Stubbed out below. You may not change the method signature
         as it will be called directly by the autograder but you
         may modify the internals as needed.

        __init__:
         Required to initialize the class.  Signature can NOT be changed.
         Basic template starter code is provided.  You may choose to
         use this starter code or modify and replace it based on
         your own solution.

    The following method is starter code you may use.
    However, it is not required and can be replaced with your
    own method(s).

        _set_initial_state_from(self, warehouse):
         creates structures based on the warehouse map

    """

    def __init__(self, warehouse, warehouse_cost, todo):

        self._set_initial_state_from(warehouse)
        self.warehouse_cost = warehouse_cost
        self.todo = todo

        # You may use these symbols indicating direction for visual debugging
        # ['^', '<', 'v', '>', '\\', '/', '[', ']']
        # or you may choose to use arrows instead
        # ['🡑', '🡐', '🡓', '🡒',  '🡔', '🡕', '🡖', '🡗']

    def _set_initial_state_from(self, warehouse):
        """Set initial state.

        Args:
            warehouse(list(list)): the warehouse map.
        """
        rows = len(warehouse)
        cols = len(warehouse[0])

        self.warehouse_state = [[None for j in range(cols)] for i in range(rows)]
        self.dropzone = None
        self.boxes = dict()

        for i in range(rows):
            for j in range(cols):
                this_square = warehouse[i][j]

                if this_square == '.':
                    self.warehouse_state[i][j] = '.'

                elif this_square == '#':
                    self.warehouse_state[i][j] = '#'

                elif this_square == '@':
                    self.warehouse_state[i][j] = '@'
                    self.dropzone = (i, j)

                else:  # a box
                    box_id = this_square
                    self.warehouse_state[i][j] = box_id
                    self.boxes[box_id] = (i, j)

    def generate_policies(self, debug=False):
        """
        generate_policies() is required and will be called by the autograder directly.
        You may not change the function signature for it.
        All print outs must be conditioned on the debug flag.
        """

        # The following is the hard coded solution to test case 1
        to_box_policy = [['B', 'lift 1', 'move w'],
                  ['lift 1', '-1', 'move nw'],
                  ['move n', 'move nw', 'move n']]

        deliver_policy = [['move e', 'move se', 'move s'],
                  ['move ne', '-1', 'down s'],
                  ['move e', 'down e', 'move n']]

        if debug:
            print("\nTo Box Policy:")
            for i in range(len(to_box_policy)):
                print(to_box_policy[i])

            print("\nDeliver Policy:")
            for i in range(len(deliver_policy)):
                print(deliver_policy[i])

        return (to_box_policy, deliver_policy)

# NOTE: Part C is optional.  It is NOT part of your grade for this project, but you are welcome to attempt it if you wish.
# run the part C testing suite to test your part C code.
class DeliveryPlanner_PartC:
    """
    [Doc string same as part B]
    Note: All print outs must be conditioned on the debug parameter.

    Required methods in this class are:

        generate_policies(self, debug = False):
         Stubbed out below. You may not change the method signature
         as it will be called directly by the autograder but you
         may modify the internals as needed.

        __init__:
         Required to initialize the class.  Signature can NOT be changed.
         Basic template starter code is provided.  You may choose to
         use this starter code or modify and replace it based on
         your own solution.

    The following method is starter code you may use.
    However, it is not required and can be replaced with your
    own method(s).

        _set_initial_state_from(self, warehouse):
         creates structures based on the warehouse map

    """

    def __init__(self, warehouse, warehouse_cost, todo, stochastic_probabilities):

        self._set_initial_state_from(warehouse)
        self.warehouse_cost = warehouse_cost
        self.todo = todo
        self.stochastic_probabilities = stochastic_probabilities

        # You may use these symbols indicating direction for visual debugging
        # ['^', '<', 'v', '>', '\\', '/', '[', ']']
        # or you may choose to use arrows instead
        # ['🡑', '🡐', '🡓', '🡒',  '🡔', '🡕', '🡖', '🡗']

    def _set_initial_state_from(self, warehouse):
        """Set initial state.

        Args:
            warehouse(list(list)): the warehouse map.
        """
        rows = len(warehouse)
        cols = len(warehouse[0])

        self.warehouse_state = [[None for j in range(cols)] for i in range(rows)]
        self.dropzone = None
        self.boxes = dict()

        for i in range(rows):
            for j in range(cols):
                this_square = warehouse[i][j]

                if this_square == '.':
                    self.warehouse_state[i][j] = '.'

                elif this_square == '#':
                    self.warehouse_state[i][j] = '#'

                elif this_square == '@':
                    self.warehouse_state[i][j] = '@'
                    self.dropzone = (i, j)

                else:  # a box
                    box_id = this_square
                    self.warehouse_state[i][j] = box_id
                    self.boxes[box_id] = (i, j)

    def generate_policies(self, debug=False):
        """
        generate_policies() is required and will be called by the autograder directly.
        You may not change the function signature for it.
        All print outs must be conditioned on the debug flag.
        """

        # The following is the hard coded solution to test case 1
        to_box_policy = [
            ['B', 'lift 1', 'move w'],
            ['lift 1', -1, 'move nw'],
            ['move n', 'move nw', 'move n'],
        ]

        to_zone_policy = [
            ['move e', 'move se', 'move s'],
            ['move se', -1, 'down s'],
            ['move e', 'down e', 'move n'],
        ]

        if debug:
            print("\nTo Box Policy:")
            for i in range(len(to_box_policy)):
                print(to_box_policy[i])

            print("\nTo Zone Policy:")
            for i in range(len(to_zone_policy)):
                print(to_zone_policy[i])

        # For debugging purposes you may wish to return values associated with each policy.
        # Replace the default values of None with your grid of values below and turn on the
        # VERBOSE_FLAG in the testing suite.
        to_box_values = None
        to_zone_values = None
        return (to_box_policy, to_zone_policy, to_box_values, to_zone_values)


def who_am_i():
    # Please specify your GT login ID in the whoami variable (ex: jsmith224).
    whoami = 'rjones402'
    return whoami


if __name__ == "__main__":
    """
    You may execute this file to develop and test the search algorithm prior to running
    the delivery planner in the testing suite.  Copy any test cases from the
    testing suite or make up your own.
    Run command:  python warehouse.py
    """

    # Test code in here will NOT be called by the autograder
    # This section is just a provided as a convenience to help in your development/debugging process

    # Testing for Part A
    print('\n~~~ Testing for part A: ~~~\n')

    from testing_suite_partA import wrap_warehouse_object, Counter

    # test case data starts here
    # testcase 1
    warehouse = [
        '######',
        '#....#',
        '#.1#2#',
        '#..#.#',
        '#...@#',
        '######',
    ]
    todo = list('12')
    benchmark_cost = 23
    viewed_cell_count_threshold = 20
    dropzone = (4,4)
    box_locations = {
        '1': (2,2),
        '2': (2,4),
    }
    # test case data ends here

    viewed_cells = Counter()
    warehouse_access = wrap_warehouse_object(warehouse, viewed_cells)
    partA = DeliveryPlanner_PartA(warehouse_access, dropzone, todo, box_locations)
    partA.plan_delivery(debug=True)
    # Note that the viewed cells for the hard coded solution provided
    # in the initial template code will be 0 because no actual search
    # process took place that accessed the warehouse
    print('Viewed Cells:', len(viewed_cells))
    print('Viewed Cell Count Threshold:', viewed_cell_count_threshold)

    # Testing for Part B
    # testcase 1
    print('\n~~~ Testing for part B: ~~~')
    warehouse = ['1..',
                 '.#.',
                 '..@']

    warehouse_cost = [[3, 5, 2],
                      [10, math.inf, 2],
                      [2, 10, 2]]

    todo = ['1']

    partB = DeliveryPlanner_PartB(warehouse, warehouse_cost, todo)
    partB.generate_policies(debug=True)

    # Testing for Part C
    # testcase 1
    print('\n~~~ Testing for part C: ~~~')
    warehouse = ['1..',
                 '.#.',
                 '..@']

    warehouse_cost = [[13, 5, 6],
                      [10, math.inf, 2],
                      [2, 11, 2]]

    todo = ['1']

    stochastic_probabilities = {
        'as_intended': .70,
        'slanted': .1,
        'sideways': .05,
    }

    partC = DeliveryPlanner_PartC(warehouse, warehouse_cost, todo, stochastic_probabilities)
    partC.generate_policies(debug=True)
