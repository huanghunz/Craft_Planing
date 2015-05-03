

from collections import namedtuple
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q

# # List of items that can be in your inventory:
# print Crafting['Items']
# # example: ['bench', 'cart', ..., 'wood', 'wooden_axe', 'wooden_pickaxe']

# # List of items in your initial inventory with amounts:
# print Crafting['Initial']
# # {'coal': 4, 'plank': 1}

# # List of items needed to be in your inventory at the end of the plan:
# # (okay to have more than this; some might be satisfied by initial inventory)
# print Crafting['Goal']
# # {'stone_pickaxe': 2}

# # Dictionary of crafting recipes:
# print
# print Crafting['Recipes']['craft wooden_pickaxe at bench']
# print
# example:
# {    'Produces': {'stone_pickaxe': 1},
#    'Requires': {'bench': True},
#    'Consumes': {'cobble': 3, 'stick': 2},
#    'Time': 1
# }


#Where are make_checker and make_effector defined? You have to do that as well:

def make_checker(rule):
	con = rule.get('Consumes', [])
	req = rule.get('Requires', [])  
   
	def check(state):
		"""
		Check if the inventory/state contains the items, 
		If tool requirement is met, check Consumes items, 
		If the Consumes items requirement is met, return True, else return False
		"""
		# checking if the state has all the requirement
        # this code runs millions of times
		
		found =  False
		items =  list(state[1])

		for r in req:
			found = False
			for each_item in items:
				if r in each_item[0]:
					found = True
					break 

			if not found:
				return False

		for c in con:
			found = False
			for each_item in items:
				if c in each_item[0]:
					if con[c] <= each_item[1]:
						found = True
						break
			if not found:
				return False

		return True


	# convert tuple to list and then list to tuple
	# state  = ( 10, (('a', 1), ('c', 3), ('b', 2)) ) # nice inventory

	# items =  state[1]
	# print items

	# items = list(items)
	# print "list: ", items

	# items = tuple (items)
	# print "tuple == ", items 

	return check
	

def make_effector(rule):
	"""
		
	"""
	def effect(state): # to a list, then to dict, change value, and then reverse
       # this code runs millions of times
		next_state = state
		item_list = list(state[1]) # (name, count)
		items = dict(item_list)
		print items
		gone = []

		for c in con:
			if c in items:
				items[c] = items[c] - con[c]
				if items[c] == 0:
					gone.append(c)
				elif items[c] < 0:
					print "Error: not enough ", c, " to produce effect"
			else:
				print "Error: ", c, " not in this effect"
		
		#add produced items to new state
		for p in pro:
			if p in items:
				items[p] += pro[p]
			else:
				items[p] = pro[p]
		
		#remove values that you no longer have any of
		for item in gone:
			del items[item]
			
		next_state = (state[0], tuple(items.items()))
		
		return next_state

	# this code runs once
	# do something with rule['Produces'] and rule['Consumes']
	con = rule.get('Consumes', [])
	pro = rule.get('Produces', [])  


	tempState = ( 10 , [('plank', 3), ('wood', 1)])	  

	test = effect(tempState)
	print test
	
	return effect


def search(graph, initial, is_goal, limit, heuristic):
	total_cost = 0
	plan = []
	priorityQueue = Q.PriorityQueue()

	return total_cost, plan


def t_graph(state):
	print " in graph ==== "
	for next_state, cost in edges.items():
	    yield ((state,next_state), next_state, cost)

def t_is_goal(state):
	print "in goal"
	return state == 'c'

def t_heuristic(state):
	print " in heuristic"
	return 0


if __name__ ==  '__main__':
	import json
	with open('simpleCraft.json') as f:
		Crafting = json.load(f)


	Recipe = namedtuple('Recipe',['name','check','effect','cost'])
	print Recipe
	all_recipes = []

	for action, rule in Crafting['Recipes'].items():
		checker = make_checker(rule)
		effector = make_effector(rule)
		recipe = Recipe(action, checker, effector, rule['Time'])
		all_recipes.append(recipe)
	

	t_initial = 'a'
	t_limit = 20
	edges = {'a': {'b':1,'c':10}, 'b':{'c':1}}

	stuff, a_list = search (t_graph, t_initial, t_is_goal, t_limit, t_heuristic)

	print "Done"




