"""
This file contains code that will kick off training and testing processes
"""
import os
import json

import numpy as np

from experiments.UNetExperiment import UNetExperiment
from data_prep.HippocampusDatasetLoader import LoadHippocampusData

class NumpyEncoder(json.JSONEncoder):
    """JSON encoder that converts numpy scalars/arrays to native Python types."""
    def default(self, o):
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        return super().default(o)

class Config:
    """
    Holds configuration parameters
    """
    def __init__(self):
        self.name = "Basic_unet"
        self.root_dir = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "..", "data", "TrainingSet"))
        self.n_epochs = 10
        self.learning_rate = 0.0002
        self.batch_size = 8
        self.patch_size = 64
        self.test_results_dir = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "results"))

if __name__ == "__main__":
    # Get configuration

    # TASK: Fill in parameters of the Config class and specify directory where the data is stored and 
    # directory where results will go
    c = Config()

    # Load data
    print("Loading data...")

    # TASK: LoadHippocampusData is not complete. Go to the implementation and complete it. 
    data = LoadHippocampusData(c.root_dir, y_shape = c.patch_size, z_shape = c.patch_size)


    # Create test-train-val split
    # In a real world scenario you would probably do multiple splits for 
    # multi-fold training to improve your model quality

    keys = range(len(data))

    # Here, random permutation of keys array would be useful in case if we do something like 
    # a k-fold training and combining the results. 

    split = dict()

    # TASK: create three keys in the dictionary: "train", "val" and "test". In each key, store
    # the array with indices of training volumes to be used for training, validation 
    # and testing respectively.
    np.random.seed(42)  # reproducible split
    keys = np.random.permutation(len(data))

    n_train = int(0.75 * len(keys))
    n_val = int(0.15 * len(keys))

    split["train"] = keys[:n_train]
    split["val"] = keys[n_train:n_train + n_val]
    split["test"] = keys[n_train + n_val:]

    print(f"Split: {len(split['train'])} train, {len(split['val'])} val, {len(split['test'])} test")

    # Set up and run experiment
    
    # TASK: Class UNetExperiment has missing pieces. Go to the file and fill them in
    exp = UNetExperiment(c, split, data)

    # You could free up memory by deleting the dataset
    # as it has been copied into loaders
    # del dataset 

    # run training
    exp.run()

    # prep and run testing

    # TASK: Test method is not complete. Go to the method and complete it
    results_json = exp.run_test()

    results_json["config"] = vars(c)

    with open(os.path.join(exp.out_dir, "results.json"), 'w') as out_file:
        json.dump(results_json, out_file, indent=2, separators=(',', ': '), cls=NumpyEncoder)

