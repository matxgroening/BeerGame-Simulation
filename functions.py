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
def pass_order(vector, v_list, v_brew_prep):
    idx = v_list.index(vector)
    if idx == 0:
        v_brew_prep = vector[1]
    else:
        v_list[idx-1][7] = vector[1]
    return v_brew_prep


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
def move_to_transp(vector, v_list, del_amt, v_brew_prep):
    idx = v_list.index(vector)
    # if bar add to delivered_cust
    if idx == 3:
        vector[10] += del_amt
    elif idx == 0:
        vector[2] = v_brew_prep
        vector[10] += del_amt
        v_list[idx + 1][2] = del_amt
    # else do the same send the amount to amt_transp to next in line
    else:
        vector[10] += del_amt
        v_list[idx + 1][2] = del_amt
    return v_brew_prep


# set order amount 
# v1 order the amount that the customer took
def calc_order_suppl_v1(vector):
    vector[1] = vector[7]

# v2 order the amount to achieve safety stock
def calc_order_suppl_v2(vector):
    safety_stock = vector[6]  # safety stock level
    cycle_stock = vector[7] # cycle stock level
    
    if vector[4] < safety_stock:
        vector[1] = safety_stock - vector[4]
    else:
        vector[1] = 0


def calc_order_suppl_v3(vector, avg_demand, current_week, total_weeks):
    safety_stock = vector[6]  # safety stock level
    cycle_stock = vector[7] # cycle stock level
    amt_stock = vector[4]  # current stock
    backlog = vector[8]  # current backlog

    # Set how aggressively we react based on the current week (higher at first, lower later)
    early_reaction_factor = min(1, (total_weeks - current_week) / total_weeks)
    
    # Aggressive response at first (cover backlog and average demand), smoothen over time
    target_stock = safety_stock + cycle_stock  # aim to maintain safety stock
    
    if backlog > 0:
        # Early aggressive ordering: Cover backlog and some extra demand
        order_amt = backlog + avg_demand * (1 + early_reaction_factor)
    else:
        # Smooth ordering: Adjust order amount as time progresses to avoid too much stock
        order_amt = (target_stock - amt_stock) * (1 + early_reaction_factor)

    # Avoid ordering more than necessary
    order_amt = max(0, min(order_amt, target_stock - amt_stock))

    vector[1] = order_amt  # Set the order amount to the supplier

    return vector



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


# FUNCTION TO PLOT BACKLOG AND STOCK

def plot_backlog_and_stock(m_brew, m_bottl, m_wholes, m_bar):
    # Define the figure and axes
    fig, axs = plt.subplots(3, 1, figsize=(10, 8))

    # Extract week, backlog, and stock columns for each matrix
    weeks = [row[0] for row in m_brew]
    
    # Backlogs
    backlog_brew = [row[8] for row in m_brew]
    backlog_bottl = [row[8] for row in m_bottl]
    backlog_wholes = [row[8] for row in m_wholes]
    backlog_bar = [row[8] for row in m_bar]

    # Stock
    stock_brew = [row[4] for row in m_brew]
    stock_bottl = [row[4] for row in m_bottl]
    stock_wholes = [row[4] for row in m_wholes]
    stock_bar = [row[4] for row in m_bar]

    # Order of station
    order_brew = [row[1] for row in m_brew]
    order_bottl = [row[1] for row in m_bottl]
    order_wholes = [row[1] for row in m_wholes]
    order_bar = [row[1] for row in m_bar]

    # Plot Backlog
    axs[0].plot(weeks, backlog_brew, label="Brewery", color='blue', marker='o')
    axs[0].plot(weeks, backlog_bottl, label="Bottler", color='green', marker='s')
    axs[0].plot(weeks, backlog_wholes, label="Wholesaler", color='orange', marker='^')
    axs[0].plot(weeks, backlog_bar, label="Bar", color='red', marker='x')
    
    axs[0].set_title('Backlog Over Time')
    axs[0].set_xlabel('Weeks')
    axs[0].set_ylabel('Backlog (units)')
    axs[0].legend()
    axs[0].grid(True)

    # Plot Stock
    axs[1].plot(weeks, stock_brew, label="Brewery", color='blue', marker='o')
    axs[1].plot(weeks, stock_bottl, label="Bottler", color='green', marker='s')
    axs[1].plot(weeks, stock_wholes, label="Wholesaler", color='orange', marker='^')
    axs[1].plot(weeks, stock_bar, label="Bar", color='red', marker='x')
    
    axs[1].set_title('Stock Over Time')
    axs[1].set_xlabel('Weeks')
    axs[1].set_ylabel('Stock (units)')
    axs[1].legend()
    axs[1].grid(True)

    # Plot Order
    axs[2].plot(weeks, order_brew, label="Brewery", color='blue', marker='o')
    axs[2].plot(weeks, order_bottl, label="Bottler", color='green', marker='s')
    axs[2].plot(weeks, order_wholes, label="Wholesaler", color='orange', marker='^')
    axs[2].plot(weeks, order_bar, label="Bar", color='red', marker='x')
    
    axs[2].set_title('Orders Over Time')
    axs[2].set_xlabel('Weeks')
    axs[2].set_ylabel('Orders (units)')
    axs[2].legend()
    axs[2].grid(True)

    # Adjust the layout
    plt.tight_layout()
    plt.show()


