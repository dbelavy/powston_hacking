# System Explainability Guide

## Using Reason Strings
The system uses a `reason` string to log decision-making processes and system state. This provides transparency and helps with debugging and monitoring system behavior.

## Best Practices for Reason Strings

1. **Start with System State**
```python
# Begin with core system metrics
reason += f" House: {house_power}W. Battery: {battery_power}W. Grid: {grid_balance}W. Battery: {battery_soc:.1f}%."
```

2. **Log Price Information**
```python
# Include current and forecasted prices
reason += f" Avg Buy price over the next 4 epochs: {avg_future_buy:.1f}c ~"
reason += f" Sell price {sell_price:.1f}c."
```

3. **Document System Suggestions**
```python
# Log what the system suggests before your logic
reason += f" Powston suggested action: ({suggested_action}) and solar: ({suggested_solar})."
```

4. **Record Time Context**
```python
# Include time-based information
reason += f" Current hour: {current_hour}. Time of day: {t_o_day}."
```

5. **Explain Decisions**
```python
# Document why a decision was made
if buy_price < 0:
    decision_reason = f" Electricity is free: {buy_price}c"
    action = 'curtail100-curtail'
    reason += decision_reason
```

6. **Log Final Decisions**
```python
# Always end with the final decision and its rationale
reason += f" {decision_reason}. Decision: action: {action}, solar: {solar}"
```

## Example of Comprehensive Reason String
```python
# Initialize reason string
reason = ""

# System state
reason += f" House: {house_power}W. Battery: {battery_power}W. Grid: {grid_balance}W."
reason += f" Battery: {battery_soc:.1f}%."

# Price information
reason += f" Avg Buy price over the next 4 epochs: {avg_future_buy:.1f}c."
reason += f" Sell price {sell_price:.1f}c."

# System suggestions
reason += f" Powston suggested action: ({suggested_action}) and solar: ({suggested_solar})."

# Time context
reason += f" Current hour: {current_hour}. Time of day: {t_o_day}."

# Decision making process
if buy_price < 0:
    decision_reason = f" Electricity is free: {buy_price}c"
    action = 'curtail100-curtail'
elif battery_soc > 95 and sell_price < 0:
    decision_reason = f" Battery full and negative sell price"
    if house_kW > 9:
        decision_reason += " High house consumption. Solar at max."
        action = 'export-export'
    else:
        curtail_level = max(1, min(9, house_kW))
        action = f'curtail{curtail_level}000-curtail'
        decision_reason += f" Curtail to {curtail_level:.1f}kW"

# Final decision
reason += f" {decision_reason}. Decision: {action} and {solar}."
```

## Benefits of Good Reason Strings

1. **Debugging**
   - Easily trace decision-making process
   - Identify unexpected behavior
   - Validate system logic

2. **Monitoring**
   - Track system performance
   - Understand state transitions
   - Verify price responsiveness

3. **Optimization**
   - Analyze decision patterns
   - Identify improvement opportunities
   - Fine-tune thresholds

4. **Maintenance**
   - Troubleshoot issues
   - Verify system health
   - Track long-term behavior

## Guidelines for Reason String Format

1. **Consistency**
   - Use consistent formatting
   - Include units (W, kW, %, c)
   - Format decimals consistently (.1f)

2. **Readability**
   - Use clear separators between components
   - Group related information
   - Include spaces after periods

3. **Completeness**
   - Include all relevant metrics
   - Document both inputs and outputs
   - Explain conditional logic

4. **Precision**
   - Use appropriate decimal places
   - Include timestamps when relevant
   - Document specific thresholds
