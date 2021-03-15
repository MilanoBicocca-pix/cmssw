import os
import datetime

#############################
##### Utility functions #####
#############################

# Change the lumis from string to list of ints
def getLSlist (stringLS):
    lista = stringLS.split(',')
    lista[0] = lista[0][1:]
    lista[-1] = lista[-1][:-1]
    lista = [int(x) for x in lista]
    return lista


##################################
##### LS and timestamp lists #####
##################################

timestampListScan1 = [
    #LSi - LSf - TimeBegin -   TimeEnd
    [11,  12,  1530358114,  1530358142],
    [13,  14,  1530358152,  1530358181],
    [15,  16,  1530358191,  1530358219],
    [16,  17,  1530358229,  1530358258],
    [18,  19,  1530358268,  1530358297],
    [20,  21,  1530358308,  1530358335],
    [21,  22,  1530358346,  1530358375],
    [23,  24,  1530358385,  1530358413],
    [25,  26,  1530358423,  1530358452],
    [26,  27,  1530358462,  1530358490],
    [28,  29,  1530358500,  1530358529],
    [30,  31,  1530358539,  1530358568],
    [31,  32,  1530358577,  1530358606],
    [33,  34,  1530358617,  1530358646],
    [35,  36,  1530358656,  1530358684],
    [36,  37,  1530358694,  1530358723],
    [38,  39,  1530358733,  1530358762],
    [40,  41,  1530358772,  1530358800],
    [41,  42,  1530358810,  1530358839],
    [43,  44,  1530358850,  1530358877],
    [44,  46,  1530358888,  1530358917],
    [46,  47,  1530358927,  1530358956],
    [48,  49,  1530358965,  1530358994],
    [49,  51,  1530359004,  1530359033],
    [51,  52,  1530359043,  1530359071],
]

timestampListScan2 = [
    [ 73,   74,  1530359555,  1530359584],
    [ 75,   76,  1530359594,  1530359623],
    [ 76,   78,  1530359634,  1530359661],
    [ 78,   79,  1530359673,  1530359700],
    [ 80,   81,  1530359711,  1530359740],
    [ 81,   83,  1530359750,  1530359779],
    [ 83,   84,  1530359789,  1530359817],
    [ 85,   86,  1530359829,  1530359856],
    [ 86,   88,  1530359867,  1530359896],
    [ 88,   89,  1530359906,  1530359935],
    [ 90,   91,  1530359945,  1530359974],
    [ 92,   93,  1530359985,  1530360012],
    [ 93,   94,  1530360023,  1530360052],
    [ 95,   96,  1530360062,  1530360091],
    [ 97,   98,  1530360101,  1530360130],
    [ 98,   99,  1530360141,  1530360168],
    [100,  101,  1530360180,  1530360208],
    [102,  103,  1530360218,  1530360247],
    [103,  104,  1530360257,  1530360286],
    [105,  106,  1530360296,  1530360324],
    [107,  108,  1530360336,  1530360363],
    [108,  109,  1530360374,  1530360403],
    [110,  111,  1530360413,  1530360442],
    [112,  113,  1530360452,  1530360480],
    [113,  114,  1530360492,  1530360519],
]

timestampListScan3 = [
    [274,  276,  1530364240,  1530364286],
    [277,  278,  1530364299,  1530364342],
    [279,  281,  1530364355,  1530364401],
    [281,  283,  1530364412,  1530364457],
    [284,  286,  1530364471,  1530364514],
    [286,  288,  1530364527,  1530364572],
    [289,  291,  1530364584,  1530364629],
    [291,  293,  1530364641,  1530364686],
    [294,  296,  1530364698,  1530364743],
    [296,  298,  1530364756,  1530364800],
    [299,  301,  1530364813,  1530364857],
    [301,  303,  1530364870,  1530364915],
    [304,  305,  1530364927,  1530364972],
    [306,  308,  1530364983,  1530365029],
    [308,  310,  1530365040,  1530365085],
    [311,  313,  1530365097,  1530365142],
    [313,  315,  1530365155,  1530365200],
    [316,  318,  1530365212,  1530365257],
    [318,  320,  1530365269,  1530365314],
]

