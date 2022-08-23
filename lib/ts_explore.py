import json
import os
from pathlib import Path

from lib import stats, corpus_analysis, plot, transform_corpus
from lib.dataset import Dataset


class TsExplore(object):

    def __init__(self, output_dir):
        self.datasets_results = {}
        self.analysis_results = []

        self.output_dir = output_dir.strip("/")
        self.img_dir = "{}/img".format(self.output_dir)
        self.npy_dir = "{}/npy".format(self.output_dir)
        self.txt_dir = "{}/txt/".format(self.output_dir)
        self.dataset_dir = "{}/datasets".format(self.output_dir)
        self.txt_distinct_dir = "{}/txt/random.distinct".format(self.output_dir)
        self.dataset_distinct_dir = "{}/datasets/random.distinct".format(self.output_dir)
        self.txt_unalig_distinct_dir = "{}/txt/unaligned.distinct".format(self.output_dir)
        self.dataset_unalig_distinct_dir = "{}/datasets/unaligned.distinct".format(self.output_dir)

        self.setup_dirs()
        pass

    def setup_dirs(self):

        paths = [self.img_dir, self.npy_dir, self.txt_dir, self.txt_distinct_dir, self.dataset_distinct_dir,
                 self.txt_unalig_distinct_dir, self.dataset_unalig_distinct_dir]

        for p in paths:
            if not Path.exists(Path(p)):
                os.makedirs(p)

    def load_datasets(self, datasets):

        print("Running scripts in directory: {}".format(Path.cwd()))
        with open(datasets) as f:
            data = json.load(f)
            for d in data:
                src_tag, dst_tag = data[d]["tag"]
                del (data[d]["tag"])
                dataset = Dataset(d, src_tag=src_tag, dst_tag=dst_tag)

                for split in data[d]:
                    dataset.add_split(split, data[d][split])

                dataset.load_all()
                self.datasets_results[d] = dataset

        return self.datasets_results

    def analyse(self, save_results=True, plot_results=True):
        features = [stats.CHANGE_PERCENTAGE_LOWER]
        for f in features:
            for k, v in self.datasets_results.items():
                self.analysis_results = corpus_analysis.analyze_corpus_using_datasets(v, f, self.txt_dir, save_results)

                if plot_results:
                    plot.hist(self.analysis_results, k, v.get_all_splits_labels(), f, self.img_dir)

    def get_dist_analysis(self):
        print("Comparing KL distribution divergence between distributions..")
        test_dev, test_train = corpus_analysis.compare_distribution(self.datasets_results)
        plot.scat(test_dev, test_train, "kl", self.img_dir)

    def get_new_dist_dataset(self, dist_type, sample, seed):
        for _, v in self.datasets_results.items():
            if "random" or "unaligned" in dist_type:
                transform_corpus.distribute(dist_type, v, stats.CHANGE_PERCENTAGE_LOWER, sample, seed, self.txt_dir,
                                            self.dataset_dir)
            else:
                raise Exception(
                    "ERROR: Unsupported algorithm for distributing datasets. Options available: random or unaligned")

    ############################
    ######## PAPER 2 ###########
    ############################
    def analyse_operations(self, save_results=True, plot_results=True):
        features = [stats.EDIT_OPERATIONS_TYPES_LOWER]
        for f in features:
            for k, v in self.datasets_results.items():
                self.analysis_results = corpus_analysis.analyze_corpus_using_datasets(v, f, self.txt_dir, save_results)

                if plot_results:
                    # This is for figure 3: we need the results of all datasets!
                    plot.count_operations(self.analysis_results, k)

    def get_new_dist_dataset_distinct(self, dist_type, sample, seed):
        for _, v in self.datasets_results.items():
            if "random" or "unaligned" in dist_type:
                transform_corpus.distribute_distinct(dist_type, v, stats.CHANGE_PERCENTAGE_LOWER, sample, seed,
                                                     self.txt_unalig_distinct_dir,
                                                     self.dataset_unalig_distinct_dir)
            else:
                raise Exception(
                    "ERROR: Unsupported algorithm for distributing datasets. Options available: random or unaligned")


def validate_params(args):
    if not args.output_dir:
        raise Exception("ERROR: Output directory is not defined. Please provide a valid directory "
                        "using: --output_dir [path]")

    if not args.datasets:
        raise Exception("ERROR: No datasets file defined, please a valid file using --datasets flag.")

    if not args.analysis and not args.load_data:
        raise Exception("ERROR: No mode was defined, please select one of the following flags: [--analysis, --create]")
