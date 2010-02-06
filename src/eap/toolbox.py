#    This file is part of EAP.
#
#    EAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    EAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with EAP. If not, see <http://www.gnu.org/licenses/>.

'''The :mod:`toolbox` module is intended to contain the operators that you need
in your evolutionary algorithms, from initialisation to evaluation. It is
always possible to use directly the operators from this module but the toolbox
does also contain the default values of the different parameters for each
method. More over, it makes your algorithms easier to understand and modify,
since once an oprerator is set, it can be reused with a simple keyword that
conatins all its arguments. Plus, every keyword or argument can be overriden
at all time.

The toolbox is also used in predefined algorithms from the :mod:`algorithms`
module.
'''

import copy
from functools import partial
import random

class Toolbox(object):
    '''A toolbox for evolution that contains the evolutionary operators.
    At first this toolbox is empty, you can populate it by using the method
    :meth:`register`.
    '''

    def register(self, methodName, method, *args, **kargs):
        '''Register an operator in the toolbox.'''
        setattr(self, methodName, partial(method, *args, **kargs))

    def unregister(self, methodName):
        '''Unregister an operator from the toolbox.'''
        delattr(self, methodName)


######################################
# Crossovers                         #
######################################

def twoPointsCx(indOne, indTwo):
    '''Execute a two points crossover on the input individuals. The two children
    produced are returned as a tuple, the two parents are left intact.
    This operation apply on a :class:`ListIndividual` without restriction.
    Whatever the passed individuals are, they are gonna be mixed like follow ::

        >>> ind1 = [A(1), ..., A(n), ..., A(n+i), ..., A(m)]
        >>> ind2 = [B(1), ..., B(n), ..., B(n+i), ..., B(k)]
        >>> # Crossover with mating points n and n+i, n > 1 and n+i <= min(m, k)
        >>> child1, child2 = twoPointsCx(ind1, ind2)
        >>> print child1
        [A(1), ..., B(n), ..., B(n+i-1), A(n+i), ..., A(m)]
        >>> print child2
        [B(1), ..., A(n), ..., A(n+i-1), B(n+i), ..., B(k)]

    This function use the :meth:`randint` method from the python base
    :mod:`random` module.
    '''
    lSize = min(len(indOne), len(indTwo))
    lChild1, lChild2 = copy.copy(indOne), copy.copy(indTwo)
    lCxPoint1 = random.randint(1, lSize)
    lCxPoint2 = random.randint(1, lSize - 1)

    if lCxPoint2 >= lCxPoint1:
        lCxPoint2 += 1
    else:			# Swap the two cx points
        lCxPoint1, lCxPoint2 = lCxPoint2, lCxPoint1

    lChild1[lCxPoint1:lCxPoint2], lChild2[lCxPoint1:lCxPoint2] \
         = lChild2[lCxPoint1:lCxPoint2], lChild1[lCxPoint1:lCxPoint2]
    lChild1.mFitness.setInvalid()
    lChild2.mFitness.setInvalid()
    return lChild1, lChild2


def onePointCx(indOne, indTwo):
    '''Execute a one point crossover on the input individuals. The two children
    produced are returned as a tuple, the two parents are left intact.
    This operation apply on a :class:`ListIndividual` without restriction.
    Whatever the passed individuals are, they are gonna be mixed like follow ::

        >>> ind1 = [A(1), ..., A(n), ..., A(m)]
        >>> ind2 = [B(1), ..., B(n), ..., B(k)]
        >>> # Crossover with mating point n, 1 < n <= min(m, k)
        >>> child1, child2 = twoPointsCx(ind1, ind2)
        >>> print child1
        [A(1), ..., B(n), ..., B(k)]
        >>> print child2
        [B(1), ..., A(n), ..., A(m)]

    This function use the :meth:`randint` method from the python base
    :mod:`random` module.
    '''
    lSize = min(len(indOne), len(indTwo))
    lChild1, lChild2 = copy.copy(indOne), copy.copy(indTwo)
    lCxPoint = random.randint(1, lSize - 1)
    lChild1[lCxPoint:], lChild2[lCxPoint:] = lChild2[lCxPoint:], lChild1[lCxPoint:]
    lChild1.mFitness.setInvalid()
    lChild2.mFitness.setInvalid()
    return lChild1, lChild2


