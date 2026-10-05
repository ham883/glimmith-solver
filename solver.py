
puzzle_data = {
    'board':[
        ['..','..','..','..','..','..','..','..','..','..','..','..','..','..','..','..','..','..','..'],
        ['..','..','..','##','..','##','..','##','..','..','..','##','..','##','..','##','..','..','..'],
        ['..','..','..','..','..','..','..','..','..','..','..','..','..','..','..','..','..','..','..'],
        ['..','##','..','##','..','P^','..','##','..','##','..','##','..','##','..','##','..','##','..'],
        ['..','..','..','..','..','..','..','..','W1','..','..','..','W2','..','..','..','..','..','..'],
        ['..','##','..','##','..','##','..','##','..','##','..','##','..','##','..','P3','..','##','..'],
        ['..','..','..','..','W1','..','..','..','..','..','..','..','..','..','..','..','..','..','..'],
        ['..','##','..','##','..','##','..','P=','..','##','..','P1','..','##','..','##','..','##','..'],
        ['..','..','..','..','..','..','..','..','..','..','..','..','..','..','W3','..','..','..','..'],
        ['..','..','..','##','..','##','..','##','..','..','..','##','..','##','..','##','..','..','..'],
        ['..','..','..','..','W2','..','..','..','..','..','..','..','..','..','..','..','..','..','..'],
        ['..','##','..','##','..','##','..','P3','..','##','..','P^','..','##','..','##','..','##','..'],
        ['..','..','..','..','..','..','..','..','..','..','..','..','..','..','W4','..','..','..','..'],
        ['..','##','..','P1','..','##','..','##','..','##','..','##','..','##','..','##','..','##','..'],
        ['..','..','..','..','..','..','W2','..','..','..','W4','..','..','..','..','..','..','..','..'],
        ['..','##','..','##','..','##','..','##','..','##','..','##','..','P3','..','##','..','##','..'],
        ['..','..','..','..','..','..','..','..','..','..','..','..','..','..','..','..','..','..','..'],
        ['..','..','..','##','..','##','..','##','..','..','..','##','..','##','..','##','..','..','..'],
        ['..','..','..','..','..','..','..','..','..','..','..','..','..','..','..','..','..','..','..'],
    ],

    'polyominoes':{},

    'polyomino shortcuts':{
        'add tetrominoes to shape bank':False,
        'add tetrominoes to soft bank':False,
        'add pentominoes to shape bank':False,
        'add pentominoes to soft bank':False
    },

    'shape bank':[],

    'global rules':{
        'mingle shape':     False,
        'size separation':  False,
        'mismatch':         False,
        'match':            False,
        'solitude':         False,
        'boxy':             False,
        'non-boxy':         False,
        'bricky':           False,
        'loopy':            False,
        'precision':        6,
        'minimum':          False,
        'maximum':          False
    },
    
    'optimizations':{
        'num regions upper bound':False,
        'two colorable':False,
        'soft bank':[]
    }
}

solver_settings = {
    'max solutions limit':10, # The solver will find this many solutions (if they exist) and then stop. Set this to False to disable the limit. 
    'pretty print solution':True, # If True the solver outputs the solution using unicode box drawing characters. If False the solver outputs which region number each cell belongs to. 
    'verbose':True, # If False disables all output except the solution itself.
    'show solution':True
}





##########   END OF USER INPUT   ##########
##########    START OF SOLVER    ##########





from pysat.card import CNF, CardEnc
from pysat.formula import IDPool
from pysat.solvers import Solver as SATSolver
import time
import re
import math

transformation_matrices = [
    [
        [1,0], # Identity
        [0,1]
    ],
    [
        [0,-1], # 90 ccw rotation
        [1,0]
    ],
    [
        [-1,0], # 180 rotation
        [0,-1]
    ],
    [
        [0,1], # 90 cw rotation
        [-1,0]
    ],
    [
        [1,0], # Vertical reflection
        [0,-1]
    ],
    [
        [-1,0], # Horizontal reflection
        [0,1]
    ],
    [
        [0,1], # Reflection over a diagonal line
        [1,0]
    ],
    [
        [0,-1], # Reflection over the other diagonal line
        [-1,0]
    ]
]

polyomino_table = [
    [
        [[1]]
    ],
    [

        [[1,1]]
    ],
    [
        [[1,1,1]],
        [[1,1],[1,0]]
    ],
    [
        [[1,1,1,1]],
        [[1,1],[1,1]],
        [[1,1,1],[0,1,0]],
        [[0,1,1],[1,1,0]],
        [[1,0,0],[1,1,1]]
    ],
    [
        [[1,1,1,1,1]],
        [[0,1,1],[1,1,0],[0,1,0]],
        [[1,0],[1,0],[1,0],[1,1]],
        [[0,1],[1,1],[1,0],[1,0]],
        [[1,0],[1,1],[1,1]],
        [[1,1,1],[0,1,0],[0,1,0]],
        [[1,0,1],[1,1,1]],
        [[1,0,0],[1,0,0],[1,1,1]],
        [[1,0,0],[1,1,0],[0,1,1]],
        [[0,1,0],[1,1,1],[0,1,0]],
        [[0,1],[1,1],[0,1],[0,1]],
        [[1,1,0],[0,1,0],[0,1,1]]
    ],
    [
        [[1,1,1,1,1,1]],
        [[1,1],[1,0],[1,0],[1,0],[1,0]],
        [[1,0],[1,1],[1,0],[1,0],[1,0]],
        [[1,0],[1,0],[1,1],[1,0],[1,0]],
        [[0,1],[1,1],[1,0],[1,0],[1,0]],
        [[1,1],[1,1],[1,0],[1,0]],
        [[1,1],[1,0],[1,1],[1,0]],
        [[1,1],[1,0],[1,0],[1,1]],
        [[1,0],[1,1],[1,1],[1,0]],
        [[1,1,1],[1,0,0],[1,0,0],[1,0,0]],
        [[1,0,0],[1,1,1],[1,0,0],[1,0,0]],
        [[1,1,1],[0,1,0],[0,1,0],[0,1,0]],
        [[0,1,1],[1,1,0],[0,1,0],[0,1,0]],
        [[0,1,1],[0,1,0],[1,1,0],[0,1,0]],
        [[0,1,1],[0,1,0],[0,1,0],[1,1,0]],
        [[0,1,0],[0,1,1],[1,1,0],[0,1,0]],
        [[0,1,0],[1,1,1],[0,1,0],[0,1,0]],
        [[0,1,0],[1,1,1],[1,0,0],[1,0,0]],
        [[0,1],[1,1],[1,0],[1,1]],
        [[0,1],[0,1],[1,1],[1,0],[1,0]],
        [[0,1],[1,1],[1,1],[1,0]],
        [[1,1],[1,1],[1,1]],
        [[0,0,1],[1,1,1],[0,1,0],[0,1,0]],
        [[1,1,1],[0,1,1],[0,1,0]],
        [[0,0,1],[0,1,1],[1,1,0],[0,1,0]],
        [[0,0,1],[1,1,1],[1,0,0],[1,0,0]],
        [[0,1,1],[1,1,0],[1,0,0],[1,0,0]],
        [[1,1,1],[1,0,1],[1,0,0]],
        [[1,0,1],[1,1,1],[1,0,0]],
        [[1,0,1],[1,1,1],[0,1,0]],
        [[0,1,1],[0,1,0],[1,1,0],[1,0,0]],
        [[1,0,0],[1,1,0],[1,1,1]],
        [[0,1,0],[1,1,1],[1,1,0]],
        [[0,0,1],[1,1,1],[1,1,0]],
        [[0,0,1],[0,1,1],[1,1,0],[1,0,0]]
    ]
]


class BadPuzzleError(Exception):
    pass

class TotalizerNode:
    def __init__(self, name, cnf, vpool, TRUE, FALSE, left=None, right=None, cnf_vars=None, cnf_prefix=None):
        self.name = name
        self.left = left
        self.right = right
        
        if cnf_vars is None:
            self.num_vars = left.num_vars + right.num_vars
            if cnf_prefix is None:
                self.cnf_vars = [TRUE] + [vpool.id() for i in range(self.num_vars)] + [FALSE]
            else:
                self.cnf_vars = [TRUE] + [vpool.id(cnf_prefix + f"_{i+1}") for i in range(self.num_vars)] + [FALSE]
        else:
            self.cnf_vars = [TRUE] + cnf_vars + [FALSE]
            self.num_vars = len(cnf_vars) # This isn't self.cnf_vars because num_vars shouldn't count the true/false vars on the ends
        
    def __str__(self):
        return f"Node {self.name}"

def rotate_cw(poly):
    return [[poly[len(poly)-1-a][b] for a in range(len(poly))] for b in range(len(poly[0]))]

def mirror(poly):
    return [poly[len(poly)-1-r] for r in range(len(poly))]

def coordinate_add(tuple1, tuple2):
    result = []
    for t in range(len(tuple1)):
        result.append(tuple1[t] + tuple2[t])

    return tuple(result)

def get_orientations(poly):
    orient = []
    for _ in range(4):
        if poly not in orient:
            orient.append(poly)

        m = mirror(poly)
        if m not in orient:
            orient.append(m)

        poly = rotate_cw(poly)

    return orient

def get_base_edge_coords(poly):
    padded = []
    padded.append([0]*(len(poly[0])+2))
    for row in poly:
        padded.append([0] + row + [0])
    padded.append([0]*(len(poly[0])+2))

    internal_edges = []
    perimeter_edges = []
    for r in range(len(padded)-1):
        for c in range(len(padded[0])-1):
            for n in [(1,0), (0,1)]:
                r2 = r + n[0]
                c2 = c + n[1]
                first = padded[r][c]
                second = padded[r2][c2]
                if first + second == 1:
                    perimeter_edges.append((r-1,c-1,r2-1,c2-1))

                if first + second == 2:
                    internal_edges.append((r-1,c-1,r2-1,c2-1))

    return {'internal':internal_edges, 'perimeter':perimeter_edges}

def normalize(region):
    min_r = min(r for r,c in region)
    min_c = min(c for r,c in region)

    return {(r - min_r, c - min_c) for r,c in region}

def regions_have_same_shape(region1, region2):
    if len(region1) != len(region2):
        return False

    target = normalize(region2)

    for matrix in transformation_matrices:
        W,X = matrix[0]
        Y,Z = matrix[1]

        transformed = {(W*r + X*c, Y*r + Z*c) for r,c in region1}

        if normalize(transformed) == target:
            return True

    return False

def adjacent(region1, region2):
    for r,c in region1:
        if (r+1,c) in region2: return True
        if (r-1,c) in region2: return True
        if (r,c+1) in region2: return True
        if (r,c-1) in region2: return True

    return False

def get_divisors(n):
    divisors = []
    for i in range(1, math.floor(math.sqrt(n)) + 1):
        if n % i == 0:
            divisors.append(i)
            other = n//i
            if i != other:
                divisors.append(other)

    return divisors

