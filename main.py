from prepare_dataset.create_dataset import *
import yaml

with open(r'utilities/configs.yml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    config = yaml.load(file, Loader=yaml.FullLoader)

dataset_preparing = PreparingDataset(config = config)
dataset_preparing.run()