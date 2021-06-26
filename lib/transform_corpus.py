import random
import numpy as np
import pandas as pd

SEED = 324

np.random.seed(SEED)
random.seed(SEED)


def distribute(dist_type, dataset, feature, sample, output_dir):
    result = []
    labels = dataset.get_all_splits_labels()
    if "random" in dist_type:
        results = get_random_dataset(dataset)
        save_new_dataset(labels, result, "{}/{}.{}.{}".format(output_dir, dataset.name, dist_type))
    elif "unaligned" in dist_type:
        results = get_poor_alignments_dataset(dataset, "{}/{}.{}.tsv".format(output_dir, dataset.name, feature), sample)
        save_new_dataframe(labels, results, "{}/{}.{}.{}".format(output_dir, dataset.name, dist_type, sample))


def get_random_dataset(dataset):
    subsets_size = dataset.get_all_splits_size()
    subsets_data = dataset.get_all_splits_data_merged()
    start_index = 0
    results = []

    np.random.shuffle(subsets_data)

    for size in subsets_size:
        x = start_index
        y = start_index + size
        results.append(subsets_data[x:y])
        start_index += size

    return results


def save_new_dataset(labels, results, filename):
    for subset, label in zip(results, labels):
        with open("{}.{}.{}.txt.src".format(filename, label), 'w') as f1, \
                open("{}.{}.{}.txt.dst".format(filename, label), 'w') as f2:
            for comp, simple in subset:
                f1.write("{}\n".format(comp))
                f2.write("{}\n".format(simple))


def get_poor_alignments_dataset(dataset, filename, random_flag=True, sample=0.95):
    subsets_size = dataset.get_all_splits_size()
    subsets_samples = [int(i * sample) for i in subsets_size]

    data = pd.read_csv(filename, sep='\t', names=["Score", "Complex", "Simple"])
    data_clean = data.copy()
    data_clean = data_clean.sort_values(by="Score")
    data_clean = data_clean.head(int(sum(subsets_samples)))
    data_clean["Complex"] = data_clean["Complex"].apply(lambda i: i.strip())
    data_clean["Simple"] = data_clean["Simple"].apply(lambda i: i.strip())

    if random_flag:
        data_clean = data_clean.sample(frac=1, random_state=SEED).reset_index(drop=True)

    results = []
    start_index = 0

    for size in subsets_samples:
        x = start_index
        y = start_index + size
        results.append(data_clean[x:y])
        start_index += size

    return results


def save_new_dataframe(labels, results, filename):
    for df, label in zip(results, labels):
        with open("{}.{}.txt.src".format(filename, label), 'w') as f1, \
                open("{}.{}.txt.dst".format(filename, label), 'w') as f2:
            for comp, simple in zip(df["Complex"].values, df["Simple"].values):
                f1.write("{}\n".format(comp))
                f2.write("{}\n".format(simple))