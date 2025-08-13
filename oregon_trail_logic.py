"""
Oregon Trail Game Logic Map
--------------------------
This file defines the game progression, events, choices, and consequences
for an Oregon Trail style game. Each event contains text, choices, and outcomes.
"""

# Game state tracking
GAME_STATE = {
    "month": "March",  # Starting month
    "weather": "mild",
    "pace": "steady",
    "rations": "filling",
    "health": 100,
    "food": 200,
    "money": 1600,
    "oxen": 4,
    "spare_parts": {
        "wagon_wheels": 2,
        "wagon_axles": 2,
        "wagon_tongues": 2
    },
    "medicine": 2,
    "clothing": 4,
    "party_members": [
        {"name": "", "health": 100, "status": "healthy"},  # Leader
        {"name": "", "health": 100, "status": "healthy"},
        {"name": "", "health": 100, "status": "healthy"},
        {"name": "", "health": 100, "status": "healthy"},
        {"name": "", "health": 100, "status": "healthy"}
    ]
}

# Starting choices
INITIAL_SETUP = {
    "profession_choice": {
        "text": "Many kinds of people made the trip to Oregon.\nYou may:",
        "choices": [
            {"text": "Be a banker from Boston", "starting_money": 1600},
            {"text": "Be a carpenter from Ohio", "starting_money": 800},
            {"text": "Be a farmer from Illinois", "starting_money": 400}
        ]
    },
    "month_choice": {
        "text": "When would you like to leave?",
        "choices": [
            {"text": "March", "weather": "wet", "grass": "poor"},
            {"text": "April", "weather": "wet", "grass": "good"},
            {"text": "May", "weather": "good", "grass": "good"},
            {"text": "June", "weather": "good", "grass": "fair"},
            {"text": "July", "weather": "hot", "grass": "poor"}
        ]
    }
}

# Store prices at different locations
STORE_PRICES = {
    "independence": {
        "oxen": 40,  # per ox
        "food": 0.20,  # per pound
        "clothing": 10,  # per set
        "ammunition": 2,  # per box
        "spare_parts": 10,  # per part
        "medicine": 2  # per bottle
    },
    "fort_kearney": {
        "multiplier": 1.25  # Prices are 25% higher
    },
    "fort_laramie": {
        "multiplier": 1.5  # Prices are 50% higher
    }
}

# Major landmarks and distances
LANDMARKS = [
    {
        "name": "Independence, Missouri",
        "distance": 0,
        "description": "Your journey begins in Independence, Missouri, the last stop for supplies before heading west.",
        "events": ["shop", "talk_to_locals", "check_supplies"],
        "next_landmark": "Kansas River Crossing"
    },
    {
        "name": "Kansas River Crossing",
        "distance": 102,
        "description": "You've reached the Kansas River. You must cross it to continue.",
        "events": ["river_crossing"],
        "choices": [
            {"text": "Attempt to ford the river", "risk": "medium"},
            {"text": "Take the ferry across ($5)", "cost": 5},
            {"text": "Wait for better weather", "delay": 2}
        ],
        "next_landmark": "Big Blue River Crossing"
    },
    {
        "name": "Big Blue River Crossing",
        "distance": 185,
        "description": "The Big Blue River lies ahead. The water looks deep.",
        "events": ["river_crossing"],
        "next_landmark": "Fort Kearney"
    },
    {
        "name": "Fort Kearney",
        "distance": 304,
        "description": "Fort Kearney offers supplies and a chance to rest.",
        "events": ["shop", "rest", "talk_to_locals"],
        "next_landmark": "Chimney Rock"
    }
]

# Random events that can occur between landmarks
RANDOM_EVENTS = [
    {
        "type": "weather",
        "events": [
            {
                "name": "Heavy Rain",
                "description": "Heavy rains have made the trail muddy. Travel will be slower.",
                "effects": {
                    "pace": -1,
                    "health": -2
                },
                "choices": [
                    {"text": "Continue at a slower pace", "effect": "minimal_damage"},
                    {"text": "Push through at normal pace", "effect": "wagon_damage"},
                    {"text": "Wait it out", "effect": "delay_journey"}
                ]
            },
            {
                "name": "Blizzard",
                "description": "A sudden blizzard has struck!",
                "effects": {
                    "food": -25,
                    "health": -10
                }
            }
        ]
    },
    {
        "type": "health",
        "events": [
            {
                "name": "Cholera",
                "description": "A member of your party has cholera!",
                "choices": [
                    {"text": "Rest for 3 days", "effect": "might_heal"},
                    {"text": "Press on", "effect": "might_die"},
                    {"text": "Use medicine", "effect": "will_heal", "requires": "medicine"}
                ]
            },
            {
                "name": "Broken Arm",
                "description": "Someone has broken their arm!",
                "effects": {
                    "health": -20
                }
            }
        ]
    },
    {
        "type": "supplies",
        "events": [
            {
                "name": "Broken Wagon Wheel",
                "description": "One of your wagon wheels has broken!",
                "choices": [
                    {"text": "Use spare part", "effect": "fix_wagon", "requires": "wagon_wheel"},
                    {"text": "Try to repair", "effect": "might_fix"},
                    {"text": "Continue with damage", "effect": "slower_pace"}
                ]
            },
            {
                "name": "Food Spoilage",
                "description": "Some of your food has spoiled.",
                "effects": {
                    "food": -50
                }
            }
        ]
    }
]

