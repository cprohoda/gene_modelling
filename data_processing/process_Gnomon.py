import gzip
import pandas as pd
import os
import argparse
import re


def resolve_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--read_folder', dest='read_folder', default='../genomes/', help='local folder to read raw gzipped files')
    parser.add_argument('--input_files', dest='input_files', default='*.gff3.gz', help='all files in folder')
    parser.add_argument('--write_folder', dest='write_folder', default='../processed_genomes/', help='local folder to write processed files')
    parser.add_argument('--gene_dataframe', dest='gene_dataframe', default='../processed_genomes/genes_present', help='dataframe file with the genes per file')
    args = parser.parse_args()
    return args


def gz_readline(filename):
    with gzip.open(filename, 'rb') as f:
        for lines in f:
            yield f.readline()


def filter_genes(line):
    filter_condition = "Gnomon\tgene" in line
    return filter_condition


def writeline_genes(filename, line, args):
    write_file = os.path.join(args.write_folder, filename)
    with open(write_file, 'a') as f:
        f.write(line)


def extract_gene_number(line):
    pattern = re.compile(r'.*Name=gene\.(.*?);.*')
    pattern_matched = pattern.search(line)
    if pattern_matched:
        gene_number = pattern_matched.group(1)
    else:
        raise ValueError('Gene number not identified in line: {}'.format(line))
    return int(gene_number)


def clean_processed(filename):
    write_file = os.path.join(args.write_folder, filename)
    if os.path.isfile(write_file):
        os.remove(write_file)


def process_all_gnomons(genes_present, args):
    read_files = os.listdir(args.read_folder)
    for read_file in read_files:
        read_file = os.path.join(args.read_folder, read_file)
        unzipped_filename = os.path.basename(read_file).rstrip('.gz')
        clean_processed(filename=unzipped_filename)
        for line in gz_readline(read_file):
            try:
                if filter_genes(line):
                    gene_number = extract_gene_number(line)
                    genes_present.loc[gene_number, unzipped_filename] = 1
                    writeline_genes(filename=unzipped_filename, line=line, args=args)
            except Exception as e:
                print('Error processing line in file {}:\n{}\nError: {} {}'.format(read_file, line, type(e), e))
                continue
    genes_present.to_csv(args.gene_dataframe)


if __name__ == '__main__':
    args = resolve_args()
    if os.path.isfile(args.gene_dataframe):
        genes_df = pd.read_csv(args.gene_dataframe, index_col=0)
    else:
        genes_df = pd.DataFrame()
    process_all_gnomons(genes_present=genes_df, args=args)