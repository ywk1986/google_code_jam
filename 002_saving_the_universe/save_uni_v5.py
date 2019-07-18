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
# 1. select 1 case in Input
# 2. starting from top, calculate how many steps in Output before we get match with input --> save to dictionary
# 3. get dictionary key with highest value --> this becomes current_search_engine (takes longest to reach this query)
# 4. iterate over list of queries --> discard queries until current_search_engine reached.
# 5. switch to different engine --> n_switches ++
# 6. go back to step (3) and repeat loop.
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

    # format list properly to make processing easier
    for i in case_list:
        case_list_2.append(''.join(i))
    
    print('number of test cases: ' + str(n_cases))
        
    return n_cases, case_list_2   
# ==============================================================================================================

def get_one_case(case_list):
    """
    function: pop one case from input text, using numbers provided in text file.
    input: text containing possibly multiple cases.
    returns: 
        search_eng_list: list of search engines
        query_list: list of queries 
        case_list: updated text WITHOUT entries which were put into search_eng_list and query_list
    """
    # number of engines to expect
    n_search_eng = int(case_list.pop(0))
    print('n_search_eng : ' + str(n_search_eng))
    
    # grab all search engines for this case
    search_eng_list = []
    for eng in range(0, n_search_eng):
        search_eng_list.append(case_list.pop(0))
    
    # number of queries to expect
    n_queries = int(case_list.pop(0))
    print('n_queries: ' + str(n_queries))
    
    # grab all queries for this case
    query_list = []
    for query in range(0, n_queries):
        query_list.append(case_list.pop(0))
    
    # print list of engines and queries
    print('search engine list: ' + str(search_eng_list))
    print('query list: ' + str(query_list))
        
    return search_eng_list, query_list, case_list
# ==============================================================================================================

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
        steps = 0

        while steps < len(queries):
            if eng not in queries:    # search engine not in query list, no switching required.
                print('engine ' + str(eng) + ' not in query list.')
                print('USE ENGINE ' + str(eng) + ' ALL THE WAY.')
                return 0
            if eng == queries[steps]:    # match: engine found in query list.
                mydict[eng] = steps     # add number of steps to dictionary
                break    # move to next engine
            
            steps += 1    # no match, move to next query

    print('dictionary of steps taken for each engine: ' + str(mydict))
    
    return mydict
# ==============================================================================================================
    
def count_switches(search_eng_list, query_list):
    """
    function: count number of times to switch engine.
    inputs: 
        search_eng_list: list of search engines
        query_list: list of queries
    returns: number of switches required to run all queries through given engines, AVOIDING query == engine.
    """
    n_switches = 0    
    
    # Either zero engines or zero queries provided. Can use any query without failure.
    # Return n_switches = 0
    if len(search_eng_list) == 0 or len(query_list) == 0:   
        print('EITHER ZERO ENGINES OR ZERO QUERIES PROVIDED! ')
        return n_switches
    
    while len(query_list) > 0:
        # for each search engine, calculate steps within query_list
        eng_step_dict = count_steps(search_eng_list, query_list)
        
        if eng_step_dict == 0:    # search engine not in query list. No switching required.
            return n_switches
        
        # get key in dict with max value
        max_eng = max(eng_step_dict, key=eng_step_dict.get)
        print('max_eng : ' + str(max_eng))
        
        if max_eng in query_list:
            query_list = query_list[eng_step_dict[max_eng]:]    # discard queries before current engine
            n_switches += 1    # re-calculate step for each engine 
            print('*** updated query list at n_swtiches=' + str(n_switches) + ' : ' + str(query_list))
            
    return n_switches
# ==============================================================================================================
    
def print_total_switches(n_switches):
    """
    function: print total number of switches to CLI. Useful for debugging.
    """
    print('total number of switches: ' + str(n_switches))
# ==============================================================================================================
    
def write2file(file, case, n_switches):
    """
    function: write total number of switches to external text file
    """
    file.write('Case #%d: %d\n' % (case, n_switches))

# ==============================================================================================================
# MAIN FUNCTION 
# ==============================================================================================================
    
def main():
    n_cases, case_list = read_data('A-large-practice.in')    # read input data.
    
    # create output file if it doesn't exist   
    file = open('save_uni_v5_out.txt', 'w+')   
    
    for case in range(1, n_cases+1):    # iterate over cases
        print('*******************************************************************************************')
        print('currently processing case #' + str(case) + ' / ' + str(n_cases))
        search_eng_list, query_list, case_list = get_one_case(case_list)    # get one case from input.

        # calculate max engine
        # iterate over list of queries --> discard queries until max_engine reached.
        # n_switches++ --> repeat analysis.
        n_switches = count_switches(search_eng_list, query_list)
        print_total_switches(n_switches)

        # write case_num and n_switches to output file.
        write2file(file, case, n_switches)
    
    file.close()
    
if __name__ == '__main__':
    main()