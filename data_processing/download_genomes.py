from ftplib import FTP
import argparse
import os
import posixpath


def resolve_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--datafile', dest='datafile', default='Gnomon', help='datafile name to get from source, defaults to genomon')
    parser.add_argument('--write_folder', dest='write_folder', default='../genomes/', help='local folder to write files')
    args = parser.parse_args()
    return args


def nih_ftp():
    ftp = FTP('ftp.ncbi.nlm.nih.gov')
    ftp.login()
    return ftp


def nih_genomes_filenames(ftp, datafile):
    genomes_filenames = []
    folders = ftp.nlst('/genomes')
    for folder in folders:
        try: 
            data_folder = posixpath.join('/genomes', folder, datafile)
            filenames = ftp.nlst(data_folder)
            for filename in filenames:
                if '_top_level.gff3.gz' in filename:
                    abs_filename = posixpath.join(data_folder, filename)
                    genomes_filenames.append(abs_filename)
        except Exception as e:
            print('Error retrieving filenames for folder {}: {} {}'.format(folder, type(e), e))
            continue
    return genomes_filenames


def get_files_from_ftp(ftp, remote_filenames, local_folder, make_local_dirs=True):
    for filename in remote_filenames:
        try:
            write_file = os.path.join(local_folder, posixpath.basename(filename))
            if make_local_dirs:
                try:
                    os.makedirs(local_folder)
                except OSError as oserr:
                    if oserr.errno != 17: # errno 17 means directory already exists
                        print('Cannot create folder {}: {} {}'.format(local_folder, type(oserr), oserr))
                        continue
            with open(write_file,'w') as f:
                ftp.retrbinary('RETR '+filename, f.write)
        except Exception as e:
            print('Error getting file {}: {} {}'.format(filename, type(e), e))
            continue


if __name__ == '__main__':
    args = resolve_args()
    ftp = nih_ftp()
    filenames = nih_genomes_filenames(ftp, args.datafile)
    get_files_from_ftp(ftp=ftp, remote_filenames=filenames, local_folder=args.write_folder)