timestampListScan4 = [
    [335,  337,  1530365656,  1530365702],
    [337,  339,  1530365716,  1530365760],
    [340,  342,  1530365775,  1530365818],
    [342,  344,  1530365833,  1530365877],
    [345,  347,  1530365891,  1530365935],
    [347,  349,  1530365949,  1530365993],
    [350,  352,  1530366006,  1530366051],
    [352,  354,  1530366064,  1530366110],
    [355,  357,  1530366123,  1530366166],
    [357,  359,  1530366181,  1530366225],
    [360,  362,  1530366239,  1530366283],
    [362,  364,  1530366296,  1530366341],
    [365,  367,  1530366354,  1530366400],
    [367,  369,  1530366413,  1530366458],
    [370,  372,  1530366471,  1530366515],
    [372,  374,  1530366529,  1530366573],
    [375,  377,  1530366587,  1530366631],
    [377,  379,  1530366644,  1530366689],
    [380,  382,  1530366703,  1530366748],
]

timestampListScan5 = [
    [ 98,  100,  1530397734,  1530397778],
    [101,  103,  1530397791,  1530397836],
    [103,  105,  1530397850,  1530397893],
    [106,  108,  1530397906,  1530397951],
    [108,  110,  1530397965,  1530398008],
    [111,  113,  1530398021,  1530398065],
    [113,  115,  1530398078,  1530398123],
    [116,  118,  1530398135,  1530398180],
    [118,  120,  1530398192,  1530398237],
    [121,  122,  1530398250,  1530398295],
    [123,  125,  1530398307,  1530398352],
    [125,  127,  1530398364,  1530398409],
    [128,  130,  1530398422,  1530398466],
    [130,  132,  1530398479,  1530398523],
    [133,  135,  1530398536,  1530398581],
    [135,  137,  1530398593,  1530398638],
    [138,  140,  1530398649,  1530398695],
    [140,  142,  1530398706,  1530398751],
    [143,  144,  1530398763,  1530398808],
]

timestampListScan6 = [
    [162,  164,  1530399225,  1530399270],
    [165,  167,  1530399283,  1530399328],
    [167,  169,  1530399341,  1530399387],
    [170,  172,  1530399400,  1530399445],
    [172,  174,  1530399458,  1530399503],
    [175,  177,  1530399516,  1530399560],
    [177,  179,  1530399575,  1530399618],
    [180,  182,  1530399631,  1530399676],
    [182,  184,  1530399690,  1530399735],
    [185,  187,  1530399748,  1530399793],
    [187,  189,  1530399806,  1530399851],
    [190,  192,  1530399864,  1530399908],
    [192,  194,  1530399921,  1530399966],
    [195,  197,  1530399980,  1530400025],
    [197,  199,  1530400038,  1530400083],
    [200,  202,  1530400096,  1530400141],
    [202,  204,  1530400154,  1530400198],
    [205,  207,  1530400213,  1530400256],
    [207,  209,  1530400270,  1530400315],
]

timestampListScan7 = [
    [232,  234,  1530400842,  1530400887],
    [234,  236,  1530400900,  1530400945],
    [237,  239,  1530400959,  1530401002],
    [239,  241,  1530401015,  1530401061],
    [242,  244,  1530401074,  1530401117],
    [244,  246,  1530401130,  1530401176],
    [247,  249,  1530401189,  1530401234],
    [249,  251,  1530401247,  1530401291],
    [252,  253,  1530401304,  1530401349],
    [254,  256,  1530401362,  1530401406],
    [256,  258,  1530401419,  1530401464],
    [259,  261,  1530401477,  1530401521],
    [261,  263,  1530401534,  1530401579],
    [264,  266,  1530401592,  1530401636],
    [266,  268,  1530401651,  1530401694],
    [269,  271,  1530401707,  1530401753],
    [271,  273,  1530401766,  1530401809],
    [274,  276,  1530401823,  1530401868],
    [276,  278,  1530401881,  1530401925],
]

