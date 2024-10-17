from anndata import AnnData
from pandas import DataFrame


def get_obs_data(
        adata: AnnData,
        obs_id: str,
        var_columns=None,
        layer_names=None) -> DataFrame:
    """ Get a dataframe for an observation including .var and specified layers

    Parameters
    ----------
    adata : AnnData
        anndata from which to retrieve observation data.
    obs_id : str
        Observation ID
    var_columns : list, optional
        List of var columns to add to returned dataframe, by default None, all columns
    layer_names : list, optional
        List of layer names to add to returned dataframe, by default None, all layers

    Returns
    -------
    DataFrame
        dataframe for an observation
    """
    if var_columns is not None and layer_names is not None and set(var_columns).intersection(layer_names):
        raise ValueError('var_columns and layer_names cannot have overlapping columns')

    elif var_columns is None and layer_names is not None:
        var_columns = list(set(adata.var.columns) - set(layer_names))

    elif layer_names is None and var_columns is not None:
        layer_names = list(set(adata.layers.keys()) - set(var_columns)) + ['_X']

    elif var_columns is None and layer_names is None:
        var_columns = adata.var.columns
        layer_names = list(adata.layers.keys()) + ['_X']

    data = adata.var[var_columns]

    for layer_name in layer_names:
        if layer_name is None or layer_name == '_X':
            layer_data = adata[obs_id].to_df().T
            assert len(layer_data.columns) == 1
            layer_data.columns = ['_X']
        else:
            layer_data = adata[obs_id].to_df(layer_name).T
            assert len(layer_data.columns) == 1
            layer_data.columns = [layer_name]

        data = data.merge(layer_data, left_index=True, right_index=True, how='left', suffixes=('', '_layer'))
    
    return data


def get_var_data(
        adata: AnnData,
        var_id: str,
        obs_columns=None,
        layer_names=None) -> DataFrame:
    """ Get a dataframe for an observation including .var and specified layers

    Parameters
    ----------
    adata : AnnData
        anndata from which to retrieve observation data.
    var_id : str
        Var ID
    obs_columns : list, optional
        List of obs columns to add to returned dataframe, by default None, all columns
    layer_names : list, optional
        List of layer names to add to returned dataframe, by default None, all layers

    Returns
    -------
    DataFrame
        dataframe for an observation
    """
    data = adata.obs

    if obs_columns is not None:
        data = data[obs_columns]

    if layer_names is None:
        layer_names = adata.layers.keys()

    for layer_name in layer_names:
        assert layer_name not in data, f'layer {layer_name} also in .obs'
        layer_data = adata[:, var_id].to_df(layer_name)
        assert len(layer_data.columns) == 1
        if layer_name is not None:
            layer_data.columns = [layer_name]
        else:
            layer_data.columns = ['_X']
        data = data.merge(layer_data, left_index=True, right_index=True, how='left')

    return data
