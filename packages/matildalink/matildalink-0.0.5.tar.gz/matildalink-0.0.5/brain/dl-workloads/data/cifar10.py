import tensorflow_datasets as tfds

def prepare_dataset(with_info=True):
    tfds_name = 'cifar10'
    return tfds.load(tfds_name, with_info=with_info)

if __name__ == '__main__':
    ds, ds_info = prepare_dataset()
    print(ds_info)