def pmCx(indOne, indTwo):
    '''Execute a partialy matched crossover on the input indviduals. The two
    childrens produced are returned as a tuple, the two parents are left intact.
    This crossover expect individuals of indices, the result for any other type
    of individuals is unpredictable.

    Moreover, this crossover consists of generating two children by matching
    pairs of values in a certain range of the two parents and swaping the values
    of those indexes. For more details see Goldberg and Lingel, "Alleles,
    loci, and the traveling salesman problem", 1985.

    For example, the following parents will produce the two following childrens
    when mated with crossover points ``a = 2`` and ``b = 3``. ::

        >>> ind1 = [0, 1, 2, 3, 4]
        >>> ind2 = [1, 2, 3, 4, 0]
        >>> child1, child2 = pmxCx(ind1, ind2)
        >>> print child1
        [0, 2, 3, 1, 4]
        >>> print child2
        [2, 3, 1, 4, 0]

    This function use the :meth:`randint` method from the python base
    :mod:`random` module.
    '''
    lChild1, lChild2 = copy.copy(indOne), copy.copy(indTwo)
    lSize = min(len(indOne), len(indTwo))
    lPos1, lPos2 = [0]*lSize, [0]*lSize
    # Initialize the position of each indices in the individuals
    for i in xrange(lSize):
        lPos1[lChild1[i]] = i
        lPos2[lChild2[i]] = i
    # Choose crossover points
    lCXPoint1 = random.randint(0, lSize)
    lCXPoint2 = random.randint(0, lSize - 1)
    if lCXPoint2 >= lCXPoint1:
        lCXPoint2 += 1
    else:			# Swap the two cx points
        lCXPoint1, lCXPoint2 = lCXPoint2, lCXPoint1
    # Apply crossover between cx points
    for i in xrange(lCXPoint1, lCXPoint2):
        # Keep track of the selected values
        lTemp1 = lChild1[i]
        lTemp2 = lChild2[i]
        # Swap the matched value
        lChild1[i], lChild1[lPos1[lTemp2]] = lTemp2, lTemp1
        lChild2[i], lChild2[lPos2[lTemp1]] = lTemp1, lTemp2
        # Position bookkeeping
        #print lTemp1, lTemp2
        lPos1[lTemp1], lPos1[lTemp2] = lPos1[lTemp2], lPos1[lTemp1]
        lPos2[lTemp1], lPos2[lTemp2] = lPos2[lTemp2], lPos2[lTemp1]
        #print lPos1

    lChild1.mFitness.setInvalid()
    lChild2.mFitness.setInvalid()
    return lChild1, lChild2


######################################
# Mutations                          #
######################################

def gaussMut(individual, mu, sigma, mutIndxPb):
    '''This function applies a gaussian mutation on the input individual and
    returns the mutant. The *individual* is left intact and the mutant is an
    independant copy. This mutation expects an iterable individual composed of
    real valued attributes. The *mutIndxPb* argument is the probability of each
    attribute to be mutated.

    .. todo::
       Add a parameter acting as constraints for the real valued attribute so
       a min, max and interval may be used.

    This function use the :meth:`random` and :meth:`gauss` methods from the
    python base :mod:`random` module.
    '''
    lMutated = False
    lIndividual = copy.copy(individual)
    for i in xrange(len(lIndividual)):
        if random.random() < mutIndxPb:
            lIndividual[i] = lIndividual[i] + random.gauss(mu, sigma)
            # TODO : add some constraint checking !!
            lMutated = True
    if lMutated:
        lIndividual.mFitness.setInvalid()
    return lIndividual

def shuffleIndxMut(individual, shuffleIndxPb):
    '''Shuffle the attributes of the input individual and return the mutant.
    The *individual* is left intact and the mutant is an independant copy. The
    *individual* is expected to be iterable. The *shuffleIndxPb* argument is the
    probability of each attribute to be moved.

    This function use the :meth:`random` and :meth:`randint` methods from the
    python base :mod:`random` module.
    '''
    lMutated = False
    lIndividual = copy.copy(individual)
    lSize = len(lIndividual)
    for i in range(lSize):
        if random.random() < shuffleIndxPb:
            lSwapIndx = random.randint(0, lSize - 2)
            if lSwapIndx >= i:
                lSwapIndx += 1
            lIndividual[i], lIndividual[lSwapIndx] = \
                lIndividual[lSwapIndx], lIndividual[i]
            lMutated = True
    if lMutated is True:
        lIndividual.mFitness.setInvalid()
    return lIndividual


def flipBitMut(individual, flipIndxPb):
    '''Flip the value of the attributes of the input individual and return the
    mutant. The *individual* is left intact and the mutant is an independant
    copy. The *individual* is expected to be iterable and the values of the
    attributes shall stay valid after the ``not`` operator is called on them.
    The *flipIndxPb* argument is the probability of each attribute to be
    flipped.

    This function use the :meth:`random` method from the python base
    :mod:`random` module.
    '''
    lMutated = False
    lIndividual = copy.copy(individual)
    for lGeneIndx in xrange(len(lIndividual)):
        if random.random() < flipIndxPb:
            lIndividual[lGeneIndx] = not lIndividual[lGeneIndx]
            lMutated = True
    if lMutated is True:
        lIndividual.mFitness.setInvalid()

    return lIndividual


######################################
# Selections                         #
######################################

def rndSel(individuals, n, replacement):
    '''Select *n* individuals at random from the input *individuals*. The
    list returned contains shallow copies of the input *individuals*. That
    means if an individual is selected twice, modifying one of the two
    occurences will modify the other. It is possible to randomly select without
    picking twice the same individual by setting *replacement* to :data:`False`.

    This function use the :meth:`choice` and :meth:`sample` method from the
    python base :mod:`random` module.
    '''
    if replacement is True:
        return [random.choice(individuals) for i in xrange(n)]
    else:
        return random.sample(individuals, n)


