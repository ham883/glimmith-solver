# Gemini compass example
# It is clear that each compass is in its own region. From left to right top down, these compasses have area at least:
# 4, 5, 8, 8, 4, 5, 5, 6
# Summing these numbers the compasses account for at least 45 area. The total area is 56.
# In the worst case the remaining 56 - 45 = 11 area could be 1x1 regions, so there is at most 11 + 8 = 19 regions.
# The remaining area could be taken by one of the compasses, hence the maximum area is 8 + 11 = 19

puzzle_data = {
    'board':[
        ['..','..','..',   '..'    ,'..',   '..'    ,'..', '..'  ,'..', '..'  ,'..',   '..'    ,'..',   '..'    ,'..','..','..'],
        ['..','##','..',   '##'    ,'..',   '##'    ,'..', '##'  ,'..', '##'  ,'..',   '##'    ,'..',   '##'    ,'..','##','..'],
        ['..','..','..',   '..'    ,'..',   '..'    ,'..', '..'  ,'..', 'Ge'  ,'..',   '..'    ,'..',   '..'    ,'..','..','..'],
        ['..','##','..',   '##'    ,'..',   '##'    ,'..','Ce1w2','..', '##'  ,'..',  'Ce3w1'  ,'..',   '##'    ,'..','##','..'],
        ['..','..','..',   '..'    ,'..',   '..'    ,'..', '..'  ,'..', '..'  ,'..',   '..'    ,'..',   '..'    ,'..','..','..'],
        ['..','##','..',   '##'    ,'Ge',   '##'    ,'..', '##'  ,'..', '##'  ,'..',   '##'    ,'..',   '##'    ,'..','##','..'],
        ['..','..','..',   '..'    ,'..',   '..'    ,'..', '..'  ,'..', '..'  ,'..',   '..'    ,'..',   '..'    ,'..','..','..'],
        ['..','##','..','Cn1e1s6w3','..','Cn7e2s0w3','..', '##'  ,'..', '##'  ,'..','Cn0e0s3w3','..','Cn2e2s2w0','..','##','..'],
        ['..','..','..',   '..'    ,'..',   '..'    ,'..', '..'  ,'..', '..'  ,'..',   '..'    ,'..',   '..'    ,'..','..','..'],
        ['..','##','..',   '##'    ,'..',   '##'    ,'..', '##'  ,'..', '##'  ,'..',   '##'    ,'Ge',   '##'    ,'..','##','..'],
        ['..','..','..',   '..'    ,'..',   '..'    ,'..', '..'  ,'..', '..'  ,'..',   '..'    ,'..',   '..'    ,'..','..','..'],
        ['..','##','..',   '##'    ,'..',  'Ce3w1'  ,'..', '##'  ,'..','Ce4w1','..',   '##'    ,'..',   '##'    ,'..','##','..'],
        ['..','..','..',   '..'    ,'..',   '..'    ,'..', 'Ge'  ,'..', '..'  ,'..',   '..'    ,'..',   '..'    ,'..','..','..'],
        ['..','##','..',   '##'    ,'..',   '##'    ,'..', '##'  ,'..', '##'  ,'..',   '##'    ,'..',   '##'    ,'..','##','..'],
        ['..','..','..',   '..'    ,'..',   '..'    ,'..', '..'  ,'..', '..'  ,'..',   '..'    ,'..',   '..'    ,'..','..','..'],
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
        'maximum':          19
    },
    
    'optimizations':{
        'num regions upper bound':19,
        'two colorable':False,
        'soft bank':[]
    }
}
