from ftplib import FTP
import argparse


def resolve_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--datafile', dest='datafile', default='genomon', help='datafile name to get from source, defaults to genomon')
    parser.add_argument('--write_folder', dest='write_folder', default='../genomes/', help='local folder to write files')

    args = parser.parse_args()

    return args

    
def nih_genomes(filetype):
    ftp = FTP('ftp.ncbi.nlm.nih.gov')
    ftp.login()
    ftp.cwd('genomes')
    lines = ftp.retrlines('LIST')
    print(type(lines))
    print(lines)


if __name__ == '__main__':
    args = resolve_args()
    nih_genomes(args.datafile)
