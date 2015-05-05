

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
all_recipes = []
Crafting = None

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
		item_list =  list(state[1])
		items = dict(item_list)

		for r in req:
			found = False
			if r in items:
				found = True

			if not found:
				return False

		for c in con:
			found = False
			if c in items:
				if con[c] <= items[c]:
					found = True
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
	
	return effect


def search(graph, initial, is_goal, limit, heuristic):
	total_cost = 0
	plan = []
	prev = {initial: None}
	recs = {initial: None}
	#prevRecipe = {initial: None}
	priorityQueue = Q.PriorityQueue()

	priorityQueue.put(initial)

	#state(5, (('a', 1), ('b', 2)))

	run = 0
	while not priorityQueue.empty() and run < limit:
		currState = priorityQueue.get()

		if is_goal(currState):

			#build path
			while currState:
				plan.append(currState)
				#plan.append((currState, recs[currState]))
				currState = prev[currState]

			plan.reverse()
			break

		adj = graph(currState)

		for state in adj:
			if state[0] not in prev: # or node[0] < heuristic(node) : #heuristic
				priorityQueue.put(state[0])
				prev[state[0]] = currState
				recs[state[0]] = state[1]

		run += 1



	total_cost = plan[-1][0]

	return total_cost, plan


def t_graph(state):
	#print " in graph ==== "
	adj = []
	for recipe in all_recipes:
		if recipe[1](state):
			#print state
			newState = recipe[2](state)
			newState = (newState[0] + recipe[3], newState[1])
			adj.append((newState, recipe[0]))
	return adj

def t_is_goal(state):
	#print "in goal"
	item_list = list(state[1]) # (name, count)
	items = dict(item_list)

	goals = Crafting['Goal']

	for goal in goals:
		if goal not in items or items[goal] < goals[goal]:
			return False
	return True

def t_heuristic(state):
	print " in heuristic"
	return 0


if __name__ ==  '__main__':
	import json
	with open('Crafting.json') as f:
		Crafting = json.load(f)


	Recipe = namedtuple('Recipe',['name','check','effect','cost'])

	for action, rule in Crafting['Recipes'].items():
		checker = make_checker(rule)
		effector = make_effector(rule)
		recipe = Recipe(action, checker, effector, rule['Time'])
		all_recipes.append(recipe)
	

	#t_initial = 'a'
	#t_limit = 20
	#edges = {'a': {'b':1,'c':10}, 'b':{'c':1}}

	#Crafting['Initial'] = {'bench': 1, 'plank': 3, 'stick': 2}
	Crafting['Goal'] =  {'furnace': 1}

	initState = (0, tuple(Crafting['Initial'].items()))

	#print t_is_goal(initState)
	#print all_recipes[0][1](initState)

	stuff, a_list = search (t_graph, initState, t_is_goal, float("inf"), t_heuristic)

	print stuff
	for rec in a_list:
		print rec
	print len(a_list)

	print "Done"




