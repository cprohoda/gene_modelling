import argparse


def resolve_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw_data_folder', dest='raw_data_folder', default='genomes/', help='local folder to read raw gzipped files')
    parser.add_argument('--processed_folder', dest='processed_folder', default='processed_genomes/', help='local folder to write processed files')
    parser.add_argument('--input_files', dest='input_files', default=None, nargs='*', help='specifiy files; default all files in folder')
    parser.add_argument('--data_type', dest='data_filetype', default='Gnomon', help='datafile name to get from source, defaults to Gnomon')
    parser.add_argument('--overwrite', default=False, action='store_true')
    parser.add_argument('--profile', default=False, action='store_true')
    parser.add_argument('--gene_map_filename', dest='gene_map_filename', default='gene_map', help='filename of genes present in each file in the processed folder')
    args = parser.parse_args()
    return args
