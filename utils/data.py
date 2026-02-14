from typing import Tuple 
from pathlib import Path
import pandas as pd 

def load_leetcodedataset_data(path_data:Path)->Tuple[pd.DataFrame, pd.DataFrame]:
    """ 
    loads data from local if exists, otherwhise from Huggingface and writes on local disk.
    """
    # Login using e.g. `huggingface-cli login` to access this dataset
    splits = {
        "train": "LeetCodeDataset-train.jsonl",
        "test": "LeetCodeDataset-test.jsonl",
    }

    train_path = path_data / splits["train"]
    test_path  = path_data / splits["test"]

    # Train data
    if not (train_path.exists() and train_path.with_suffix('.csv').exists()):
        df_train = pd.read_json(
            "hf://datasets/newfacade/LeetCodeDataset/" + splits["train"],
            lines=True,
        )
        df_train.to_json(train_path, orient="records", lines=True)
        df_train.to_csv(train_path.with_suffix('.csv'), index=False, encoding="utf-8-sig")
    else:
        df_train = pd.read_json(train_path, lines=True)

    # Test data
    if not (test_path.exists() and test_path.with_suffix('.csv').exists()):
        df_test = pd.read_json(
            "hf://datasets/newfacade/LeetCodeDataset/" + splits["test"],
            lines=True,
        )
        df_test.to_json(test_path, orient="records", lines=True)
        df_test.to_csv(test_path.with_suffix('.csv'), index=False, encoding="utf-8-sig")
    else:
        df_test = pd.read_json(test_path, lines=True)

    return df_train, df_test