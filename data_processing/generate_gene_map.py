import pandas as pd
import numpy as np
import os
import re
import cProfile
import json

from .gene_modelling_utils import resolve_args


class GeneMap:
    def __init__(self, args):
        self.gene_map_filename = args.gene_map_filename
        self.gene_index_map_filename = args.gene_index_map_filename
        self.processed_folder = args.processed_folder
        self.overwrite = args.overwrite
        self.gene_map = set()
        self.gene_index_map = {}
        self.gene_index_length = 0

    def generate_gene_index_map(self):
        for basename, line in generate_processed_lines(self.processed_folder):
            self.map_gene_index(extract_gene_number(line))
        with open(self.gene_index_map_filename, 'w') as f:
            f.write(json.dumps(self.gene_index_map, indent=2, separators=(',', ': ')))

    def generate_each_gene_map(self):
        previous_basename = ''
        for basename, line in generate_processed_lines(self.processed_folder):
            if basename != previous_basename and previous_basename != '':
                self.append_gene_map_to_csv(previous_basename)
                self.gene_map = set()
                print('{} gene map written'.format(previous_basename))
            self.gene_map.add(extract_gene_number(line))
            previous_basename = basename

    def build(self):
        try:
            if self.overwrite or not os.path.isfile(self.gene_map_filename) or not os.path.isfile(self.gene_index_map_filename):
                self.generate_gene_index_map()
                self.generate_each_gene_map()
        except Exception as e:
            print('Error generating gene map to {}\nError: {} {}'.format(self.gene_map_filename, type(e), e))
            raise

    def map_gene_index(self, gene_number):
        if gene_number in self.gene_index_map:
            return self.gene_index_map[gene_number]
        else:
            self.gene_index_map[gene_number] = self.gene_index_length
            self.gene_index_length += 1
            return self.gene_index_map[gene_number]

    def append_gene_map_to_csv(self, organism_name):
        with open(self.gene_map_filename, 'a') as f:
            f.write(organism_name + ',')
            for num in range(self.gene_index_length):
                if num in self.gene_map:
                    f.write(str(num))
                if num != (self.gene_index_length-1):
                    f.write(',')
                else:
                    f.write('\n')


def extract_gene_number(line):
    pattern = re.compile(r'.*Name=gene\.(.*?);.*')
    pattern_matched = pattern.search(line)
    if pattern_matched:
        gene_number = pattern_matched.group(1)
    else:
        raise ValueError('Gene number not identified in line: {}'.format(line))
    return int(gene_number)


def generate_processed_lines(processed_folder):
    for file in get_processed_files(processed_folder):
            basename = os.path.basename(file.name)
            for line in file:
                yield basename, line


def get_processed_files(processed_folder):
    processed_filenames = os.listdir(processed_folder)
    for processed_filename in processed_filenames:
        processed_abs_filename = os.path.join(processed_folder, processed_filename)
        with open(processed_abs_filename, 'r') as f:
            yield f


def main():
    args = resolve_args()
    gene_map = GeneMap(args)
    if args.profile:
        cProfile.runctx('gene_map.build()', None, locals())
    else:
        gene_map.build()


if __name__ == '__main__':
    main()
