# Decision Logging Class

The `decisions` object provides structured logging for your Powston automation script. Instead of building complex reason strings, use the decision logger to track your logic flow and ensure higher priority decisions take precedence.

## Basic Usage

```python
action = decisions.reason(new_action, reason_text)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `new_action` | string | required | The action you want to take (e.g. 'auto', 'charge', 'import', 'export') |
| `reason_text` | string | required | Text describing why this decision was made |
| `priority` | integer | 2 | Priority level (1-5+). Higher priorities cannot be overridden |
| `kwargs` | any | None | Key values that influenced this decision for debugging |

## Priority Levels

| Priority | Level | Description | Examples |
|----------|-------|-------------|----------|
| 1 | Low | Default decisions | Initial setup, fallback logic |
| 2 | Medium | Normal trading logic | Arbitrage, time-of-day rules |
| 3 | High | Market conditions | Price spikes, forecast-driven decisions |
| 4 | Very High | Emergency conditions | Negative prices, grid events |
| 5+ | Critical | Safety overrides | Battery protection, system limits |

**Note:** Priority 5+ locks the action - no subsequent decisions can change it.

## Examples

### Simple Decisions
```python
# Start with default
action = decisions.reason('auto', 'Default starting action')

# Basic condition
if battery_soc < 40:
    action = decisions.reason('import', 'assume import under 40% SOC')

# Market-driven decision
if sell_price > (low_buy_price + 8):
    action = decisions.reason('export', 'lots of SOC, good sun and better buys coming', 
                              sell_price=sell_price, low_buy_price=low_buy_price)
```

### Priority-Based Decisions
```python
# Normal trading logic
action = decisions.reason('discharge', 'morning arbitrage opportunity', priority=2)

# High priority market condition
if rrp < 0:
    action = decisions.reason('charge', 'negative wholesale prices', priority=4)

# Critical safety override (locks action)
if battery_soc < min_soc and action == 'export':
    action = decisions.reason('auto', 'battery protection - minimum SOC', priority=5)

# This won't apply if safety override was triggered
action = decisions.reason('export', 'late spike detected', priority=3)
```

### Complex Decision with Values
```python
if 14 < current_hour < 16 and battery_soc < 60:
    if buy_forecast and buy_price > min(buy_forecast[:6]):
        # Decision made but action not changed
        decisions.reason('auto', 'waiting for lower buy price soon', 
                         current_buy=buy_price, 'min_upcoming=min(buy_forecast[:6]))
    else:
        # Decision applied
        action = decisions.reason('import', 'panic buy - low SOC before evening', priority=3,
                                  soc=battery_soc, buy_price=buy_price)
```

## Getting the Reason String

At the end of your script, get the formatted reason displayed on the actions page with automatic visual indicators for each decision:

This generates a visual summary like:
```
"✅ morning_arb→discharge | ✅ neg_prices→charge | ❌ safety_check→auto | ❌ spike_export→export | final:charge"
```

**Visual Indicators:**
- ✅ Decision was applied (action changed)
- ❌ Decision was blocked by higher priority
- ℹ️ Informational log (no action change attempted)

## Best Practices

### 1. Start with Default
```python
action = decisions.reason('auto', 'Default starting action', priority=1)
```

### 2. Use Descriptive Reasons
```python
# Good
action = decisions.reason('import', 'panic buy - low SOC before evening peak')

# Less helpful
action = decisions.reason('import', 'buy now')
```

### 3. Include Key Values
```python
action = decisions.reason('export', 'arbitrage opportunity detected', 
                          sell=sell_price, future_buy=min_buy_price, margin=margin)
```

### 4. Use Appropriate Priorities
```python
# Safety checks should be critical
if battery_soc < 5:
    action = decisions.reason('auto', 'emergency battery protection', priority=5)

# Normal trading should be medium
if good_arbitrage_opportunity:
    action = decisions.reason('export', 'profitable sell opportunity', priority=2)
```

### 5. Log Failed Conditions Too
```python
if buy_forecast and buy_price > min(buy_forecast[:6]):
    # Log why we're NOT changing action
    decisions.reason('auto', 'waiting for better buy price', 
                     current=buy_price, upcoming_min=min(buy_forecast[:6]))
else:
    action = decisions.reason('import', 'good buy price available')
```

## Migration from String Concatenation

### Old way:
```python
reason = f'Default auto {current_hour} @ {battery_soc}%'
if rrp > 990:
    action = 'export'
    reason += f', high RRP {rrp}'
if battery_soc < min_soc:
    action = 'auto'
    reason += f', safety override SOC < {min_soc}%'
```

### New way:
```python
action = decisions.reason('auto', f'starting state @ {battery_soc}%', priority=1)

if rrp > 990:
    action = decisions.reason('export', 'high wholesale prices', priority=3, 
                              rrp=rrp)

if battery_soc < min_soc:
    action = decisions.reason('auto', 'battery protection', priority=5,
                              soc=battery_soc, min_soc=min_soc)

reason = decisions.get_reason()
```

The new approach provides better debugging, clearer decision flow, and automatic priority handling while maintaining compatibility with Powston's existing reason field.
