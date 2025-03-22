if buy_price > 20 and (sunrise > interval_time > sunset) and action == 'auto':
    action = 'export200'
    reason += ' aim higher auto -> export200'

if rrp > 1000:
    action = 'export'
    reason += f' take the money rrp:{rrp}'

if interval_time.hour > 17 and interval_time.hour < 21 and battery_soc < 10 and action == 'export':
    action = 'export200'
    reason += ' need that for peak time'

if 'import' in action and battery_soc > 95:
    action = 'charge'
    reason += ' high soc import -> charge'