class PuzzleEncoding():
    def __init__(self, puzzle_data, verbose):
        self.board = puzzle_data['board']
        self.polyominoes = puzzle_data['polyominoes']
        self.polyomino_shortcuts = puzzle_data['polyomino shortcuts']
        self.shape_bank_names = puzzle_data['shape bank']
        self.shape_bank_data = []
        self.soft_bank_names = puzzle_data['optimizations']['soft bank']
        self.soft_bank_data = []
        self.verbose = verbose
        self.global_rules = puzzle_data['global rules']
        self.optimizations = puzzle_data['optimizations']
        self.num_regions_upper_bound = puzzle_data['optimizations']['num regions upper bound']
        self.area_upper_bound = puzzle_data['global rules']['maximum']
        self.used_polyominoes = {}
        
        self.cnf = CNF()
        self.vpool = IDPool()
        self.R = len(puzzle_data['board'])//2
        self.C = len(puzzle_data['board'][0])//2
        self.cell_coords = [(r,c) for r in range(self.R) for c in range(self.C) if self.board[2*r+1][2*c+1] != '..']
        self.total_area = len(self.cell_coords)
        self.area_totalizer_roots = []
        self.bank_index_count_totalizer_roots = []
        self.TRUE = self.vpool.id("TRUE")
        self.FALSE = self.vpool.id("FALSE")
        self.cnf.append([self.TRUE])
        self.cnf.append([-self.FALSE])
        
        self.verify_and_process_puzzle()
        self.do_polyomino_shortcuts()
        self.check_solver_support()
        
        self.auto_fill_shape_bank()
        self.calc_upper_bounds()

        self.print_warnings()

        if self.verbose:
            print("Building CNF...")

        self.enforce_shape_bank()
        self.enforce_soft_bank()
        self.build_encoding()

    def print_warnings(self):
        # mismatch/mingle without shape/soft bank uses a lot of ram and takes a long time
        if self.global_rules['mismatch'] and len(self.shape_bank_data) == 0 and len(self.soft_bank_data) == 0:
            print()
            print("Warning!")
            print("Solver may use significant RAM. Ensure your system has enough available.")
            print("Mismatch without shape bank or soft bank is incredibly difficult.")
            print("RAM usage and solve times can be reduced by adding a shape or soft bank if possible.")
            print()

        if self.global_rules['mingle shape'] and len(self.shape_bank_data) == 0 and len(self.soft_bank_data) == 0:
            print()
            print("Warning!")
            print("Solver may use significant RAM. Ensure your system has enough available.")
            print("Mingle shape without shape bank or soft bank is incredibly difficult.")
            print("RAM usage and solve times can be reduced by adding a shape or soft bank if possible.")
            print()

        if self.num_regions_upper_bound >= 60 or self.area_upper_bound >= 90:
            print()
            print("Warning!")
            print("Solver may use significant RAM. Ensure your system has enough available.")
            print("This puzzle is very large. Consider specifying smaller values for num_regions_upper_bound and area_upper_bound if possible.")
            print()

    def check_solver_support(self):
        if len(self.soft_bank_data) > 0:
            if self.global_rules['mingle shape']:
                raise BadPuzzleError("Solver does not support mingle shape and soft bank")

            if self.contains_gemini:
                raise BadPuzzleError("Solver does not support gemini and soft bank")

            if self.contains_delta:
                raise BadPuzzleError("Solver does not support delta and soft bank")
    
    def do_polyomino_shortcuts(self):
        if self.polyomino_shortcuts['add tetrominoes to shape bank']:
            self.shape_bank_names += ['Qshortcut4i', 'Qshortcut4o', 'Qshortcut4t', 'Qshortcut4s', 'Qshortcut4l']
            self.shape_bank_data += polyomino_table[3]

        if self.polyomino_shortcuts['add tetrominoes to soft bank']:
            self.soft_bank_names += ['Qshortcut4i', 'Qshortcut4o', 'Qshortcut4t', 'Qshortcut4s', 'Qshortcut4l']
            self.soft_bank_data += polyomino_table[3]

        if self.polyomino_shortcuts['add pentominoes to shape bank']:
            self.shape_bank_names += ['Qshortcut5i', 'Qshortcut5f', 'Qshortcut5l', 'Qshortcut5n',
                                      'Qshortcut5p', 'Qshortcut5t', 'Qshortcut5u', 'Qshortcut5v',
                                      'Qshortcut5w', 'Qshortcut5x', 'Qshortcut5y', 'Qshortcut5z']
            self.shape_bank_data += polyomino_table[4]

        if self.polyomino_shortcuts['add pentominoes to soft bank']:
            self.soft_bank_names += ['Qshortcut5i', 'Qshortcut5f', 'Qshortcut5l', 'Qshortcut5n',
                                     'Qshortcut5p', 'Qshortcut5t', 'Qshortcut5u', 'Qshortcut5v',
                                     'Qshortcut5w', 'Qshortcut5x', 'Qshortcut5y', 'Qshortcut5z']
            self.soft_bank_data += polyomino_table[4]

    def verify_and_process_puzzle(self):
        # We check that all symbols are defined and appear in the correct places

        def check_at_cell(i,j,symbol):
            if i%2 == 0 or j%2 == 0:
                raise BadPuzzleError(f"Symbol {symbol} at index {i},{j} must appear at a cell but is at an edge or vertex.")

        def check_at_edge(i,j,symbol):
            if i%2 == j%2:
                raise BadPuzzleError(f"Symbol {symbol} at index {i},{j} must appear at an edge but is at a cell or vertex.")

        def check_at_vertex(i,j,symbol):
            if i%2 == 1 or j%2 == 1:
                raise BadPuzzleError(f"Symbol {symbol} at index {i},{j} must appear at a vertex but is at a cell or edge.")
            
        self.given_edge_coords = []
        self.contains_rose_windows = False
        self.contains_gemini = False
        self.contains_delta = False
        self.rose_colors = ['red', 'blue', 'yellow', 'green', 'purple']
        self.rose_color_letters = [color[0] for color in self.rose_colors]
        self.rose_coords = [[] for _ in range(len(self.rose_colors))]
        self.polyomino_coords = []
        self.all_polyomino_positions = []
        self.compass_coords = []
        self.gemini_coords = []
        self.delta_coords = []
        self.difference_coords = []
        self.area_number_coords = []
        self.palisade_coords = []
        self.inequality_coords = []
        self.watchtower_coords = []
        self.total_num_symbols = 0
        
        compass_counter = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                symbol = self.board[i][j]
                r = i//2
                c = j//2
                r0 = r - (i%2==0)
                c0 = c - (i%2==1)
                if symbol[0] not in ['.', '#', '-', '|']:
                    self.total_num_symbols += 1
                    
                match symbol[0]:
                    case '.':
                        continue

                    case '#':
                        check_at_cell(i,j,symbol)

                    case 'R':
                        check_at_cell(i,j,symbol)
                        self.contains_rose_windows = True
                        try:
                            color_index = self.rose_color_letters.index(symbol[1])
                        except:
                            raise BadPuzzleError(f"Unknown rose window {symbol} at index {i},{j}")
                        self.rose_coords[color_index].append((r,c))

                    case 'C':
                        check_at_cell(i,j,symbol)
                        for char in symbol[1:]:
                            if char.lower() not in ['c','n','e','s','w','0','1','2','3','4','5','6','7','8','9']:
                                raise BadPuzzleError(f"Unknown compass {symbol} at index {i},{j}")
                            
                        directions = [(d, int(n)) for d, n in re.findall(r'([nesw])(\d+)', symbol.lower())]
                        for pair1 in directions:
                            for pair2 in directions:
                                if pair1[0] == pair2[0] and pair1[1] != pair2[1]:
                                    # Two instances of the same direction but different numbers. There are trivially no solutions; this is probably a typo from the user
                                    raise BadPuzzleError(f"Unsatisfiable compass {symbol}. Direction {pair1[0]} is repeated with different values.")
                                
                        self.compass_coords.append((r,c,directions,compass_counter))
                        compass_counter += 1

                        

                    case 'A':
                        check_at_cell(i,j,symbol)
                        try:
                            value = int(symbol[1:])
                        except:
                            raise BadPuzzleError(f"Unknown area number {symbol} at index {i},{j}")
                        self.area_number_coords.append((r,c,value))

                    case 'P':
                        check_at_cell(i,j,symbol)
                        if symbol[1] == '2':
                            raise BadPuzzleError(f"Palisade P2 is ambiguous. Use P= or P^")
                        if symbol[1] not in ['0', '1', '=', '^', '3', '4']:
                            raise BadPuzzleError(f"Unknown palisade {symbol} at index {i},{j}")
                        self.palisade_coords.append((r,c,symbol[1]))

                    case 'Q':
                        check_at_cell(i,j,symbol)
                        if symbol not in self.polyominoes:
                            raise BadPuzzleError(f"Polyomino {symbol} is undefined")
                        
                        self.polyomino_coords.append((r,c,self.polyominoes[symbol]))
                        self.all_polyomino_positions.append([])
                        self.used_polyominoes[symbol] = True
                        
                    
                    case 'D':
                        check_at_edge(i,j,symbol)
                        if symbol[1] == 'e':
                            self.delta_coords.append((r0,c0,r,c))
                            self.contains_delta = True

                        else:
                            try:
                                value = int(symbol[1:])
                            except:
                                raise BadPuzzleError(f"Unknown difference {symbol} at index {i},{j}")
                            self.difference_coords.append((r0,c0,r,c,value))
                            
                    case '-' | '|':
                        check_at_edge(i,j,symbol)    
                        self.given_edge_coords.append((r0,c0,r,c))

                    case 'G':
                        check_at_edge(i,j,symbol)
                        self.contains_gemini = True
                        self.gemini_coords.append((r0,c0,r,c))

                    case 'I':
                        check_at_edge(i,j,symbol)
                        if symbol[1] not in ['>','<', 'v', '^']:
                            raise BadPuzzleError(f"Unknown inequality {symbol} at index {i},{j}")
                        self.inequality_coords.append((r0,c0,r,c,symbol[1]))
                        
                    case 'W':
                        check_at_vertex(i,j,symbol)
                        if symbol[1] not in ['1', '2', '3', '4']:
                            raise BadPuzzleError(f"Unknown watchtower {symbol} at index {i},{j}")
                        self.watchtower_coords.append((i,j,symbol[1]))

                    case _:
                        raise BadPuzzleError(f"Unknown symbol {symbol} at index {i},{j}")

        for name in self.shape_bank_names:
            if name not in self.polyominoes:
                raise BadPuzzleError(f"Undefined polyomino {name} in shape bank")
            self.shape_bank_data.append(self.polyominoes[name])
            self.used_polyominoes[name] = True

        for name in self.soft_bank_names:
            if name not in self.polyominoes:
                raise BadPuzzleError(f"Undefined polyomino {name} in soft bank")
            self.soft_bank_data.append(self.polyominoes[name])
            self.used_polyominoes[name] = True
            
        for poly in self.polyominoes:
            if poly not in self.used_polyominoes and self.verbose:
                print(f"Note: Unused polyomino {poly}")

    def box_fits_in_puzzle(self,poly):
        for r in range(self.R):
            for c in range(self.C):
                fits_here = True
                for i in range(len(poly)):
                    for j in range(len(poly[0])):
                        if not self.is_a_cell(r+i, c+j):
                            fits_here = False
                            break

                    if fits_here == False:
                        break

                if fits_here == True:
                    return True

        return False
                    
    def auto_fill_shape_bank(self):
        # Boxy is actually just a shape bank
        if self.global_rules['boxy']:
            if len(self.shape_bank_data) > 0:
                raise BadPuzzleError("Solver does not support boxy and shape bank simultaneously")

            if len(self.soft_bank_data) > 0:
                raise BadPuzzleError("Solver does not support boxy and soft bank simultaneously")

            for r in range(1,self.R+1):
                for c in range(1,self.C+1):
                    poly = [[1]*c for _ in range(r)]
                    if self.box_fits_in_puzzle(poly):
                        self.shape_bank_data.append(poly)

            self.area_upper_bound = self.total_area

        # If the puzzle only uses small polyominoes we can pre-compute all of them in a shape bank
        prec = self.global_rules['precision']
        mini = self.global_rules['minimum']
        maxi = self.global_rules['maximum']
        area_range = [max(1, mini), 0]
        if 1 <= prec and prec <= 6:
            area_range[0] = prec
            area_range[1] = prec

        if 1 <= maxi and maxi <= 6:
            area_range[1] = maxi

        if area_range[1] <= 6 and self.global_rules['boxy'] == False and len(self.soft_bank_data) == 0 and len(self.shape_bank_data) == 0:
            for i in range(area_range[0], area_range[1]+1):
                for poly in polyomino_table[i-1]:
                    self.shape_bank_data.append(poly)
                    
                    
                                    
    def enforce_shape_bank(self):
        if len(self.shape_bank_data) > 0:
            shapes_covering_cell = [[[[] for _ in range(8*len(self.shape_bank_data))] for _ in range(self.C)] for _ in range(self.R)]
            for i in range(len(self.shape_bank_data)):
                poly = self.shape_bank_data[i]
                    
                for orient in get_orientations(poly):
                    for r in range(self.R):
                        for c in range(self.C):
                            result = self.make_var_for_polyomino_placement(r,c,orient)
                            if result is not None:
                                for r2,c2 in result['occupied_cells']:
                                    shapes_covering_cell[r2][c2][i].append(result['var'])
                                
            for r,c in self.cell_coords:
                # Enforce shape bank: every cell gets covered by at least one option
                flattened = []
                for option in shapes_covering_cell[r][c]:
                    flattened += option
                        
                if len(flattened) == 0:
                    raise BadPuzzleError(f"Cell (r,c)=({r},{c}) cannot be covered by anything in the shape bank; there are no solutions.")                    
                
                self.cnf.extend(CardEnc.atleast(lits=flattened, bound=1, vpool=self.vpool))
                # Track which shape is chosen to cover each cell
                # cell_bank_index(r,c,i) <=> shapes_covering_cell[r][c][i][0] or shapes_covering_cell[r][c][i][1] or ...
                for i in range(len(shapes_covering_cell[r][c])):
                    self.cnf.append([-self.cell_bank_index(r,c,i)] + shapes_covering_cell[r][c][i])

                    for n in range(len(shapes_covering_cell[r][c][i])):
                        self.cnf.append([-shapes_covering_cell[r][c][i][n], self.cell_bank_index(r,c,i)])
                
                # Once we know which shape in the bank covers a cell, we instantly know all values of cell_area_at_least
                # if cell_bank_index(r,c,i) then [cell_area_at_least(r,c,poly_area) and -cell_area_at_least(r,c,poly_area+1)]
                for i in range(len(self.shape_bank_data)):
                    poly = self.shape_bank_data[i]
                    poly_area = sum([sum(row) for row in poly])
                    self.cnf.append([-self.cell_bank_index(r,c,i), self.cell_area_at_least(r,c,poly_area)])
                    self.cnf.append([-self.cell_bank_index(r,c,i), -self.cell_area_at_least(r,c,poly_area+1)])

    def belongs_to_soft_bank(self, r, c):
        return self.vpool.id(f"belongs_to_soft_bank_{r}_{c}")
                
    def enforce_soft_bank(self):
        if len(self.soft_bank_data) > 0:
            if len(self.shape_bank_data) > 0:
                raise BadPuzzleError("Shape bank and soft bank are mutually exclusive")

            shapes_covering_cell = [[[[] for _ in range(8*len(self.soft_bank_data))] for _ in range(self.C)] for _ in range(self.R)]
            for i in range(len(self.soft_bank_data)):
                poly = self.soft_bank_data[i]
                    
                for orient in get_orientations(poly):
                    for r in range(self.R):
                        for c in range(self.C):
                            result = self.make_var_for_polyomino_placement(r,c,orient)
                            if result is not None:
                                for r2,c2 in result['occupied_cells']:
                                    shapes_covering_cell[r2][c2][i].append(result['var'])
                                
            for r,c in self.cell_coords:
                # Define belongs_to_soft_bank
                flattened = []
                for option in shapes_covering_cell[r][c]:
                    flattened += option
                        
                if len(flattened) == 0:
                    # This cell can't be covered by anything in the soft bank. That is ok.
                    self.cnf.append([-self.belongs_to_soft_bank(r,c)])
                    continue

                # belongs_to_soft_bank(r,c) <=> atleastone(flattened)
                self.cnf.append([-self.belongs_to_soft_bank(r,c)] + flattened)
                for v in flattened:
                    self.cnf.append([-v, self.belongs_to_soft_bank(r,c)])
                
                # Track which shape is chosen to cover each cell
                # cell_bank_index(r,c,i) <=> shapes_covering_cell[r][c][i][0] or shapes_covering_cell[r][c][i][1] or ...
                for i in range(len(shapes_covering_cell[r][c])):
                    self.cnf.append([-self.cell_bank_index(r,c,i)] + shapes_covering_cell[r][c][i])

                    for n in range(len(shapes_covering_cell[r][c][i])):
                        self.cnf.append([-shapes_covering_cell[r][c][i][n], self.cell_bank_index(r,c,i)])
                
                # Once we know which shape in the bank covers a cell, we instantly know all values of cell_area_at_least
                # if cell_bank_index(r,c,i) then [cell_area_at_least(r,c,poly_area) and -cell_area_at_least(r,c,poly_area+1)]
                for i in range(len(self.soft_bank_data)):
                    poly = self.soft_bank_data[i]
                    poly_area = sum([sum(row) for row in poly])
                    self.cnf.append([-self.cell_bank_index(r,c,i), self.cell_area_at_least(r,c,poly_area)])
                    self.cnf.append([-self.cell_bank_index(r,c,i), -self.cell_area_at_least(r,c,poly_area+1)])

            # If two cells are both not in the soft bank, they are part of the same region
            for r1,c1 in self.cell_coords:
                for r2,c2 in self.cell_coords:
                    # if -belongs_to_soft_bank(r1,c1) and -belongs_to_soft_bank(r2,c2) then cells_in_same_region(r1,c1,r2,c2)
                    self.cnf.append([self.belongs_to_soft_bank(r1,c1), self.belongs_to_soft_bank(r2,c2), self.cells_in_same_region(r1,c1,r2,c2)])
                    
            
    
    def calc_upper_bounds(self):
        # We loop over the entire puzzle to check if there are any isolated regions and if so enforce that maximum area
        # We also calculate self.num_regions_upper_bound and self.area_upper_bound from any global rules
        max_cell_areas = [[-1]*(self.C) for _ in range(self.R)]
        neighbors = [(-1,0), (0,1), (1,0), (0,-1)]
        greatest_area = -1
        for r in range(self.R):
            for c in range(self.C):
                if self.is_a_cell(r,c) and max_cell_areas[r][c] == -1:
                    frontier = [(r,c)]
                    visited_cells = [(r,c)]
                    current_area = 1
                    while len(frontier) > 0:
                        current = frontier[0]
                        for n in neighbors:
                            r2 = current[0] + n[0]
                            c2 = current[1] + n[1]
                            edge_coords = (current[0] + r2 + 1, current[1] + c2 + 1)
                            if self.is_a_cell(r2,c2) and self.board[edge_coords[0]][edge_coords[1]] == '..' and (r2,c2) not in visited_cells:
                                current_area += 1
                                visited_cells.append((r2,c2))
                                frontier.append((r2,c2))

                        del frontier[0]

                    for a,b in visited_cells:
                        max_cell_areas[a][b] = current_area

                    greatest_area = max(greatest_area, current_area)

        self.area_upper_bound = greatest_area

        # Enforce cell area upper bounds
        for r in range(self.R):
            for c in range(self.C):
                m = max_cell_areas[r][c]
                if m != -1:
                    self.cnf.append([-self.cell_area_at_least(r,c,m+1)])

        if len(self.shape_bank_data) > 0:
            areas = [sum([sum(row) for row in poly]) for poly in self.shape_bank_data]
            if self.global_rules['minimum'] == False:
                self.global_rules['minimum'] = min(areas)

            if self.global_rules['maximum'] == False:
                self.global_rules['maximum'] = max(areas)        
        
        bounds = []
        
        if self.contains_rose_windows:
            if len(self.rose_coords[0]) == 0:
                raise BadPuzzleError(f"You must use red roses before using roses of other colors")
            for i in range(1, len(self.rose_coords)):
                if len(self.rose_coords[i]) > 0 and len(self.rose_coords[i]) != len(self.rose_coords[0]):
                    raise BadPuzzleError(f"Different numbers of {self.rose_colors[i]} and red roses")

            bounds.append(len(self.rose_coords[0]))

        prec = self.global_rules['precision']
        if prec >= 1:
            if self.total_area % prec != 0:
                raise BadPuzzleError(f"Total area {self.total_area} is not divisible by precision value {prec}")
            bounds.append(self.total_area // prec)
            self.area_upper_bound = prec
            
        if self.global_rules['solitude']:
            bounds.append(self.total_num_symbols)

        if self.global_rules['non-boxy']:
            # Non-boxy implies every region has area >= 3
            bounds.append(self.total_area // 3)
                
        if self.optimizations['num regions upper bound'] >= 1:
            bounds.append(self.optimizations['num regions upper bound'])

        mini = self.global_rules['minimum']
        if mini >= 2:
            bounds.append(self.total_area // mini)

        maxi = self.global_rules['maximum']
        if maxi >= 1:
            self.area_upper_bound = maxi

        if self.global_rules['mismatch']:
            # There are only so many polyominoes of a given size and we can't repeatedly use them
            # If the total area was 35 for example, the smallest 11 regions we could use are 1 + 2 + 3 + 3 + 4 + 4 + 4 + 4 + 4 + 5 + 5 = 39 > 35, so n = 10 is the maximum
            num_polyominoes_of_area_n = [1,1,2,5,12,35,108,369]
            area_sequence = []
            counter = 0
            for n in num_polyominoes_of_area_n:
                counter += 1
                area_sequence += [counter for _ in range(n)]

            partial_sum = 0
            i = 0
            while partial_sum <= self.total_area:
                partial_sum += area_sequence[i]
                i += 1

            bounds.append(i-1)
            
        if len(bounds) > 0:
            self.num_regions_upper_bound = min(bounds)
            
        if self.num_regions_upper_bound <= 0 or self.num_regions_upper_bound > self.total_area:
            self.num_regions_upper_bound = self.total_area

        if self.verbose:
            print(f"\nUsing num_regions_upper_bound={self.num_regions_upper_bound} and area_upper_bound={self.area_upper_bound}\n")

        
    
    def is_a_cell(self, r, c):
        return r >= 0 and r < self.R and c >= 0 and c < self.C and self.board[2*r+1][2*c+1] != '..'

    # If the cell at (r,c) is part of region n
    def cell_in_region(self, r, c, n):
        return self.vpool.id(f"cell_in_region_{r}_{c}_{n}")

    def cells_in_same_region(self, r1, c1, r2, c2):
        # Returns a single cnf variable that is true iff the cells are in the same region. The cells do not need to be adjacent.
        # same <=> [cell_in_region(r1,c1,0) and cell_in_region(r2,c2,0)] or [cell_in_region(r1,c1,1) and cell_in_region(r2,c2,1)] or ...

        if (r1,c1) > (r2,c2):
            r1, c1, r2, c2 = r2, c2, r1, c1

        # Check if the variable already exists
        name = f"cells_in_same_region_{r1}_{c1}_{r2}_{c2}"
        if name in self.vpool.obj2id:
            return self.vpool.id(name)

        # Make a new variable if it doesn't already exist
        same = self.vpool.id(name)
        aux_vars = []
        for n in range(self.num_regions_upper_bound):
            aux = self.vpool.id()
            aux_vars.append(aux)

            # aux <=> cell_in_region(r1,c1,n) and cell_in_region(r2,c2,n)
            self.cnf.append([-aux, self.cell_in_region(r1,c1,n)])
            self.cnf.append([-aux, self.cell_in_region(r2,c2,n)])
            self.cnf.append([-self.cell_in_region(r1,c1,n), -self.cell_in_region(r2,c2,n), aux])

            # same <=> [aux1 or aux2 or ...]
            self.cnf.append([-aux, same])
        self.cnf.append([-same] + aux_vars)

        return same

    def edge(self, r1, c1, r2, c2):
        # When talking about an edge it is implied (r1,c1) and (r2,c2) are adjacent
        # cells_in_same_region does not care about adjacency
        return -self.cells_in_same_region(r1,c1,r2,c2)

    def region_is_empty(self, n):
        return self.vpool.id(f"region_is_empty_{n}")

    def root(self, r, c, n):
        # The starting cell for the reachability
        return self.vpool.id(f"root_{r}_{c}_{n}")

    def reachable(self, r, c, k):
        # True iff the cell at (r,c) is reachable from its corresponding root within k steps 
        return self.vpool.id(f"reachable_{r}_{c}_{k}")
    
    def totalizer(self, variables, root_name):
        if len(variables) == 0:
            raise ValueError("Totalizer needs at least one variable")
    
        prev_layer = [TotalizerNode(f"leaf_node_{i}", self.cnf, self.vpool, self.TRUE, self.FALSE, cnf_vars=[variables[i]]) for i in range(len(variables))]
        counter = 0
        while 1:
            current_layer = []
            counter += 1
            num_pairs = len(prev_layer) // 2
            is_root = (len(prev_layer) == 2)
        
            for k in range(num_pairs):
                parent = TotalizerNode(f"layer {counter} number {k}", self.cnf, self.vpool, self.TRUE, self.FALSE, prev_layer[2*k], prev_layer[2*k+1], cnf_prefix=root_name if is_root else None)
                current_layer.append(parent)

                # For every node Z with children X and Y, we do
                # Xi and Yj -> Z(i+j)
                # Z(i+j+1) -> X(i+1) or Y(j+1)
                for i in range(parent.left.num_vars + 1):
                    for j in range(parent.right.num_vars + 1):
                        self.cnf.append([-parent.left.cnf_vars[i], -parent.right.cnf_vars[j], parent.cnf_vars[i+j]])
                        self.cnf.append([-parent.cnf_vars[i+j+1], parent.left.cnf_vars[i+1], parent.right.cnf_vars[j+1]])

            # If there are an odd number of nodes we can't pair the last one up with anything so we carry the node up into the next layer
            if len(prev_layer) % 2 == 1:
                current_layer.append(prev_layer[-1])

            if len(current_layer) == 1:
                return current_layer[0]
    
            prev_layer = current_layer


    def area_at_least(self, n, a):
        return self.area_totalizer_roots[n].cnf_vars[a]

    def cell_area_at_least(self, r, c, a):
        # Each cell (r,c) is associated with a region n, and just the region n is associated with area a.
        # This variable relates (r,c) to a directly.
        if a <= 1:
            return self.TRUE
    
        elif a > self.area_upper_bound:
            return self.FALSE

        else:
            return self.vpool.id(f"cell_area_at_least_{r}_{c}_{a}")
    
    def same_shape(self, n1, n2):
        if n1 > n2:
            n1,n2 = n2,n1
            
        return self.vpool.id(f"same_shape_{n1}_{n2}")
    
    def rigid_transformation(self, t, dr, dc, n1, n2):
        return self.vpool.id(f"rigid_transformation_{t}_{dr}_{dc}_{n1}_{n2}")

    def get_cells_mapped(self, r1, c1, n1, r2, c2, n2):
        if (r1,c1) > (r2,c2):
            r1,c1,n1,r2,c2,n2 = r2,c2,n2,r1,c1,n1
            
        name = f"cells_mapped_{r1}_{c1}_{n1}_{r2}_{c2}_{n2}"
        if name in self.vpool.obj2id:
            return {'var':self.vpool.id(name), 'clauses':[]}

        clauses = []
        mapped = self.vpool.id(name)

        first = self.FALSE
        if self.is_a_cell(r1, c1):
            first = self.cell_in_region(r1,c1,n1)

        second = self.FALSE
        if self.is_a_cell(r2, c2):
            second = self.cell_in_region(r2,c2,n2)
            
        # mapped represents whether or not the two input cells are part of their corresponding regions
        # mapped <=> [first <=> second]
        clauses.append([-mapped, -first, second])
        clauses.append([-mapped, first, -second])
        clauses.append([mapped, -first, -second])
        clauses.append([mapped, first, second])

        return {'var':mapped, 'clauses':clauses}

    def define_same_shape(self, n1, n2):
        R = self.R
        C = self.C
        translation_bounds = [
            # Each entry [[A,B],[C,D]] corresponds to a rigid transformation. The bounds on dr,dc are A <= dr < B, C <= dc < D
            [[0, R], [-(C-1),C]], # pure translation
            [[0, R+C-1], [1-R, C]], # 90 ccw rotation
            [[0, 2*R-1], [0, 2*C-1]], # 180
            [[1-C, R], [0, R+C-1]], # 90 cw
            [[-(R-1), R], [0, 2*C-1]], # v reflection
            [[0,2*R-1], [1-C,C]], # h reflection
            [[1-C, R], [1-R, C]], # first diagonal
            [[0, R+C-1], [0, R+C-1]] # second diagonal
        ]

        # The function same_shape just returns the cnf variable without defining anything. This function returns the clauses that relate same_shape to the rigid transformations
        # We are very careful to only define same_shape pairs when absolutely necessary because it is incredibly expensive to do so.

        if n1 > n2:
            n1, n2 = n2, n1
        
        clauses = []
        all_rigid_transforms = []
        for t in range(8):
            matrix = transformation_matrices[t]
            W, X = matrix[0]
            Y, Z = matrix[1]
                
            bounds = translation_bounds[t]
            min_dr, max_dr = bounds[0]
            min_dc, max_dc = bounds[1]
            for dr in range(min_dr, max_dr):
                for dc in range(min_dc, max_dc):
                    mapped_vars = []
                    for r,c in self.cell_coords:
                        r2 = W*r + X*c + dr
                        c2 = Y*r + Z*c + dc
                            
                        # mapped <=> [cell_in_region(r,c,n1) <=> cell_in_region(r2,c2,n2)]
                        mapping = self.get_cells_mapped(r,c,n1,r2,c2,n2)
                        if len(mapping['clauses']) > 0:
                            for cls in mapping['clauses']:
                                clauses.append(cls)

                        map_var = mapping['var']
                        mapped_vars.append(map_var)
                        # rigid_transformation(t,dr,dc,n1,n2) -> mapped_vars[0] and mapped_vars[1] and ...
                        clauses.append([-self.rigid_transformation(t,dr,dc,n1,n2), map_var])

                            
                        # Do the mapping in the reverse direction too
                        pre_r = (Z*(r-dr) - X*(c-dc))//(W*Z-X*Y)
                        pre_c = (-Y*(r-dr) + W*(c-dc))//(W*Z-X*Y)

                        pre_mapping = self.get_cells_mapped(r,c,n2,pre_r,pre_c,n1)
                        if len(pre_mapping['clauses']) > 0:
                            for cls in pre_mapping['clauses']:
                                clauses.append(cls)

                        pre_map_var = pre_mapping['var']
                        mapped_vars.append(pre_map_var)
                        # rigid_transformation(t,dr,dc,n1,n2) -> mapped_vars[0] and mapped_vars[1] and ...
                        clauses.append([-self.rigid_transformation(t,dr,dc,n1,n2), pre_map_var])


                    # rigid_transformation(t,dr,dc,n1,n2) <- mapped_vars[0] and mapped_vars[1] and ...
                    clauses.append([-m for m in mapped_vars] + [self.rigid_transformation(t,dr,dc,n1,n2)])

                    all_rigid_transforms.append(self.rigid_transformation(t,dr,dc,n1,n2))
                    # same_shape <- trans[0] or trans[1] or ...
                    clauses.append([-self.rigid_transformation(t,dr,dc,n1,n2), self.same_shape(n1,n2)])

        # same_shape -> trans[0] or trans[1] or ...
        clauses.append([-self.same_shape(n1,n2)] + all_rigid_transforms)

        
        # if same_shape(n1,n2) then [area_at_least(n1,a) <=> area_at_least(n2,a)]
        for a in range(1, self.area_upper_bound+1):
            clauses.append([-self.same_shape(n1,n2), -self.area_at_least(n1,a), self.area_at_least(n2,a)])
            clauses.append([-self.same_shape(n1,n2), self.area_at_least(n1,a), -self.area_at_least(n2,a)])
        
        # If both regions have area 1 they are the same shape
        # if [area_at_least(n1,1) and -area_at_least(n1,2) and area_at_least(n2,1) and -area_at_least(n2,2)] then same_shape(n1,n2)
        clauses.append([-self.area_at_least(n1,1), self.area_at_least(n1,2), -self.area_at_least(n2,1), self.area_at_least(n2,2), self.same_shape(n1,n2)])
        
        # If both regions have area 2 they are the same shape
        # if [area_at_least(n1,2) and -area_at_least(n1,3) and area_at_least(n2,2) and -area_at_least(n2,3)] then same_shape(n1,n2)
        clauses.append([-self.area_at_least(n1,2), self.area_at_least(n1,3), -self.area_at_least(n2,2), self.area_at_least(n2,3), self.same_shape(n1,n2)])
        
        
        return clauses
    
    def add_fundamental_clauses(self):
        # Defines cells, edges, connectivity stuff

        # Every cell needs to be part of exactly one region
        for r,c in self.cell_coords:
            self.cnf.extend(CardEnc.equals(lits=[self.cell_in_region(r,c,n) for n in range(self.num_regions_upper_bound)], bound=1, vpool=self.vpool))

        # Define the edges
        for r,c in self.cell_coords:
            for n in [(0,1),(1,0)]: # right and down
                r2 = r + n[0]
                c2 = c + n[1]
                if self.is_a_cell(r2,c2):
                    # We call the function to generate the cnf but we don't need to do anything else with it here
                    self.edge(r,c,r2,c2)
        
        # Define what an empty region is
        # empty(n) <=> [-cell_in_region(r1,c1,n) and -cell_in_region(r2,c2,n) and ...]
        for n in range(self.num_regions_upper_bound):
            all_cells = []
            for r,c in self.cell_coords:
                self.cnf.append([-self.region_is_empty(n), -self.cell_in_region(r,c,n)])
                all_cells.append(self.cell_in_region(r,c,n))

            self.cnf.append(all_cells + [self.region_is_empty(n)])
        
        # We enforce connectivity by the following rules:
        # Empty regions are considered trivially connected.
        # (1) If a region is not empty then the lexicographically first cell is the root
        # (2) A cell is reachable at step 0 iff the cell is the root
        # (3) If a cell is reachable at step k:
        #       (a) it is still reachable at step k+1,
        #       (b) all of its neighbors (in the same region) are reachable at step k+1
        #       (c) it must be adjacent to a cell (in the same region) that was reachable at step k-1, unless it's the root
        # (4) A region is connected iff every cell is reachable at some step
        
        # (1)
        for n in range(self.num_regions_upper_bound):
            all_possible_roots = [self.root(r,c,n) for r,c in self.cell_coords]

            # -region_is_empty(n) -> at least one(all possible roots)
            self.cnf.append([self.region_is_empty(n)] + all_possible_roots)

            # root(r,c,n) -> cell_in_region(r,c,n)
            for r,c in self.cell_coords:
                self.cnf.append([-self.root(r,c,n), self.cell_in_region(r,c,n)])

            # root is the lexicographically first cell
            earlier_cells = []
            for r,c in self.cell_coords:
                # if root(r,c,n) then [-cell_in_region(r1,c1,n) and -cell_in_region(r2,c2,n) and ...] for all earlier cells
                for cell in earlier_cells:
                    self.cnf.append([-self.root(r,c,n), -self.cell_in_region(cell[0],cell[1],n)])

                earlier_cells.append((r,c))
        
        # (2)
        for r,c in self.cell_coords:
            for n in range(self.num_regions_upper_bound):
                # root(r,c,n) -> reachable(r,c,0)
                self.cnf.append([-self.root(r,c,n), self.reachable(r,c,0)])

            # if reachable(r,c,0) then [(root(r,c,0) or root(r,c,1) or root(r,c,2) or ...]
            self.cnf.append([-self.reachable(r,c,0)] + [self.root(r,c,n) for n in range(self.num_regions_upper_bound)])


        # (3)
        for r,c in self.cell_coords:
            for k in range(self.area_upper_bound): # k runs from 0 <= k <= area_upper_bound - 1
                # (a) if reachable(r,c,k) then reachable(r,c,k+1)
                self.cnf.append([-self.reachable(r,c,k), self.reachable(r,c,k+1)])

                for neighbor in [(-1,0), (0,1), (1,0), (0,-1)]:
                    r2 = r + neighbor[0]
                    c2 = c + neighbor[1]
                    if self.is_a_cell(r2,c2):
                        for n in range(self.num_regions_upper_bound):
                            # (b) if [reachable(r,c,k) and cell_in_region(r,c,n) and cell_in_region(r',c',n)] then reachable(r',c',k+1)
                            self.cnf.append([-self.reachable(r,c,k), -self.cell_in_region(r,c,n), -self.cell_in_region(r2,c2,n), self.reachable(r2,c2,k+1)])  
                
                for n in range(self.num_regions_upper_bound):
                    aux_vars = []
                    for neighbor in [(-1,0), (0,1), (1,0), (0,-1)]:
                        r2 = r + neighbor[0]
                        c2 = c + neighbor[1]
                        if self.is_a_cell(r2,c2):
                            aux = self.vpool.id()
                            aux_vars.append(aux)
                            # aux <=> cell_in_region(r2,c2,n) and reachable(r2,c2,k)
                            self.cnf.append([-aux, self.cell_in_region(r2,c2,n)])
                            self.cnf.append([-aux, self.reachable(r2,c2,k)])
                            self.cnf.append([-self.cell_in_region(r2,c2,n), -self.reachable(r2,c2,k), aux])
                    
                    # (c) if [reachable(r,c,k+1) and cell_in_region(r,c,n) and -root(r,c,n)] then [{cell_in_region(r1,c1,n) and reachable(r1,c1,k)} or {cell_in_region(r2,c2,n) and reachable(r2,c2,k)} or ...]
                    self.cnf.append([-self.reachable(r,c,k+1), -self.cell_in_region(r,c,n), self.root(r,c,n)] + aux_vars)

        # (4)
        for r,c in self.cell_coords:
            self.cnf.append([self.reachable(r,c,k) for k in range(self.area_upper_bound)])
        

    
    def add_symmetry_breaking_clauses(self):
        #   (1) Order the regions by one of the following ways:
        #       (a) If the puzzle has rose windows we can assign regions via red roses
        #       (b) If the puzzle has solitude we can assign regions via symbols
        #       (c) If the puzle has neither, then by default assign regions by the lexicographic order of their roots
        #   (2) If a region is empty all higher numbered regions are empty

        if self.contains_rose_windows:
            for n in range(self.num_regions_upper_bound):
                # (1a)
                self.cnf.append([self.cell_in_region(self.rose_coords[0][n][0], self.rose_coords[0][n][1], n)])

                # Enforce the rest of rose window logic
                # For all blue, yellow, green, and purple roses, if the rose belongs to region n then all other roses of that color can't belong to region n
                for color in range(1,5):
                    # if cell_in_region(r1,c1,n) then [-cell_in_region(r2,c2,n) and -cell_in_region(r3,c3,n) and ...]
                    for cell in self.rose_coords[color]:
                        for other in self.rose_coords[color]:
                            if cell == other:
                                continue

                            self.cnf.append([-self.cell_in_region(cell[0], cell[1], n), -self.cell_in_region(other[0], other[1], n)])

        elif self.global_rules['solitude']:
            symbol_counter = 0
            for i in range(1, len(self.board), 2):
                for j in range(1, len(self.board[0]), 2):
                    if self.board[i][j] != '..' and self.board[i][j] != '##':
                        self.cnf.append([self.cell_in_region(i//2, j//2, symbol_counter)])
                        symbol_counter += 1

        else:
            for n in range(1,self.num_regions_upper_bound):
                # if root(r,c,n) then [root(r1,c1,n-1) or root(c2,c2,n-1) or ...] for all earlier cells
                earlier_cells = []
                for r,c in self.cell_coords:
                    self.cnf.append([-self.root(r,c,n)] + earlier_cells)

                    earlier_cells.append(self.root(r,c,n-1))
    
        # (2)
        for n in range(self.num_regions_upper_bound-1):
            # if region_is_empty(n) then [region_is_empty(n+1) and region_is_empty(n+2) and ...]
            for m in range(n+1,self.num_regions_upper_bound):
                self.cnf.append([-self.region_is_empty(n), self.region_is_empty(m)])

    def region_has_area_one(self, n):
        return self.vpool.id(f"region_has_area_one_{n}")

    def region_has_area_two(self, n):
        return self.vpool.id(f"region_has_area_two_{n}")

    def bank_index_count_at_least(self, i, k):
        return self.bank_index_count_totalizer_roots[i].cnf_vars[k]
    
    def add_totalizer_clauses(self):
        for n in range(self.num_regions_upper_bound):
            all_cells = [self.cell_in_region(r,c,n) for r,c in self.cell_coords]
            t_root = self.totalizer(all_cells, f"area_at_least_{n}")    
            self.area_totalizer_roots.append(t_root)

        # Define cell_area_at_least
        # if cell_in_region(r,c,n) then [cell_area_at_least(r,c,a) <=> area_at_least(n,a)]
        for r,c in self.cell_coords:
            for n in range(self.num_regions_upper_bound):
                for a in range(1, self.area_upper_bound+1):
                    # Let x be cell_area_at_least(r,c,a) and y be area_at_least(n,a)
                    # if cell_in_region(r,c,n) then [(x or -y) and (-x or y)]
                    # -cell_in_region(r,c,n) or [(x or -y) and (-x or y)]
                    self.cnf.append([-self.cell_in_region(r,c,n), self.cell_area_at_least(r,c,a), -self.area_at_least(n,a)])
                    self.cnf.append([-self.cell_in_region(r,c,n), -self.cell_area_at_least(r,c,a), self.area_at_least(n,a)])

        # Define region_has_area_one and two
        # region_has_area_one <=> area_at_least(n,1) and -area_at_least(n,2)
        for n in range(self.num_regions_upper_bound):
            self.cnf.append([-self.region_has_area_one(n), self.area_at_least(n,1)])
            self.cnf.append([-self.region_has_area_one(n), -self.area_at_least(n,2)])
            self.cnf.append([-self.area_at_least(n,1), self.area_at_least(n,2), self.region_has_area_one(n)])

        # region_has_area_two <=> area_at_least(n,2) and -area_at_least(n,3)
        for n in range(self.num_regions_upper_bound):
            self.cnf.append([-self.region_has_area_two(n), self.area_at_least(n,2)])
            self.cnf.append([-self.region_has_area_two(n), -self.area_at_least(n,3)])
            self.cnf.append([-self.area_at_least(n,2), self.area_at_least(n,3), self.region_has_area_two(n)])

        if self.global_rules['mismatch']:
            if len(self.shape_bank_data) > 0:
                for i in range(len(self.shape_bank_data)):
                    all_cells = [self.cell_bank_index(r,c,i) for r,c in self.cell_coords]
                    t_root = self.totalizer(all_cells, f"bank_index_count_at_least_{i}")
                    self.bank_index_count_totalizer_roots.append(t_root)

            if len(self.soft_bank_data) > 0:
                for i in range(len(self.soft_bank_data)):
                    all_cells = [self.cell_bank_index(r,c,i) for r,c in self.cell_coords]
                    t_root = self.totalizer(all_cells, f"bank_index_count_at_least_{i}")
                    self.bank_index_count_totalizer_roots.append(t_root)
    
    def add_two_colorable_clauses(self):
        for i in range(2, len(self.board), 2):
            for j in range(2, len(self.board[0]), 2):
                diagonal_neighbors = [(-1,-1), (-1,1), (1,1), (1,-1)]
                nbr_cell_coords = [(), (), (), ()]
                num_cells = 0
                for n in range(len(diagonal_neighbors)):
                    r = (i + diagonal_neighbors[n][0])//2
                    c = (j + diagonal_neighbors[n][1])//2
                    if self.is_a_cell(r,c):
                        nbr_cell_coords[n] = (r,c)
                        num_cells += 1

                if num_cells == 4:
                    edge_vars = []
                    for k in range(4):
                        first = nbr_cell_coords[k]
                        second = nbr_cell_coords[(k+1)%4]
                        if len(first) > 0 and len(second) > 0:
                            edge_vars.append(self.edge(first[0], first[1], second[0], second[1]))

                    A = self.vpool.id()
                    self.cnf.append([-A, edge_vars[0], edge_vars[1]])
                    self.cnf.append([-A, -edge_vars[0], -edge_vars[1]])
                    self.cnf.append([A, -edge_vars[0], edge_vars[1]])
                    self.cnf.append([A, edge_vars[0], -edge_vars[1]])

                    B = self.vpool.id()
                    self.cnf.append([-B, edge_vars[2], edge_vars[3]])
                    self.cnf.append([-B, -edge_vars[2], -edge_vars[3]])
                    self.cnf.append([B, -edge_vars[2], edge_vars[3]])
                    self.cnf.append([B, edge_vars[2], -edge_vars[3]])

                    self.cnf.append([-A, B])
                    self.cnf.append([A, -B])
                            

    def belongs_to_compass(self, r, c, k):
        return self.vpool.id(f"belongs_to_compass_{r}_{c}_{k}")

    def add_compass_clauses(self, comp):
        rcomp = comp[0]
        ccomp = comp[1]
        directions = comp[2]
        compass_id = comp[3]
        for r,c in self.cell_coords:
            for n in range(self.num_regions_upper_bound):
                # if [cell_in_region(r,c,n) and cell_in_region(rcomp, ccomp, n)] then belongs_to_compass(r,c,k)
                self.cnf.append([-self.cell_in_region(r,c,n), -self.cell_in_region(rcomp, ccomp, n), self.belongs_to_compass(r,c,compass_id)])

            # if belongs_to_compass(r,c,k) then cells_in_same_region(r,c,rcomp,ccomp)
            same = self.cells_in_same_region(r,c,rcomp,ccomp)
            self.cnf.append([-self.belongs_to_compass(r,c,compass_id), same])

        for d, k in directions:
            match d:
                # compass_cells is the available pool of cells that can satisfy the compass
                # non_compass_cells are the cells that cannot be part of the compass since they're too far away
                case 'n':
                    compass_cells = [(a,b) for a in range(max(0,rcomp-k), rcomp) for b in range(self.C) if self.is_a_cell(a,b)]
                    non_compass_cells = [(a,b) for a in range(0, rcomp-k) for b in range(self.C) if self.is_a_cell(a,b)]           
                    
                case 'e':
                    compass_cells = [(a,b) for a in range(self.R) for b in range(ccomp+1, min(self.C, ccomp+k+1)) if self.is_a_cell(a,b)]
                    non_compass_cells = [(a,b) for a in range(self.R) for b in range(ccomp+k+1, self.C) if self.is_a_cell(a,b)]

                case 's':
                    compass_cells = [(a,b) for a in range(rcomp+1, min(self.R, rcomp+k+1)) for b in range(self.C) if self.is_a_cell(a,b)]
                    non_compass_cells = [(a,b) for a in range(rcomp+k+1, self.R) for b in range(self.C) if self.is_a_cell(a,b)]

                case 'w':
                    compass_cells = [(a,b) for a in range(self.R) for b in range(max(0,ccomp-k),ccomp) if self.is_a_cell(a,b)]
                    non_compass_cells = [(a,b) for a in range(self.R) for b in range(0, ccomp-k) if self.is_a_cell(a,b)]

            self.cnf.extend(CardEnc.equals(lits=[self.belongs_to_compass(a,b,compass_id) for a,b in compass_cells], bound=k, vpool=self.vpool))
            for a,b in non_compass_cells:
                self.cnf.append([-self.belongs_to_compass(a,b,compass_id)])

    def make_var_for_polyomino_placement(self, r, c, poly):
        # poly is the grid of 0s and 1s
        # r,c is the top left corner cell
        # We check if the polyomino is out of bounds and if not then create a cnf variable representing the corresponding edges being on/off
        occupied_cells = [(r+a,c+b) for a in range(len(poly)) for b in range(len(poly[0])) if poly[a][b] == 1]

        if 0 not in [self.is_a_cell(a,b) for a,b in occupied_cells]:
            base_edge_coords = get_base_edge_coords(poly)
            internal_edges = [coordinate_add(e, (r,c,r,c)) for e in base_edge_coords['internal']]
            perimeter_edges = []
            for outer in base_edge_coords['perimeter']:
                first = [outer[0]+r, outer[1]+c]
                second = [outer[2]+r, outer[3]+c]
                if self.is_a_cell(first[0], first[1]) and self.is_a_cell(second[0], second[1]):
                    perimeter_edges.append((first[0], first[1], second[0], second[1]))

            variables = [-self.edge(coord[0], coord[1], coord[2], coord[3]) for coord in internal_edges] + [self.edge(coord[0], coord[1], coord[2], coord[3]) for coord in perimeter_edges]

            # placement_var <=> [-internal_1 and -internal_2 and ... and perimeter_1 and perimeter_2 and ...]
            placement_var = self.vpool.id()
            for v in variables:
                self.cnf.append([-placement_var, v])
            self.cnf.append([-v for v in variables] + [placement_var])

            return {'var':placement_var, 'occupied_cells':occupied_cells}

        return None
    
    def add_polyomino_clauses(self, poly, poly_id):
        r_base = poly[0]
        c_base = poly[1]
        poly_data = poly[2]
        aux_vars = []
        for orient in get_orientations(poly_data):
            orient_cells = [(a,b) for a in range(len(orient)) for b in range(len(orient[0])) if orient[a][b] == 1]
                
            for r_trans, c_trans in orient_cells:
                # (r,c) is the top left corner of the translated polyomino
                r = r_base - r_trans
                c = c_base - c_trans

                result = self.make_var_for_polyomino_placement(r,c,orient)
                if result is not None:
                    aux_vars.append(result['var'])
                    self.all_polyomino_positions[poly_id].append((result['occupied_cells'], result['var']))

        self.cnf.append(aux_vars)

        # We know the area of the cell containing the polyomino
        poly_area = sum([sum(row) for row in poly_data])
        self.cnf.append([self.cell_area_at_least(r_base, c_base, poly_area)])
        self.cnf.append([-self.cell_area_at_least(r_base, c_base, poly_area+1)])

    def check_polyomino_pairs(self):
        if self.global_rules['mingle shape']:
            for i in range(len(self.all_polyomino_positions)):
                for j in range(i+1, len(self.all_polyomino_positions)):
                    for poly1 in self.all_polyomino_positions[i]:
                        for poly2 in self.all_polyomino_positions[j]:
                            if adjacent(poly1[0], poly2[0]) and poly1[0] != poly2[0] and regions_have_same_shape(poly1[0], poly2[0]):
                                self.cnf.append([-poly1[1], -poly2[1]])

    def add_palisade_clauses(self, pal):
        r1 = pal[0]
        c1 = pal[1]
        p = pal[2]
        edge_vars = [None, None, None, None]
        defined_edge_vars = [] # edge_vars without the Nones
        neighbors = [(-1,0), (0,1), (1,0), (0,-1)]
        for i in range(len(neighbors)):
            n = neighbors[i]
            r2 = r1 + n[0]
            c2 = c1 + n[1]
            if self.is_a_cell(r2,c2):
                e = self.edge(r1,c1,r2,c2)
                edge_vars[i] = e
                defined_edge_vars.append(e)

        match p:
            case '0':
                # There can be no edges anywhere
                for e in edge_vars:
                    self.cnf.append([-e])

            case '1':
                # If the palisade is against a wall, that is the edge and there can't be any other edges
                if None in edge_vars:
                    for e in defined_edge_vars:
                        self.cnf.append([-e])

                else:
                    self.cnf.extend(CardEnc.equals(lits=edge_vars, bound=1, vpool=self.vpool))

            case '^':
                # Handle one-sided edges/puzzle boundary
                for i in range(4):
                    if edge_vars[i] is None:
                        opposite_edge = edge_vars[(i+2)%4]
                        self.cnf.append([-opposite_edge])

                # Opposite (two-sided) edges must be different
                if edge_vars[0] is not None and edge_vars[2] is not None:
                    # We require (-edge_vars[0] and edge_vars[1]) or (edge_vars[0] and -edge_vars[1])
                    # This is equivalent to (-edge_vars[0] or -edge_vars[1]) and (edge_vars[0] or edge_vars[1])
                    self.cnf.append([-edge_vars[0], -edge_vars[2]])
                    self.cnf.append([edge_vars[0], edge_vars[2]])

                if edge_vars[1] is not None and edge_vars[3] is not None:
                    self.cnf.append([-edge_vars[1], -edge_vars[3]])
                    self.cnf.append([edge_vars[1], edge_vars[3]])

            case '=':
                # Handle one-sided edges/puzzle boundary
                against_wall = False
                for i in range(4):
                    if edge_vars[i] is None:
                        adjacent_edge1 = edge_vars[(i+1)%4]
                        opposite_edge = edge_vars[(i+2)%4]
                        adjacent_edge2 = edge_vars[(i+3)%4]
                        self.cnf.append([opposite_edge])
                        self.cnf.append([-adjacent_edge1])
                        self.cnf.append([-adjacent_edge2])
                        against_wall = True
                        break

                if not against_wall:
                    # The palisade must be {e[0] and -e[1] and e[2] and -e[3]} or {-e[0] and e[1] and -e[2] and e[3]}
                    # We enforce this as e[0] <=> e[2] and e[1] <=> e[3] and e[0] <=> -e[1]
                    e = edge_vars
                    self.cnf.append([-e[0], e[2]])
                    self.cnf.append([-e[2], e[0]])
                    self.cnf.append([-e[1], e[3]])
                    self.cnf.append([-e[3], e[1]])
                    self.cnf.append([-e[0], -e[1]])
                    self.cnf.append([e[1], e[0]])
                        
            case '3':
                # We have exactly one edge off in this case
                self.cnf.extend(CardEnc.equals(lits=[-e for e in defined_edge_vars], bound=1, vpool=self.vpool))


            case '4':
                # All edges must be on
                for e in edge_vars:
                    self.cnf.append([e])

    def add_watchtower_clauses(self, w):
        i = w[0]
        j = w[1]
        w_count = w[2]
        diagonal_neighbors = [(-1,-1), (-1,1), (1,1), (1,-1)]
        cell_coords = [(), (), (), ()]
        num_cells = 0
        for n in range(len(diagonal_neighbors)):
            r = (i + diagonal_neighbors[n][0])//2
            c = (j + diagonal_neighbors[n][1])//2
            if self.is_a_cell(r,c):
                cell_coords[n] = (r,c)
                num_cells += 1
        
        edge_vars = []
        for a in range(4):
            first = cell_coords[a]
            second = cell_coords[(a+1)%4]
            if len(first) > 0 and len(second) > 0:
                edge_vars.append(self.edge(first[0], first[1], second[0], second[1]))
        
        # We will need to enforce whether diagonal pairs of cells are in the same region or not
        if num_cells == 3:
            if len(cell_coords[0]) and len(cell_coords[2]) > 0:
                same = self.cells_in_same_region(cell_coords[0][0], cell_coords[0][1], cell_coords[2][0], cell_coords[2][1])
            else:
                same = self.cells_in_same_region(cell_coords[1][0], cell_coords[1][1], cell_coords[3][0], cell_coords[3][1])

        if num_cells == 4:
            same1 = self.cells_in_same_region(cell_coords[0][0], cell_coords[0][1], cell_coords[2][0], cell_coords[2][1])
            same2 = self.cells_in_same_region(cell_coords[1][0], cell_coords[1][1], cell_coords[3][0], cell_coords[3][1])

        num_edges = len(edge_vars)
        match (w_count, num_cells, num_edges):
            case ('1', 2, 0):
                # A diagonal pair of edges like
                #   '..','..','##'
                #   '..','W1','..'
                #   '##','..','..'
                # The two cells need to be in the same region
                if len(cell_coords[0]) > 0:
                    pair = self.cells_in_same_region(cell_coords[0][0], cell_coords[0][1], cell_coords[2][0], cell_coords[2][1])
                else:
                    pair = self.cells_in_same_region(cell_coords[1][0], cell_coords[1][1], cell_coords[3][0], cell_coords[3][1])
                
                self.cnf.append([pair])

            case ('2', 2, 0):
                # A diagonal pair of edges like
                #   '..','..','##'
                #   '..','W2','..'
                #   '##','..','..'
                # The two cells need to be in opposite regions
                if len(cell_coords[0]) > 0:
                    pair = self.cells_in_same_region(cell_coords[0][0], cell_coords[0][1], cell_coords[2][0], cell_coords[2][1])
                else:
                    pair = self.cells_in_same_region(cell_coords[1][0], cell_coords[1][1], cell_coords[3][0], cell_coords[3][1])

                self.cnf.append([-pair])

            case ('1', 1, 0) | ('1', 2, 1) | ('1', 3, 2) | ('1', 4, 4):
                # Everything is in the same region; no edges anywhere
                for e in edge_vars:
                    self.cnf.append([-e])

            case ('2', 2, 1):
                # Two adjacent cells, the edge must be on
                self.cnf.append([edge_vars[0]])

            case ('2', 3, 2):
                # Exactly one edge is on and the other is off, or both edges are on with the diagonal pair part of the same region
                # (-e0 and e1) or (e0 and -e1) or (e0 and e1 and same_region(diagonal_pair))
                # The above is logically equivalent to (e0 or e1) and (-0 or -e1 or same_region)
                self.cnf.append([edge_vars[0], edge_vars[1]])
                self.cnf.append([-edge_vars[0], -edge_vars[1], same])

            case ('2', 4, 4):
                # We need exactly two edges to be on
                self.cnf.extend(CardEnc.equals(lits=edge_vars, bound=2, vpool=self.vpool))

            case ('3', 3, 2):
                # Both edges must be on and the two diagonal cells must be in different regions
                for e in edge_vars:
                    self.cnf.append([e])

                self.cnf.append([-same])

            case ('3', 4, 4):
                # We could have exactly 3 edges on or we could have all 4 edges on with one pair of diagonal cells in the same region
                # We can encode this as saying
                #   (1) at least 3 edges on, and
                #   (2) if 4 edges on then at least one diagonal pair in the same region: if {e[0] and e[1] and e[2] and e[3]} then {same1 or same2}
                self.cnf.extend(CardEnc.atleast(lits=edge_vars, bound=3, vpool=self.vpool))
                self.cnf.append([-edge_vars[0], -edge_vars[1], -edge_vars[2], -edge_vars[3], same1, same2])
                
            case ('4', 4, 4):
                # We need all edges on and both diagonal pairs in different regions
                for e in edge_vars:
                    self.cnf.append([e])

                self.cnf.append([-same1])
                self.cnf.append([-same2])

            case _:
                raise BadPuzzleError(f"Unsatisfiable watchtower W{w_count} at index {i},{j}")
                    
        
    
    def add_loopy_bricky_clauses(self):
        num_edges_not_allowed = []
        if self.global_rules['loopy']:
            num_edges_not_allowed.append(3)
        if self.global_rules['bricky']:
            num_edges_not_allowed.append(4)
        if len(num_edges_not_allowed) > 0:
            for i in range(0, len(self.board), 2):
                for j in range(0, len(self.board[0]), 2):
                    diagonal_neighbors = [(-1,-1), (-1,1), (1,1), (1,-1)]
                    nbr_cell_coords = [(), (), (), ()]
                    num_cells = 0
                    for n in range(len(diagonal_neighbors)):
                        r = (i + diagonal_neighbors[n][0])//2
                        c = (j + diagonal_neighbors[n][1])//2
                        if self.is_a_cell(r,c):
                            nbr_cell_coords[n] = (r,c)
                            num_cells += 1

                    edge_vars = []
                    for k in range(4):
                        first = nbr_cell_coords[k]
                        second = nbr_cell_coords[(k+1)%4]
                        if len(first) > 0 and len(second) > 0:
                            edge_vars.append(self.edge(first[0], first[1], second[0], second[1]))

                    if self.global_rules['loopy'] and self.global_rules['bricky']:
                        match len(edge_vars):
                            case 1:
                                # Avoid the potential T by forcing the edge off
                                self.cnf.append([-edge_vars[0]])
                                
                            case 2:
                                # We already have 2 (one-sided) edges on and there can be no others
                                self.cnf.append([-edge_vars[0]])
                                self.cnf.append([-edge_vars[1]])

                            case 4:
                                # We can have exactly 0 or 2 edges on
                                # Since 1 is already impossible we enforce at most 2
                                self.cnf.append([-edge_vars[0], -edge_vars[1], -edge_vars[2]])
                                self.cnf.append([-edge_vars[0], -edge_vars[1], -edge_vars[3]])
                                self.cnf.append([-edge_vars[0], -edge_vars[2], -edge_vars[3]])
                                self.cnf.append([-edge_vars[1], -edge_vars[2], -edge_vars[3]])
                    else:
                        for count in num_edges_not_allowed:
                            match (len(edge_vars), count):
                                # Loopy rules
                                case (1,3):
                                    # When two cells are against a wall we must avoid the T and force the edge off
                                    self.cnf.append([-edge_vars[0]])

                                case (2,3):
                                    # Around a corner we need both edges to be the same
                                    self.cnf.append([edge_vars[0], -edge_vars[1]])
                                    self.cnf.append([-edge_vars[0], edge_vars[1]])
                                
                                case (4,3):
                                    # In general we can't have exactly 3 edges
                                    # Since exactly one edge is also impossible we enforce there must be an even number of edges
                                    # not(e0 xor e1 xor e2 xor e3)
                                    # A <=> e0 xor e1
                                    # B <=> e2 xor x3
                                    # not(A xor B) is equivalently (-A or B) and (A or -B)
                                    
                                    A = self.vpool.id()
                                    self.cnf.append([-A, edge_vars[0], edge_vars[1]])
                                    self.cnf.append([-A, -edge_vars[0], -edge_vars[1]])
                                    self.cnf.append([A, -edge_vars[0], edge_vars[1]])
                                    self.cnf.append([A, edge_vars[0], -edge_vars[1]])

                                    B = self.vpool.id()
                                    self.cnf.append([-B, edge_vars[2], edge_vars[3]])
                                    self.cnf.append([-B, -edge_vars[2], -edge_vars[3]])
                                    self.cnf.append([B, -edge_vars[2], edge_vars[3]])
                                    self.cnf.append([B, edge_vars[2], -edge_vars[3]])

                                    self.cnf.append([-A, B])
                                    self.cnf.append([A, -B])
                                
                                    
                                # Bricky rules
                                case (2,4):
                                    # Around a corner we can only have at most one edge
                                    self.cnf.append([-edge_vars[0], -edge_vars[1]])

                                case (4,4):
                                    # In general we have at most 3 edges
                                    self.cnf.extend(CardEnc.atmost(lits=edge_vars, bound=3, vpool=self.vpool))
                
    
    def add_board_clauses(self):
        # Rose windows are implemented in symmetry breaking
        
        for i in range(len(self.polyomino_coords)):
            poly = self.polyomino_coords[i]
            self.add_polyomino_clauses(poly, i)
        self.check_polyomino_pairs()
        
        for r,c,a in self.area_number_coords:
            self.cnf.append([self.cell_area_at_least(r,c,a)])
            self.cnf.append([-self.cell_area_at_least(r,c,a+1)])

        for p in self.palisade_coords:
            self.add_palisade_clauses(p)

        for comp in self.compass_coords:
            self.add_compass_clauses(comp)

        for e in self.given_edge_coords:
            self.cnf.append([self.edge(e[0], e[1], e[2], e[3])])
        
        
        for r1, c1, r2, c2, d in self.difference_coords:
            # Difference implies an edge
            self.cnf.append([self.edge(r1,c1,r2,c2)])

            # If one side has area A and the difference is d then the other side has area A+d or A-d.
            # If the total area is 7, one side has area 4, and the difference is 2, then in unary the implications would look like
            # 4 -> 2 or 6
            # 1111000 -> (1100000 or 1111110)
            # We summarize this by saying the other side has area 11xxxx0, where all of the xs are the same.
            # In general the other side has area at least A-d, at most A+d, and all middle variables must be equal.
            for a in range(1, self.area_upper_bound+1):
                # if area(r1,c1,a) and -area(r1,c1,a+1) then { area(r2,c2,2) and ... and area(r2,c2,a-d) and
                #                                              [area(r2,c2,a-d+1) <=> area(r2,c2,a-d+2)] and ... and [area(r2,c2,a+d-1) <=> area(r2,c2,a+d)] and
                #                                              -area(r2,c2,a+d+1) and ... and -area(r2,c2,max) }
                
                for t in range(1, a-d+1):
                    self.cnf.append([-self.cell_area_at_least(r1,c1,a), self.cell_area_at_least(r1,c1,a+1), self.cell_area_at_least(r2,c2,t)])
                    
                    self.cnf.append([-self.cell_area_at_least(r2,c2,a), self.cell_area_at_least(r2,c2,a+1), self.cell_area_at_least(r1,c1,t)])

                for t in range(a-d+1, a+d):
                    self.cnf.append([-self.cell_area_at_least(r1,c1,a), self.cell_area_at_least(r1,c1,a+1), -self.cell_area_at_least(r2,c2,t), self.cell_area_at_least(r2,c2,t+1)])
                    self.cnf.append([-self.cell_area_at_least(r1,c1,a), self.cell_area_at_least(r1,c1,a+1), self.cell_area_at_least(r2,c2,t), -self.cell_area_at_least(r2,c2,t+1)])
                    
                    self.cnf.append([-self.cell_area_at_least(r2,c2,a), self.cell_area_at_least(r2,c2,a+1), -self.cell_area_at_least(r1,c1,t), self.cell_area_at_least(r1,c1,t+1)])
                    self.cnf.append([-self.cell_area_at_least(r2,c2,a), self.cell_area_at_least(r2,c2,a+1), self.cell_area_at_least(r1,c1,t), -self.cell_area_at_least(r1,c1,t+1)])

                for t in range(a+d+1, self.area_upper_bound+1):
                    self.cnf.append([-self.cell_area_at_least(r1,c1,a), self.cell_area_at_least(r1,c1,a+1), -self.cell_area_at_least(r2,c2,t)])
                    
                    self.cnf.append([-self.cell_area_at_least(r2,c2,a), self.cell_area_at_least(r2,c2,a+1), -self.cell_area_at_least(r1,c1,t)])

            
        for inequal in self.inequality_coords:
            r1 = inequal[0]
            c1 = inequal[1]
            r2 = inequal[2]
            c2 = inequal[3]
            direction = inequal[4]
            match direction:
                case '>' | 'v':
                    bigger = (r1, c1)
                    smaller = (r2, c2)

                case '^' | '<':
                    bigger = (r2, c2)
                    smaller = (r1, c1)

                # Inequality implies an edge
            self.cnf.append([self.edge(smaller[0], smaller[1], bigger[0], bigger[1])])
    
            for a in range(0, self.area_upper_bound + 1):
                # if cell_area_at_least(smaller[0],smaller[1],a) then cell_area_at_least(bigger[0],bigger[1],a+1)
                self.cnf.append([-self.cell_area_at_least(smaller[0], smaller[1], a), self.cell_area_at_least(bigger[0], bigger[1], a+1)])
            

        for gem in self.gemini_coords:
            r1,c1,r2,c2 = gem
            self.cnf.append([self.edge(r1,c1,r2,c2)])
            if len(self.shape_bank_data) == 0:
                # Initial guess is same area
                # cell_area_at_least(r1,c1,a) <=> cell_area_at_least(r2,c2,a)
                for a in range(1, self.area_upper_bound+1):
                    self.cnf.append([-self.cell_area_at_least(r1,c1,a), self.cell_area_at_least(r2,c2,a)])
                    self.cnf.append([self.cell_area_at_least(r1,c1,a), -self.cell_area_at_least(r2,c2,a)])

                for n1 in range(self.num_regions_upper_bound):
                    for n2 in range(self.num_regions_upper_bound):
                        # if cell_in_region(r1,c1,n1) and cell_in_region(r2,c2,n2) then same_shape(n1,n2)
                        self.cnf.append([-self.cell_in_region(r1,c1,n1), -self.cell_in_region(r2,c2,n2), self.same_shape(n1,n2)])

            else:
                for i in range(len(self.shape_bank_data)):
                    self.cnf.append([self.cell_bank_index(r1,c1,i), -self.cell_bank_index(r2,c2,i)])
                    self.cnf.append([-self.cell_bank_index(r1,c1,i), self.cell_bank_index(r2,c2,i)])

        for delta in self.delta_coords:
            r1,c1,r2,c2 = delta
            self.cnf.append([self.edge(r1,c1,r2,c2)])
            if len(self.shape_bank_data) == 0:
                # Initial guess is just an edge
                for n1 in range(self.num_regions_upper_bound):
                    for n2 in range(self.num_regions_upper_bound):
                        # if cell_in_region(r1,c1,n1) and cell_in_region(r2,c2,n2) then -same_shape(n1,n2)
                        self.cnf.append([-self.cell_in_region(r1,c1,n1), -self.cell_in_region(r2,c2,n2), -self.same_shape(n1,n2)])
                        
            else:
                for i in range(len(self.shape_bank_data)):
                    self.cnf.append([-self.cell_bank_index(r1,c1,i), -self.cell_bank_index(r2,c2,i)])
                

        for w in self.watchtower_coords:
            self.add_watchtower_clauses(w)

    def cell_bank_index(self,r,c,i):
        return self.vpool.id(f"cell_bank_index_{r}_{c}_{i}")

    def add_two_region_optimization_clauses(self):
        if self.is_a_cell(0,0) and self.is_a_cell(0, self.C-1) and self.is_a_cell(self.R-1, 0) and self.is_a_cell(self.R-1, self.C-1):
            puzzle_is_a_rectangle = True
            border_edges = []
            for r in range(self.R-1):
                if self.is_a_cell(r,0):
                    border_edges.append(self.edge(r,0,r+1,0))
                    border_edges.append(self.edge(r, self.C-1, r+1, self.C-1))
                else:
                    puzzle_is_a_rectangle = False
                    break

            for c in range(self.C-1):
                if self.is_a_cell(0,c):
                    border_edges.append(self.edge(0,c,0,c+1))
                    border_edges.append(self.edge(self.R-1, c, self.R-1, c+1))
                else:
                    puzzle_is_a_rectangle = False
                    break

            if puzzle_is_a_rectangle:
                #self.cnf.extend(CardEnc.equals(lits=border_edges, bound=2, vpool=self.vpool))
                border_edge_at_least = self.totalizer(border_edges, "border_edge_count")
                brdr = border_edge_at_least.cnf_vars
                
                # There can be exactly 0 or 2 border edges on
                # (-brdr[1]) or (brdr[2] and -brdr[3])
                self.cnf.append([-brdr[1], brdr[2]])
                self.cnf.append([-brdr[1], -brdr[3]])
                
    
    def add_global_rule_clauses(self):
        # Solitude is implemented in symmetry breaking
        # Shape bank is handled individually
        
        if self.global_rules['mingle shape']:
            if len(self.shape_bank_data) == 0:
                initial_bound = min(20, self.num_regions_upper_bound)
                for n in range(initial_bound-1):
                    self.cnf.extend(self.define_same_shape(n,n+1))

                for n1 in range(self.num_regions_upper_bound):
                    for n2 in range(self.num_regions_upper_bound):
                        for r1,c1 in self.cell_coords:
                            for neighbor in [(0,1), (1,0), (0,-1), (-1,0)]:
                                r2 = r1 + neighbor[0]
                                c2 = c1 + neighbor[1]
                                if self.is_a_cell(r2, c2):
                                    # if cell_in_region(r1,c1,n) and cell_in_region(r2,c2,n+1) then -same_shape(n,n+1)
                                    self.cnf.append([-self.cell_in_region(r1,c1,n1), -self.cell_in_region(r2,c2,n2), -self.same_shape(n1,n2)])
                                
            else:
                for r1,c1 in self.cell_coords:
                    for n in [(0,1),(1,0)]: # right and down
                        r2 = r1 + n[0]
                        c2 = c1 + n[1]
                        if self.is_a_cell(r2,c2):
                            for i in range(len(self.shape_bank_data)):
                                # if there is an edge then there is no pair of cell_bank_index values where both are true
                                # if edge(r1,c1,r2,c2) then [-cell_bank_index(r1,c1,0) or -cell_bank_index(r2,c2,0)] and [-cell_bank_index(r1,c1,1) or -cell_bank_index(r2,c2,1)] and ...
                                # aux <=> -cell_bank_index(r1,c1,i) or -cell_bank_index(r2,c2,i)
                                aux = self.vpool.id()
                                self.cnf.append([-aux, -self.cell_bank_index(r1,c1,i), -self.cell_bank_index(r2,c2,i)])
                                self.cnf.append([self.cell_bank_index(r1,c1,i), aux])
                                self.cnf.append([self.cell_bank_index(r2,c2,i), aux])

                                self.cnf.append([-self.edge(r1,c1,r2,c2), aux])

        if self.global_rules['mismatch']:
            if len(self.shape_bank_data) == 0 and len(self.soft_bank_data) == 0:
                if self.contains_rose_windows or self.global_rules['solitude']:
                    # Mismatch rose window puzzles usually don't have any other mechanics for the solver to find deductions with resulting in the solver being re-ran many times with no substantial progress being made
                    # Since we know the exact number of regions we might as well just define all the same_shape pairs immediately
                    upp = self.num_regions_upper_bound
                else:
                    upp = min(10, self.num_regions_upper_bound)
                    
                for n1 in range(upp):
                    for n2 in range(n1+1, upp):
                        # if -region_is_empty(n1) and -region_is_empty(n2) then -same_shape(n1,n2)
                        self.cnf.append([self.region_is_empty(n1), self.region_is_empty(n2), -self.same_shape(n1,n2)])
                        self.cnf.extend(self.define_same_shape(n1,n2))

                # There is at most one area 1 region and at most one area 2 region
                self.cnf.extend(CardEnc.atmost(lits=[self.region_has_area_one(n) for n in range(self.num_regions_upper_bound)], bound=1, vpool=self.vpool))
                self.cnf.extend(CardEnc.atmost(lits=[self.region_has_area_two(n) for n in range(self.num_regions_upper_bound)], bound=1, vpool=self.vpool))
                
            elif len(self.shape_bank_data) > 0:
                for i in range(len(self.shape_bank_data)):
                    poly = self.shape_bank_data[i]
                    poly_area = sum([sum(row) for row in poly])
                    self.cnf.append([-self.bank_index_count_at_least(i, poly_area+1)])

            else:
                for i in range(len(self.soft_bank_data)):
                    poly = self.soft_bank_data[i]
                    poly_area = sum([sum(row) for row in poly])
                    self.cnf.append([-self.bank_index_count_at_least(i, poly_area+1)])

        if self.global_rules['match']:
            if len(self.shape_bank_data) == 0:
                for n in range(1, self.num_regions_upper_bound):
                    self.cnf.extend(self.define_same_shape(0,n))
                    
                    # if -region_is_empty(n) then same_shape(0,n)
                    self.cnf.append([self.region_is_empty(n), self.same_shape(0,n)])

                # All cells have the same area
                first = self.cell_coords[0]
                for r,c in self.cell_coords[1:]:
                    for a in range(1, self.area_upper_bound+1):
                        self.cnf.append([-self.cell_area_at_least(r,c,a), self.cell_area_at_least(first[0], first[1], a)])
                        self.cnf.append([self.cell_area_at_least(r,c,a), -self.cell_area_at_least(first[0], first[1], a)])

                # The area of the shape must divide the total area
                divisors = get_divisors(self.total_area)
                aux_vars = []
                for d in divisors:
                    aux = self.vpool.id()
                    aux_vars.append(aux)
                    
                    # aux <=> cell_area_at_least(0,0,d) and -cell_area_at_least(0,0,d+1)
                    self.cnf.append([-aux, self.cell_area_at_least(first[0], first[1], d)])
                    self.cnf.append([-aux, -self.cell_area_at_least(first[0], first[1], d+1)])
                    self.cnf.append([-self.cell_area_at_least(first[0], first[1], d), self.cell_area_at_least(first[0], first[1], d+1), aux])

                self.cnf.append(aux_vars)

            else:
                r_first, c_first = self.cell_coords[0]
                for n in range(1, len(self.cell_coords)):
                    r,c = self.cell_coords[n]
                    for i in range(len(self.shape_bank_data)):
                        self.cnf.append([self.cell_bank_index(r,c,i), -self.cell_bank_index(r_first,c_first,i)])
                        self.cnf.append([-self.cell_bank_index(r,c,i), self.cell_bank_index(r_first,c_first,i)])
        
        if self.global_rules['size separation']:
            for r,c in self.cell_coords:
                for neighbor in [(0,1),(1,0)]: # right and down
                    r2 = r + neighbor[0]
                    c2 = c + neighbor[1]
                    if self.is_a_cell(r2,c2):
                        # We need to enforce if edge(r,c,r2,c2) then the two regions have different areas
                        # Here we abbreviate cell_area_at_least(r,c,a) to just area(r,c,a)
                        # Define D_a in two equivalent ways:
                        #   D_a <=> [area(r,c,a) and -area(r2,c2,a)] or [-area(r,c,a) and area(r2,c2,a)]    (1)
                        #   D_a <=> [area(r,c,a) or area(r2,c2,a)] and [-area(r,c,a) or -area(r2,c2,a)]     (2)
                        # It is easiest to enforce just the forward direction of (2) and just the reverse direction of (1)
                        # The original if statement becomes if edge then [D_2 or D_3 or ...]. Note that D_1 is always false since all regions have area at least 1. 
                        aux_vars = []
                        for a in range(2, self.area_upper_bound+1):
                            D_a = self.vpool.id()
                            aux_vars.append(D_a)

                            # D_a -> [area(r,c,a) or area(r2,c2,a)] and [-area(r,c,a) or -area(r2,c2,a)]
                            self.cnf.append([-D_a, self.cell_area_at_least(r,c,a), self.cell_area_at_least(r2,c2,a)])
                            self.cnf.append([-D_a, -self.cell_area_at_least(r,c,a), -self.cell_area_at_least(r2,c2,a)])

                            # [area(r,c,a) and -area(r2,c2,a)] or [-area(r,c,a) and area(r2,c2,a)] -> D_a
                            self.cnf.append([-self.cell_area_at_least(r,c,a), self.cell_area_at_least(r2,c2,a), D_a])
                            self.cnf.append([self.cell_area_at_least(r,c,a), -self.cell_area_at_least(r2,c2,a), D_a])

                        self.cnf.append([-self.edge(r,c,r2,c2)] + aux_vars)


        if self.global_rules['non-boxy']:
            # Non-boxy is like an anti-shape-bank
            # We pre-compute every possible rectangle and say that particular assignment is invalid
            for r,c in self.cell_coords:
                for h in range(1, self.R+1):
                    for w in range(1, self.C+1):
                        poly = [[1]*w for _ in range(h)]
                        placement = self.make_var_for_polyomino_placement(r,c,poly)
                        if placement is not None:
                            self.cnf.append([-placement['var']])

        self.add_loopy_bricky_clauses()
        

        if self.global_rules['minimum'] >= 2:
            for r,c in self.cell_coords:
                self.cnf.append([self.cell_area_at_least(r,c,self.global_rules['minimum'])])

        # Enforce area upper bound
        for n in range(self.num_regions_upper_bound):
            self.cnf.append([-self.area_at_least(n,self.area_upper_bound+1)])
        
    def build_encoding(self):
        self.add_fundamental_clauses()
        if self.optimizations['two colorable'] or self.num_regions_upper_bound == 2:
            # The two colorable clauses are a weak form of loopy. It is pointless to enforce both loopy and these clauses
            self.add_two_colorable_clauses()
            
        self.add_symmetry_breaking_clauses()
        self.add_totalizer_clauses()
        
        self.add_board_clauses()
        self.add_global_rule_clauses()

        if self.num_regions_upper_bound == 2:
            self.add_two_region_optimization_clauses()

class PuzzleSolver():
    def __init__(self, puzzle_data, solver_settings):
        self.puzzle_data = puzzle_data
        self.global_rules = puzzle_data['global rules']
        self.solver_settings = solver_settings
        self.num_sol_found = 0
        self.verbose = solver_settings['verbose']
        
        start_cnf_time = time.time()
        self.encoding = PuzzleEncoding(puzzle_data, self.verbose)
        self.cnf_time = round(time.time() - start_cnf_time, 3)
        self.cumulative_solve_time = 0
        self.s = SATSolver("Lingeling", bootstrap_with=self.encoding.cnf)
        self.solutions = []
        
        self.blocking_clause = []
        self.present_edges = []
        self.region_nums_by_cell = [[-1]*self.encoding.C for _ in range(self.encoding.R)]
        self.region_cells_by_num = [set() for _ in range(self.encoding.num_regions_upper_bound)]
        
        self.solve_mode = 'normal'

        uses_shape_rules = (puzzle_data['global rules']['mingle shape'] or self.encoding.contains_gemini or self.encoding.contains_delta or puzzle_data['global rules']['mismatch'])    
        if uses_shape_rules and len(puzzle_data['shape bank']) == 0 and len(puzzle_data['optimizations']['soft bank']) == 0:
            self.solve_mode = 'incremental'
            # Incremental mode is used when the puzzle involves rules about the shape of regions and does not have a shape or soft bank.
            # In general it is incredibly expensive to enforce that two regions have same or different shapes. 
            # In incremental mode we only define some of the same_shape variables and leave the rest hanging for performance. The initial output of the solver will almost certainly be wrong. 
            # We need to verify if the output is actually a solution. If not we don't report it to the user, add more definitions to fix the contradiction, and re-run the solver. 
            #   Gemini initial: Enforce an edge and both sides having the same area
            #   Gemini iteration: Check if the two regions are the same shape, if not then define same_shape(n1,n2) for just the two regions n1,n2 touching the gemini clue. 
            #	
            #	Delta initial: Enforce just an edge, nothing else
            #	Delta iteration: Check if the two regions are different shapes, if not then define same_shape(n1,n2) for just the two regions n1,n2 touching the delta clue. 
            #
            #	Mingle initial: Define same_shape(n,n+1) for all 0 <= n <= min(20, num_regions_upper_bound). Enforce mechanic over just these pairs
            #   Mingle iteration: Check every pair of adjacent regions and if two have the same shape define same_shape for that pair and enforce mechanic for them
            #
            #	Mismatch initial: Define same_shape for all pairs 0 <= n1,n2 <= min(10, num_regions_upper_bound).
            #	Mismatch iteration: Compare every possible pair and define same_shape as needed
            #
            #   We never use incremental mode for match puzzles

    def pretty_print_solution(self):
        puzzle = self.puzzle_data['board']
        edges = self.present_edges
        # Add the one-sided edges
        neighbors = [(-1,0), (0,1), (1,0), (0,-1)]
        for r in range(len(puzzle)//2):
            for c in range(len(puzzle[0])//2):
                if puzzle[2*r+1][2*c+1] != '..':
                    if r == 0:
                        edges.append(f'edge_-1_{c}_0_{c}')
                    if r == len(puzzle)//2-1:
                        edges.append(f'edge_{r}_{c}_{r+1}_{c}')
                    if c == 0:
                        edges.append(f'edge_{r}_-1_{r}_0')
                    if c == len(puzzle[0])//2-1:
                        edges.append(f'edge_{r}_{c}_{r}_{c+1}')

                    for n in neighbors:
                        r2 = r + n[0]
                        c2 = c + n[1]
                        if r2 >= 0 and r2 < len(puzzle)//2 and c2 >= 0 and c2 < len(puzzle[0])//2 and puzzle[2*r2+1][2*c2+1] == '..':
                            edges.append(f'edge_{r}_{c}_{r2}_{c2}')

        symbols = [' ', '═══', '   ', '╚', '', '║', '╔', '╠', '', '╝', '═', '╩', '╗', '╣', '╦', '╬']
        output_table = [[2 for i in range(len(puzzle[0]))] for j in range(len(puzzle))]

        # Draw edges
        for edge in edges:
            coords = [int(n) for n in edge.split('_')[1:]]
            symbol = 1 # long horizontal line
            if coords[0] == coords[2]:
                symbol = 5 # vertical line
    
            r = coords[0] + coords[2] + 1
            c = coords[1] + coords[3] + 1
            output_table[r][c] = symbol

        # Draw lattice points 
        for r in range(0, len(output_table), 2):
            for c in range(0, len(output_table[0]), 2):
                bitmask = 0
                for n in range(len(neighbors)):
                    r2 = r + neighbors[n][0]
                    c2 = c + neighbors[n][1]
                    if r2 >= 0 and r2 < len(output_table) and c2 >= 0 and c2 < len(output_table[0]) and output_table[r2][c2] != 2:
                        bitmask += (1 << n)

                output_table[r][c] = bitmask

        # Fix width of non-present vertical edges
        for r in range(1, len(output_table), 2):
            for c in range(0, len(output_table[0]), 2):
                if output_table[r][c] == 2:
                    output_table[r][c] = 0
        
        output = ''
        for row in output_table:
            for num in row:
                output += symbols[num]
            output += '\n'

        print(output)

    def ugly_print_solution(self):
        num_nonempty_regions = 0
        for r in self.region_cells_by_num:
            if len(r) > 0:
                num_nonempty_regions += 1

        num_digits = 1 + (num_nonempty_regions >= 10)
        for row in self.region_nums_by_cell:
            for n in row:
                if n == -1:
                    if num_digits == 1:
                        print('. ', end='')
                    else:
                        print('.. ', end='')

                elif n <= 9 and num_digits == 2:
                    print(f"0{n} ", end='')
                    
                else:
                    print(f"{n} ", end='')

            print()
    
    def output_solution(self):
        if self.solver_settings['pretty print solution']:
            self.pretty_print_solution()
        else:
            self.ugly_print_solution()
    
    def check_solution(self):
        if self.solve_mode == 'normal':
            return True
        
        is_valid_solution = True
        if self.solve_mode == 'incremental':
            if self.global_rules['mingle shape']:
                checked_pairs = []
                for e in self.present_edges:
                    r1, c1, r2, c2 = [int(a) for a in e.split('_')[1:]]
                    n1 = self.region_nums_by_cell[r1][c1]
                    n2 = self.region_nums_by_cell[r2][c2]
                    region1 = self.region_cells_by_num[n1]
                    region2 = self.region_cells_by_num[n2]
                    if regions_have_same_shape(region1, region2) and (n1,n2) not in checked_pairs and (n2,n1) not in checked_pairs:
                        # We found a contradiction to mingle shape
                        is_valid_solution = False
                        checked_pairs.append((n1,n2))
                                    
                        for cls in self.encoding.define_same_shape(n1, n2):
                            self.s.add_clause(cls)

            if self.global_rules['mismatch']:
                checked_pairs = []
                for n1 in range(self.encoding.num_regions_upper_bound):
                    region1 = self.region_cells_by_num[n1]
                    if len(region1) == 0:
                        continue
                            
                    for n2 in range(n1+1, self.encoding.num_regions_upper_bound):
                        region2 = self.region_cells_by_num[n2]
                        if len(region2) == 0:
                            continue
                                
                        if regions_have_same_shape(region1, region2):
                            is_valid_solution = False
                            for cls in self.encoding.define_same_shape(n1,n2):
                                self.s.add_clause(cls)

                            self.s.add_clause([self.encoding.region_is_empty(n1), self.encoding.region_is_empty(n2), -self.encoding.same_shape(n1,n2)])

            for gem in self.encoding.gemini_coords:
                r1,c1,r2,c2 = gem
                n1 = self.region_nums_by_cell[r1][c1]
                n2 = self.region_nums_by_cell[r2][c2]
                region1 = self.region_cells_by_num[n1]
                region2 = self.region_cells_by_num[n2]
                if not regions_have_same_shape(region1,region2):
                    is_valid_solution = False
                    for cls in self.encoding.define_same_shape(n1,n2):
                        self.s.add_clause(cls)

            for delta in self.encoding.delta_coords:
                r1,c1,r2,c2 = delta
                n1 = self.region_nums_by_cell[r1][c1]
                n2 = self.region_nums_by_cell[r2][c2]
                region1 = self.region_cells_by_num[n1]
                region2 = self.region_cells_by_num[n2]
                if regions_have_same_shape(region1,region2):
                    is_valid_solution = False
                    for cls in self.encoding.define_same_shape(n1,n2):
                        self.s.add_clause(cls)

        return is_valid_solution

    def reconstruct_solution(self):
        # We construct a more human readable solution given the sat solver's variable assignments
        for i in self.s.get_model():
            name = self.encoding.vpool.obj(abs(i))
                
            if name != None and name[:14] == 'cell_in_region' and i > 0:
                r, c, n = [int(i) for i in name.split('_')[3:]]
                self.region_cells_by_num[n].add((r,c))
                self.region_nums_by_cell[r][c] = n
                
            if name != None and name[:20] == 'cells_in_same_region':
                self.blocking_clause.append(-i)
                coords = [int(num) for num in name.split('_')[4:]]
                dx = abs(coords[0] - coords[2])
                dy = abs(coords[1] - coords[3])
                if i < 0 and dx + dy <= 1:
                    self.present_edges.append("edge_" + name[21:])
                        
    def solve(self):
        if self.verbose:
            #print(f"Starting solve... ({self.encoding.cnf.nv} variables and {len(self.encoding.cnf.clauses)} clauses)\n")
            print(f"Starting solve...\n")
            
        time_since_last_valid_solution = time.time()
        
        while True:
            # Clear helper variables from the previous loop
            self.blocking_clause = []
            self.present_edges = []
            self.region_nums_by_cell = [[-1]*self.encoding.C for _ in range(self.encoding.R)]
            self.region_cells_by_num = [set() for _ in range(self.encoding.num_regions_upper_bound)]
            
            start_solve_time = time.time()
            result = self.s.solve()
            
            if not result:
                self.cumulative_solve_time += time.time() - start_solve_time
                if self.verbose:
                    if self.num_sol_found == 0:
                        print("\nThere are no solutions.\nIf you were expecting any, double check you have entered the puzzle correctly.")
                    elif self.num_sol_found == 1:
                        print("Found all solutions. The solution is unique.")
                    else:
                        print(f"Found all solutions. There are {self.num_sol_found} solutions.")

                break

            self.reconstruct_solution()
            is_valid_solution = self.check_solution()
            self.s.add_clause(self.blocking_clause)
            
            end_solve_time = time.time()
            solve_time = end_solve_time - start_solve_time
            self.cumulative_solve_time += solve_time
            
            if is_valid_solution:
                self.num_sol_found += 1
                self.solutions.append(self.region_nums_by_cell)

                if self.verbose:
                    print(f"Solution {self.num_sol_found} ({round(end_solve_time - time_since_last_valid_solution,3)} seconds)")

                if self.solver_settings['show solution']:
                    self.output_solution()

                if self.num_sol_found == self.solver_settings['max solutions limit']:
                    if self.verbose:
                        print("Reached maximum solution count; stopping solve now.")

                    break
                else:
                    if self.verbose:
                        print("Searching for more solutions...\n\n")
                        

                time_since_last_valid_solution = time.time()

        self.grand_total_time = round(self.cnf_time + self.cumulative_solve_time, 3)
        self.cumulative_solve_time = round(self.cumulative_solve_time, 3)

        if self.verbose:
            print(f"\n\nCNF time: {self.cnf_time} seconds")
            print(f"Cumulative solve time: {self.cumulative_solve_time} seconds")
            print(f"Grand total time: {self.grand_total_time} seconds")

        return self.solutions

if __name__ == "__main__":
    solver = PuzzleSolver(puzzle_data, solver_settings)
    solutions = solver.solve()
