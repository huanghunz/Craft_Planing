import json
with open('Crafting.json') as f:
    Crafting = json.load(f)

# List of items that can be in your inventory:
print Crafting['Items']
# example: ['bench', 'cart', ..., 'wood', 'wooden_axe', 'wooden_pickaxe']

# List of items in your initial inventory with amounts:
print Crafting['Initial']
# {'coal': 4, 'plank': 1}

# List of items needed to be in your inventory at the end of the plan:
# (okay to have more than this; some might be satisfied by initial inventory)
print Crafting['Goal']
# {'stone_pickaxe': 2}

# Dictionary of crafting recipes:
print Crafting['Recipes']['craft stone_pickaxe at bench']
# example:
# {    'Produces': {'stone_pickaxe': 1},
#    'Requires': {'bench': True},
#    'Consumes': {'cobble': 3, 'stick': 2},
#    'Time': 1
# }
