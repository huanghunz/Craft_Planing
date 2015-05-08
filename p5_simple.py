from collections import namedtuple, Counter
import time, copy
TIME_LIMIT = 30
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


all_recipes = {}
recipe_dict = Counter()
Crafting = None

maxes = {}


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

		for r in req:
			if r not in state[1]:
				return False

		for c in con:
			if c not in state[1] or con[c] > state[1][c]:
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
		items = copy.copy(state[1])
		gone = []
	
		for c in con:
			#if c in items:
			items[c] = items[c] - con[c]
			if items[c] == 0:
				del items[c]
			# 	elif items[c] < 0:
			# 		print "Error: not enough ", c, " to produce effect"
			# else:
			# 	print "Error: ", c, " not in this effect"
				
		
		#add produced items to new state
		for p in pro:
			if p in items:
				items[p] += pro[p]
			else:
				items[p] = pro[p]
	
			
		next_state = (state[0], items)
		
		return next_state

	# this code runs once
	# do something with rule['Produces'] and rule['Consumes']
	con = rule.get('Consumes', [])
	pro = rule.get('Produces', [])  
	
	return effect

def recipe_pruner(state):
	recs = copy.copy(all_recipes)

	#first remove redundant recipes
	if 'iron_axe' in state:
		del recs['punch for wood']
		del recs['wooden_axe for wood']
		del recs['stone_axe for wood']
		#remove the less efficient axes if not in goal
		if 'iron_axe' not in Crafting['Goal']:
			del recs['craft iron_axe at bench']
		if 'stone_axe' not in Crafting['Goal']:
			del recs['craft stone_axe at bench']
		if 'wooden_axe' not in Crafting['Goal']:
			del recs['craft wooden_axe at bench']

	elif 'stone_axe' in state:
		del recs['punch for wood']
		del recs['wooden_axe for wood']
		if 'stone_axe' not in Crafting['Goal']:
			del recs['craft stone_axe at bench']
		if 'wooden_axe' not in Crafting['Goal']:
			del recs['craft wooden_axe at bench']
	elif 'wooden_axe' in state:
		del recs['punch for wood']
		if 'wooden_axe' not in Crafting['Goal']:
			del recs['craft wooden_axe at bench']

	if 'iron_pickaxe' in state:
		del recs['wooden_pickaxe for cobble']
		del recs['wooden_pickaxe for coal']
		del recs['stone_pickaxe for cobble']
		del recs['stone_pickaxe for coal']
		del recs['stone_pickaxe for ore']
		if 'iron_pickaxe' not in Crafting['Goal']:
			del recs['craft iron_pickaxe at bench']
		if 'stone_pickaxe' not in Crafting['Goal']:
			del recs['craft stone_pickaxe at bench']
		if 'wooden_pickaxe' not in Crafting['Goal']:
			del recs['craft wooden_pickaxe at bench']
	elif 'stone_pickaxe' in state:
		del recs['wooden_pickaxe for cobble']
		del recs['wooden_pickaxe for coal']
		if 'stone_pickaxe' not in Crafting['Goal']:
			del recs['craft stone_pickaxe at bench']
		if 'wooden_pickaxe' not in Crafting['Goal']:
			del recs['craft wooden_pickaxe at bench']
	elif 'wooden_pickaxe' in state and 'wooden_pickaxe' not in Crafting['Goal']:
		del recs['craft wooden_pickaxe at bench']	

	#remove tools that aren't necessary to have more than 1 of
	if 'bench' in state and 'bench' not in Crafting['Goal']:
		del recs['craft bench']

	if 'furnace' in state and 'furnace' not in Crafting['Goal']:
		del recs['craft furnace at bench']	



	return recs

def search(graph, initial, is_goal, limit, heuristic):
	total_cost = 0
	plan = []
	prev = {initial: None}
	step = {initial: None}

	priorityQueue = Q.PriorityQueue()

	priorityQueue.put(initial)

	t_now = time.time()
	t_deadline = t_now + TIME_LIMIT


	run = 0
	while not priorityQueue.empty():# and t_now < t_deadline:
		currState = priorityQueue.get()

		currStateDict = dict(list(currState[1]))

		if is_goal(currStateDict):
			break

		valid_recs = recipe_pruner(currStateDict)
		# getting a list of possible states
		adj = graph((currState[0], currStateDict), valid_recs)

		for state in adj:
			if heuristic(state[0][1]) == 0:
				state = ((state[0][0], tuple(state[0][1].items())), state[1] )
				if state[0] not in prev: 
					priorityQueue.put(state[0])
					prev[state[0]] = currState
					step[state[0]] = state[1]

		run += 1
		t_now = time.time()

	
	#if t_now > t_deadline:
	#	print "time out"
	#	print currState
	#	total_cost = -1

	#else: 
		#build path
	total_cost = currState[0]
	while currState:
		#plan.append(currState) # appending the inventory of each state
		#plan.append((currState, step[currState])) # appending the invertory and each step
		plan.append(step[currState]) # appending each step 
		currState = prev[currState]

	plan.reverse()
	plan.remove(step[initial])
		
	return total_cost, plan


