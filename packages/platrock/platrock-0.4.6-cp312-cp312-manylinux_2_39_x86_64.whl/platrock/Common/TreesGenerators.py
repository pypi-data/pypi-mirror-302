"""
Module that handles the generation of trees.
"""

import numpy as np
from scipy import stats


class OneDTreeGenerator():
	"""
	Computes the (1D) distance before the next tree impact from the trees/rock properties and a probability law. Instanciate then launch :meth:`getOneRandomTreeImpactDistance` to get the next distance.

	Note:
		The cdf follow an exponential law which parameter is a function of basal area (treesDensity*trees_dhp), trees_dhp and dRock.

	Attributes:
		sim (:class:`~Common.Simulations.GenericSimulation`, optional): the parent simulation
		treesDensity (float): the trees density, in trees/m²
		trees_dhp (float, optional): the trees mean diameter, in meters
		dRock (float, optional): the rock equivalent diameter, in meters
		coef (float): the computed parameters of the cdf exponential law
		prob0 (float): the probability to hit a tree immediately
		random_generator (): copied from simulation or :class:`numpy.random`
	"""
	def __init__(self,sim,treesDensity=0.1,trees_dhp=0.3,dRock=0.5):
		self.treesDensity = treesDensity
		self.basalArea = treesDensity*10000*(trees_dhp*0.5)**2*np.pi #in m2/ha
		self.trees_dhp = trees_dhp
		self.dRock = dRock
		self.sim=sim
		self.no_trees = False
		self._precomputeData()

	def _precomputeData(self):
		# scale is the inverse of lambda, see https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.expon.html for scale param
		# using simu from june 2024 set based on French NFI data
		if self.treesDensity<1e-10 or self.trees_dhp<1e-10:
			#there is no trees to account for so next impact is theorically infinite
			self.no_trees = True
		else:
			a, b, c, d = -0.9920, 1.8211, -0.8323, 8.4221
			#apply statistical formula
			log_scale = a*np.log(self.basalArea)+b*np.log(self.trees_dhp)
			log_scale += c*np.log(self.dRock)+d
			self.scale = np.exp(log_scale)
			self.coef = 1/self.scale
			self.prob0=self._PDF_impact(0)
			if(self.sim==None):
				self.random_generator=np.random
			else:
				self.random_generator=self.sim.random_generator

	def _PDF_impact(self,x):
		return self.coef*np.exp(-x*self.coef)

	def getOneRandomTreeImpactDistance(self):
		"""
		Get the next impact distance from the instanciated object (pick a value from the previously computed PDF function).

		Returns:
			float
		"""
		if (self.no_trees): return np.inf
		random=self.prob0*self.random_generator.rand()
		return -1/self.coef*np.log(random/self.coef)
