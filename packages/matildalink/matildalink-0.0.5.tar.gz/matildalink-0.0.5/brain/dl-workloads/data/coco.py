import tensorflow_datasets as tfds

def prepare_dataset():
    return tfds.load('coco/2017', with_info=True)

if __name__ == '__main__':
    prepare_dataset()
