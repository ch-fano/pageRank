import argparse
import os
import sys


class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="DrugsRank command line interface. ")
        self.me_group = self.parser.add_mutually_exclusive_group()
        self.me_group.add_argument("-d", "--dataset", help="The dataset file/s to be indexed. It can be a "
                                                           "directory path or a single file.")
        self.me_group.add_argument('-a', '--auto', action='store_true', default=False, required=False,
                                   help="automatically downloads the dataset in "
                                        "\'drugreview\' folder")
        self.args = self.parser.parse_args()

if __name__ == "__main__":
    cli = CLI()
    print(cli.args)
