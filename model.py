import kagglehub
from fastai.data.all import *
from fastai.text.data import TextBlock
from fastai.vision.all import *


def label_func(name):
    return "cat" if name.name[0].isupper() else "dog"


# Download latest version
# path = kagglehub.dataset_download("tanlikesmath/the-oxfordiiit-pet-dataset")
# print("Path to dataset files:", path)


dBlock = DataBlock(
    blocks=(ImageBlock, CategoryBlock),
    get_items=get_image_files,
    splitter=RandomSplitter(valid_pct=0.2, seed=42),
    get_y=label_func,
    item_tfms=[Resize(192, method='squish')],
).dataloaders("images")


learner = vision_learner(dBlock, resnet34, metrics=error_rate)
learner.fine_tune(3)


learner.export("model.pkl")


