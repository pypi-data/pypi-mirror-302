import tensorflow_datasets as tfds

def download_dataset():
    tfds_name = 'coco/2017'
    _, ds_info = tfds.load(tfds_name, with_info=True)

if __name__ == '__main__':
    download_dataset()
