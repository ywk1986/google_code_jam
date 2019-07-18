# -*- coding: utf-8 -*-

# Google Code Jam 2008 - Problem A: Saving the Universe
# URL: https://code.google.com/codejam/contest/32013/dashboard
# Date program written: 17 July 2019
# =============================================================================
# Calculate how many times to switch between search engines.
# Optimal solution: number of switches should be minimized.
# 
# Example:
# ---------------
# Input:
# 5
# Yeehaw
# NSM
# Dont Ask
# B9
# Googol
# 10
# Yeehaw
# Yeehaw
# Googol
# B9
# Googol
# NSM
# B9
# NSM
# Dont Ask
# Googol
# 
# Output:
# Case #1: 1
# 
# Optimal solution: start by using Dont Ask (farthest down the list), and switch to NSM (next farthest) after query #8.
# ---------------
# 
# Pseudocode:
# ---------------
# select 1 item in Input
# starting from top, calculate how many steps in Output before we get match with input
# save this value to dictionary
# get dictionary key with highest value --> this becomes current_search_engine (takes longest to reach this query)
# iterate over list of queries --> discard queries until current_search_engine reached.
# discard current_search_engine from dictionary 
# switch to different engine --> n_switches ++
# go back to line 42 and repeat loop.
# =============================================================================

from csv import reader

def read_data(file):
    """
    function: read input text file. 
    returns: 
        n_cases: integer, number of test cases
        case_list_2: input in list format, without first row (number of test cases)
    """
    f = open(file)
    read_file = reader(f)
    cases = list(read_file)
    n_cases = int(''.join(cases[0]))   # number of test cases
    case_list = cases[1:]   # everything except number of cases
    case_list_2 = []

    for i in case_list:
        case_list_2.append(''.join(i))
    
    print('number of test cases: ' + str(n_cases))
    print('Original full input: ' + str(case_list_2))
        
    return n_cases, case_list_2   

def count_steps(engines, queries):
    """
    function: for a given engine, search for it's match in queries list. How many steps to reach it's match?
    input: 
        engines: list of engines 
        queries: list of queries.
    returns: dictionary containing number of steps for each engine.
    special case: if an engine does not exist in queries list, it can be used all the way. Return 0 and end program.
    """
    mydict = {}
    
    for eng in engines:
        print('eng: ' + str(eng))
        steps = 0

        while steps < len(queries):
            if eng not in queries: # special case: search engine not in query list, so no problem.
                print('search engine ' + str(eng) + ' not in query list.')
                print('USE ENGINE ' + str(eng) + ' ALL THE WAY. IT IS SAFE')
                print('total number of switches : 0')    
                return 0
            if eng == queries[steps]:    # match: engine found in query list.
                print('engine matches query. Num steps : ' + str(steps))
                mydict[eng] = steps     # add number of steps to dictionary
                break    # move to next engine
            else:
                steps += 1    # no match, move to next query

    print('dictionary of steps taken for each engine: ' + str(mydict))
    return mydict

def count_switches(queries, eng_step_dict):
    """
    function: count number of times to switch engine.
    inputs: 
        queries: list of queries
        eng_step_dict: dictionary containing number of steps for each engine.
    returns: number of switches required to run all queries through given engines, AVOIDING query == engine.
    """
    n_switches = 0
    
    while len(queries) > 0:
        # get key in dict with max value
        max_eng = max(eng_step_dict, key=eng_step_dict.get)
        print('max_eng : ' + str(max_eng))
        
        if max_eng not in queries:    # done... all remaining queries will go to this engine without any problems.
            print('done... all remaining queries will go to ' + str(max_eng) + ' engine.')
            print('total number of switches : ' + str(n_switches))
            break    
        
        if max_eng in queries:
            queries = queries[eng_step_dict[max_eng]:]    # discard queries before current engine
            eng_step_dict.pop(max_eng)    # discard current search engine from dict. 
            n_switches += 1    # switch to engine with next highest step length
            print('updated query list at n_swtiches=' + str(n_switches) + ' : ' + str(queries))
            
    return n_switches
    
def get_one_case(case_list):
    """
    function: pop one case from input text, using numbers provided in text file.
    input: text containing possibly multiple cases.
    returns: 
        search_eng_list: list of search engines
        query_list: list of queries 
        case_list: updated text WITHOUT entries which were put into search_eng_list and query_list
    """
    n_search_eng = int(case_list.pop(0))
    print('n_search_eng : ' + str(n_search_eng))
    search_eng_list = []
    for eng in range(0, n_search_eng):
        search_eng_list.append(case_list.pop(0))
    print(search_eng_list)
    print(case_list)
    n_queries = int(case_list.pop(0))
    print('n_queries: ' + str(n_queries))
    print(case_list)
    query_list = []
    for query in range(0, n_queries):
        query_list.append(case_list.pop(0))
        
    print('search engine list: ' + str(search_eng_list))
    print('query list: ' + str(query_list))
    print('remaining case_list: ' + str(case_list))
        
    return search_eng_list, query_list, case_list

# ==============================================================================================================
# MAIN FUNCTION 
# ==============================================================================================================
    
def main():
    n_cases, case_list = read_data('sample_input_3.txt')    # read input data.
    
    # create output file if it doesn't exist   
    file = open('save_uni_out.txt', 'w+')   
    
    for case in range(1, n_cases+1):
        print('currently processing case #' + str(case) + ' / ' + str(n_cases))
        search_eng_list, query_list, case_list = get_one_case(case_list)    # get one case from input.
    
        # calculate how many steps in query_list before we get match with search engine.
        # save steps for each engine to dictionary
        eng_step_dict = count_steps(search_eng_list, query_list)
        
        # iterate over list of queries --> discard queries until max_engine reached.
        # discard max_engine from dictionary 
        # n_switches++ --> switch to engine with next highest step length --> repeat loop.
        if eng_step_dict != 0:
            n_switches = count_switches(query_list, eng_step_dict)
        else:    # search engine not in query list. No switching required.
            n_switches = 0
        
        # write case_num and n_switches to output file.
        file.write('Case #%d: %d\n' % (case, n_switches))
    
    file.close()
    
if __name__ == '__main__':
    main()