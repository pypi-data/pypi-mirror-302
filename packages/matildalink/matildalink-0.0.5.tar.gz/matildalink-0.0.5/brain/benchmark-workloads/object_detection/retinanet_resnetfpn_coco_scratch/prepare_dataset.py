import tensorflow_datasets as tfds

def download_dataset():
    _, ds_info = tfds.load('coco/2017', with_info=True)

if __name__ == '__main__':
    download_dataset()
