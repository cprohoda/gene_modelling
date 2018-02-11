import pandas as pd
import os

from .gene_modelling_utils import resolve_args


def build_gene_map(args): 
    try:
        for file in get_processed_files(args):
            basename = os.path.basename(file.name)
            for line in file:
                gene_number = extract_gene_number(line)
                gene_map.loc[gene_number, unzipped_filename] = 1
    except Exception as e:
        print('Error generating gene map to {}\nError: {} {}'.format(args.gene_map_filename, type(e), e))
        raise


def extract_gene_number(line):
    pattern = re.compile(r'.*Name=gene\.(.*?);.*')
    pattern_matched = pattern.search(line)
    if pattern_matched:
        gene_number = pattern_matched.group(1)
    else:
        raise ValueError('Gene number not identified in line: {}'.format(line))
    return int(gene_number)


def get_processed_files(args):
    processed_filenames = os.listdir(args.processed_folder)
    for processed_filename in processed_filenames:
        processed_abs_filename = os.path.join(args.processed_folder, processed_filename)
        with open(processed_abs_filename, 'r') as f:
            yield f


def init_gene_map(args):
    if args.overwrite or not os.path.isfile(args.gene_map_filename):
        genes_df = pd.DataFrame()
    else:
        genes_df = pd.read_csv(args.gene_dataframe, index_col=0)


if __name__ == '__main__':
    args = resolve_args()
    gene_map = init_gene_map(args)
    full_gene_map = build_gene_map(gene_map, args)
    full_gene_map.to_csv(args.gene_map_filename)
