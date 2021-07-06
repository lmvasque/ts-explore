import numpy as np
from scipy.spatial.distance import jensenshannon
from scipy.special import kl_div

from lib import stats


def analyze_corpus_using_datasets(dataset, feature, output_dir, save_results=False):
    labels = dataset.get_all_splits_labels()
    results = [[] for _ in labels]
    full_results = []
    data = dataset.get_all_splits_data()
    for i, split in enumerate(data):

        count = 0
        for x, y in split:
            dist = stats.feature(x, y, feature)
            results[i].append(dist)
            full_results.append([dist, x, y])
            count += 1

        dataset.splits_feature[labels[i]] = results[i]

    if save_results:
        filename = "{}/{}.{}".format(output_dir, dataset.name, feature)
        full_results = sorted(full_results, key=lambda z: z[0])
        save_txt_file(full_results, filename)

    return results


def save_txt_file(results, filename):
    with open("{}.tsv".format(filename), 'w') as f:
        for item in results:
            score = item[0]
            comp = item[1]
            simple = item[2]
            f.write("{}\t{}\t{}\n".format(score, comp, simple))


def compare_distribution(datasets, metric="kl"):
    datasets_test_dev = []
    results_test_dev = []

    datasets_test_train = []
    results_test_train = []

    for k, d in datasets.items():
        if d.has_test() and d.has_dev():
            print("Comparing test and dev distributions for {}..".format(k))
            results_test_dev.append(get_dist_analysis(d.splits_feature["test"],
                                                      d.splits_feature["dev"],
                                                      metric))
            datasets_test_dev.append(k)

        if d.has_test() and d.has_train():
            print("Comparing test and train distributions for {}..".format(k))
            results_test_train.append(get_dist_analysis(d.splits_feature["test"],
                                                        d.splits_feature["train"],
                                                        metric))
            datasets_test_train.append(k)

    if not datasets_test_dev and not datasets_test_train:
        raise Exception("The provided datasets does not have any split pair (e.g., test/dev or test/train) to compare.")

    return (datasets_test_dev, results_test_dev), (datasets_test_train, results_test_train)


def get_dist_analysis(set_a, set_b, metric):
    a = kl_analysis_hist(set_a)
    b = kl_analysis_hist(set_b)

    if metric is "js":
        result = jensenshannon(a, b, base=2)
    else:
        result = sum(kl_div(a, b))

    return result


def kl_analysis_hist(x):
    values, _ = np.histogram(x)
    return stats.values_to_pdist(values)


def merge_datasets_turk(output_dir, tag):
    merge_datasets(output_dir, tag, "{}.8turkers.tok.norm", "{}.8turkers.tok.turk.{}", "../data/turkcorpus",
                   "turkcorpus",
                   8, ["{}.8turkers.tok.simp".format(tag)])


def merge_datasets_asset(output_dir, tag, ):
    merge_datasets(output_dir, tag, "asset.{}.orig.new", "asset.{}.simp.{}.new", "../data/asset", "asset", 10, [])


def merge_datasets(output_dir, tag, template_complex, template_simple, root, name, num_ref, simple_sent_init):
    complex_sent = template_complex.format(tag)
    simple_sent = simple_sent_init

    for i in range(0, num_ref):
        simple_sent.append(template_simple.format(tag, i))

    results_complex = []
    results_simple = []
    for ref in simple_sent:
        with open("{}/{}".format(root, complex_sent), 'r') as f1, \
                open("{}/{}".format(root, ref), 'r') as f2:
            for x, y in zip(f1, f2):
                results_complex.append(x)
                results_simple.append(y)

    with open("{}/{}.{}.orig.all".format(output_dir, name, tag), 'w') as f3, \
            open("{}/{}.{}.simp.all".format(output_dir, name, tag), 'w') as f4:
        for a, b in zip(results_complex, results_simple):
            f3.write(a)
            f4.write(b)
