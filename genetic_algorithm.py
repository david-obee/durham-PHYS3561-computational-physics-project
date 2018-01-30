'''
Simple Genetic Algorithm, utilising numpy.
'''

from __future__ import division

import numpy
import random



class Problem:
	
	def __init__(self):
		
		self.mutator_functions = []
		self.crossover_functions = []
		
		self.population = []
		self.initial_population = []
		self.population_size = None
		
		self.fitness_function = None
		
		self.selection_function = None
		self.iterations = None
		
		self.p_mut = None
		
	


class Individual:
	
	def __init__(self):
		
		self.properties = []
		self.fitness = None
		
	



def ga_solve(prob):
	
	# First prepare the problem
	
	prob.population = prob.initial_population
	
	overall_best_member = None
	overall_best_fitness = float('inf')
	
	for i in range(prob.iterations):
		
		# The first step is to prepare the child population
		
		child_population = []
		
		# Now we use our selection method to populate the child population
		
		for n in range(prob.population_size):
			
			# First, we select two parent individuals from the parent population
			
			p1 = prob.selection_function(prob.population)
			p2 = prob.selection_function(prob.population)
			
			# Now we cross these two parents over
			
			child = crossover(prob, p1, p2)
			
			# Now we possibly mutate the child
			
			if probability(prob.p_mut):
				
				child = mutate(prob, child)
				
			
			# Now we evaluate the fitness of this child
			
			child.fitness = prob.fitness_function(child.properties)
			
			# Now we add this child to the new child_population
			
			child_population.append(child)
			
		
		# Now we set the current population to be the child_population
		
		prob.population = child_population
		
		bm = find_best_member(prob.population)
		
		if bm.fitness < overall_best_fitness:
			overall_best_fitness = bm.fitness
			overall_best_member = bm
		
		'''DIAGNOSTIC'''
		# Find the average fitness
		avg_f = 0
		for member in prob.population:
			avg_f += member.fitness
		avg_f = avg_f / prob.population_size
		
		
		prob.iteration_best_function(i, bm, avg_f)
		print "Iteration {0}, best fitness: {1}, average fitness: {2}".format(i, bm.fitness, avg_f)
		
	
	return overall_best_member
	


def crossover(prob, p1, p2):
	
	# First we prepare the child Individual
	
	child = Individual()
	
	for i in range(len(prob.crossover_functions)):
		
		child.properties.append(prob.crossover_functions[i](p1.properties[i], p2.properties[i]))
		
	
	# Now we return the child Individual
	
	return child


def mutate(prob, child):
	
	for i in range(len(prob.mutator_functions)):
		
		child.properties[i] = prob.mutator_functions[i](child.properties[i])
		
	
	return child


def probability(p):
	
	if random.random() < p:
		return True
	else:
		return False


def find_best_member(population):
	
	best_fitness = float("inf")
	best_member = None
	
	for i in population:
		
		if i.fitness < best_fitness:
			
			best_fitness = i.fitness
			best_member = i
			
		
	
	return best_member



''' Utility functions '''


def roulette_wheel_selection(population):
	
	weight_function = lambda x : numpy.exp(-5*x/1000000)
	
	intervals = [] # Will go [[start, end]]
	total_weight = 0
	
	for i in population:
		
		weight = weight_function(i.fitness)
		
		intervals.append([total_weight, total_weight + weight])
		
		total_weight += weight
		
	
	# Now select a number
	
	n = random.uniform(0, total_weight)
	
	# Now find this member
	
	chosen_index = None
	
	for index, interval in enumerate(intervals):
		
		# Check in interval, or on lower interval boundary
		
		if n >= interval[0] and n <= interval[1]:
			
			chosen_index = index
			break
			
		
	
	selection = population[chosen_index]
	
	return selection




def adaptive_roulette_wheel_selection(population):
	''' In the adaptive roulette wheel selection, weight the highest fitness as exp(-1), and the lowest fitness as exp(0) '''
	
	fitnesses = [i.fitness for i in population]
	min_f = min(fitnesses)
	max_f = max(fitnesses)
	if min_f == max_f:
		max_f = min_f + 1
	
	#weight_function = lambda x : numpy.exp(-5*x/1000000)
	#weight_function = lambda x : numpy.exp(-3 * (x - min_f)/(max_f - min_f))
	weight_function = lambda x : numpy.exp(-5 * (x - min_f)/(max_f - min_f))
	#weight_function = lambda x : numpy.exp(-20 * (x - min_f)/(max_f - min_f))
	#weight_function = lambda x : numpy.exp(-40 * (x - min_f)/(max_f - min_f))
	
	intervals = [] # Will go [[start, end]]
	total_weight = 0
	
	for i in population:
		
		weight = weight_function(i.fitness)
		
		intervals.append([total_weight, total_weight + weight])
		
		total_weight += weight
		
	
	# Now select a number
	
	n = random.uniform(0, total_weight)
	
	# Now find this member
	
	chosen_index = None
	
	for index, interval in enumerate(intervals):
		
		# Check in interval, or on lower interval boundary
		
		if n >= interval[0] and n <= interval[1]:
			
			chosen_index = index
			break
			
		
	
	selection = population[chosen_index]
	
	return selection


































