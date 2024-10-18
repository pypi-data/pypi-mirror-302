"""A module that keeps track of up-to-date cloud offerings.

"""

import enum
import sky.clouds

import matildalink.cloud

class Catalog:
    """The Catalog class.

    Catalog retains up-to-date cloud offerings, which include the pricing
    and the resource availability of target clouds and their services.

    Notes
    -----
    We implement the catalog using the Service Catalog implementation of
    SkyPilot[1]_.

    References
    ----------
    .. [1] Yang, Zongheng, et al. "{SkyPilot}: An intercloud broker for sky
       computing." 20th USENIX Symposium on Networked Systems Design and
       Implementation (NSDI 23). 2023.

    """
   
    @staticmethod
    def get_unit_cost(instance_type, use_spot, region, zone, clouds):
        """Return hourly cost for the specified instance.

        Parameters
        ----------
        instance_type : matildalink.cloud.InstanceType
            Instance type of interest.
        use_spot : bool
            Whether to use spot instance.
        region : matildalink.cloud.Region
            Region.
        zone : matildalink.cloud.AZ, Optional
            Availability zone.
        clouds : Union[matildalink.cloud.Cloud, list of matildalink.cloud.Cloud]

        Returns
        -------
        float
            Hourly on-demand cost of the instance of `instance_type` under
            the specified condition.

        """
        match clouds:
            case [clouds] | clouds if isinstance(clouds, matildalink.cloud.Cloud):
                return sky.clouds.service_catalog.get_hourly_cost(
                    instance_type=instance_type.value,
                    use_spot=use_spot,
                    region=region.value,
                    zone=None,
                    clouds = clouds.value)
            case [cloud, *_]:
                raise ValueError(('`clouds` is a list with more than one '
                    'element. Check the proper type of `clouds`.'))
            case []:
                raise ValueError(('`clouds` is an empty list. Check the '
                    'proper type of `clouds`.'))
            case _:
                raise ValueError('Check the proper type of `clouds`.')
        
        #return sky.clouds.service_catalog.get_hourly_cost(instance_type='g6.xlarge', use_spot=False, region='us-east-1', zone=None, clouds='aws')


