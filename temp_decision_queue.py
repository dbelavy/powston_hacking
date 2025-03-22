decision_queue = [
    (
        lambda b=buy_price, thr=buy_opport: b < thr, 
        ('import', 'maximize', ' Opportunistic buy;')
    ),
    (
        lambda r=rrp, s=surplus_energy, thr=always_sell_rrp: (r > thr) and s,
        ('export', 'maximize', ' High RRP opportunity;')
    ),
    (
        lambda h= hour, d=day, b=buy_price, sm = buy_max_soft : (h in d) and b < sm,
        ('charge', 'maximize', ' Daytime charge below soft max buy price.')
    ),

    (
        lambda h=hour, p=prepare_for_peak, s= surplus_energy: (h in p) and not s,
        ('import', 'maximize', ' Afternoon charge before peak.')
    ),
    (
        lambda h=hour, p=peak, s=surplus_energy, sp = sell_price, smh = sell_min_hard: (h in p) and s and sp > smh,
        ('export', 'maximize', ' Peak sell price above sell threshold and surlus.')
    ),
    (
        lambda h=hour, n=night, b = buy_price, sm = buy_max_soft : (h in n) and b < sm,
        ('charge', 'maximize', ' Nighttime low price. Use grid.')
    ),
    (
        lambda: True,
        ('auto', 'maximize', ' Default behavior;')
    )
]






# Define the decision logic without using a state dictionary
decision_queue = [
    (
        lambda: buy_price < buy_opport, 
        ('import', 'maximize', ' Opportunistic buy.')
    ),
    (
        lambda: (rrp > always_sell_rrp) and surplus_energy,
        ('export', 'maximize', ' High RRP opportunity.')
    ),
    (
        lambda: (hour in day) and buy_price < buy_max_soft,
        ('charge', 'maximize', ' Daytime charge below soft max buy price.')
    ),
    (
        lambda: (hour in prepare_for_peak) and not surplus_energy,
        ('import', 'maximize', ' Afternoon charge before peak.')
    ),
    (
        lambda: (hour in peak) and surplus_energy and sell_price > sell_min_hard,
        ('export', 'maximize', ' Peak sell price above sell threshold and surplus.')
    ),
    (
        lambda: (hour in night) and buy_price < buy_max_soft,
        ('charge', 'maximize', ' Nighttime low price. Use grid.')
    ),
    (
        lambda: True,
        ('auto', 'maximize', ' Default behavior;')
    )
]

for check, (act, sol, reas) in decision_queue:
    if check():  # Call the lambda function to evaluate the condition
        action = act
        solar = sol
        reason += reas
        break





# Create a state dictionary to hold all the variables
state = {
    'buy_price': buy_price,
    'buy_opport': buy_opport,
    'rrp': rrp,
    'surplus_energy': surplus_energy,
    'always_sell_rrp': always_sell_rrp,
    'hour': hour,
    'day': day,
    'buy_max_soft': buy_max_soft,
    'prepare_for_peak': prepare_for_peak,
    'peak': peak,
    'sell_price': sell_price,
    'sell_min_hard': sell_min_hard,
    'night': night
}

decision_queue = [
    (
        lambda: state['buy_price'] < state['buy_opport'], 
        ('import', 'maximize', ' Opportunistic buy.')
    ),
    (
        lambda: (state['rrp'] > state['always_sell_rrp']) and state['surplus_energy'],
        ('export', 'maximize', ' High RRP opportunity.')
    ),
    (
        lambda: (state['hour'] in state['day']) and state['buy_price'] < state['buy_max_soft'],
        ('charge', 'maximize', ' Daytime charge below soft max buy price.')
    ),
    (
        lambda: (state['hour'] in state['prepare_for_peak']) and not state['surplus_energy'],
        ('import', 'maximize', ' Afternoon charge before peak.')
    ),
    (
        lambda: (state['hour'] in state['peak']) and state['surplus_energy'] and state['sell_price'] > state['sell_min_hard'],
        ('export', 'maximize', ' Peak sell price above sell threshold and surlus.')
    ),
    (
        lambda: (state['hour'] in state['night']) and state['buy_price'] < state['buy_max_soft'],
        ('charge', 'maximize', ' Nighttime low price. Use grid.')
    ),
    (
        lambda: True,
        ('auto', 'maximize', ' Default behavior;')
    )
]

for check, (act, sol, reas) in decision_queue:
    if check():  # Note the function call here
        action = act
        solar = sol
        reason += reas
        break



# needed to do late binding of variables for Powston's system.
decision_queue = [
    (
        lambda b=buy_price, bo=buy_opport: b < bo, 
        ('import', 'maximize', ' Opportunistic buy.')
    ),
    (
        lambda r=rrp, s=surplus_energy, thr=always_sell_rrp: (r > thr) and s,
        ('export', 'maximize', ' High RRP opportunity.')
    ),
    (
        lambda h= hour, d=day, b=buy_price, sm = buy_max_soft : (h in d) and b < sm,
        ('charge', 'maximize', ' Daytime charge below soft max buy price.')
    ),

    (
        lambda h=hour, p=prepare_for_peak, s= surplus_energy: (h in p) and not s,
        ('import', 'maximize', ' Afternoon charge before peak.')
    ),
    (
        lambda h=hour, p=peak, s=surplus_energy, sp = sell_price, smh = sell_min_hard: (h in p) and s and sp > smh,
        ('export', 'maximize', ' Peak sell price above sell threshold and surlus.')
    ),
    (
        lambda h=hour, n=night, b = buy_price, sm = buy_max_soft : (h in n) and b < sm,
        ('charge', 'maximize', ' Nighttime low price. Use grid.')
    ),
    (
        lambda: True,
        ('auto', 'maximize', ' Default behavior;')
    )
]

for check, (act, sol, reas) in decision_queue:  # Destructure upfront
    if check: # as soon as we find one that works, it will set action and break
        action = act
        solar = sol
        reason += reas  
        break




decision_queue = [
    (
        lambda b=buy_price, bo=buy_opport: b < bo, 
        ('import', 'maximize', ' Opportunistic buy.')
    ),
    (
        lambda r=rrp, s=surplus_energy, thr=always_sell_rrp: (r > thr) and s,
        ('export', 'maximize', ' High RRP opportunity.')
    ),
    (
        lambda h= hour, d=day, b=buy_price, sm = buy_max_soft : (h in d) and b < sm,
        ('charge', 'maximize', ' Daytime charge below soft max buy price.')
    ),

    (
        lambda h=hour, p=prepare_for_peak, s= surplus_energy: (h in p) and not s,
        ('import', 'maximize', ' Afternoon charge before peak.')
    ),
    (
        lambda h=hour, p=peak, s=surplus_energy, sp = sell_price, smh = sell_min_hard: (h in p) and s and sp > smh,
        ('export', 'maximize', ' Peak sell price above sell threshold and surlus.')
    ),
    (
        lambda h=hour, n=night, b = buy_price, sm = buy_max_soft : (h in n) and b < sm,
        ('charge', 'maximize', ' Nighttime low price. Use grid.')
    ),
    (
        lambda: True,
        ('auto', 'maximize', ' Default behavior;')
    )
]

for check, (act, sol, reas) in decision_queue:  # Destructure upfront
    if check(): # as soon as we find one that works, it will set action and break
        action = act
        solar = sol
        reason += reas  
        break