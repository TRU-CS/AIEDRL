import pandas as pd
from typing import *

def get_code_definitions(problem_code:str)->str:
    """
    Returns class definitions, usually under a line like:
    # Definition for singly-linked list.
    """
    definition_lines = []
    for line in problem_code.split("\n"):
        if line.startswith("# ") and not line.startswith("# Definition"):
            clean_line = line.removeprefix("# ")
            definition_lines.append(clean_line)
    
    return "\n".join(definition_lines)

def show_all_dataset_definitions(df:pd.DataFrame)->None:
    """
    prints unique class definitions (data structures) from input pd.DataFrame
    Used for checking what it's being used in the Dataset. 
    """
    unique_definitions = set()
    for problem in list(df.iloc):
        if "# Definition" in problem.starter_code:
            # print(p.starter_code)

            definitions = get_code_definitions(problem.starter_code)
            if definitions not in unique_definitions:
                print(definitions)
                unique_definitions.add(definitions)

def code_runs(student_code:str)->bool:
    """
    checks wheter the code can run at least
    requires:
        - 'from typing import *' since typing structures are used everywhere. 
        - running dataset definitions before (see above). 
    """
    try: 
        exec(student_code)
        return True
    except Exception as e:
        Warning(f"Student Code Exception {e}")
        return False