timestampListScan8 = [
    [299,  301,  1530402405,  1530402449],
    [301,  303,  1530402462,  1530402507],
    [304,  306,  1530402519,  1530402564],
    [306,  308,  1530402577,  1530402621],
    [309,  311,  1530402634,  1530402679],
    [311,  313,  1530402692,  1530402736],
    [314,  315,  1530402749,  1530402794],
    [316,  318,  1530402806,  1530402851],
    [318,  320,  1530402864,  1530402908],
    [321,  323,  1530402921,  1530402966],
    [323,  325,  1530402979,  1530403023],
    [326,  328,  1530403036,  1530403081],
    [328,  330,  1530403095,  1530403138],
    [331,  333,  1530403151,  1530403196],
    [333,  335,  1530403210,  1530403253],
    [336,  338,  1530403266,  1530403312],
    [338,  340,  1530403325,  1530403368],
    [341,  343,  1530403382,  1530403427],
    [343,  345,  1530403438,  1530403483],
]

timestampListScan9 = [
    [53,  54,  1530406839,  1530406868],
    [55,  56,  1530406878,  1530406907],
    [56,  57,  1530406918,  1530406945],
    [58,  59,  1530406955,  1530406985],
    [60,  61,  1530406995,  1530407022],
    [61,  62,  1530407033,  1530407062],
    [63,  64,  1530407072,  1530407100],
    [64,  66,  1530407110,  1530407139],
    [66,  67,  1530407149,  1530407178],
    [68,  69,  1530407189,  1530407216],
    [69,  71,  1530407226,  1530407256],
    [71,  72,  1530407266,  1530407293],
    [73,  74,  1530407304,  1530407333],
    [74,  76,  1530407343,  1530407371],
    [76,  77,  1530407381,  1530407410],
    [78,  79,  1530407420,  1530407449],
    [79,  81,  1530407460,  1530407487],
    [81,  82,  1530407497,  1530407526],
    [83,  84,  1530407537,  1530407564],
    [84,  86,  1530407575,  1530407604],
    [86,  87,  1530407614,  1530407643],
    [88,  89,  1530407653,  1530407681],
    [89,  91,  1530407691,  1530407720],
    [91,  92,  1530407730,  1530407758],
    [93,  94,  1530407768,  1530407798],
]

timestampListScan10 = [
    [120,  121,  1530408401,  1530408428],
    [121,  123,  1530408439,  1530408468],
    [123,  124,  1530408478,  1530408507],
    [125,  126,  1530408517,  1530408545],
    [127,  128,  1530408557,  1530408584],
    [128,  129,  1530408594,  1530408624],
    [130,  131,  1530408634,  1530408663],
    [132,  133,  1530408673,  1530408702],
    [133,  134,  1530408712,  1530408740],
    [135,  136,  1530408750,  1530408780],
    [137,  138,  1530408790,  1530408819],
    [138,  139,  1530408829,  1530408858],
    [140,  141,  1530408868,  1530408896],
    [142,  143,  1530408908,  1530408935],
    [143,  144,  1530408946,  1530408975],
    [145,  146,  1530408985,  1530409014],
    [147,  148,  1530409024,  1530409053],
    [148,  149,  1530409064,  1530409091],
    [150,  151,  1530409102,  1530409131],
    [152,  153,  1530409141,  1530409170],
    [153,  155,  1530409180,  1530409209],
    [155,  156,  1530409219,  1530409247],
    [157,  158,  1530409259,  1530409287],
    [158,  160,  1530409297,  1530409326],
    [160,  161,  1530409336,  1530409365],
]

timestampListScan11 = [
    [184,  186,  1530409906,  1530409935],
    [186,  187,  1530409945,  1530409973],
    [188,  189,  1530409984,  1530410012],
    [189,  191,  1530410022,  1530410051],
    [191,  192,  1530410062,  1530410089],
    [193,  194,  1530410100,  1530410129],
    [194,  196,  1530410139,  1530410168],
    [196,  197,  1530410177,  1530410206],
    [198,  199,  1530410216,  1530410245],
    [199,  201,  1530410255,  1530410283],
    [201,  202,  1530410295,  1530410322],
    [203,  204,  1530410333,  1530410362],
    [204,  206,  1530410372,  1530410401],
    [206,  207,  1530410411,  1530410440],
    [208,  209,  1530410451,  1530410478],
    [209,  211,  1530410489,  1530410518],
    [211,  212,  1530410528,  1530410557],
    [213,  214,  1530410567,  1530410596],
    [214,  216,  1530410607,  1530410634],
    [216,  217,  1530410644,  1530410674],
    [218,  219,  1530410684,  1530410711],
    [219,  221,  1530410722,  1530410751],
    [221,  222,  1530410761,  1530410789],
    [223,  224,  1530410799,  1530410828],
    [224,  226,  1530410838,  1530410867],
]

