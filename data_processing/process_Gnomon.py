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
    parser.add_argument('--overwrite', default=False, action='store_true')
    args = parser.parse_args()
    return args


def gz_readline(filename):
    with gzip.open(filename, 'rb') as f:
        for lines in f:
            yield f.readline()


def filter_genes(line):
    filter_condition = "Gnomon\tgene" in line
    return filter_condition


def writeline_genes(filename, filtered_lines, args):
    with open(filename, 'w') as f:
        f.write(filtered_lines)


def extract_gene_number(line):
    pattern = re.compile(r'.*Name=gene\.(.*?);.*')
    pattern_matched = pattern.search(line)
    if pattern_matched:
        gene_number = pattern_matched.group(1)
    else:
        raise ValueError('Gene number not identified in line: {}'.format(line))
    return int(gene_number)


def process_all_gnomons(genes_present, args):
    read_files = os.listdir(args.read_folder)
    for read_file in read_files:
        filtered_lines = ""
        read_file = os.path.join(args.read_folder, read_file)
        unzipped_filename = os.path.basename(read_file).rstrip('.gz')
        write_file = os.path.join(args.write_folder, unzipped_filename)
        if args.overwrite or not os.path.isfile(write_file):
            print('Processing {} to {}'.format(read_file, write_file))
            for line in gz_readline(read_file):
                try:
                    if filter_genes(line):
                        gene_number = extract_gene_number(line)
                        genes_present.loc[gene_number, unzipped_filename] = 1
                        filtered_lines += line + '\n'
                except Exception as e:
                    print('Error processing line in file {}:\n{}\nError: {} {}'.format(read_file, line, type(e), e))
                    continue
            try:
                    writeline_genes(filename=write_file, filtered_lines=filtered_lines, args=args)
            except Exception as e:
                print('Error writing lines for file {}\nError: {} {}'.format(unzipped_filename, type(e), e))
        else:
            print('Found {}. Skipping {}.'.format(write_file, read_file))
    try:
        genes_present.to_csv(args.gene_dataframe)
    except Exception as e:
           print('Error writing gene dataframe to {}\nError: {} {}'.format(args.gene_dataframe, type(e), e))


if __name__ == '__main__':
    args = resolve_args()
    if os.path.isfile(args.gene_dataframe):
        genes_df = pd.read_csv(args.gene_dataframe, index_col=0)
    else:
        genes_df = pd.DataFrame()
    process_all_gnomons(genes_present=genes_df, args=args)