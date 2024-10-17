# functions file for scripts

# import packages

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import truncnorm

# FUNCTIONS

def generate_positive_normal(mean, std_dev):
    # Set lower limit to 0, and use the standard deviation and mean for the normal distribution
    a = 0  # lower limit
    b = np.inf  # no upper limit

    # Calculate the truncation
    lower_limit = (a - mean) / std_dev
    upper_limit = (b - mean) / std_dev

    # Generate a random number from the truncated normal distribution
    return truncnorm.rvs(lower_limit, upper_limit, loc=mean, scale=std_dev)





# save the vector data into matrix for KPI
def save_into_matrix(m_list, vector, v_list):
    m_list[v_list.index(vector)].append(vector.copy())
    return 
   

# calculate demand of customer (order current week + backlog)
def calc_demand_cust(vector):
    vector[9] = vector[7] + vector[8]
    return vector


# calculate backlog for company from place 7 and 8 of company vector
def calc_blog(vector):
    if vector[4] < vector[9]:
        vector[8] += (vector[9] - vector[4])
    return vector

# move products from wip into stock
def move_to_stock(vector):
    vector[4] += vector[3]
    return vector


# move products from transport into wip
def move_to_wip(vector):
    vector[3] = vector[2]
    vector[2] = 0
    return vector

# checks if brewery: order will be next in transport to brewery, 
# else: moves order_suppl of next in line into order_cust of current company
def pass_order(vector, v_list):
    if v_list.index(vector) == 0:
        v_list[0][3] = v_list[0][2]
    elif v_list.index(vector) == 3:
        pass
    else:
        v_list[v_list.index(vector)+1][7] = v_list[v_list.index(vector)][1]

# calculate delivery amount
def calc_delivery(vector):
    amt_stock = vector[4]
    demand_cust = vector[9]

    if amt_stock >= demand_cust:
        delivery_amt = demand_cust
        vector[4] -= demand_cust
        if vector[8] > 0:
            vector[8] -= delivery_amt
            vector[9] -= delivery_amt
        else:
            vector[9] -= delivery_amt
    else:
        
        delivery_amt = amt_stock
        vector[4] = 0 
        if vector[8] > 0:
            vector[8] -= delivery_amt
            vector[9] -= delivery_amt
        else:
            vector[9] -= delivery_amt

    return delivery_amt


# dispatch products to transport in direction of customer
def move_to_transp(vector, v_list, del_amt):
    # if bar add to delivered_cust
    if v_list.index(vector) == 3:
        v_list[v_list.index(vector)][10] += del_amt
    # else do the same send the amount to amt_transp to next in line
    else:
        v_list[v_list.index(vector)][10] += del_amt
        v_list[v_list.index(vector)+1][2] = del_amt

    return

# change var:week to current
def change_week(vector, i):
    vector[0] = i
    return vector