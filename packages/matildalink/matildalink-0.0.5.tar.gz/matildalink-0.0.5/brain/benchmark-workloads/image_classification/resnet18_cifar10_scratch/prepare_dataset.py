import tensorflow_datasets as tfds

def download_dataset():
    tfds_name = 'cifar10'
    return tfds.load(tfds_name, with_info=True)

if __name__ == '__main__':
    prepare_dataset()
