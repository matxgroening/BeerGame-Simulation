# main file for running simulations

# import packages
import matplotlib as m 
import numpy as n

# import seperate .py into main
import functions as f



# CONSTANTS
# starting conditions
s_amt_transp = 4
s_amt_wip = 4
s_amt_stock = 12
# speculated inventory variables
s_cycle_stock = 8
s_safety_stock = 8


# SIMULATION

# start simulation, define starting vector and start weekly cycle
def sim(s_amt_transp, s_amt_wip, s_amt_stock):
    # define starting vector
    v_brew = [0, 4, s_amt_transp, s_amt_wip, s_amt_stock, s_cycle_stock, s_safety_stock, 4, 0, 4]
    v_bottl = [0, 4, s_amt_transp, s_amt_wip, s_amt_stock, s_cycle_stock, s_safety_stock, 4, 0, 4]
    v_wholes = [0, 4, s_amt_transp, s_amt_wip, s_amt_stock, s_cycle_stock, s_safety_stock, 4, 0, 4]
    v_bar = [0, 4, s_amt_transp, s_amt_wip, s_amt_stock, s_cycle_stock, s_safety_stock, 4, 0, 4]

    # define starting matrix
    m_brew = []
    m_bottl = []
    m_wholes = []
    m_bar = []

    # define list with every vector
    v_list = (v_brew, v_bottl, v_wholes, v_bar)

    # define list with every matrix
    m_list = (m_brew, m_bottl, m_wholes, m_bar)


    # loop for 30 weeks (TEST for 2)
    for i in range(1, 6):
        
        # loop for every company
        for c in v_list:
            # move products from wip into stock
            f.move_to_stock(c)

            # move products from transport into wip
            f.move_to_wip(c)

            # change var:week to current
            f.change_week(c, i)
            print(c)

            # save vector in matrix
            for m in m_list:
                f.save_into_matrix(m, c)
        



#RUN

sim(s_amt_transp, s_amt_wip, s_amt_stock)
