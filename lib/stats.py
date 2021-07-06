from py4j.java_gateway import JavaGateway

from lib.config import *


def lev_per_word_percentage_lower_case(sent_a, sent_b):
    return lev_per_word_percentage(sent_a, sent_b, "lower")


def lev_per_word_percentage(sent_a, sent_b, case="default"):
    gateway = JavaGateway()
    edit_distance = gateway.entry_point.getEditDistance()

    if case == 'lower':
        sent_a = sent_a.lower()
        sent_b = sent_b.lower()

    result = edit_distance.calculate(sent_a, sent_b, "percentage")
    return result


def values_to_pdist(values):
    total = sum(values)

    if total != 0:
        result = [x / total for x in values]
    else:
        result = values

    return result


def simple_len(sent_a, sent_b):
    return len(sent_a) - len(sent_b)


FEATURES = {
    CHANGE_PERCENTAGE_LOWER: lev_per_word_percentage_lower_case,
    LEN_DIFF: simple_len
}


def feature(sent_a, sent_b, name):
    return FEATURES[name](sent_a, sent_b)