# FUNCTION TO PLOT COSTS PER ACTOR AND ENTIRE SUPPLY CHAIN

def plot_costs_per_actor_and_supply_chain(m_brew, m_bottl, m_wholes, m_bar):
    # Extract week, backlog, and stock columns for each matrix
    weeks = [row[0] for row in m_brew]

    # Initialize cumulative cost lists for each actor and for the entire supply chain
    costs_brew = {'stock': [], 'backlog': [], 'total': []}
    costs_bottl = {'stock': [], 'backlog': [], 'total': []}
    costs_wholes = {'stock': [], 'backlog': [], 'total': []}
    costs_bar = {'stock': [], 'backlog': [], 'total': []}
    
    total_supply_chain_costs = {'stock': [], 'backlog': [], 'total': []}

    # Helper function to calculate costs
    def calculate_costs(matrix):
        stock_costs = []
        backlog_costs = []
        total_costs = []
        cum_stock = cum_backlog = cum_total = 0

        for row in matrix:
            stock_cost = row[4] * 0.5  # 0.5€ per unit of stock
            backlog_cost = row[8] * 1  # 1€ per unit of backlog
            total_cost = stock_cost + backlog_cost

            # Cumulative costs
            cum_stock += stock_cost
            cum_backlog += backlog_cost
            cum_total += total_cost

            stock_costs.append(cum_stock)
            backlog_costs.append(cum_backlog)
            total_costs.append(cum_total)

        return stock_costs, backlog_costs, total_costs

    # Calculate costs for each actor
    costs_brew['stock'], costs_brew['backlog'], costs_brew['total'] = calculate_costs(m_brew)
    costs_bottl['stock'], costs_bottl['backlog'], costs_bottl['total'] = calculate_costs(m_bottl)
    costs_wholes['stock'], costs_wholes['backlog'], costs_wholes['total'] = calculate_costs(m_wholes)
    costs_bar['stock'], costs_bar['backlog'], costs_bar['total'] = calculate_costs(m_bar)

    # Calculate total costs for the entire supply chain
    for i in range(len(weeks)):
        total_stock = costs_brew['stock'][i] + costs_bottl['stock'][i] + costs_wholes['stock'][i] + costs_bar['stock'][i]
        total_backlog = costs_brew['backlog'][i] + costs_bottl['backlog'][i] + costs_wholes['backlog'][i] + costs_bar['backlog'][i]
        total_total = costs_brew['total'][i] + costs_bottl['total'][i] + costs_wholes['total'][i] + costs_bar['total'][i]

        total_supply_chain_costs['stock'].append(total_stock)
        total_supply_chain_costs['backlog'].append(total_backlog)
        total_supply_chain_costs['total'].append(total_total)

    # Plot costs for each actor
    fig_actor, axs_actor = plt.subplots(4, 1, figsize=(10, 12))
    actors = ['Brewery', 'Bottler', 'Wholesaler', 'Bar']
    costs = [costs_brew, costs_bottl, costs_wholes, costs_bar]
    colors = ['blue', 'green', 'orange', 'red']

    for idx, actor in enumerate(actors):
        axs_actor[idx].plot(weeks, costs[idx]['stock'], label="Stock Costs/Week", color=colors[idx], linestyle='--')
        axs_actor[idx].plot(weeks, costs[idx]['backlog'], label="Backlog Costs/Week", color=colors[idx], linestyle=':')
        axs_actor[idx].plot(weeks, costs[idx]['total'], label="Total Costs/Week", color=colors[idx])
        axs_actor[idx].set_title(f'{actor} Costs Over Time')
        axs_actor[idx].set_xlabel('Weeks')
        axs_actor[idx].set_ylabel('Cumulative Costs (€)')
        axs_actor[idx].legend()
        axs_actor[idx].grid(True)

    plt.tight_layout()
    plt.show()

    # Plot total costs for the entire supply chain
    fig_total, ax_total = plt.subplots(figsize=(10, 6))

    ax_total.plot(weeks, total_supply_chain_costs['stock'], label="Stock Costs/Week", color='blue', linestyle='--')
    ax_total.plot(weeks, total_supply_chain_costs['backlog'], label="Backlog Costs/Week", color='orange', linestyle=':')
    ax_total.plot(weeks, total_supply_chain_costs['total'], label="Total Costs/Week", color='green')

    ax_total.set_title('Cumulative Costs of the Entire Supply Chain Over Time')
    ax_total.set_xlabel('Weeks')
    ax_total.set_ylabel('Cumulative Costs (€)')
    ax_total.legend()
    ax_total.grid(True)

    plt.tight_layout()
    plt.show()
