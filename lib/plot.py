import matplotlib.pyplot as plt
import matplotlib.style as style
import matplotlib.ticker as mtick
import numpy as np
import time
import pandas
from lib.config import COLORS, DATA_SPLITS

style.use('tableau-colorblind10')


def hist(x, title, labels, feature, output_dir):
    plt.rcParams.update({'font.size': 16})

    if len(x) == 0:
        print("{}: There is no data available to plot. Size: {}", __file__, 0)
        return

    new_labels = []
    for label in labels:
        if "Tune" in label:
            new_labels.append("Dev")
        else:
            new_labels.append(label)

    data_to_plot = x
    if len(x) > 1:
        data_to_plot = np.array(x, dtype="object")  # This avoids the 'VisibleDeprecationWarning' notice
        np.save("{}/{}.{}.{}".format(output_dir, title, feature, time.time()), data_to_plot)
    else:
        np.save("{}/{}.{}.{}".format(output_dir, title, feature, time.time()), np.array(data_to_plot))

    plt.hist(data_to_plot, histtype='bar', stacked=False, label=new_labels, density=True)
    # plt.hist(data_to_plot, histtype='bar', stacked=False, label=new_labels)

    if "percentage" in feature:
        plt.xlim(0, 100)

    # p_format = "{:.3f}"
    # new_ticks = [p_format.format(x) for x in plt.gca().get_yticks()]
    # plt.gca().set_yticklabels(new_ticks)

    # plt.title("{} dataset".format(title.capitalize()))
    plt.legend()
    plt.savefig("{}/{}.{}.svg".format(output_dir, title, feature), bbox_inches='tight')
    plt.clf()


    # plt.show()


def scat(test_dev, test_train, metric, output_dir):
    datasets_test_dev, results_test_dev = test_dev
    datasets_test_train, results_test_train = test_train

    print_stats(datasets_test_dev, results_test_dev, datasets_test_train, results_test_train)

    plt.scatter(datasets_test_dev, results_test_dev, label="Test vs Dev", color=[COLORS[0]], alpha=1)
    plt.scatter(datasets_test_train, results_test_train, label="Test vs Train", color=[COLORS[1]], alpha=1)

    if metric is "js":
        plt.title("Jensen-Shannon Divergence (distance)")
    else:
        plt.title("Kullback-Leibler Divergence (nats)")

    plt.yticks(np.arange(0, 0.55, step=0.05))
    plt.ylim(0, 0.5)
    plt.legend(loc=9)
    plt.savefig("{}/{}_distribution_analysis_all_datasets.png".format(output_dir, metric))
    # plt.show()


def print_stats(datasets_test_dev, results_test_dev, datasets_test_train, results_test_train):
    if datasets_test_dev:
        print("\nDistribution divergences between Test/Dev subsets")
        pretty_print(datasets_test_dev, results_test_dev)

    if datasets_test_train:
        print("\nDistribution divergences between Test/Train subsets")
        pretty_print(datasets_test_train, results_test_train)


def pretty_print(set_a, set_b):
    data = zip(set_a, set_b)
    df = pandas.DataFrame(data, columns=["Dataset", "Value"])
    print(df.to_string(index=False))


def count_operations(x, dataset):
    labels = DATA_SPLITS[0:2]
    width = 0.2
    deletes = []
    inserts = []
    replaces = []
    total_count = 0

    r1 = np.arange(len(labels))
    r2 = [x + width for x in r1]
    r3 = [x + width for x in r2]

    for i, split in enumerate(x[0:2]):
        delete_count = 0
        insert_count = 0
        replace_count = 0
        for sent in split:
            delete_count += sent.count("DELETE")
            insert_count += sent.count("INSERT")
            replace_count += sent.count("REPLACE")
            total_count += len(sent)

        deletes.append(delete_count)
        inserts.append(insert_count)
        replaces.append(replace_count)

        total_count = delete_count + insert_count + replace_count
        deletes_p = delete_count / total_count
        inserts_p = insert_count / total_count
        replaces_p = replace_count / total_count

        print("{},{},{},{},{}".format(dataset, i, deletes_p, inserts_p, replaces_p))

    fig, ax = plt.subplots()
    ax.bar(r1, deletes_p, width, label="Deletes")
    ax.bar(r2, inserts_p, width, label="Inserts")
    ax.bar(r3, replaces_p, width, label="Replace")

    # plt.title(title)
    ax.set_xticks([r + width for r in range(len(labels))])
    ax.set_xticklabels(labels)
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))
    plt.legend()
    fig.tight_layout()
    plt.show()

    return [deletes, inserts, replaces]