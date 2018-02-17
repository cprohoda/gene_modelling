import pandas as pd
import os
import re

from .gene_modelling_utils import resolve_args


class GeneMap:
    def __init__(self, args):
        self.gene_map_filename = args.gene_map_filename
        self.processed_folder = args.processed_folder
        self.genes_df = self.init_gene_map(args)
        self.gene_index_map = {}

    def init_gene_map(self, args):
        if args.overwrite or not os.path.isfile(args.gene_map_filename):
            processed_filenames = os.listdir(args.processed_folder)
            genes_df = pd.DataFrame(columns=processed_filenames, index=range(50000))
        else:
            genes_df = pd.read_csv(args.gene_map_filename, index_col=0)
        return genes_df

    def build(self):
        try:
            for file in get_processed_files(self.processed_folder):
                basename = os.path.basename(file.name)
                print("Building gene map from file: {}".format(file.name))
                for line in file:
                    gene_index = self.map_gene_index(extract_gene_number(line))

                    self.genes_df.loc[gene_index, basename] = 1
                print("Memory usage: {}".format(self.genes_df.memory_usage(index=True).sum()))
        except Exception as e:
            print('Error generating gene map to {}\nError: {} {}'.format(self.gene_map_filename, type(e), e))
            raise

    def map_gene_index(self, gene_number):
        if gene_number in self.gene_index_map:
            return self.gene_index_map[gene_number]
        else:
            self.gene_index_map[gene_number] = len(self.gene_index_map)
            return self.gene_index_map[gene_number]

    def write(self, args):
        self.genes_df.to_csv(self.gene_map_filename)


def extract_gene_number(line):
    pattern = re.compile(r'.*Name=gene\.(.*?);.*')
    pattern_matched = pattern.search(line)
    if pattern_matched:
        gene_number = pattern_matched.group(1)
    else:
        raise ValueError('Gene number not identified in line: {}'.format(line))
    return int(gene_number)


def get_processed_files(processed_folder):
    processed_filenames = os.listdir(processed_folder)
    for processed_filename in processed_filenames:
        processed_abs_filename = os.path.join(processed_folder, processed_filename)
        with open(processed_abs_filename, 'r') as f:
            yield f


def main():
    args = resolve_args()
    gene_map = GeneMap(args)
    gene_map.build()
    gene_map.write()


if __name__ == '__main__':
    main()