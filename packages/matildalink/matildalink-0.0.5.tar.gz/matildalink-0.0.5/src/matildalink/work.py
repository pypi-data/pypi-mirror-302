"""A module that defines work.

Work corresponds to workload in our usual terms. Conceptually, the
ingredients of a work include data, data loading/preprocessing logic, and
training or inference logic.

Notes
-----
In terms of implementation, a work could have data and computation logic
(data loading/preprocessing, and a training or inference procedure)
separately. In our current implementation, a work just has code, which
includes everything in a single Python file, instead of having the
fine-grained objects aforementioned. Also, in order to extract useful
information (e.g., features for the Brain AI/ML model) easily, a work type
is additionally defined for each work.

"""

import enum

# All work types in the Brain TE set.
#
# TODO: Similar types should be defined for the Brain TR set.
#
# IDEA: We use work types in order to make it easier to extract useful
# information from work by case-splitting based on them. However, doing so
# might become tedious and complex as we start to consider more diverse
# work types. Later, we might decide to adopt a more general general
# procedure that extracts information from *any* type of work of interest,
# without case-splitting based on work types.
class WorkType(enum.Enum):
    """Work types.

    WorkType defines all the work types that Brain can process.
    """

    RESNET_TR = enum.auto()
    RESNET_INF = enum.auto()
    RETINANET_TR = enum.auto()
    RETINANET_INF = enum.auto()
    MASKRCNN_TR = enum.auto()
    MASKRCNN_INF = enum.auto()
    BERT_TR = enum.auto()
    BERT_INF = enum.auto()
    
class Work:
    """The Work class.

    Parameters
    ----------
    code : pathlib.Path
        The local path for the Python(.py) file for the work. This
        single file is supposed to have full information of the work
        including data (e.g., where and how to load).
    worktype : WorkType
        Type that identifies the work.

    """

    # IDEA: As noted in the module docstring, a work could take data and
    # logic separately. In that case, the signature of the initializer
    # would be as follows: ``__init__(self, data, code, worktype)``.
    def __init__(self, code, worktype):
        """Initializer.

        """
        self.code = code
        self.worktype = worktype

    # TODO
    def _gen_resnet_tr_graphdef(self):
        """Return TF graph definition for the ResNet training work.

        Returns
        -------
        
        """
        pass

    # TODO
    def _gen_retinanet_tr_graphdef(self):
        """Return TF graph definition for the RetinaNet training work.

        """
        pass

    # TODO
    def _gen_maskrcnn_tr_graphdef(self):
        """Return TF graph definition for the Mask R-CNN training work.

        """
        pass

    # TODO
    def _gen_bert_tr_graphdef(self):
        """Return TF graph definition for the BERT training work.

        """
        pass

    # TODO
    def _gen_resnet_inf_graphdef(self):
        """Return TF graph definition for the ResNet inference work.
        
        """
        pass

    # TODO
    def _gen_retinanet_inf_graphdef(self):
        """Return TF graph definition for the RetinaNet inference work.

        """
        pass

    # TODO
    def _gen_maskrcnn_inf_graphdef(self):
        """Return TF graph definition for the Mask R-CNN inference work.
 
        """
        pass

    # TODO
    def _gen_bert_inf_graphdef(self):
        """Return TF graph definition for the BERT inference work.

        """
        pass

    # Here we do DY's case-splitting based on `work.worktype`, instead of
    # based on `exp_name` strings, e.g., 'resnet_train'.
    def gen_graphdef(self):
        """Return the TF graph definition of the given work.

        Returns
        -------

        """
        match self.worktype:
            case WorkType.RESNET_TR:
                return self._gen_resnet_tr_graphdef()
            case WorkType.RETINANET_TR:
                return self._gen_retinanet_tr_graphdef()
            case WorkType.MASKRCNN_TR:
                return self._gen_maskrcnn_tr_graphdef()
            case WorkType.BERT_TR:
                return self._gen_bert_tr_graphdef()
            case WorkType.RESNET_INF:
                return self._gen_resnet_inf_graphdef()
            case WorkType.RETINANET_INF:
                return self._gen_retinanet_inf_graphdef()
            case WorkType.MASKRCNN_INF:
                return self._gen_maskrcnn_inf_graphdef()
            case WorkType.BERT_INF:
                return self._gen_bert_inf_graphdef()
            case _:
                raise ValueError("Unsupported work type")
            
