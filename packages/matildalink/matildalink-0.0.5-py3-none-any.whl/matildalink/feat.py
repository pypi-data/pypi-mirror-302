"""A module for features and the feature extractor.

"""

import numpy as np

# TODO (feature type): Currently, each feature is temporarily assumed to
# be (and represented as) a float. We should make a clear decision on it
# during the AI/ML modeling work.
class FeatExtractor:
    """Feature extractor.

    The feature extractor provides two separate procedures for feature
    extraction, one (`extract_from_work`) for extraction from work and the
    other (`extract_from_eenv`) for that from execution environment.

    Notes
    -----
    The reason that we provide the two extraction procedures is to enable
    the user (of this package) to save computation in their use cases. The
    Brain algorithm, for example, extracts feature from the given work
    only once, and then extracts features from different execution
    environments for that shared work by only calling `extract_from_eenv`
    multiple times.

    """

    @staticmethod
    def _calc_num_flops(graph):
        """Calculate the total number of FLOPs for the given work.

        This procedure returns the estimated total number of FLOPs of the
        work that is represented by the given `graph`.

        Parameters
        ----------
        graph : [TODO: specify type.]
            TensorFlow graph definition of the work of interest.

        Returns
        -------
        int
            The estimated total number of FLOPs for the work represented
            by the given graph `graph`.

        Notes
        -----
        It is worth noting that its computation has the following
        characters: (1) it only reads the code in order to produce the
        number, without actually running the code (that is, it is a kind
        of static analysis rather than a profiling technique); and (2) the
        result may not represent the true value of the total number of
        FLOPs for the work.

        The computed total number of FLOPs for the given work is used in
        the two sub-steps of the Brain algorithm: (1) it becomes a feature
        for the Brain AI/ML model (in the feature-generation step); and
        (2) it is used to derive the estimated time from the FLOPS
        computed from the Roofline-model application:
        estimated time = total number of FLOPs / FLOPS.

        """
        return 200 # HACK: Just for scaffolding

    @staticmethod
    def _calc_actmem(graph):
        """Return the est. size of activation memory of the given work.

        Parameters
        ----------
        graph : [TODO: specify type.]
            [TODO: explain.]

        Returns
        -------
        int
            Estimated size of activation memory.

        """
        return 114 # HACK: Just for scaffolding

    @staticmethod
    def _calc_parmem(graph):
        """Return the size of parmeter memory of the given work.
        
        Parameters
        ----------
        graph : [TODO: specify type.]
            [TODO: explain.]
        
        Returns
        -------
        int
            Size of parameter memory.

        """
        return 112 # HACK: Just for scaffolding

    # TODO: Define more features from work.
    @staticmethod
    def extract_from_work(work):
        """Extract features from a work.

        Extract features from the given work `work`, and returns a tuple
        of the partial feature vector and the value of the first feature
        --the estimated total number of FLOPs for the given work `work`.
        The second element of the tuple is redundant information; that is,
        the first element is the complete partial feature vector itself.

        Parameters
        ----------
        work : work.Work
            The work of interest.

        Returns
        -------
        tupe of numpy.ndarray and int
            Size-2 tuple where the first element is the partial feature
            vector that only contains features from the given work `work`,
            and the second element the value of the first feature--the
            estimated total number of FLOPs for `work`.

        Notes
        -----
        The second element of the returned tuple is actually redundant
        information; that is, the first element is already the full
        feature vector from the work `work`. This procedure additionally
        returns the second element for explicitness, since another step
        of the Brain algorithm also uses that information (specifically
        when transforming the estimated FLOPS into the estimated time and
        cost).

        """
        graph = work.gen_graphdef()

        fval1 = FeatExtractor._calc_num_flops(graph)
        fval2 = FeatExtractor._calc_actmem(graph)
        fval3 = FeatExtractor._calc_parmem(graph)
       
        fvec = np.array([
            float(fval1),
            float(fval2),
            float(fval3)
        ])

        return (fvec, fval1)

    # TODO: Define features from execution environments.
    @staticmethod
    def extract_from_eenv(eenv):
        """Extract features from an execution environment.

        Extract features from the given execution environment `eenv` and
        return the corresponding partial feature vector.

        Parameters
        ----------
        eenv : eenv.Eenv
            The execution environment of interest.

        Returns
        -------
        numpy.array
            Partial feature vector that only contains features from
            the execution environment `eenv`.

        """
        return np.array([7.8, 54.1]) # HACK: Just for scaffolding

