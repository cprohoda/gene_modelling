import argparse

def resolve_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw_data_folder', dest='read_folder', default='../genomes/', help='local folder to read raw gzipped files')
    parser.add_argument('--processed_folder', dest='write_folder', default='../processed_genomes/', help='local folder to write processed files')
    parser.add_argument('--input_files', dest='input_files', default=None, nargs='*', help='specifiy files; default all files in folder')
    parser.add_argument('--data_type', dest='datafile', default='Gnomon', help='datafile name to get from source, defaults to Gnomon')
    parser.add_argument('--overwrite', default=False, action='store_true')
    parser.add_argument('--profile', default=False, action='store_true')
    args = parser.parse_args()
    return args