import matplotlib.pyplot as plt
import matplotlib.style as style
import numpy as np
import pandas
from config import COLORS

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

    plt.hist(data_to_plot, histtype='bar', stacked=False, label=new_labels, density=True)

    if "percentage" in feature:
        plt.xlim(0, 100)

    p_format = "{:.3f}"
    new_ticks = [p_format.format(x) for x in plt.gca().get_yticks()]
    plt.gca().set_yticklabels(new_ticks)

    plt.title("{} dataset".format(title.capitalize()))
    plt.legend()
    plt.savefig("{}/{}.{}.png".format(output_dir, title, feature), bbox_inches='tight')
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
