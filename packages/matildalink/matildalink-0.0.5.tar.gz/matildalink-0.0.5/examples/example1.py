import numpy as np
import pathlib

import matildalink.feat as feat
import matildalink.work as work
import matildalink.eenv as eenv
import matildalink.predictor as predictor
import matildalink.optimizer as optimizer
import matildalink.estimator as estimator
import matildalink.catalog as catalog
import matildalink.cloud as cloud

# 1. Define work and execution environments.
print('Define work and execution environments..')
code = pathlib.Path('workloads/textclf.py') # HACK: Just for testing
work = work.Work(code, work.WorkType.RESNET_TR)

eenv1 = eenv.Eenv(
    cloud=cloud.Cloud.AWS,
    instance_type=cloud.InstanceType.G5_XLARGE,
    use_spot=False,
    region=cloud.Region.US_EAST_1,
    zone=None)
eenv2 = eenv.Eenv(
    cloud=cloud.Cloud.AWS,
    instance_type=cloud.InstanceType.G6_XLARGE,
    use_spot=False,
    region=cloud.Region.US_EAST_1,
    zone=None)

# 2. Generate features.
print('Generate features..')
(fvec_from_work, num_flops) = feat.FeatExtractor.extract_from_work(work)
fvec_from_eenv1 = feat.FeatExtractor.extract_from_eenv(eenv1)
fvec_from_eenv2 = feat.FeatExtractor.extract_from_eenv(eenv2)

fvec1 = np.concatenate((fvec_from_work, fvec_from_eenv1))
fvec2 = np.concatenate((fvec_from_work, fvec_from_eenv2))
print(fvec1)
print(fvec2)

# 3. Compute the predicted operational intensity.
print('Predict operational intensity using Brain AI/ML model..')
model = predictor.ScikitLearnModel(pathlib.Path('my-sklearn-model.pkl'))
predictor = predictor.Predictor(model)

intensity1 = predictor.predict(fvec1)
intensity2 = predictor.predict(fvec2)
print(intensity1)
print(intensity2)

# 4. Estimate time and cost.
print('Estimated time and cost..')
flops1 = estimator.Estimator.calc_flops(eenv1, intensity1)
flops2 = estimator.Estimator.calc_flops(eenv2, intensity2)

est_time1 = estimator.Estimator.calc_time(num_flops, flops1)
est_time2 = estimator.Estimator.calc_time(num_flops, flops2)

est_cost1 = estimator.Estimator.calc_cost(est_time1, eenv1)
est_cost2 = estimator.Estimator.calc_cost(est_time2, eenv2)

# 5. Optimize over all pairs of (time, cost)
print('Pick optimal execution environment..')
optdata1 = optimizer.OptimizationData(work, eenv1, est_time1, est_cost1)
optdata2 = optimizer.OptimizationData(work, eenv2, est_time2, est_cost2)
target = optimizer.OptimizationTarget.COST

optimal = optimizer.SimpleOptimizer.pick((optdata1, optdata2), target)
print(optimal.est_cost)

# A. Test the catalog.
print('* Test catalog(AWS)..')
print(catalog.Catalog.get_unit_cost(
    instance_type=cloud.InstanceType.G6_XLARGE,
    use_spot=False,
    region=cloud.Region.US_EAST_1,
    zone=None,
    clouds=cloud.Cloud.AWS))

'''
import matildalink.cloud as cloud

print(cloud.InstanceType.G5_XLARGE.value)
print(type(cloud.InstanceType.G5_XLARGE.value))
print(cloud.InstanceType.G5_XLARGE.value == 'g5.xlarge')

print(cloud.Region.US_EAST_1.value)
print(type(cloud.Region.US_EAST_1.value))
print(cloud.Region.US_EAST_1.value == 'us-east-1')

print(cloud.Cloud.AWS.value)
print(cloud.Cloud.AWS.value == 'aws')
'''
