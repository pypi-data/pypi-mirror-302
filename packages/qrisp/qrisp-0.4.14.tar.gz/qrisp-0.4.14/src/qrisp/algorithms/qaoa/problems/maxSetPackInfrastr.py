"""
\********************************************************************************
* Copyright (c) 2023 the Qrisp authors
*
* This program and the accompanying materials are made available under the
* terms of the Eclipse Public License 2.0 which is available at
* http://www.eclipse.org/legal/epl-2.0.
*
* This Source Code may also be made available under the following Secondary
* Licenses when the conditions for such availability set forth in the Eclipse
* Public License, v. 2.0 are satisfied: GNU General Public License, version 2
* with the GNU Classpath Exception which is
* available at https://www.gnu.org/software/classpath/license.html.
*
* SPDX-License-Identifier: EPL-2.0 OR GPL-2.0 WITH Classpath-exception-2.0
********************************************************************************/
"""

from qrisp import QuantumVariable, mcx, rz, x, rx, auto_uncompute

from qrisp import control
from collections.abc import Iterable
# This is pretty much maxIndependent set, but with a twist
# instead of swapping out singular qubits, we swap out whole predefined sets. 
# This means we apply the mixers to all elements in the sets.

# we have a graph of 9 vertices

#######################
## reformulate using @auto_uncompute !!!
## https://www.qrisp.eu/reference/Core/Uncomputation.html


def maxSetPackCostOp(problem):
    
    """
    |  Create the cost/problem operator for this problem instance. The swapping rule is to swap a set in and out of the solution, if it is not intersecting with any other set.
    |  Idea - Per set: 

    * Create ancillas for every element, they represent these elements
    * Perform multi controlled x operations on each ancilla
    * Controls are given by sets with also contain the considered element
    * If all controls are "0" (see ``ctrl_state`` for ``mcx``-operation) we set this ancilla to "1"

    |  Then perform mcx on the qubit describing the set as follows:
    |  If all ancillas are "1" this means the qubits describing the sets contain no intersections with the considered set. We can then swap the set in (or out).
    |  Afterwards uncompute the ancillas.

    Parameters
    ----------
    sets : list(Lists)
        The sets the universe is seperated into as by the problem definition

    universe: Tuple
        The universe for the problem instance, i.e. all possible values (all graph vertices)

    Returns
    -------
    QuantumCircuit: qrisp.QuantumCircuit
        the Operator applied to the circuit-QuantumVariable

    Examples
    --------
    Definition of the sets, given as list of lists. Full universe ``sol`` is given by the amount of elements (+1, since its 0-indexed)
    
    >>> sets = [[0,7,1],[6,5],[2,3],[5,4],[8,7,0],[1]]
    >>> sol = 9
    >>> problem = [sol, sets]

    The relations between the sets, i.e. which vertice is in which other sets

    >>> print(get_neighbourhood_relations(sets, len_universe=len(sol)))

    Assign the operators

    >>> cost_fun = maxSetPackclCostfct(problem)
    >>> mixerOp = RZ_mixer
    >>> costOp = maxSetPackCostOp(problem)
    """

    universe = list(range(problem[0]))
    sets = problem[1]
    
    if not isinstance(sets, Iterable):
        raise Exception("Wrong structure of problem - clauses have to be iterable!")
    for clause in sets:
        if not isinstance(clause, Iterable):
            raise Exception("Wrong structure of problem - each set has to be a tuple!")
        for item in clause:
            if not isinstance(item, int):
                raise Exception("Wrong structure of problem - each literal has to an int!")

    # get neigbhorhood relations from helper function
    nbh_rel = get_neighbourhood_relations(problem)

    @auto_uncompute
    def theCostOpEmbedded(qv, gamma):
        # check all sets
        for set_index in range(len(sets)):
            # get set elements and create an ancilla for every set element
            nodes = sets[set_index]
            ancillas = QuantumVariable(len(nodes))
            # go through all ancillas and, equivalently set elements
            for ancilla_index in range(len(ancillas)):
                # if the element is only in one set, we can set this ancilla to 1
                if len(nbh_rel[nodes[ancilla_index]])<2:
                    x(ancillas[ancilla_index])
                    continue
                # else save the sets with also contain the considered element
                nbh_sets_list = [ item for item in nbh_rel[nodes[ancilla_index]] if item != set_index]
                # perform mcx on ancilla, control given by the relevant set
                mcx([qv[nbh_sets_index] for nbh_sets_index in nbh_sets_list], ancillas[ancilla_index], ctrl_state= "0" * len(nbh_sets_list))
            # perform mcx gate on the qubit describing the considered set
            with control(ancillas):
                rx(gamma, qv[set_index])  

            #ancillas.uncompute()

    return theCostOpEmbedded


def get_neighbourhood_relations(problem):
    """
    helper function to return a dictionary describing neighbourhood relations in the sets, i.e. for each element in the universe, gives the info in which the element is contained in.


    Parameters
    ----------
    problem : List 
        The problem definition, as described above

    Returns
    -------
    neighbourhood relation dictionary :  dict
        |  keys: all universe elements (all graph vertices)
        |  values: per universe element the sets it is contained in

    """

    sets = problem[1]
    
    n_dict = {}
    for index_node in range(problem[0]):
        adding_list = [index_set for index_set in range(len(sets)) if index_node in sets[index_set]]
        #if len(adding_list)>1: 
        n_dict[index_node] = adding_list
    return n_dict


def maxSetPackclCostfct(problem):
    """
    create the classical cost function for the problem instance

    Parameters
    ----------
    problem : list
        The problem definition, as described above

    Returns
    -------
    cl_cost_function : function
        The classical function for the problem instance, which takes a dictionary of measurement results as input.

    """

    universe = list(range(problem[0]))
    sets = problem[1]

    def cl_cost_function(res_dic):
        tot_energy = 0
        for state, prob in res_dic.items():
            list_universe = [True]*len(universe)
            temp = True
            energy = 0
            # get all sets marked by the solution
            indices = [index for index, value in enumerate(state) if value == '1']
            sol_sets = [sets[index] for index in indices]
            
            for set in sol_sets:
                for val in set:
                    if list_universe[val]:
                        # if the value appears in the sets, set this value to False
                        list_universe[val] = False
                    else: 
                        # if the value is False, this element appeared in another solution set
                        # the sets then intersect and the solution is invalid
                        temp = False 
                        break
            if temp:
                energy = -len(indices)
                tot_energy += energy*prob

        return tot_energy
    
    return cl_cost_function


def init_state(qv):
    # all in 0
    return qv


