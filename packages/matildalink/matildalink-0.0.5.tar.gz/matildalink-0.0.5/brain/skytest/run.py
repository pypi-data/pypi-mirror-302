#!/bin/python3

from sky import Dag, Task, Resources, launch, OptimizeTarget
from sky.clouds import AWS

def weird_time_estimator_detectron2(resources):
    """Return estimated runtime in seconds."""

    if not isinstance(resources.cloud, AWS):
        assert False, 'Not supported: {}'.format(resources)
    else:
        instance = resources.instance_type
        if instance == 'p3.2xlarge':
            return 5 # 5sec
        elif instance == 'g4dn.xlarge':
            return 36000 # 10hr
        
        assert False, 'Not supported: {}'.format(resources)

with Dag() as dag:
    task = Task.from_yaml('detectron2_app.yaml').set_time_estimator(weird_time_estimator_detectron2)
    
    launch(task, cluster_name='gwonsoo', dryrun=True, optimize_target=OptimizeTarget.COST)

    '''
    resources1 = Resources(cloud=AWS(), instance_type='g5.xlarge')
    resources2 = Resources(cloud=AWS(), instance_type ='g6.xlarge')
    
    print(resources1.is_launchable())
    print(resources2.is_launchable())

    task = Task(name='task1', setup=None, run=None) # TODO
        .set_resources(resources1, resources2)
        .set_time_estimator(weird_time_estimator)
    '''


