# -*- coding: utf-8 -*-

# Copyright 2024 Spanish National Research Council (CSIC)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import numpy as np
import pandas as pd
import pycanon
from anjana.anonymity.utils import utils
from copy import copy
from anjana.anonymity import k_anonymity_inner
from beartype import beartype
from beartype import typing


@beartype()
def t_closeness(
    data: pd.DataFrame,
    ident: typing.Union[typing.List, np.ndarray],
    quasi_ident: typing.Union[typing.List, np.ndarray],
    sens_att: str,
    k: int,
    t: typing.Union[float, int],
    supp_level: typing.Union[float, int],
    hierarchies: dict,
) -> pd.DataFrame:
    """Anonymize a dataset using t-closeness and k-anonymity.

    :param data: data under study.
    :type data: pandas dataframe

    :param ident: list with the name of the columns of the dataframe
        that are identifiers.
    :type ident: list of strings

    :param quasi_ident: list with the name of the columns of the dataframe
        that are quasi-identifiers.
    :type quasi_ident: list of strings

    :param sens_att: str with the name of the sensitive attribute.
    :type sens_att: string

    :param k: value of k for k-anonymity to be applied.
    :type k: int

    :param t: value of t for t-closeness to be applied.
    :type t: float

    :param supp_level: maximum level of record suppression allowed
        (from 0 to 100).
    :type supp_level: float

    :param hierarchies: hierarchies for generalizing the QI.
    :type hierarchies: dictionary containing one dictionary for QI
        with the hierarchies and the levels

    :return: anonymized data.
    :rtype: pandas dataframe
    """
    if t < 0 or t > 1:
        raise ValueError(f"Invalid value of t for t-closeness, t={t}")

    data_kanon, supp_records, gen_level = k_anonymity_inner(
        data, ident, quasi_ident, k, supp_level, hierarchies
    )

    t_real = pycanon.anonymity.t_closeness(data_kanon, quasi_ident, [sens_att])
    quasi_ident_gen = copy(quasi_ident)

    if t_real <= t:
        print(f"The data verifies t-closeness with t={t_real}")
        return data_kanon

    while t_real > t:
        if len(quasi_ident_gen) == 0:
            print(f"The anonymization cannot be carried out for the given value t={t}")
            return pd.DataFrame()

        qi_gen = quasi_ident_gen[
            np.argmax([len(np.unique(data_kanon[qi])) for qi in quasi_ident_gen])
        ]

        try:
            generalization_qi = utils.apply_hierarchy(
                data_kanon[qi_gen].values, hierarchies[qi_gen], gen_level[qi_gen] + 1
            )
            data_kanon[qi_gen] = generalization_qi
            gen_level[qi_gen] = gen_level[qi_gen] + 1
        except ValueError:
            if qi_gen in quasi_ident_gen:
                quasi_ident_gen.remove(qi_gen)

        t_real = pycanon.anonymity.t_closeness(data_kanon, quasi_ident, [sens_att])
        if t_real <= t:
            return data_kanon

    return data_kanon
