# functions file for scripts





# creation of vector for weekly data of company 
# takes variables and returns vector
# (week, order_suppl, amt_transp, amt_wip, amt_stock, 
# cycle_stock, safety_stock, order_cust, blog_cust, demand_cust)
def create_new(week, order_suppl, amt_transp, amt_wip, amt_stock, cycle_stock, safety_stock, order_cust, blog_cust, demand_cust):
    
    v = [week, order_suppl, amt_transp, amt_wip, amt_stock, cycle_stock, safety_stock, order_cust, blog_cust, demand_cust]
    
    return v


# save the vector data into matrix for KPI
def save_into_matrix(matrix, vector):
    matrix.append(vector)
    return matrix


# calculate backlog for company from place 7 and 8 of company vector
def calc_blog(vector):

    return vector
    

# move products from wip into stock
def move_to_stock(vector):
    vector[4] = vector[4] + vector[3]
    return vector


# move products from transport into wip
def move_to_wip(vector):
    vector[3] = vector[2]
    return vector


# change var:week to current
def change_week(vector, i):
    vector[0] = i
    return vector