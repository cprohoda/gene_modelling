import gzip
import os
import re
import cProfile


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


def get_read_files(args):
    if args.input_files:
        not_found = []
        for filenames in args.input_files:
            if not os.path.isfile(filename):
                not_found.append(filename)
        if not_found:
            raise ValueError('Specified input files not found: {}'.format(file))
        else:
            return args.input_files
    else:
        return os.listdir(args.raw_data_folder)


def process_all_gnomons(args):
    read_files = get_read_files(args)
    for read_file in read_files:
        filtered_lines = ""
        read_file = os.path.join(args.raw_data_folder, read_file)
        unzipped_filename = os.path.basename(read_file).rstrip('.gz')
        write_file = os.path.join(args.processed_folder, unzipped_filename)
        if args.overwrite or not os.path.isfile(write_file):
            print('Processing {} to {}'.format(read_file, write_file))
            for line in gz_readline(read_file):
                try:
                    if filter_genes(line):
                        gene_number = extract_gene_number(line)
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


if __name__ == '__main__':
    args = resolve_args()
    if args.profile:
        cProfile.run('process_all_gnomons(args)')
    else:
        process_all_gnomons(args)