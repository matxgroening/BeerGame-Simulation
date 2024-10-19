# functions file for scripts

# import packages

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import truncnorm
import pandas as pd

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
    return m_list


# move products from wip into stock
def move_to_stock(vector):
    vector[4] += vector[3]
    vector[3] = 0
    return vector


# move products from transport into wip
def move_to_wip(vector):
    vector[3] = vector[2]
    vector[2] = 0
    return vector


# checks if brewery: order will be next in transport to brewery, 
# else: moves order_suppl of previous company in line into order_cust of current company
def pass_order(vector, v_list):
    idx = v_list.index(vector)
    if idx == 0:
        vector[3] = vector[2]
    else:
        v_list[idx-1][7] = vector[1]
    return vector


# calculate demand of customer (order current week + backlog)
def calc_demand_cust(vector):
    vector[9] = vector[7] + vector[8]
    return vector


# calculate delivery amount
def calc_delivery(vector):
    amt_stock = vector[4]
    demand_cust = vector[9]
    order_cust = vector[7]
    # if stock bigger or equal to demand
    if amt_stock >= demand_cust:
        # demand is delivered
        delivery_amt = demand_cust
        # stock is reduced by delivery amount
        vector[4] -= delivery_amt
        # in this case there will be no backlog
        vector[8] = 0
    # if stock is lower than demand
    else:
        # delivery amount is all that is in stock
        delivery_amt = amt_stock
        # stock empty
        vector[4] = 0 
        # backlog rises by difference of demand to stock
        vector[8] += (order_cust - delivery_amt)
    return delivery_amt


# dispatch products to transport in direction of customer
def move_to_transp(vector, v_list, del_amt):
    idx = v_list.index(vector)
    # if bar add to delivered_cust
    if idx == 3:
        vector[10] += del_amt
    # else do the same send the amount to amt_transp to next in line
    else:
        vector[10] += del_amt
        v_list[idx + 1][2] = del_amt
    return vector


# set order amount 
# v1 order the amount that the customer took
def calc_order_suppl_v1(vector):
    vector[1] = vector[7]

# v2 order the amount to achieve 20 in stock
def calc_order_suppl_v2(vector):
    if vector[4] < 20:
        vector[1] = 20 - vector[4]
    else:
        vector[1] = 0



# change var:week to current
def change_week(vector, i):
    vector[0] = i
    return vector


# KPI FUNCTIONS

# Function to print each matrix as a table
def print_matrices_as_tables(m_brew, m_bottl, m_wholes, m_bar):
    # Define column names for readability
    columns = ['Week', 'Order_Suppl', 'Amt_Transp', 'Amt_WIP', 'Amt_Stock', 
               'Cycle_Stock', 'Safety_Stock', 'Order_Cust', 'Backlog_Cust', 
               'Demand_Cust', 'Delivered_Cust']
    
    # Convert each matrix to a DataFrame for pretty printing
    df_brew = pd.DataFrame(m_brew, columns=columns)
    df_bottl = pd.DataFrame(m_bottl, columns=columns)
    df_wholes = pd.DataFrame(m_wholes, columns=columns)
    df_bar = pd.DataFrame(m_bar, columns=columns)
    
    # Print each DataFrame as a table
    print("\nBrewery Table:")
    print(df_brew.to_string(index=False))

    print("\nBottler Table:")
    print(df_bottl.to_string(index=False))

    print("\nWholesaler Table:")
    print(df_wholes.to_string(index=False))

    print("\nBar Table:")
    print(df_bar.to_string(index=False))

# Example of how you might call this function after the simulation
# Assuming m_brew, m_bottl, m_wholes, m_bar have been updated in your simulation
# Call the function like this:
# print_matrices_as_tables(m_brew, m_bottl, m_wholes, m_bar)
