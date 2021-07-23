import csv
import os
from os import walk
import glob
import itertools


PATH = os.path.abspath(".")
dataset = [f for f in glob.glob(PATH + "/dataset/*/*.csv")]
query_dataset = [f for f in glob.glob(PATH + "/query_dataset/*/*.csv")]


def csv_util(csv_file_path):
    with open(csv_file_path, "r") as file:
        reader = csv.reader(file)
        x = [list(map(float, row[0].split(" "))) for row in reader if len(row[0]) > 0]

    y = list(itertools.chain.from_iterable(x))

    with open(csv_file_path, "w") as f:
        writer = csv.writer(f)
        writer.writerow(y)


if __name__ == "__main__":
    for i in dataset:
        csv_util(os.path.abspath(i))

    for j in query_dataset:
        csv_util(os.path.abspath(j))