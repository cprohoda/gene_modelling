import download_genomes
import process_Gnomon
import generate_gene_map
import gene_clustering
from gene_modelling_utils import resolve_args

if __name__=='__main__':
    args = resolve_args()
    if 'download_genomes' in args.scripts:
        download_genomes.main()
    if 'process_Gnomon' in args.scripts:
        process_Gnomon.main()
    if 'generate_gene_map' in args.scripts:
        generate_gene_map.main()
    if 'gene_clustering' in args.scripts:
        gene_clustering.main()