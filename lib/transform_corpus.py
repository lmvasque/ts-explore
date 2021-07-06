import random
import numpy as np
import pandas as pd


def set_random(seed):
    np.random.seed(seed)
    random.seed(seed)


def distribute(dist_type, dataset, feature, sample, seed, input_dir, output_dir):
    set_random(seed)
    labels = dataset.get_all_splits_labels()
    if "random" in dist_type:
        results = get_random_dataset(dataset)
        save_new_dataset(labels, results, "{}/{}.{}.{}".format(output_dir, dataset.name, dist_type, seed))
    elif "unaligned" in dist_type:
        results = get_poor_alignments_dataset(dataset, "{}/{}.{}.tsv".format(input_dir, dataset.name, feature), seed,
                                              sample)
        save_new_dataframe(labels, results, "{}/{}.{}.{}.{}".format(output_dir, dataset.name, dist_type, seed, sample))


def get_random_dataset(dataset):
    subsets_size = dataset.get_all_splits_size()
    subsets_data = dataset.get_all_splits_data_merged()

    start_index = 0
    results = []
    # np.random.shuffle(subsets_data)
    random.shuffle(subsets_data)

    for size in subsets_size:
        x = start_index
        y = start_index + size
        results.append(subsets_data[x:y])
        start_index += size

    return results


def save_new_dataset(labels, results, filename):
    for subset, label in zip(results, labels):
        with open("{}.{}.txt.src".format(filename, label), 'w') as f1, \
                open("{}.{}.txt.dst".format(filename, label), 'w') as f2:
            for comp, simple in subset:
                f1.write("{}\n".format(comp))
                f2.write("{}\n".format(simple))


def get_poor_alignments_dataset(dataset, filename, seed, sample):
    subsets_size = dataset.get_all_splits_size()
    subsets_samples = []
    for i in subsets_size:
        subsets_samples.append(i * sample)

    data = pd.read_csv(filename, sep='\t', names=["Score", "Complex", "Simple"])
    data_clean = data.copy()
    data_clean = data_clean.sort_values(by="Score")
    data_clean = data_clean.head(int(sum(subsets_samples)))
    data_clean = data_clean.sample(frac=1, random_state=seed).reset_index(drop=True)
    data_clean['Complex'] = data_clean['Complex'].apply(lambda c: c.strip())
    data_clean['Simple'] = data_clean['Simple'].apply(lambda c: c.strip())

    results = []
    start_index = 0

    for size in subsets_samples:
        x = int(start_index)
        y = int(start_index + size)
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
