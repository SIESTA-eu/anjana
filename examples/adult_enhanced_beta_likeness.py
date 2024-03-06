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

import pandas as pd
from anonymity import basic_beta_likeness, enhanced_beta_likeness
import pycanon
from pycanon import anonymity
import time

data = pd.read_csv("adult.csv")  # 32561 rows
data.columns = data.columns.str.strip()
data = data[:1000]
cols = [
    "workclass",
    "education",
    "marital-status",
    "occupation",
    "sex",
    "native-country",
]
for col in cols:
    data[col] = data[col].str.strip()
print(data)
quasi_ident = [
    "age",
    "education",
    "marital-status",
    "occupation",
    "sex",
    "native-country",
]
ident = ["race"]
sens_att = ["salary-class"]
k = 10
beta = 0.5
supp_level = 50

hierarchies = {
    "age": dict(pd.read_csv("hierarchies/age.csv", header=None)),
    "education": dict(pd.read_csv("hierarchies/education.csv", header=None)),
    "marital-status": dict(pd.read_csv("hierarchies/marital.csv", header=None)),
    "occupation": dict(pd.read_csv("hierarchies/occupation.csv", header=None)),
    "sex": dict(pd.read_csv("hierarchies/sex.csv", header=None)),
    "native-country": dict(pd.read_csv("hierarchies/country.csv", header=None)),
}

start = time.time()
data_anon = enhanced_beta_likeness(
    data, ident, quasi_ident, sens_att, k, beta, supp_level, hierarchies
)
end = time.time()
print(f"Elapsed time: {end - start}")
print(f"Value of k calculated: {pycanon.anonymity.k_anonymity(data_anon, quasi_ident)}")
print(
    f"Value of beta (enhanced) calculated: {pycanon.anonymity.enhanced_beta_likeness(data_anon, quasi_ident, sens_att)}"
)

# Elapsed time: 85.62421894073486
# Value of k calculated: 158
# Value of beta (enhanced) calculated: 0.3363878057426444
