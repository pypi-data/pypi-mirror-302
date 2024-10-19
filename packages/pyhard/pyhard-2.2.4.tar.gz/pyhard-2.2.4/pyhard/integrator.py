"""
Module that gathers wrapper functions for the IS building steps.
"""

import json
import logging
from pathlib import Path
from typing import Union, Tuple

import numpy as np
import pandas as pd
from pyispace import train_is
from pyispace.train import Model
from pyispace.utils import scriptcsv

from .classification import ClassifiersPool
from .measures import ClassificationMeasures, RegressionMeasures
from .regression import RegressorsPool
from .structures import Configurations


metadata_file = 'metadata.csv'
options_file = 'options.json'
ih_file = 'ih.csv'
instances_index = 'instances'


def build_metadata(
        data: pd.DataFrame,
        config: Configurations,
        return_ih: bool = False,
        verbose: bool = False
) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
    """
    Wrapper function that builds the metadata set.

    Args:
        data (pandas.DataFrame): input dataset
        config (Configurations): configuration object
        return_ih (bool): whether to return instance hardness array of values
        verbose (bool): controls verbosity

    Returns:
        (pandas.DataFrame, pandas.DataFrame): The metadata set, and instance hardness values (optional, depending on
        `return_ih`)

    """
    problem = config.general.problem
    target_col = config.general.target_col
    if problem == 'classification':
        measures = ClassificationMeasures(data, target_col=target_col)
        learners = ClassifiersPool(data, labels_col=target_col)
    elif problem == 'regression':
        measures = RegressionMeasures(data, target_col=target_col)
        learners = RegressorsPool(data, output_col=target_col)
    else:
        raise ValueError(f"Unknown type of problem: '{problem}'.")

    df_measures = measures.calculate_all(
        measures_list=config.measures.list
    )

    df_algo = learners.run_all(
        metric=config.algos.metric,
        n_folds=config.algos.n_folds,
        n_iter=config.algos.n_iter,
        algo_list=config.algos.pool,
        parameters=config.algos.parameters,
        resampling=config.algos.resampling,
        hyper_param_optm=config.hpo.enabled,
        hpo_evals=config.hpo.evals,
        hpo_timeout=config.hpo.timeout,
        verbose=verbose
    )

    df_metadata = pd.concat([df_measures, df_algo], axis=1)
    n_inst = len(df_metadata)
    df_metadata.insert(0, instances_index, np.arange(1, n_inst + 1))
    df_metadata.set_index(instances_index, inplace=True)

    if return_ih:
        ih_values = learners.estimate_ih()
        df_ih = pd.DataFrame(
            {'instance_hardness': ih_values},
            index=pd.Index(range(1, n_inst + 1), name=instances_index)
        )
        return df_metadata, df_ih
    else:
        return df_metadata


def run_isa(
        rootdir: Path,
        metadata: Union[pd.DataFrame, Path] = None,
        settings: dict = None,
        save_output: bool = True,
        rotation_adjust: bool = True,
        verbose: bool = False
) -> Model:
    """
    Run Instance Space Analysis with Python engine (PyISpace).

    Args:
        rootdir (Path): rootdir path
        metadata (pandas.DataFrame or Path): the metadata or a path pointing to it
        settings (dict): optional settings to update
        save_output (bool): whether to save output files
        rotation_adjust (bool): whether to adjust IS rotation
        verbose (bool): controls verbosity

    Returns:
        ISA outputs

    """
    if rotation_adjust is None:
        rotation_adjust = False

    if not rootdir.exists():
        raise NotADirectoryError(f"Invalid directory {repr(repr(rootdir))}.")

    opts_path = rootdir / options_file
    if opts_path.is_file():
        with open(str(opts_path)) as f:
            opts = json.load(f)
    else:
        raise FileNotFoundError(f"File 'options.json' not found in specified path {repr(str(rootdir))}.")

    meta_path = rootdir / metadata_file
    if isinstance(metadata, pd.DataFrame):
        pass
    elif meta_path.is_file():
        metadata = pd.read_csv(meta_path, index_col='instances')
    else:
        raise FileNotFoundError(f"File 'metadata.csv' not found in specified path {repr(str(rootdir))}.")

    opts = update_options(opts, settings)

    if verbose:
        logging.getLogger('pyispace').setLevel(logging.DEBUG)
    else:
        logging.getLogger('pyispace').setLevel(logging.INFO)
    out = train_is(metadata, opts, rotation_adjust)
    if save_output:
        scriptcsv(out, rootdir)
    return out


def update_options(d1: dict, d2: dict):
    d1 = d1.copy()
    for k in d1.keys():
        d1[k] = {**d1[k], **d2.get(k, dict())}
    return d1
