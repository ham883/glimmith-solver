puzzle_data = {
    # Enter your board data
    'board':[

    ],

    # Define any polyominoes your puzzle uses
    'polyominoes':{

    },

    'polyomino shortcuts':{
        'add tetrominoes to shape bank':False,
        'add tetrominoes to soft bank':False,
        'add pentominoes to shape bank':False,
        'add pentominoes to soft bank':False
    },

    # Add the names of your polyominoes here if the puzzle uses shape bank
    'shape bank':[],

    # For precision, minimum, and maximum specify the numerical value or False if unused. For the other rules specify True or False. 
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
        
        'precision':        False,
        'minimum':          False,
        'maximum':          False
    },

    # These values are optional 
    'optimizations':{
        'num regions upper bound':False,
        'two colorable':False,
        'soft bank':[]
    }
}
