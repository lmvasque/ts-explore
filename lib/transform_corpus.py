import random
import numpy as np
import pandas as pd

from lib.config import DATA_SPLITS, RANDOM_SEED
from lib import stats


##################
##   COMMON     ##
##################
def set_random(seed):
    np.random.seed(seed)
    random.seed(seed)


##################
##   PAPER #1   ##
##################
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


##################
##   PAPER #2   ##
##################
def distribute_distinct(dist_type, dataset, feature, sample, seed, input_dir, output_dir):
    set_random(seed)
    labels = dataset.get_all_splits_labels()
    if "random" in dist_type:
        results = build_random_seed_set(dataset, seed)
        out_file = "{}/{}.{}.{}".format(output_dir, dataset.name, dist_type, seed)
        save_new_dataset(labels, results, out_file)
    elif "unaligned" in dist_type:
        results = build_poor_alignments_set(dataset, sample)

        sample = str(sample)
        if len(sample) <= 3:
            sample = "{}0".format(sample)

        out_file = "{}/{}.{}.{}.{}".format(output_dir, dataset.name, dist_type, seed, sample)
        save_new_dataset(labels, results, out_file)


def build_poor_alignments_set(dataset, sample):
    all_data = dataset.get_all_splits_data()
    results = []

    for s, t in zip(all_data, DATA_SPLITS):
        edit_values = calculate_edit_distances(s)
        data = remove_poor_alignments(s, edit_values, sample)
        results.append(data)

    return results


def calculate_edit_distances(s):
    results = []
    for x, y in s:
        z = stats.feature(x, y, stats.CHANGE_PERCENTAGE_LOWER)
        results.append(z)
    return results


def remove_poor_alignments(data, values, sample):
    lines_num = int(len(data) * (1 - sample))

    for i in range(0, lines_num):
        max_num = max(values)
        del_index = values.index(max_num)
        data.pop(del_index)
        values.pop(del_index)

    return data


def build_random_seed_set(dataset, seed):
    random.seed(seed)
    subsets = get_random_dataset(dataset)
    random.seed(RANDOM_SEED)

    return subsets


def shuffle_data(dataset, data, sets, sampling=1):
    random.shuffle(data)
    test_size = round(len(dataset.test * sampling))
    dev_size = round(len(dataset.dev * sampling))

    if "Test/Dev" in sets:
        test_set_rand, dev_set_rand, train_set_rand = data[:test_size], data[test_size:test_size + dev_size], []
    else:
        test_set_rand, dev_set_rand, train_set_rand = data[:test_size], data[test_size:test_size + dev_size], \
                                                      data[test_size + dev_size:]

    return test_set_rand, dev_set_rand, train_set_rand


def distribute_data_monte_carlo(data, in_subsets_size, iterations, tag):
    # log.info("Iterations: {}".format(iterations))
    print("Iterations: {}".format(iterations))
    shuffle_data = np.copy(data)
    x, y, z = get_data_percentages(in_subsets_size, len(data))
    min_std, min_set = create_mc_set(shuffle_data, x, y, z)

    for i in range(iterations):
        min_std_new, min_set_new = create_mc_set(shuffle_data, x, y, z)

        if min_std_new < min_std:
            min_std = min_std_new
            min_set = min_set_new

        if i % 1000 == 0:
            # log.info("Amount of items processed: {}/{}: {}%".format(i, iterations, (i / iterations) * 100))
            print("Amount of items processed: {}/{}: {}%".format(i, iterations, (i / iterations) * 100))

    return min_set


def create_mc_set(shuffle_data, x, y, z):
    np.random.shuffle(shuffle_data)
    sets = [shuffle_data[:x], shuffle_data[x:x + y], shuffle_data[x + y:x + y + z]]

    set_std = []
    for j, s in enumerate(sets):
        op_sum = np.sum(s[:, 1:], axis=0)
        set_std.append(np.std(op_sum))

    return np.std(set_std), sets


def get_data_percentages(in_subsets_size, total_data):
    total_subsets = sum(in_subsets_size)

    percentages = [in_subsets_size[0] / total_subsets,
                   in_subsets_size[1] / total_subsets,
                   in_subsets_size[2] / total_subsets]
    percentages = [round(p * total_data) for p in percentages]

    return percentages
