import argparse
import os
from pathlib import Path

from lib import stats, corpus_analysis, plot, transform_corpus
from lib.dataset import Dataset


class TsEval(object):

    def __init__(self, output_dir):
        self.datasets_results = {}
        self.analysis_results = []

        self.output_dir = output_dir.strip("/")
        self.img_dir = "{}/img".format(self.output_dir)
        self.npy_dir = "{}/npy".format(self.output_dir)
        self.txt_dir = "{}/txt".format(self.output_dir)

        self.setup_dirs()
        pass

    def setup_dirs(self):

        paths = [self.img_dir, self.npy_dir, self.txt_dir]

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

    def analyse(self, save_results=True):
        features = [stats.CHANGE_PERCENTAGE_LOWER]
        for f in features:
            for k, v in self.datasets_results.items():
                self.analysis_results = corpus_analysis.analyze_corpus_using_datasets(v, f, self.txt_dir, save_results)
                plot.hist(self.analysis_results, k, v.get_all_splits_labels(), f, self.img_dir)

    def get_dist_analysis(self):
        print("Comparing KL distribution divergence between distributions..")
        test_dev, test_train = corpus_analysis.compare_distribution(self.datasets_results)
        plot.scat(test_dev, test_train, "kl", self.img_dir)

    def get_new_dist_dataset(self, dist_type, sample):
        for _, v in self.datasets_results.items():
            if "random" or "unaligned" in dist_type:
                transform_corpus.distribute(dist_type, v, stats.CHANGE_PERCENTAGE_LOWER, sample, self.txt_dir)
            else:
                raise Exception(
                    "ERROR: Unsupported algorithm for distributing datasets. Options available: random or unaligned")


def get_user_params():
    parser = argparse.ArgumentParser(description='TS datasets analysis')

    parser.add_argument("-a", "--analysis", action="store_true", help='Datasets analysis by edit-distance')
    parser.add_argument("-c", "--create", help='Create better distributed datasets')
    parser.add_argument("-o", "--output_dir", help="Output directory")
    parser.add_argument("-d", "--datasets", help="Datasets JSON file")
    parser.add_argument("-s", "--sample", help="Poor alignments percentage to remove. For example: 0.03, 0.05")

    args = parser.parse_args()

    if args.output_dir:
        output_dir = args.output_dir
    else:
        raise Exception("ERROR: Output directory is not defined. "
                        "Please provide a valid directory using: --output_dir [path]")

    if args.datasets:
        datasets = args.datasets
    else:
        raise Exception("ERROR: No datasets file defined, please a valid file using --datasets flag.")

    if args.sample:
        sample = args.sample
    else:
        sample = 1

    if args.analysis:
        print("Running datasets analysis..")
        analyze(datasets, output_dir)
    elif args.create:
        print("Creating better distributed datasets..")
        create(datasets, sample, args.create, output_dir)
    else:
        raise Exception("ERROR: No mode was defined, please select one of the following flags: [--analysis, --create]")


def analyze(datasets, output_dir):
    ts_eval = TsEval(output_dir)
    ts_eval.load_datasets(datasets)
    ts_eval.analyse(save_results=True)
    ts_eval.get_dist_analysis()


def create(datasets, sample, flag, output_dir):
    if "random" in flag:
        ts_eval = TsEval(output_dir)
        ts_eval.load_datasets(datasets)
        ts_eval.get_new_dist_dataset("random")
    elif "unaligned" in flag:
        ts_eval = TsEval(output_dir)
        ts_eval.load_datasets(datasets)
        ts_eval.analyse(save_results=True)
        ts_eval.get_new_dist_dataset("unaligned", sample)
    else:
        raise Exception("ERROR: Invalid values for --create flag. Valid values are: 'random' or 'unaligned'")


def main():
    import time
    start = time.time()
    get_user_params()
    end = time.time()
    print("Time elapsed: {} min".format((end - start) / 60))


main()
