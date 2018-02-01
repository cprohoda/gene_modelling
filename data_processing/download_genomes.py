from ftplib import FTP
import argparse
import os


def resolve_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--datafile', dest='datafile', default='genomon', help='datafile name to get from source, defaults to genomon')
    parser.add_argument('--write_folder', dest='write_folder', default='../genomes/', help='local folder to write files')
    args = parser.parse_args()
    return args


def nih_ftp():
    ftp = FTP('ftp.ncbi.nlm.nih.gov')
    ftp.login()
    return ftp


def nih_genomes_files(ftp):
    ftp.cwd('/genomes')
    return ftp.nlst()


def get_files_from_cwd(ftp, remote_filenames, local_folder):
    for filename in remote_filenames:
        write_file = os.path.join(local_folder, filename)
        with open(write_file,'w') as f:
            ftp.retrbinary('RETR '+filename, f.write)


if __name__ == '__main__':
    args = resolve_args()
    ftp = nih_ftp()
    filenames = nih_genomes_files(ftp)
    get_files_from_cwd(ftp=ftp, remote_filenames=filenames, local_folder=args.write_folder)

