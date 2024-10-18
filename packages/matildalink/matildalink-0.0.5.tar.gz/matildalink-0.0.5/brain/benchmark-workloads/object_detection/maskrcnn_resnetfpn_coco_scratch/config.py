from typing import Optional
import dataclasses

import tensorflow as tf

from official.core import config_definitions as cfg
from official.core import task_factory

from official.vision.configs import maskrcnn as maskrcnn_config
from official.vision.configs import common
from official.vision.configs.maskrcnn import Anchor, DetectionGenerator

from official.vision.dataloaders import tfds_factory, maskrcnn_input, input_reader, input_reader_factory
from official.vision.tasks import maskrcnn as maskrcnn_task

from official.common import dataset_fn as dataset_fn_lib

from official.modeling import optimization

@dataclasses.dataclass
class MRTaskConfig(maskrcnn_config.MaskRCNNTask):
    pass

@task_factory.register_task_cls(MRTaskConfig)
class MRTask(maskrcnn_task.MaskRCNNTask):

    def build_inputs(self, params: maskrcnn_config.DataConfig, input_context: Optional[tf.distribute.InputContext] = None, dataset_fn: Optional[dataset_fn_lib.PossibleDatasetType] = None) -> tf.data.Dataset:

        decoder = tfds_factory.get_detection_decoder(params.tfds_name)

        parser = maskrcnn_input.Parser(
            output_size=self.task_config.model.input_size[:2],
            min_level=self.task_config.model.min_level,
            max_level=self.task_config.model.max_level,
            num_scales=self.task_config.model.anchor.num_scales,
            aspect_ratios=self.task_config.model.anchor.aspect_ratios,
            anchor_size=self.task_config.model.anchor.anchor_size,
            rpn_match_threshold=params.parser.rpn_match_threshold,
            rpn_unmatched_threshold=params.parser.rpn_unmatched_threshold,
            rpn_batch_size_per_im=params.parser.rpn_batch_size_per_im,
            rpn_fg_fraction=params.parser.rpn_fg_fraction,
            aug_rand_hflip=params.parser.aug_rand_hflip,
            aug_rand_vflip=params.parser.aug_rand_vflip,
            aug_scale_min=params.parser.aug_scale_min,
            aug_scale_max=params.parser.aug_scale_max,
            aug_type=params.parser.aug_type,
            skip_crowd_during_training=params.parser.skip_crowd_during_training,
            max_num_instances=params.parser.max_num_instances,
            include_mask=self.task_config.model.include_mask,
            outer_boxes_scale=self.task_config.model.outer_boxes_scale,
            mask_crop_size=params.parser.mask_crop_size,
            dtype=params.dtype
        )

        if not dataset_fn:
            dataset_fn = dataset_fn_lib.pick_dataset_fn(params.file_type)

        reader = input_reader_factory.input_reader_generator(
            params,
            dataset_fn=dataset_fn,
            decoder_fn=decoder.decode,
            combine_fn=input_reader.create_combine_fn(params),
            parser_fn=parser.parse_fn(params.is_training)
        )

        dataset = reader.read(input_context=input_context)

        return dataset
        
def mrcnn_resnetfpn_coco_scratch():

    coco_train_samples = 118280 # acutal: 118287
    train_batch_size = 8
    steps_per_epoch = 1250
    epochs = 30

    coco_val_samples = 5000
    eval_batch_size = 8

    config = cfg.ExperimentConfig(
      runtime=cfg.RuntimeConfig(
          mixed_precision_dtype='bfloat16', enable_xla=True),
      task=MRTaskConfig(
          init_checkpoint=None,
          init_checkpoint_modules='backbone',
          annotation_file=None,
          model=maskrcnn_config.MaskRCNN(
              num_classes=91, 
              input_size=[640,640,3], 
              anchor=Anchor(anchor_size=3),
              norm_activation=common.NormActivation(norm_epsilon=0.001, norm_momentum=0.99, use_sync_bn=True),
              detection_generator=DetectionGenerator(pre_nms_top_k=1000),
              min_level=3,
              max_level=7,
              include_mask=False),
          losses=maskrcnn_config.Losses(l2_weight_decay=0.00008),
          train_data=maskrcnn_config.DataConfig(
              input_path='',
              is_training=True,
              global_batch_size=train_batch_size,
              tfds_name='coco/2017',
              tfds_split='train',
              parser=maskrcnn_config.Parser(
                  aug_rand_hflip=True, aug_scale_min=0.5, aug_scale_max=2.0)),
          validation_data=maskrcnn_config.DataConfig(
              input_path='',
              is_training=False,
              global_batch_size=eval_batch_size,
              tfds_name='coco/2017',
              tfds_split='validation',
              drop_remainder=False)),
      trainer=cfg.TrainerConfig(
          train_steps=steps_per_epoch*epochs,
          validation_steps=coco_val_samples // eval_batch_size,
          validation_interval=steps_per_epoch,
          steps_per_loop=steps_per_epoch,
          summary_interval=steps_per_epoch,
          checkpoint_interval=steps_per_epoch,
          optimizer_config=optimization.OptimizationConfig({
              'optimizer': {
                  'type': 'sgd',
                  'sgd': {
                      'momentum': 0.9
                  }
              },
              'learning_rate': {
                  'type': 'stepwise',
                  'stepwise': {
                      'boundaries': [15000, 20000],
                      'values': [0.32, 0.032, 0.0032],
                  }
              },
              'warmup': {
                  'type': 'linear',
                  'linear': {
                      'warmup_steps': 500,
                      'warmup_learning_rate': 0.0067
                  }
              }
          })),
      restrictions=['task.train_data.is_training != None','task.validation_data.is_training != None']
    )

    return config