timestampListScan12 = [
    [234,  235,  1530411064,  1530411093],
    [236,  237,  1530411103,  1530411131],
    [237,  239,  1530411143,  1530411170],
    [239,  240,  1530411181,  1530411210],
    [241,  242,  1530411220,  1530411249],
    [242,  244,  1530411259,  1530411287],
    [244,  245,  1530411299,  1530411326],
    [246,  247,  1530411336,  1530411366],
    [247,  249,  1530411376,  1530411405],
    [249,  250,  1530411415,  1530411444],
    [251,  252,  1530411454,  1530411482],
    [252,  254,  1530411492,  1530411521],
    [254,  255,  1530411532,  1530411561],
    [256,  257,  1530411571,  1530411600],
    [258,  259,  1530411610,  1530411638],
    [259,  260,  1530411650,  1530411677],
    [261,  262,  1530411688,  1530411717],
    [263,  264,  1530411727,  1530411756],
    [264,  265,  1530411766,  1530411794],
    [266,  267,  1530411806,  1530411833],
    [268,  269,  1530411843,  1530411873],
    [269,  270,  1530411883,  1530411912],
    [271,  272,  1530411922,  1530411950],
    [273,  274,  1530411961,  1530411989],
    [274,  275,  1530411999,  1530412028],
]

timestampListScan13 = [
    [802,  803,  1530424294,  1530424324],
    [803,  805,  1530424334,  1530424363],
    [805,  806,  1530424373,  1530424402],
    [807,  808,  1530424412,  1530424440],
    [808,  810,  1530424452,  1530424479],
    [810,  811,  1530424490,  1530424519],
    [812,  813,  1530424529,  1530424557],
    [813,  815,  1530424567,  1530424596],
    [815,  816,  1530424606,  1530424634],
    [817,  818,  1530424644,  1530424673],
    [818,  820,  1530424683,  1530424713],
    [820,  821,  1530424721,  1530424750],
    [822,  823,  1530424761,  1530424788],
    [823,  825,  1530424798,  1530424828],
    [825,  826,  1530424838,  1530424867],
    [827,  828,  1530424877,  1530424905],
    [828,  830,  1530424915,  1530424944],
    [830,  831,  1530424954,  1530424982],
    [832,  833,  1530424992,  1530425021],
    [833,  834,  1530425032,  1530425059],
    [835,  836,  1530425069,  1530425099],
    [837,  838,  1530425109,  1530425138],
    [838,  839,  1530425148,  1530425176],
    [840,  841,  1530425186,  1530425215],
    [842,  843,  1530425225,  1530425253],
]

timestampListScan14 = [
    [853,  854,  1530425492,  1530425521],
    [855,  856,  1530425531,  1530425561],
    [856,  858,  1530425571,  1530425598],
    [858,  859,  1530425610,  1530425638],
    [860,  861,  1530425648,  1530425677],
    [861,  863,  1530425687,  1530425716],
    [863,  864,  1530425727,  1530425756],
    [865,  866,  1530425766,  1530425794],
    [866,  868,  1530425805,  1530425833],
    [868,  869,  1530425843,  1530425872],
    [870,  871,  1530425883,  1530425912],
    [871,  873,  1530425922,  1530425950],
    [873,  874,  1530425961,  1530425989],
    [875,  876,  1530425999,  1530426028],
    [876,  878,  1530426038,  1530426068],
    [878,  879,  1530426078,  1530426107],
    [880,  881,  1530426117,  1530426145],
    [881,  883,  1530426155,  1530426184],
    [883,  884,  1530426194,  1530426223],
    [885,  886,  1530426234,  1530426263],
    [887,  888,  1530426273,  1530426301],
    [888,  889,  1530426312,  1530426340],
    [890,  891,  1530426350,  1530426379],
    [892,  893,  1530426390,  1530426419],
    [893,  894,  1530426429,  1530426457],
]

