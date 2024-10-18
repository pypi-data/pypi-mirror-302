"""A module that computes expected execution time and cost.

The estimator computes the estimated time and cost for the pair of work
and execution environment. It transforms the predicted operational
intensity for the given pair into the expected time and cost for the pair.

Notes
-----
From the algorithm perspective, the estimator uses the predictor as an
algorithmic sub-step. Concretely, the predictor computes the predicted
operational intensity for the given pair of work and execution
environment, but that step is only part of the estimation process; the
estimator takes the predicted operational intensity for the given pair,
and transforms it into the expected time and cost for the pair.

Note that the computation of the estimator is directed by the Roofline
framework[1]_ from the field of performance modeling. Specifically, the
estimator benchmarks the Roofline modeling, and one of the key ideas is
this: compute a throughput-based performance metric first, and then
transforms the metric into expected time and cost. For the throughput
metric, we use FLOPS (as in the Roofline standard).

References
----------
.. [1] Williams, Samuel, Andrew Waterman, and David Patterson. "Roofline:
   an insightful visual performance model for multicore architectures."
   Communications of the ACM 52.4 (2009): 65-76.

"""

import matildalink.catalog as catalog

class Estimator:
    """The Estimator class.
    
    """

    # TODO: Finish implementation.
    @staticmethod
    def calc_flops(eenv, intensity):
        """Calculate FLOPS at the given operational intensity.

        This procedure calculates the FLOPS that summarizes the
        performance (througput) of the given execution environment `eenv`
        for the given operational intensity `intensity`. Specifically, it
        evaluates the Roofline model that represents the executions (of
        various kinds of work) in the given execution environment `eenv`
        at the given opereational intensity `intensity`.

        The given operational intensity `intensity` is assumed to be the
        one that the predictor produces for the pair of work and execution
        environment `eenv` of interest.

        Parameters
        ----------
        eenv : eenv.Eenv
            Execution environment of interest.
        intensity : float
            Operational intensity that is computed by the predictor for
            the pair of work and execution environment (`eenv`) of
            interest.

        Returns
        -------
        float
            FLOPS for the work with the given operational intensity
            `intensity` when executed in the given execution environment
            `eenv`.

        Notes
        -----
        In our Brain algorithm, the predictor first predicts the
        operational intensity for the given pair of work and execution
        environment. Then, the estimator applies the Roofline model for
        the given execution environment (`eenv`) to the predicted
        operational intensity in order to get an estimated FLOPS, a
        throughput-based performance metric.

        """
        #roofline = ... get_roofline_model(eenv) # TODO: Define roofline models.
        #flops = roofline(intensity)

        #return flops
        return 60. # HACK: Just for scaffolding

    @staticmethod
    def calc_time(num_flops, flops):
        """Estimate the expected execution time.

        This procedure computes the estimated time (in sec) for executing
        the work of interest in the execution environment of interest.
        IMPORTANT: the returned estimated time is in sec, not in hour. Be
        careful with the unit.

        Pararmeters
        -----------
        num_flops : int
            The estimated total number of FLOPs for the given work `work`.
        flops : float
            FLOPS that represents the expected execution performance for
            the pair of work and execution environment of interest.

        Returns
        -------
        float
            Expected execution time in sec.

        Notes
        -----
        Since this procedure takes the key information that has already
        been computed, its computation is simple:
        estimated time = `num_flops` / `flops`.

        """
        return num_flops / flops

    @staticmethod
    def calc_cost(est_time, eenv):
        """Estimate the expected execution cost.

        This procedure computes the estimated cost (in USD) for executing
        the work of interest in the given execution environment `eenv`
        for `est_time` seconds.

        Parameters
        ----------
        est_time : float
            Expected execution time in sec.
        eenv : eenv.Eenv
            Execution environment of interest.

        Returns
        -------
        float
            Expected execution cost in USD

        Notes
        -----
        The computation is done by multiplying the expected execution time
        `est_time` by the unit price of the execution environment (e.g.,
        the unit price of Amazon EC2).

        """
        #unit_price_in_hour = Estimator._get_unit_price(eenv)
        unit_price_in_hour = catalog.Catalog.get_unit_cost(
            instance_type=eenv.instance_type,
            use_spot=eenv.use_spot,
            region=eenv.region,
            zone=eenv.zone,
            clouds=eenv.cloud)
        
        return est_time / 3600. * unit_price_in_hour
        
