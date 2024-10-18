"""Module that identifies the optimal execution environment.

The optimizer takes a set of optimization data that share the same work,
and an optimization target, and then identifies an optimization data that
has the optimal execution enivronment for the given work in terms of the
given optimization target.

Notes
-----
TODO

References
----------
TODO

"""

import enum
import dataclasses as dc
import abc

import matildalink.work as work
import matildalink.eenv as eenv

class OptimizationTarget(enum.Enum):
    """Optimization target.

    The optimizer picks the optimal execution environment for the given
    work. But optimal in terms of what? We currently support time and
    cost, binary.
    """
    TIME = enum.auto()
    COST = enum.auto()

@dc.dataclass
class OptimizationData():
    """Full representation of an input data to the optimizer.

    An optimization data is a 4-tuple that represents the full
    information for the estimated execution result of a pair of work and
    execution environment:
    (work, execution environment, estimated time, estimated cost).

    The optimizer takes a set of optimization data, and pick one of
    them that is optimal.

    """
    work: work.Work
    eenv: eenv.Eenv
    est_time: float
    est_cost: float

class Optimizer(abc.ABC):
    """The Optimizer class.

    This is an abstract class. Implement your own optimizer according to
    your needs.
    """

    @staticmethod
    @abc.abstractmethod
    def pick(dataset, target):
        """Identify the optimal execution environment for the given work.

        Given a set of optimization data, where all the data in the set
        share the same work, this procedure identifies the one that has
        the optimal execution environment, with respect to time or cost
        according to the specified optimization target `target`.

        IMPORTANT: all the given optimization data in the given set must
        share the same work.

        Parameters
        ----------
        dataset : tuple of OptimizationData
            A set of optimization data, among which this procedure picks
            the optimal one.
        target : OptimizationTarget
            Optimizing with respect to what? Either time or cost, binary.

        Returns
        -------
        OptimizationData
            An optimization data that has the optimal exec. environment.
        
        """
        # TODO: assert all the optimization data in the set share the same
        # work.

# Ths assumption of the size-2 set of optimization data is aligned with
# our 2nd-year project goal, where we consider exactly two execution
# environments for the given work: g5.xlarge and g6.xlarge of Amazon EC2.
class SimpleOptimizer(Optimizer):
    """Optimizer for size-2 set of optimization data.

    This optimizer assuems the set of only two optimization data. That is,
    for the given work (shared accross the optimization data in the set),
    it picks one of the two execution environments.
    
    """

    @staticmethod
    def pick(dataset, target):
        """Pick the optimal optimization data using simple calculation.

        This procedure identifies a specific optimization data that has
        the optimal execution environment, and the identification process
        is directed by simple comparison calculation based on the
        optimization target `target`.

        Parameters
        ----------
        dataset : tuple of OptimizationData
            A size-2 set of optimization data, among which this procedure
            picks the optimal one.
        target : OptimizationTarget
            Optimizing with respect to what? Either time or cost, binary.

        Returns
        -------
        OptimizationData
            An optimization data that has the optimal exec. environment.

        """
        assert len(dataset) == 2
        assert isinstance(dataset[0], OptimizationData)
        assert isinstance(dataset[1], OptimizationData)

        match target:
            case OptimizationTarget.TIME:
                if dataset[0].est_time < dataset[1].est_time:
                    return dataset[0]
                else:
                    return dataset[1]
            case OptimizationTarget.COST:
                if dataset[0].est_cost < dataset[1].est_cost:
                    return dataset[0]
                else:
                    return dataset[1]
            case _:
                raise ValueError("Unsupported optimization target")

# We use SkyPilot for implementing the ILP optimization. SkyPilot, in
# turn, uses the CBC solver for ILP internally.
class ILPOptimizer(Optimizer):
    """ILP-optimizer.

    This optimizer formulates and solves an integer linear programming
    (ILP) optimization problem in order to pick an optimal execution
    environment for the given work. This optimizer tends to become useful
    as the size and complexity of the optimization dataset grow.

    Notes
    -----
    From the implementation perspective, we use SkyPilot[1]_ in order to
    implement the ILP optimizer. Specifically, we use the Optimizer
    module of SkyPilot, which implements the optimization procedure using
    PuLP[2]_, a linear and mixed integer programming modeler (package)
    written in Python, which in turn calls CBC[3]_, an off-the-shelf ILP
    solver, internally.

    References
    ----------
    .. [1] Yang, Zongheng, et al. "{SkyPilot}: An intercloud broker for
       sky computing." 20th USENIX Symposium on Networked Systems Design
       and Implementation (NSDI 23). 2023.
    .. [2] Mitchell, Stuart, Michael OSullivan, and Iain Dunning. "Pulp: a
       linear programming toolkit for python." The University of Auckland,
       Auckland, New Zealand 65 (2011): 25.
    .. [3] Forrest, John, and Robin Lougee-Heimer. "CBC user guide."
       Emerging theory, methods, and applications. INFORMS, 2005. 257-277.

    """

    # TODO: Implement the ILP optimization logic using SkyPilot.
    @staticmethod
    def pick(dataset, target):
        """Pick the optimal optimization data using ILP solving.

        This procedure identifies a specific optimization data that has
        the optimal execution environment, and the identification process
        is directed by ILP problem solving whose optimization target is
        specified by `target`.

        Parameters
        ----------
        dataset : tuple of OptimizationDdata
            A set of optimization data, among which this procedure picks
            the optimal one.
        target : OptimizationTarget
            Optimizing with respect to what? Either time or cost, binary.

        Returns
        -------
        OptimizationData
            An optimization data that has the optimal exec. environment.

        """
        pass
