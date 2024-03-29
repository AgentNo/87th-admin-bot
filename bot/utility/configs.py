# enums.py
# Collections of shared enums such as reactions, role IDs etc.

###########
## ROLES ##
###########

BOT_USER_ROLE = 1106690316448317562

GRANTABLE_ROLES = {
    "merc": 743881676467470376,
    "rep": 743881155442376746,
    "visitor": 744919071098667020,
    "unassigned": 743881620154744882,
    "regiment": 743156110625603654,
    "enlistment": [
        788813932398641172,
        816680476256501813,
        743869775012298882,
        743156110625603654,
        744181436298297435,
        744890961464655992,
        744178737934893057,
        853414165694906408,
        743903165383966761,
        743883052081479740
    ]
}


#############
## CONFIGS ##
#############


EVENT_ANNOUNCEMENT_CONFIG = {
    "Monday": {
        "numEvents": 0
    },
    "Tuesday": {
        "numEvents": "one event",
        "eventBody": "- 19:00 GMT / 14:00 EST: 63e Tuesday Siege",
        "reactions": "<:RegimentalColours:863525506779054120> if you are attending the 63e event\n❓ if you are unsure of your attendance\n❌ if you cannot attend today"
    },
    "Wednesday": {
        "numEvents": 0
    },
    "Thursday": {
        "numEvents": 0
    },
    "Friday": {
        "numEvents": "one event",
        "eventBody": "- 19:00 GMT / 14:00 EST: 28steON Friday Linebattle",
        "reactions": "<:RegimentalColours:863525506779054120> if you are attending the 28steON event\n❓ if you are unsure of your attendance\n❌ if you cannot attend today"
    },
    "Saturday": {
        "numEvents": "one event",
        "eventBody": "- 20:00 GMT / 15:00 EST: 26th Saturday Linebattle",
        "reactions": "<:RegimentalColours:863525506779054120> if you are attending the 26th event\n❓ if you are unsure of your attendance\n❌ if you cannot attend today" 
    },
    "Sunday": {
        "numEvents": "one event",
        "eventBody": "- 19:00 GMT / 14:00 EST: KRA Sunday Linebattle",
        "reactions": "<:RegimentalColours:863525506779054120> if you are attending the KRA event\n❓ if you are unsure of your attendance\n❌ if you cannot attend today"
    }
}

PRIMARY_SIGNUP_REACTIONS = [
    '<:RegimentalColours:863525506779054120>',
    '❓',
    '❌'
]

SECONDARY_SIGNUP_REACTIONS = [
    '<:KingsColours:863525505515782184>',
    '❔',
    '❎'
]

TERTIARY_SIGNUP_REACTIONS = [
    '<:UnionColours:746464693400371220>',
    '<:Cringe_Pepe:973337254946811935>',
    '<:crying:816636872960901130>'
]

GAME_ROLE_REACTIONS = {
    "\U0001f52a": 813521936944463962,
    "\U0001f52b": 813521934150270996,
    "\U0001f482": 813521937292591146,
    "\U0001f98a": 829726113923203072,
    "\U0001f694": 853734746030473247,
    "\U0001f4b0": 813836832298369034,
    "\U0001f9f1": 813844908241584149,
    "\U0001f973": 853734908701835335,
    "\U0001f47b": 813521937014849606,
    "\U0001f920": 813836836820484166,
    "\U0001f95c": 813836836601724948,
    "\u26f5": 813836834173878324,
    "\U0001f991": 820410240250937385,
    "\U0001f6ec": 820409790731386910,
    "\U0001fae3": 1173034915135225876,
    "\U0001f451": 1173339047469514783,
    "\U0001f310": 1173339378106511511,
    "\U0001f480": 1190445919179649126,
    "\U0001fA93": 1190449882750783489
}

ATTENDANCE_TRACKING_MAPPINGS = {
    "months": {
        1: 58,
        2: 59,
        3: 60,
        4: 61,
        5: 62,
        6: 63,
        7: 64,
        8: 65,
        9: 66,
        10: 67,
        11: 68,
        12: 69
    },
    "days": {
        1: "C",
        2: "D",
        3: "E",
        4: "F",
        5: "G",
        6: "H",
        7: "I",
        8: "J",
        9: "K",
        10: "L",
        11: "M",
        12: "N",
        13: "O",
        14: "P",
        15: "Q",
        16: "R",
        17: "S",
        18: "T",
        19: "U",
        20: "V",
        21: "W",
        22: "X",
        23: "Y",
        24: "Z",
        25: "AA",
        26: "AB",
        27: "AC",
        28: "AD",
        29: "AE",
        30: "AF",
        31: "AG",
    }
}

##############
## CHANNELS ##
##############

EVENT_ANNOUNCEMENT_CHANNEL_ID = 744708888250810459
TEST_CHANNEL_ID = 1114539801501241425
