import argparse

from py4j.java_gateway import JavaGateway

parser = argparse.ArgumentParser()
parser.add_argument("--source", type=str, default="The house was painted last week by John .", help="Source sentence")
parser.add_argument("--target", type=str, default="John painted the house last week .", help="Target sentence")
args = parser.parse_args()


def main():

    gateway = JavaGateway()
    edit_distance = gateway.entry_point.getEditDistance()

    result = edit_distance.calculate_all(args.source, args.target)
    output = [s for s in result.split("\t")]

    for line in output:
        print(line)


main()
