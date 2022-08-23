def read_file_to_string(file):
    f = open(file, "r")
    data = f.readlines()
    data_to_str = [i.strip() for i in data]

    return data_to_str


def write_arrays_to_file(file, arrays):
    with open(file, "w") as f:
        for item in arrays:
            f.write("{}\n".format(" ".join([str(i) for i in item])))
