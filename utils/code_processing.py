import pandas as pd
from typing import *
from typing import Literal
from utils.code_dependencies import *

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

def code_runs(code_definitions:str, student_code:str)->bool:
    """
    checks wheter the code can run at least
    requires:
        - 'from typing import *' since typing structures are used everywhere. 
        - running dataset definitions before (see above). 
    """
    if student_code == "":
        return False
    
    # code definitions
    try: 
        exec(code_definitions)
    except Exception as e: raise Warning("Problem runnning code definitions!")
    
    try: 
        exec(student_code)
        return True
    except Exception as e:
        Warning(f"Student Code Exception {e}")
        return False
    
def numeric_test_score(problem, code_definitions:str, student_python_code:str, verbose:Literal[0,1,2]=0):
    asserts = problem.test.split("assert")[1:]
    asserts = [ass.strip() for ass in asserts]
    if verbose>0: print(asserts)

    # code definitions
    try: 
        exec(code_definitions)
    except Exception as e: raise Warning("Problem runnning code definitions!")

    count_passed = 0
    for idx,ass in enumerate(asserts):
        try:
            # replace first occurrence of substring by entry point
            assestent_line_code = ass.replace("candidate", problem.entry_point, 1) 
            # evaluate assert
            exec(student_python_code)
            evaluation_passed = eval(assestent_line_code)
            if (verbose == 2) or (verbose == 1 and not evaluation_passed):
                print(idx, assestent_line_code)
                print(evaluation_passed, '\n')
            if evaluation_passed:
                count_passed += 1
        except: pass
    # return proportion of passed asserts 
    return count_passed / len(asserts)