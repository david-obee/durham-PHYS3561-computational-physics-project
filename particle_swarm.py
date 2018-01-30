''' Particle swarm optimisation algorithm '''

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
		
		self.weight = None
		self.c1 = None
		self.c2 = None
		#self.g_best = None
		self.bounds = []
		
	


class Individual:
	
	def __init__(self):
		
		self.properties = []
		self.fitness = None
		
		self.velocity = []
		self.p_best = []
		self.p_best_fitness = None
		#self.inertia = None
		
	



def pso_solve(prob):
	
	# First, prepare the problem
	
	prob.population = prob.initial_population
	
	# Evaluate the fitnesses
	
	for member in prob.population:
		
		member.fitness = prob.fitness_function(member.properties)
		member.p_best = member.properties
		member.p_best_fitness = member.fitness
		
	
	# Find the global best
	
	best_fitness = float('inf')
	best_properties = []
	
	for member in prob.population:
		if member.fitness < best_fitness:
			best_fitness = member.fitness
			best_properties = member.properties
	
	
	# Now, enter the main interation loop
	
	for i in range(prob.iterations):
		
		# The first step is to calculate the new velocities
		
		for member in prob.population:
			
			new_velocity = []
			
			for cpt in range(len(member.velocity)):
				
				new_velocity.append(prob.weight * member.velocity[cpt] + prob.c1 * random.random() * (member.p_best[cpt] - member.properties[cpt]) + prob.c2 * random.random() * (best_properties[cpt] - member.properties[cpt]))
				
			
			member.velocity = new_velocity
		
		
		# The next step is to advance the positions by the velocities
		
		for member in prob.population:
			
			new_properties = []
			
			for cpt in range(len(member.properties)):
				
				new_cpt = member.properties[cpt] + member.velocity[cpt]
				
				if new_cpt < prob.bounds[cpt][0] or new_cpt > prob.bounds[cpt][1]:
					new_cpt = member.properties[cpt] - member.velocity[cpt]
				if new_cpt < prob.bounds[cpt][0] or new_cpt > prob.bounds[cpt][1]:
					new_cpt = member.properties[cpt]
					member.velocity[cpt] = 0
				
				new_properties.append(new_cpt)
				
			
			member.properties = new_properties
		
		
		# The final step is to update the fitnesses, and the best fitnesses
		
		for member in prob.population:
			
			member.fitness = prob.fitness_function(member.properties)
			
			if member.fitness < member.p_best_fitness:
				
				member.p_best = member.properties
				member.p_best_fitness = member.fitness
				
			
			if member.fitness < best_fitness:
				
				best_properties = member.properties
				best_fitness = member.fitness
				
			
		
		''' DIAGNOSTICS '''
		# Find the average fitness
		avg_f = 0
		for member in prob.population:
			avg_f += member.fitness
		avg_f = avg_f / prob.population_size
		
		
		bm = Individual()
		bm.properties = best_properties
		bm.fitness = best_fitness
		prob.iteration_best_function(i, bm, avg_f)
		
		# Find the average velocity magnitude
		avg_v = 0
		for member in prob.population:
			new_v = 0
			for vi in member.velocity:
				new_v += vi**2
			new_v = numpy.sqrt(new_v)
			avg_v += new_v
		avg_v = avg_v / prob.population_size
		
		print "Iteration {0}, best fitness: {1}, average fitness: {2}".format(i, bm.fitness, avg_f)
		print "Average velocity: {0}".format(avg_v)
		
	
	
	# Finally, we return the fitesst member
	
	best_member = Individual()
	best_member.properties = best_properties
	best_member.fitness = best_fitness
	
	return best_member














































