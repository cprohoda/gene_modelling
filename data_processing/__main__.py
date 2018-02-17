import download_genomes
import process_Gnomon
import generate_gene_map

if __name__=='__main__':
    download_genomes.main()
    process_Gnomon.main()
    generate_gene_map.main()