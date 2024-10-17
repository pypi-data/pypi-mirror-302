import pandas as pd
import anndata as ad
from scipy.sparse import csr_matrix

from anndata import AnnData


def read_snv_genotyping(filename: str) -> AnnData:
    """ Read SNV genotyping into an AnnData

    Parameters
    ----------
    filename : str
        SNV genotyping filename

    Returns
    -------
    AnnData
        SNV matrix with alt_count in X and ref_count in layers['ref_count']
    """    

    data = pd.read_csv(filename, dtype={
        'chromosome': 'category',
        'ref': 'category',
        'alt': 'category',
        'cell_id': 'category'})

    data['snv_idx'] = data.groupby(['chromosome', 'position', 'ref', 'alt'], observed=True).ngroup()

    alt_counts_matrix = csr_matrix(
        (data['alt_count'], (data['cell_id'].cat.codes, data['snv_idx'].values)),
        shape=(data['cell_id'].cat.categories.size, data['snv_idx'].max() + 1))

    ref_counts_matrix = csr_matrix(
        (data['ref_count'], (data['cell_id'].cat.codes, data['snv_idx'].values)),
        shape=(data['cell_id'].cat.categories.size, data['snv_idx'].max() + 1))

    obs = data[['cell_id']].drop_duplicates()
    obs['cell_idx'] = obs['cell_id'].cat.codes
    obs = obs.sort_values('cell_idx').set_index('cell_id').drop('cell_idx', axis=1)

    var = data[['snv_idx', 'chromosome', 'position', 'ref', 'alt']].drop_duplicates()
    var['snv_id'] = (
        var['chromosome'].astype(str) + '_' +
        var['position'].astype(str) + '_' +
        var['ref'].astype(str) + '_' +
        var['alt'].astype(str))
    var = var.sort_values('snv_idx').set_index('snv_id')
    assert (var['snv_idx'].values == range(len(var.index))).all()

    adata = ad.AnnData(
        alt_counts_matrix,
        obs,
        var,
        layers={
            'ref_count': ref_counts_matrix,
        }
    )
    
    return adata
