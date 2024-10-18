# main file for running simulations

# import packages

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import truncnorm
import pandas as pd

# import seperate .py into main
import functions as f


# CONSTANTS

# sim constants
variance = 10
std_dev = np.sqrt(variance)
avg_demand =10
sim_time = 100
cost_stock = 0.5
cost_blog = 1
np.random.seed(42)

# starting conditions
s_amt_transp = 4
s_amt_wip = 4
s_amt_stock = 12

# speculated inventory variables
s_cycle_stock = 8
s_safety_stock = 8


# SIMULATION

# start simulation, define starting vector and start weekly cycle
def sim():
    
    # definition of vectors for weekly data of companys
    # (week, order_suppl, amt_transp, amt_wip, amt_stock, 
    # cycle_stock, safety_stock, order_cust, blog_cust, demand_cust, delivered_cust]
    v_brew = [0, 2, s_amt_transp, s_amt_wip, s_amt_stock, s_cycle_stock, s_safety_stock, 4, 0, 4, 4]
    v_bottl = [0, 4, s_amt_transp, s_amt_wip, s_amt_stock, s_cycle_stock, s_safety_stock, 4, 0, 4, 4]
    v_wholes = [0, 6, s_amt_transp, s_amt_wip, s_amt_stock, s_cycle_stock, s_safety_stock, 4, 0, 4, 4]
    v_bar = [0, 8, s_amt_transp, s_amt_wip, s_amt_stock, s_cycle_stock, s_safety_stock, 4, 0, 4, 0]

    # define starting matrix
    m_brew = []
    m_bottl = []
    m_wholes = []
    m_bar = []

    # define list with every vector
    v_list = (v_brew, v_bottl, v_wholes, v_bar)

    # define list with every matrix
    m_list = (m_brew, m_bottl, m_wholes, m_bar)


    # loop for sim_time
    for i in range(1, sim_time+1):
        
        # calculation of demand with normal distribution
        demand_ak = int(f.generate_positive_normal(avg_demand, std_dev))
        v_list[3][7] = demand_ak
        print(f"AK Demand: {demand_ak}")

        # loop for every company
        for c in v_list:
            # move products from wip into stock
            f.move_to_stock(c)

            # move products from transport into wip
            f.move_to_wip(c)

            # calculate demand
            f.calc_demand_cust(c)

            # calculate delivery amount
            del_amt = f.calc_delivery(c)

            # dispatch order to customer
            f.move_to_transp(c, v_list, del_amt)

            # change order amout from supplier
            f.calc_order_suppl_v1(c)

            # save vector in matrix
            f.save_into_matrix(m_list, c, v_list)

            # change var:week to current
            f.change_week(c, i)
        
        print(f"Bar: {v_bar}")
        print(f"WhS: {v_wholes}")

        for c in v_list:
            # pass order_suppl of company previous in line into order_cust of current company
            f.pass_order(c, v_list)
    
    f.print_matrices_as_tables(m_brew, m_bottl, m_wholes, m_bar)
    return
        



#RUN

sim()
