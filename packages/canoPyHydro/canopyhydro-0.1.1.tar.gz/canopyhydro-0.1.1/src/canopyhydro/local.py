from __future__ import annotations

import os
import sys

cwd = os.getcwd()
sys.path.append("../" + cwd)
sys.path.append(cwd + "/src")
from canopyhydro.CylinderCollection import pickle_collection
from canopyhydro.Forester import Forester

for file in [
    # ("Secrest10-08_000000.csv",-0.16),
    #  ("Secrest07-32_000000.csv",-0.16),
    ("Secrest16-3TI-CO_000000", -0.24),
    ("Secrest07-32_000000.csv", -0.08),
    ("Secrest07-32_000000.csv", -0.24),
]:
    collection = None
    name, angle = file
    try:
        forest = Forester("data/input/")
        forest.qsm_to_collection(file_name=name)
        collection = forest.cylinder_collections[0]
        collection.initialize_digraph_from(in_flow_grade_lim=angle)
        collection.find_flow_components()
        # print("finished_find_flow_components")
        collection.calculate_flows()
        collection.statistics(file_name_ext=str(angle))
    except Exception as error:
        try:
            pickle_collection(collection, file_name_ext=str(angle))
        except Exception as error:
            print(f"Error pickling {file}: {error}")
        print(f"Error in {file}: {error}")
        continue