def search_backward(graph, initial, is_goal, limit, heuristic):
	total_cost = 0
	plan = []
	prev = {initial: None}
	step = {initial: None}

	priorityQueue = Q.PriorityQueue()

	priorityQueue.put(initial)

	t_now = time.time()
	t_deadline = t_now + TIME_LIMIT


	run = 0
	while not priorityQueue.empty() and t_now < t_deadline:
		currState = priorityQueue.get()

		if is_goal(currState):
			break

		#get list of possible states
		adj = graph(currState)

		#print " == "

		

		for state in adj:
			if state[0] not in prev: # or node[0] < heuristic(node) : #heuristic
				priorityQueue.put(state[0])
				prev[state[0]] = currState
				step[state[0]] = state[1]

				
		run += 1
		t_now = time.time()

	
	if t_now > t_deadline:
		print "time out"
		total_cost = -1

	else: 
		#build path
		total_cost = currState[0]
		while currState:
			#plan.append(currState) # appending the inventory of each state
			#plan.append((currState, step[currState])) # appending the invertory and each step
			plan.append(step[currState]) # appending each step 
			currState = prev[currState]

		plan.remove(step[initial])

		
	return total_cost, plan


def t_graph(state, recs):
	
	adj = []
	for recipe in recs.items():
		if recipe[1][1](state):
			newState = recipe[1][2](state)
			newState = (newState[0] + recipe[1][3], newState[1])
			adj.append((newState, recipe[1][0])) # returning the step of the plan
	return adj

def b_graph(state):
	adj = []
	item_list = list(state[1]) # (name, count)
	#items = dict(item_list)
	tick = 0
	for item in item_list:
		#print " right in the for loop:"
		#print item
		#print
		rec = recipe_dict[item[0]]
		for r in rec:
			new_list = None
			new_list = copy.copy(item_list)

			pindex = 0
			new_pro = None

			if r[1]:
				for pro in r[1].items():
					for producable in item_list:
						if pro[0] == producable[0]:
							index = item_list.index(producable)
							if producable[1] - pro[1] < 0:
								new_pro = (producable[0], 0) 
							else:	
								new_pro = (producable[0], producable[1] - pro[1]) 
							break
			

			if r[2]:
				for req in r[2].items():
					in_list = False
					for thing in item_list:
						if req[0] == thing[0]:
							in_list = True
							break

					if not in_list:
						new_list.append(req)

			if r[3]:
				for con in r[3].items():
					found = False
					index = 0
					new_con = None
					for consumable in item_list:
						if con[0] == consumable[0]:
							index = new_list.index(consumable)
							new_con = (consumable[0], consumable[1] + con[1]) 
							found = True
							break

					if found:
						new_list[index] = new_con
					else:
						new_list.append(con)

			if new_pro:
				if new_pro[1] == 0:
					new_list.remove(new_list[pindex])
				else:
					new_list[pindex] = new_pro

			adj.append( (         (            state[0] + r[4],               tuple(new_list)               )              , r[0]               )   )
		

	return adj




def t_is_goal(state):

	goals = Crafting['Goal']

	for goal in goals:
		if goal not in state or state[goal] < goals[goal]:
			return False
	return True

def b_is_goal(state):
	item_list = list(state[1]) # (name, count)
	items = dict(item_list)

	if not Crafting['Initial'] and items:
		return False

	for item in Crafting['Initial'] :
		if item not in items or Crafting['Initial'][item] < items[item]:
			return False

	return True


def t_heuristic(state):

	for item in state:
		#print item
		if item in maxes and state[item] > maxes[item]:
			return float("inf")


	return 0


if __name__ ==  '__main__':
	import json
	with open('Crafting.json') as f:
		Crafting = json.load(f)

	Recipe = namedtuple('Recipe',['name','check','effect','cost'])

	for action, rule in Crafting['Recipes'].items():
		checker = make_checker(rule)
		effector = make_effector(rule)
		all_recipes[action] = ((action, checker, effector, rule['Time']))
		#recipe = Recipe(action, checker, effector, rule['Time'])
		#all_recipes.append(recipe)

		pro = rule.get('Produces', [])
		con = rule.get('Consumes', [])
		req = rule.get('Requires', [])
		cost = rule['Time']

		for c in con:
			if c not in maxes or maxes[c] < con[c]:
				maxes[c] = con[c]

		for r in req:
			if r not in maxes or maxes[r] < req[r]:
				maxes[r] = req[r]

		for p in pro:
			if p not in maxes or maxes[p] < pro[p]:
				maxes[p] = pro[p]

		key = pro.keys()[0]
		recipe_dict.setdefault(key, [])

		recipe_dict[key].append((action, pro, req, con, cost))

	#make the maxes by going through each object and adding the max produced and max cost

	produces_dict = {}

	for item in maxes:
		cmax = 1
		pmax = 0
		for thing, rule in Crafting['Recipes'].items():
			pro = rule.get('Produces', [])
			con = rule.get('Consumes', [])
			if item in pro and pmax < pro[item]:
				pmax = pro[item]
				produces_dict[item] = pmax
			if item in con and cmax < con[item]:
				cmax = con[item]
		maxes[item] = cmax + pmax -1
	#print recipe_dict['wood']
	
	#print produces_dict

	Crafting['Initial'] = {}
	Crafting['Goal'] =  {'cart': 1}

	for g in Crafting['Goal']:
		while maxes[g] < Crafting['Goal'][g]:
			maxes[g] = maxes[g] + produces_dict[g]

	for i in Crafting['Initial']:

		if i in maxes and Crafting['Initial'][i] > maxes[i]:
			maxes[i] = Crafting['Initial'][i]

	for m in maxes:
		print m, ' ', maxes[m]

	initState = (0, tuple(Crafting['Initial'].items()))

	startTime = time.time()


	total_cost, plan = search(t_graph, initState, t_is_goal, float("inf"), t_heuristic)


	print "Done"
	print "Goal is: ", Crafting['Goal']
	print "Cost is: ", total_cost
	print "Plan is: "
	for step in plan:
		print step
	print "Total steps: ",len(plan) 
	print "Time taken: ", time.time() - startTime

