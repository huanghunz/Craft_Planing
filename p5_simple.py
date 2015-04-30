

from collections import namedtuple
import json
with open('simpleCraft.json') as f:
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
print
print Crafting['Recipes']['craft wooden_pickaxe at bench']
print
# example:
# {    'Produces': {'stone_pickaxe': 1},
#    'Requires': {'bench': True},
#    'Consumes': {'cobble': 3, 'stick': 2},
#    'Time': 1
# }

Recipe = namedtuple('Recipe',['name','check','effect','cost'])
all_recipes = []

#Where are make_checker and make_effector defined? You have to do that as well:

def make_checker(rule):
    # this code runs once
      # do something with rule['Consumes'] and rule['Requires']
    def check(state):
        # this code runs millions of times
        return True # or False
    return True

def make_effector(rule):
  # this code runs once
  # do something with rule['Produces'] and rule['Consumes']
  	def effect(state):
       # this code runs millions of times
		return next_state
	return rule['Produces'] # check

# print Crafting['Recipes'].items()
for name, rule in Crafting['Recipes'].items():
	checker = make_checker(rule)
	effector = make_effector(rule)
	recipe = Recipe(name, checker, effector, rule['Time'])
	all_recipes.append(recipe)