def bestSel(individuals, n):
    '''Select the *n* best individuals among the input *individuals*. The
    list returned contains shallow copies of the input *individuals*.
    '''
    return sorted(individuals, key=lambda ind : ind.mFitness, reverse=True)[:n]


def worstSel(individuals, n):
    '''Select the *n* worst individuals among the input *individuals*. The
    list returned contains shallow copies of the input *individuals*.
    '''
    return sorted(individuals, key=lambda ind : ind.mFitness)[:n]


def tournSel(individuals, n, tournSize):
    '''Select *n* individuals from the input *individuals* using *n*
    tournaments of *tournSize* individuals. The list returned contains shallow
    copies of the input *individuals*. That means if an individual is selected
    twice, modifying one of the two occurences will modify the other.

    This function use the :meth:`choice` method from the python base
    :mod:`random` module.
    '''
    lChosenList = []
    for i in xrange(n):
        lChosenList.append(random.choice(individuals))
        for j in xrange(tournSize - 1):
            lAspirant = random.choice(individuals)
            if lAspirant.mFitness > lChosenList[i].mFitness:
                lChosenList[i] = lAspirant

    return lChosenList

######################################
# Evaluation                         #
######################################

def evaluateExpr(expr):
    try:
        return expr[0](*expr[1])
    except :
        values = [evaluateExpr(value) for value in expr[1]]
        return evaluateExpr([expr[0],values])

######################################
# Migrations                         #
######################################

def ringMig(populations, n=1, selection=None, replacement=None, migArray=None,
            selKArgs={}, replKArgs={}):
    '''Perform a ring migration between the ``populations``.'''
    # TODO: Check if the migration is compliant to the new selection sheme
    if selection is None:
        selection = self.__bestSel
    if migArray is None:
        migArray = []
        for i in range(len(population)):
            migArray.append((i + 1) % (len(population)))
    print migArray
    lImmigrantsIndx = [[] for i in range(len(migArray))]
    lEmigrantsIndx = [[] for i in range(len(migArray))]
    lMigBuf = []
    for lFromDeme, lToDeme in enumerate(migArray):
        lEmigrantsIndx[lFromDeme].extend(selection(population[lFromDeme], n=n,
                                         **selKArgs))
        if replacement is None:
            # If no replacement strategy is selected, replace those who migrate
            lImmigrantsIndx[lFromDeme] = lEmigrantsIndx[lFromDeme]
        else:
            # Else select those who will be replaced
            lImmigrantsIndx[lFromDeme].extend(replacement(population[lFromDeme],
                                              n=n, **replKArgs))

    # Assing a temporary buffer to contain the emigrants of the first deme will
    # be usefull if the same indexes are choosen as immigrant indexes
    for lIndx in lEmigrantsIndx[0]:
        lMigBuf.append(deepcopy(population[0][lIndx]))

    for lFromDeme in range(1, len(migArray)):
        lToDeme = migArray[lFromDeme]
        for i, lIndx in enumerate(lEmigrantsIndx[lFromDeme]):
            population[lToDeme][lImmigrantsIndx[lToDeme][i]] = \
                      population[lFromDeme][lIndx]

    lToDeme = migArray[0]
    for i in range(len(lEmigrantsIndx[0])):
        population[lToDeme][lImmigrantsIndx[lToDeme][i]] = lMigBuf[i]


#class SimpleGAToolbox(EvolutionToolbox):
#    '''An evolutionary toolbox intended for simple genetic algorithms. Is is
#    initialized with :meth:`mate` that apply a two points crossover with method
#    :meth:`eap.operators.twoPointsCx`, :meth:`mutate` that apply a gaussian
#    mutation with method :meth:`eap.operators.gaussMut` and :meth:`select` that
#    select individuals using a tournament with method
#    :meth:`eap.operators.tournSel`.
#    '''
#
#    def __init__(self):
#        self.register('mate', operators.twoPointsCx)
#        self.register('mutate', operators.gaussMut)
#        self.register('select', operators.tournSel)
#
#
#class IndicesGAToolbox(EvolutionToolbox):
#    '''An evolutionary toolbox intended for simple genetic algorithms. Is is
#    initialized with :meth:`mate` that apply a partialy matched crossover with
#    method :meth:`eap.operators.pmxCx`, :meth:`mutate` that apply a shuffle
#    indices mutation with method :meth:`eap.operators.shuffleIndxMut` and
#    :meth:`select` that select individuals using a tournament with method
#    :meth:`eap.operators.tournSel`.
#
#    .. versionadded:: 0.2.0a
#       The toolbox for indice representation has been added for convenience.
#    '''
#
#    def __init__(self):
#        self.register('mate', operators.pmxCx)
#        self.register('mutate', operators.shuffleIndxMut)
#        self.register('select', operators.tournSel)