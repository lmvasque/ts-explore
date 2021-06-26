class Dataset(object):

    def __init__(self, name, src_tag="src", dst_tag="dst"):
        self.splits = {}
        self.splits_feature = {}
        self.split_labels = ["test", "dev", "train"]
        self.name = name
        self.src_tag = src_tag
        self.dst_tag = dst_tag

    def add_split(self, name, file):
        if name in self.split_labels:
            self.splits[name] = {}
            self.splits[name]["file"] = file
            self.splits[name]["data"] = []
        else:
            raise Exception("'{}' is not a supported split! Please use one of the following labels: {}"
                            .format(name, ", ".join(self.split_labels)))

    def load(self, file):
        result = []
        with open("{}.{}".format(file, self.src_tag), encoding='utf8') as f1, \
                open("{}.{}".format(file, self.dst_tag), encoding='utf8') as f2:
            for x, y in zip(f1, f2):
                result.append([x.strip(), y.strip()])
        return result

    def load_split(self, tag):
        if tag in self.splits:
            x = self.load(self.splits[tag]["file"])
            self.splits[tag]["data"].extend(x)

    def load_all(self):
        self.load_split("test")
        self.load_split("dev")
        self.load_split("train")

    def get_all_splits_data(self):
        data = []
        for label in self.split_labels:
            if label in self.splits:
                data.append(self.splits[label]["data"])
        return data

    def get_all_splits_data_merged(self):
        data = []
        for label in self.split_labels:
            if label in self.splits:
                for item in self.splits[label]["data"]:
                    data.append(item)
        return data

    def get_all_splits_labels(self):
        labels = []
        for label in self.split_labels:
            if label in self.splits:
                labels.append(label)
        return labels

    def get_all_splits_size(self):
        sizes = []
        for label in self.split_labels:
            if label in self.splits:
                sizes.append(len(self.splits[label]["data"]))
        return sizes

    def has_test(self):
        return "test" in self.splits

    def has_dev(self):
        return "dev" in self.splits

    def has_train(self):
        return "train" in self.splits
