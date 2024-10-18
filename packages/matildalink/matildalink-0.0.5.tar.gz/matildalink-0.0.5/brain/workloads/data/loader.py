import tensorflow as tf
import tensorflow_datasets as tfds

from official.common import dataset_fn

from official.core import task_factory
from official.core.config_definitions import ExperimentConfig

from official.vision.configs import image_classification as exp_cfg, maskrcnn as maskrcnn_config
from official.vision.dataloaders import tfds_factory, classification_input, input_reader, input_reader_factory, retinanet_input
from official.vision.dataloaders import retinanet_input, maskrcnn_input

from official.nlp.data.pretrain_text_dataloader import BertPretrainTextDataConfig
from official.nlp.data import data_loader_factory

def cifar10(tfm_config: ExperimentConfig, input_context=None):

    params = tfm_config.task.train_data

    tfds_name = 'cifar10'
    tfds.load(tfds_name, with_info=True)

    num_classes = 10
    input_size = [32, 32, 3]
    image_field_key = 'image/encoded'
    label_field_key = 'image/class/label'
    is_multilabel = False

    decoder = tfds_factory.get_classification_decoder(tfds_name)

    parser = classification_input.Parser(
        output_size=input_size[:2],
        num_classes=num_classes,
        image_field_key=image_field_key,
        label_field_key=label_field_key,
        decode_jpeg_only=True,
        aug_rand_hflip=True,
        aug_crop=False,
        aug_type=None,
        color_jitter=0.0,
        random_erasing=None,
        is_multilabel=is_multilabel,
        dtype='float32',
        center_crop_fraction=0.875,
        tf_resize_method='bilinear',
        three_augment=False)
    
    reader = input_reader_factory.input_reader_generator(
        params,
        dataset_fn=dataset_fn.pick_dataset_fn(params.file_type),
        decoder_fn=decoder.decode,
        combine_fn=input_reader.create_combine_fn(params),
        parser_fn=parser.parse_fn(params.is_training)
    )

    dataset = reader.read(input_context=input_context)
    return dataset

def coco_retinanet(tfm_config: ExperimentConfig, input_context=None):

    task_config = tfm_config.task
    params = task_config.train_data

    decoder = tfds_factory.get_detection_decoder(params.tfds_name)

    parser = retinanet_input.Parser(
        output_size=task_config.model.input_size[:2],
        min_level=task_config.model.min_level,
        max_level=task_config.model.max_level,
        num_scales=task_config.model.anchor.num_scales,
        aspect_ratios=task_config.model.anchor.aspect_ratios,
        anchor_size=task_config.model.anchor.anchor_size,
        dtype=params.dtype,
        match_threshold=params.parser.match_threshold,
        unmatched_threshold=params.parser.unmatched_threshold,
        box_coder_weights=(
            task_config.model.detection_generator.box_coder_weights
        ),
        aug_type=params.parser.aug_type,
        aug_rand_hflip=params.parser.aug_rand_hflip,
        aug_rand_jpeg=None,
        aug_scale_min=params.parser.aug_scale_min,
        aug_scale_max=params.parser.aug_scale_max,
        skip_crowd_during_training=params.parser.skip_crowd_during_training,
        max_num_instances=params.parser.max_num_instances,
        pad=params.parser.pad,
        keep_aspect_ratio=params.parser.keep_aspect_ratio,
    )

    reader = input_reader_factory.input_reader_generator(
        params,
        dataset_fn=dataset_fn.pick_dataset_fn(params.file_type),
        decoder_fn=decoder.decode,
        combine_fn=input_reader.create_combine_fn(params),
        parser_fn=parser.parse_fn(params.is_training))

    dataset = reader.read(input_context=input_context)

    return dataset

def coco_maskrcnn(tfm_config: ExperimentConfig, input_context=None):

    task_config = tfm_config.task
    params = task_config.train_data

    decoder = tfds_factory.get_detection_decoder(params.tfds_name)
    parser = maskrcnn_input.Parser(
        output_size=task_config.model.input_size[:2],
        min_level=task_config.model.min_level,
        max_level=task_config.model.max_level,
        num_scales=task_config.model.anchor.num_scales,
        aspect_ratios=task_config.model.anchor.aspect_ratios,
        anchor_size=task_config.model.anchor.anchor_size,
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
        include_mask=task_config.model.include_mask,
        outer_boxes_scale=task_config.model.outer_boxes_scale,
        mask_crop_size=params.parser.mask_crop_size,
        dtype=params.dtype
    )

    reader = input_reader_factory.input_reader_generator(
        params,
        dataset_fn=dataset_fn.pick_dataset_fn(params.file_type),
        decoder_fn=decoder.decode,
        combine_fn=input_reader.create_combine_fn(params),
        parser_fn=parser.parse_fn(params.is_training)
    )

    dataset = reader.read(input_context=input_context)

    return dataset

def wiki_bert(tfm_config: ExperimentConfig, input_context=None):
    data_config = BertPretrainTextDataConfig(tfm_config.task.train_data)
    return data_loader_factory.get_data_loader(data_config).load(input_context)

def load(tfm_config: ExperimentConfig, input_context=None):
    task_name = tfm_config.task.name
    if task_name == 'image_classification':
        return cifar10(tfm_config, input_context)
    elif task_name == 'object_detection_retinanet':
        return coco_retinanet(tfm_config, input_context)
    elif task_name == 'object_detection_maskrcnn':
        return coco_maskrcnn(tfm_config, input_context)
    elif task_name == 'natural_language_processing':
        return wiki_bert(tfm_config, input_context)
    else:
        return None