# Special encounters
SPECIAL_ENCOUNTERS = [
    {
        "name": "Native American Traders",
        "description": "You encounter a friendly Native American trading party.",
        "choices": [
            {"text": "Trade with them", "effect": "trade_options"},
            {"text": "Continue on your way", "effect": "no_effect"}
        ],
        "trade_options": [
            {"give": "clothing", "receive": "food", "ratio": "1:20"},
            {"give": "ammunition", "receive": "food", "ratio": "1:15"}
        ]
    },
    {
        "name": "Abandoned Wagon",
        "description": "You find an abandoned wagon by the trail.",
        "choices": [
            {"text": "Search for supplies", "effect": "might_find_supplies"},
            {"text": "Take wagon parts", "effect": "gain_parts"},
            {"text": "Leave it alone", "effect": "no_effect"}
        ]
    }
]

# Hunting mini-game
HUNTING = {
    "animals": [
        {"name": "Buffalo", "food": 500, "difficulty": "hard"},
        {"name": "Deer", "food": 150, "difficulty": "medium"},
        {"name": "Rabbit", "food": 5, "difficulty": "easy"}
    ],
    "success_rates": {
        "easy": 0.8,
        "medium": 0.5,
        "hard": 0.2
    },
    "ammunition_required": {
        "Buffalo": 2,
        "Deer": 1,
        "Rabbit": 1
    }
}

# End game scenarios
END_GAME_CONDITIONS = {
    "victory": {
        "reach_oregon": "You've reached Oregon! Your journey is complete.",
        "good_health": "Your party survived in good health.",
        "supplies_remaining": "You have supplies remaining."
    },
    "failure": {
        "all_dead": "Your entire party has died.",
        "out_of_time": "Winter has arrived. You cannot continue.",
        "no_food": "You have run out of food and starved.",
        "no_oxen": "All your oxen have died. You cannot continue."
    }
}

# Scoring system
SCORING = {
    "base_points": {
        "banker": 1.0,
        "carpenter": 2.0,
        "farmer": 3.0
    },
    "multipliers": {
        "party_health": {
            "excellent": 1.5,
            "good": 1.2,
            "fair": 1.0,
            "poor": 0.8
        },
        "supplies_remaining": {
            "abundant": 1.3,
            "sufficient": 1.1,
            "scarce": 0.9
        },
        "time_taken": {
            "early": 1.4,
            "on_time": 1.0,
            "late": 0.7
        }
    }
}

# Tips and advice that can be received from other travelers
TRAIL_ADVICE = [
    "The Platte River is too shallow for rafting. Better to ford it.",
    "Buffalo chips make good fuel for fires when wood is scarce.",
    "Keep your powder dry and your food covered during rain.",
    "Indians are often willing to help lost or starving travelers.",
    "Hunting is good near the river, but watch for quicksand.",
    "Many have died trying to float the Columbia River.",
    "Some roots along the trail can be eaten in emergencies.",
    "Snow in the mountains can trap you until spring.",
    "Trading with Indians can save your life if you run low on food.",
    "Don't drink river water without boiling it first."
]

# Weather patterns by month and region
WEATHER_PATTERNS = {
    "March": {
        "plains": {"rain": 0.4, "snow": 0.2, "clear": 0.4},
        "mountains": {"rain": 0.2, "snow": 0.6, "clear": 0.2}
    },
    "April": {
        "plains": {"rain": 0.5, "snow": 0.1, "clear": 0.4},
        "mountains": {"rain": 0.3, "snow": 0.4, "clear": 0.3}
    },
    "May": {
        "plains": {"rain": 0.4, "snow": 0.0, "clear": 0.6},
        "mountains": {"rain": 0.4, "snow": 0.2, "clear": 0.4}
    },
    "June": {
        "plains": {"rain": 0.3, "snow": 0.0, "clear": 0.7},
        "mountains": {"rain": 0.3, "snow": 0.1, "clear": 0.6}
    },
    "July": {
        "plains": {"rain": 0.2, "snow": 0.0, "clear": 0.8},
        "mountains": {"rain": 0.2, "snow": 0.0, "clear": 0.8}
    }
}

# River crossing difficulties based on season and recent weather
RIVER_CONDITIONS = {
    "depth_multiplier": {
        "dry": 0.7,
        "normal": 1.0,
        "wet": 1.5,
        "flood": 2.0
    },
    "crossing_methods": {
        "ford": {
            "max_depth": 3,  # feet
            "risk": "medium"
        },
        "float": {
            "max_depth": 20,  # feet
            "risk": "high"
        },
        "ferry": {
            "cost": 5,  # dollars
            "risk": "low"
        },
        "wait": {
            "days": 2,
            "food_cost": 10  # per person
        }
    }
}

# Disease risks and prevention
DISEASES = {
    "cholera": {
        "risk": 0.1,
        "prevention": ["clean_water", "rest"],
        "treatment": ["medicine", "rest"],
        "mortality": 0.5
    },
    "dysentery": {
        "risk": 0.15,
        "prevention": ["clean_water", "food"],
        "treatment": ["medicine", "rest"],
        "mortality": 0.3
    },
    "measles": {
        "risk": 0.05,
        "prevention": ["isolation"],
        "treatment": ["rest"],
        "mortality": 0.1
    },
    "typhoid": {
        "risk": 0.08,
        "prevention": ["clean_water"],
        "treatment": ["medicine", "rest"],
        "mortality": 0.4
    }
} 