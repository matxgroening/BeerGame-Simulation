# BeerGame-Simulation
Simulation of Beer Game (SCMg)

constants for the simulation:
cycletime 1 week
cost/part in stock 0.5€
cost/part in backlog 1€

defining variables for every part of the supply chain:
week
order to supplier
product amount in transport to facility
product amount in production (work in progress)
product amount in stock
cyclestock
safetystock
order of customer
backlog to customer
demand of customer


        # loop for every company
# for c in v_list:
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