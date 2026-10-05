# Watchtower small example

puzzle_data = {
    'board':[
        ['..','..','..','..','..','..','W2','..','..'],
        ['..','..','..','##','..','##','..','##','..'],
        ['..','..','..','..','..','..','W2','..','W2'],
        ['..','##','..','##','..','..','..','##','..'],
        ['..','..','..','..','W3','..','..','..','..'],
        ['..','##','..','##','..','##','..','##','..'],
        ['..','..','..','..','..','..','..','..','..'],
        ['..','##','..','##','..','##','..','##','..'],
        ['..','..','..','..','..','..','..','..','..'],
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
        'precision':        False,
        'minimum':          False,
        'maximum':          False
    },
    
    'optimizations':{
        'num regions upper bound':False,
        'two colorable':False,
        'soft bank':[]
    }
}
