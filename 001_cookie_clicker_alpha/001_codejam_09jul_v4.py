# -*- coding: utf-8 -*-
"""
Google code jam 2014, problem B "Cookie Clicker Alpha"

- Accumulate cookies until C is reached, to buy farm.
- Buying farm increases cookie accumulation by F per sec (initial = 2 cookies/sec)
- At some point, it is quicker to stop buying farms, just accumulate cookies till X is reached.
  i.e. (win time: accumulate using N farms) < (win time: buy farm (N+1) + accumulate using (N+1) farms)

Each input case is a list with 3 cols [c, f, x]:
c = cost of farm
f = for each farm, get additional F cookies/sec 
x = number of cookies required to win

Output:
-----------
time taken to buy N farms + accumulate until n_cookies==x
in format: Case #x: y
y: time in seconds with 7 decimals, with error tolerance 10^-6

Example:
-----------
Input:
30.0 1.0 2.0
30.0 2.0 100.0
30.50000 3.14159 1999.19990
500.0 4.0 2000.0

Output:
Case #1: 1.0000000
Case #2: 39.1666667
Case #3: 63.9680013
Case #4: 526.1904762

Pseudocode:
--------------
1. Read text file and put cases into list. 1 row per case. Columns in cfx format.
2. Initialise elapsed_time = 0 
3. Iterate over rows:
    a. Calculate time to n_cookies==C, using N farms.
    b. Calculate time to n_cookies==X, using N farms. (accumulate without increasing farms)
    c. Calculate time to n_cookies==X, (a) + accumulate using N+1 farms. (increase farm and then accumulate)
    d. If (b) > (c): accumulating is slower, increase farm and repeat. 
        - elapsed time += (a)
        - n_farms++
        - go back to (a)

Spreadsheet modelling this problem at /proj/waiking/007_PYTHON/team_meetings/analysis.xlsx
"""

from csv import reader
from decimal import Decimal   # avoid issues with accuracy when using floating point

"""
read input text file containing c, f and x
first row is number of cases... not to be processed
return: list of cases , 1 case per row
"""
def read_data(file):
    f = open(file)
    read_file = reader(f, delimiter=' ')
    cases = list(read_file)
    case_list = cases[1:]   # cfx cases from second row onwards
    return case_list   # 1 case per row

"""
calculate time (secs) to achieve 'cost' number of cookies
"""
init_rate = 2   # initial cookie rate: 2 per sec

def get_time(cost, n_farms, cookie_rate):
    return (Decimal(cost) / (init_rate + (n_farms * Decimal(cookie_rate))))

"""
for a given case, iterate until x number of cookies achieved to win game.
"""
def win_elapsed_time(farm_cost, cookie_rate, win_cookies):
    n_farms = 0   # start with no farms    
    elapsed_time = Decimal(0)   # reset timer to 0 secs
    while True:   # keep iterating until accumulating is faster than buying
        t_buy_farm = get_time(farm_cost, n_farms, cookie_rate)   # time to afford to buy farm
        t_win = get_time(win_cookies, n_farms, cookie_rate)   # don't buy more farms, just accumulate cookies till win
        t_buy_farm_win = t_buy_farm + get_time(win_cookies, n_farms+1, cookie_rate)   # buy another farm, then accumulate cookies till win
        if t_win > t_buy_farm_win:   # accumulating is slower. Buy another farm.
            elapsed_time += t_buy_farm   
            n_farms += 1    # repeat While loop
        else:   # accumulating is faster. Stop buying farms.
            elapsed_time += t_win
            break   # WIN!
    return elapsed_time


cases = read_data('B-large-practice.in')
case_num = 1   # case number counter: starts from 1 

for case in cases:   # iterate over cases
    farm_cost, cookie_rate, win_cookies = case[0], case[1], case[2]
    elapsed_time = win_elapsed_time(farm_cost, cookie_rate, win_cookies)
    print('Case #%d: %.7f' % (case_num, elapsed_time))   # print result with 7 decimal places
    case_num += 1   # move to next case
    