## How to run a workload

```
python main.py -p [path/to/config/file]
```

## Configuration file structure

* debug
    * resnet_debug.yaml
    * retinanet_debug.yaml
    * maskrcnn_debug.yaml
    * bert_debug.yaml
* te
    * te_resnet_train/inference.yaml
    * te_retinanet_train/inference.yaml
    * te_maskrcnn_train/inference.yaml
    * te_bert_train/inference.yaml
* tr
    * tr_resnet_train/inference_idx.yaml
    * tr_retinanet_train/inference_idx.yaml
    * tr_maskrcnn_train/inference_idx.yaml
    * tr_bert_train/inference_idx.yaml
