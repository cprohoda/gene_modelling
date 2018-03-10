import pandas as pd
import cProfile
import os

import generate_gene_map
from .gene_modelling_utils import resolve_args


def generate_similarity_map(args, gene_map):
    similarity = pd.DataFrame(0, index = gene_map.columns, columns=gene_map.columns)
    for row_organism in similarity.iterrows():
        row_organism_index, row_organism_genes = row_organism
        row_organism_genes = set(row_organism_genes)
        for column_organism in similarity.iterrows():
            column_organism_index, column_organism_genes = column_organism
            column_organism_genes = set(column_organism_genes)
            if row_organism_index == column_organism_index:
                similarity.loc[row_organism_index, column_organism_index] = 1
            else:
                similarity.loc[row_organism_index, column_organism_index] = len(row_organism_genes.intersection(column_organism_genes))/len(row_organism_genes)


def get_gene_map(args):
    if os.path.isfile(args.gene_map_filename):
        return pd.read_csv(args.gene_map_filename)
    else:
        generate_gene_map.main()
        return pd.read_csv(args.gene_map_filename)


def gene_clusters():
    args = resolve_args()
    similarity = generate_similarity_map(args, get_gene_map(args))
    similarity.to_csv(args.similarity_filename)


def main():
    args = resolve_args()
    if args.profile:
        cProfile.runctx('gene_clusters()', None, locals())
    else:
        gene_clusters()


if __name__ == '__main__':
    main()