"""A module that defines execution environment.

"""

import enum

class Eenv:
    """The class for execution environments.

    Parameters
    ----------
    cloud : matildalink.cloud.Cloud
        The CSP of interest.
    instance_type : matildalink.cloud.InstanceType
        Type of the instance.
    use_spot : bool
        Whether to use spot instance.
    region : matildalink.cloud.Region
        The region of the cloud `cloud`.
    zone : matildalink.cloud.AZ
        The availability zone in the region `region` of the cloud `cloud`.

    """

    def __init__(self, cloud, instance_type, use_spot, region, zone):
        """Initializer.

        """
        self.cloud = cloud
        self.instance_type = instance_type
        self.use_spot = use_spot
        self.region = region
        self.zone = zone