runs2018 = [
#    ['318984', [ 
#                 ['Scan1', timestampListScan1],
#                 ['Scan2', timestampListScan2],
#                 ['Scan3', timestampListScan3],
#                 ['Scan4', timestampListScan4],
#               ],
    ['319018', [ 
                 ['Scan5', timestampListScan5],
                 ['Scan6', timestampListScan6],
                 ['Scan7', timestampListScan7],
                 ['Scan8', timestampListScan8]
               ]
    ],
#    ['319019', [ 
#                 ['Scan9' , timestampListScan9 ],
#                 ['Scan10', timestampListScan10],
#                 ['Scan11', timestampListScan11],
#                 ['Scan12', timestampListScan12],
#                 ['Scan13', timestampListScan13],
#                 ['Scan14', timestampListScan14]
#               ]
#    ]
]



################
##### MAIN #####
################

### Datasets and runs
datasets2018 = [
    '/ZeroBias1/Run2018B-12Nov2019_UL2018_LUM-v2/AOD',
    '/ZeroBias2/Run2018B-12Nov2019_UL2018_LUM-v2/AOD',
    '/ZeroBias3/Run2018B-12Nov2019_UL2018_LUM-v2/AOD',
    '/ZeroBias4/Run2018B-12Nov2019_UL2018_LUM-v2/AOD',
    '/ZeroBias5/Run2018B-12Nov2019_UL2018_LUM-v2/AOD',
    '/ZeroBias6/Run2018B-12Nov2019_UL2018_LUM-v2/AOD',
    '/ZeroBias7/Run2018B-12Nov2019_UL2018_LUM-v2/AOD',
    '/ZeroBias8/Run2018B-12Nov2019_UL2018_LUM-v2/AOD',
]

# Loop on runs
for run in runs2018:
    print 'Run:', run[0]
 
    # Filter files that contain this run from all datasets
    allfiles = []   
    for dataset in datasets2018:
        print '  Doing dataset:', dataset

        command = 'dasgoclient -query="file dataset=%s run=%s" ' % (dataset,run[0])
        tmp_files = os.popen(command).read()
        tmp_files = tmp_files.split('\n')
        print '   tmp files:', len(tmp_files)
        allfiles += tmp_files

    print '  Tot files Before cleaning:', len(allfiles)

    # Now filter files that contain interesting lumis
    for lumiRange in run[1]:
        LsTimestampList = lumiRange[1] # List of timestamps and corresponding LSs

        # Write the selected files in a .py file as a python list
        fout = open('filelist_2018_Run'+run[0]+'_'+lumiRange[0]+'_timestamps.py','w')

        # Loop on all timestamps to get the files to be saved
        for timestamp in LsTimestampList:
            beginLS   = timestamp[0]
            endLS     = timestamp[1]
            beginTime = timestamp[2]
            endTime   = timestamp[3]

            newfiles = []
            for file in allfiles:

                if len(file) == 0: continue
                command = 'dasgoclient -query="lumi file=%s run=%s" ' % (file,run[0])
                stringLS = os.popen(command).read().strip() # string cotaining all the LS in the file
                if 'ERROR' in stringLS:
                    print 'ERROR for file:', file, ' --> skipping!'
                    continue
                LSs = getLSlist(stringLS)

                # Check if ANY of the LS in the file is a 'good' one so the file must be saved
                goodfile = False
                for ls in LSs:
                    if ls >= beginLS and ls <= endLS:
                        goodfile = True

                if goodfile:
                    newfiles.append(file)

            print '      Files after cleaning for this timestamp:', len(newfiles), ' at:', datetime.datetime.now()

            # Create a list of good files for each timestamp
            fout.write('\n')
            fout.write('file_list_%s_%s = [\n' % (beginTime, endTime) )
            for file in newfiles:
                fout.write('\'file:/eos/cms%s\',\n' % file )
            fout.write(']\n')

        # Close file at the end of the Scan
        fout.close()

#import pdb; pdb.set_trace()


