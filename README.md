# glimmith-solver
A Python SAT-based solver for puzzles in the game The Artisan of Glimmith. 

## Setup
This project requires Python 3.10 or newer and [PySAT](https://pysathq.github.io/). PySAT can be installed using 
`pip install python-sat`  

## Usage
Enter your puzzle in the `puzzle_data` variable in `solver.py`, then run the program. Example puzzle:
```
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
```
Example output:
```

Using num_regions_upper_bound=12 and area_upper_bound=6

Building CNF...
Starting solve...

Solution 1 (0.109 seconds)
    ╔═══════════╗   ╔═══╦═══════╗    
    ║           ║   ║   ║       ║    
╔═══╝       ╔═══╩═══╣   ╚═══╗   ╚═══╗
║           ║       ║       ║       ║
╠═══════════╣       ╠═══╗   ╚═══╗   ║
║           ║       ║   ║       ║   ║
║           ║   ╔═══╝   ║   ╔═══╣   ║
║           ║   ║       ║   ║   ║   ║
╚═══╦═══════╣   ╠═══╗   ╚═══╣   ╠═══╝
    ║       ║   ║   ║       ║   ║    
╔═══╩═══╗   ╠═══╩═══╩═══╗   ║   ╚═══╗
║       ║   ║           ║   ║       ║
║       ║   ╚═══════╗   ╚═══╬═══╗   ║
║       ║           ║       ║   ║   ║
║       ╠═══════════╬═══╗   ║   ║   ║
║       ║           ║   ║   ║   ║   ║
╚═══╦═══╝       ╔═══╣   ╚═══╝   ╠═══╝
    ║           ║   ║           ║    
    ╚═══════════╝   ╚═══════════╝    

Searching for more solutions...


Found all solutions. The solution is unique.


CNF time: 0.401 seconds
Cumulative solve time: 0.109 seconds
Grand total time: 0.51 seconds
```
The solver draws the completed puzzle using unicode box drawing characters. This looks best using a fixed-width font. If this is not displayed correctly you can choose to have the solution shown in a simpler way in the `solver_settings` variable. 

## How To Express Your Puzzle
### Board
The solver represents puzzles on an expanded cell-edge-vertex grid. This provides room to easily enter edge and vertex mechanics. If the original puzzle has `R` rows and `C` columns, the expanded grid has `2R+1` rows and `2C+1` columns. The image below shows a 2x2 board segment. Cells are colored orange, edges are green, and vertices are purple. The `'##'` symbol means a cell is present and has no mechanics while `'..'` means empty space. 

<p align="center">
  <img src="https://github.com/user-attachments/assets/f08eae19-1072-4c36-a0f2-00cc23010d86" alt="Visual depiction of expanded grid."/>
</p>

Each board mechanic is represented as a two or more character string, see the table below. 

### Table of Symbols

| Symbol | Mechanic | Description|
| :----: | :------: | ---------- |
| `..` | n/a | Empty space. This could be a cell, edge, or vertex. |
| `##` | n/a | A cell with no mechanics. |
| `--`, `\|\|` | Given Edge | An edge in the interior of the puzzle. Either symbol can be used interchangeably; the difference between horizontal and vertical edges is purely visual. |
| `A{number}` | Area Number | Area numbers are prefixed with A and followed by the number. Examples: `A1`, `A2`, `A30` |
| `Rr`, `Rb`, `Ry`, `Rg`, `Rp` | Rose Windows | Rose windows are prefixed with R followed by the first letter of their color (in lowercase): red, blue, yellow, green, or purple. |
| `P0`, `P1`, `P^`, `P=`, `P3`, `P4` | Palisade | Palisades are prefixed with P followed by the number of edges shown in the clue. P2 is ambiguous; use `P^` or `P=`. |
| `Q{name}` | Polyomino | Polyominoes must start with `Q` then be followed by their name. You need to name the polyomino and define its shape in `puzzle_data['polyominoes']`. |
| `C{directions}` | Compass | Compasses start with `C` and are followed by `n`, `e`, `s`, or `w` with the number of cells. If a direction of the compass is blank the corresponding letter is omitted. Examples: `Cn1e2s3w4` means north 1, east 2, south 3, west 4. `Cn1s0` means north 1, south 0, east/west unspecified. `C` means a fully blank compass. |
| `Ge`, `De` | Gemini and Delta | Gemini is `Ge`, Delta is `De`. |
| `D{number}` | Difference | Differences start with `D` followed by the number |
| `I>`,`I<`,`Iv`,`I^` | Inequality | Inequality starts with `I` followed by `>` (greater than), `<` (less than), `v` (lowercase v), or `^` (caret). |
| `W1`, `W2`, `W3`, `W4` | Watchtower | Watchtower starts with `W` followed by the number of regions. |

> [!important]
> Do not mark the perimeter of the puzzle; this is automatically inferred. The symbols `--` and `||` are for marking interior or two-sided edges only.

### Polyominoes
Define polyominoes as a key/value pair in `puzzle_data['polyominoes']`. The key is the name of the polyomino and the value is the shape: a two dimensional array of 1s and 0s. Polyomino names must start with `Q` and be at least two characters long. Example:
```
puzzle_data = {

    ...

    'polyominoes':{
        'Q2':[
            [1,1],
        ],
        'Q3':[
            [1,1,1]
        ],
        'Qstair':[
            [0,0,0,1],
            [0,0,1,1],
            [0,1,1,1],
            [1,1,1,1]
        ],
        'Qloop':[
            [1,1,1,1],
            [1,0,0,1],
            [0,0,0,1],
            [0,0,1,1]
        ]
    },

    ...

}
```
This is just to define a polyomino. Make sure to include it in `puzzle_data['board']`, `puzzle_data['shape bank']`, or `puzzle_data['optimizations']['soft bank']` depending on the puzzle. Soft banks are discussed at the end of this README. 

### Polyomino Shortcuts
You can quickly add the tetrominoes and pentominoes to a shape or soft bank via these shortcuts. You can probably ignore this for most puzzles but sometimes it is convenient for optimizations. 

### Shape Bank
Enter the names of the polyominoes in the shape bank if your puzzle uses it. Do not enter the actual shape data. Continuing the polyomino example from above:
```
puzzle_data = {

    ...

    'shape_bank':['Q2', 'Q3', 'Qstair', 'Qloop'],

    ...

}
```

### Global Rules
For precision, minimum, and maximum, enter the numerical value or `False` if unused. Use `True` and `False` for all other rules.

## Optimizations
At this point you know everything necessary to start using the solver. More examples and a template are provided in the `Examples` folder. While the solver is pretty efficient at most puzzles there are some rule combinations that are particularly tricky. In some cases you may be able to provide the solver with more information to help it work through the puzzle faster. This is completely optional but can make a big difference!

### About Upper Bounds
Two big factors that influence difficulty are the number of regions in a puzzle and the area of the biggest region. By default the solver assumes the worst-case scenario in every puzzle. The worst-case number of regions is if every region is a 1x1 cell, then the number of regions is the total area. The worst-case region area is when there is only a single region, then the region area is the total area. Thus the value  `puzzle_data['optimizations']['num regions upper bound']` is initialized to the total area. If the actual number of regions is much lower than this bound the solver wastes significant time exploring what ultimately ends up as empty regions. This value and the `area_upper_bound` are printed to the screen every time the solver runs. If you can come up with a more optimal bound you should specify it!**An area upper bound is precisely what the maximum mechanic is. Specify area bounds in `puzzle_data['global rules']['maximum']` and num region bounds in `puzzle_data['optimizations']['num regions upper bound']`.**

An easy way to come up with better bounds is to identify a few large regions. Suppose we identify $n$ regions $R_1,\dots,R_n$ with areas $A_1,\dots,A_n$. In the worst case, the remaining area $A_{rem}=A_{total}-\sum A_i$ could be all 1x1s, so the maximum number of regions is $n+A_{rem}$. In general the remaining area may merge with one of the identified regions so the maximum region area is $\max(A_i)+A_{rem}$. See the gemini compass puzzle for an example. 

### Two colorability
If a puzzle is known to be two colorable you can tell the solver that, which may make it easier to solve. This value is automatically set if the puzzle uses loopy or if there are exactly two regions. Some situations where you might manually set this are range(x,x+1) with size separation, puzzles with `W2` at every interior vertex, or maybe shape bank with mingle shape/size separation. 

### Soft Banks
Mismatch is the hardest rule for the solver and soft banks are designed to help. Testing if two regions have the same shape is very difficult in general but is made much easier with a shape bank or soft bank. When we have either bank the solver tests if two regions have the same shape via bank indices rather than comparing shapes directly. For this reason we should **always try to use a bank with mismatch**. In puzzles like loopy + mismatch it is not possible to use a shape bank since we don't know the shape of the "background" region but we might be able to use a soft bank. 

**Definition: A soft bank is a shape bank that allows a one-region exception. If two cells don't belong to the soft bank then they belong to the same region.**

Using either bank allows the solver to efficiently work through the puzzle. Two examples of using soft banks are provided in `Examples`. 

## Disclaimer
This project is a work in progress. Please report any issues or bugs you come across. This is an unofficial fan-made project and is not affiliated with the developers of the game. 
