# ⚡ Peak Demand Hacking (for Everyone)

## What's This About?

Sometimes during the evening, when a coal or gas generator fails unexpectedly, energy prices can go crazy—fast. We might see price spikes that last hours, or ones that vanish just as suddenly as they came. These events are unpredictable, and trying to chase every spike can backfire.

That's where “Peak Demand Hacking” comes in. It’s a smart strategy that helps your battery stay useful all night instead of blowing all your energy too early on a maybe-spike.

### The Simple Rule:

Pick the percentage of your battery you're willing to use during a price spike—and *stick to it*. Think of it like Kenny Rogers said:

> "You've got to know when to hold 'em, know when to fold 'em..."

This approach means even if prices look tempting early, the system holds back unless it’s *really* sure it's worth it.

---

## For Technical Users (Hacker Mode)

This logic works by looking at upcoming price forecasts compared to current prices and deciding whether it's worth exporting now, holding back, or even importing to get ready for something bigger.

### Sample Code Snippet


```python
# Spike Hacking
if forecast and battery_soc and battery_soc > 0:
    over_count = int(np.sum(np.array(forecast) > (rrp + 2000)))
    is_spike = (max(forecast) - rrp) > 1000
    if action == 'export':
        if rrp > 1000 and soc_diff_remaining > 0:
            action = 'export'
            reason += f' exporting at ${rrp}/MWH, feed in power limitation {feed_in_power_limitation}W'
        elif is_spike and over_count > 1:
            action = 'auto'
            reason += f' not exporting, {over_count} prices over sell price {sell_price}c'
        else:
            reason += f' exporting at ${rrp}/MWH'
    elif over_count > 3 and soc_diff_remaining < BATTERY_SOC_BUYBACK:
        if max(forecast) > (rrp + 2000) * 2:
            action = 'import'
            reason += f' import battery, {over_count} prices over sell price {sell_price}c'
        elif max(forecast) > (rrp + 2000):
            action = 'stopped'
            reason += f' saving battery, {over_count} prices over sell price {sell_price}c'

```

### Breakdown:

* `forecast`: List of upcoming market prices
* `rrp`: Current spot price
* `battery_soc`: Current battery state of charge
* `soc_diff_remaining`: How much charge you can still risk/export
* `BATTERY_SOC_BUYBACK`: Minimum SOC reserve for later buybacks
* `action`: What the system will do (`export`, `import`, `auto`, etc.)
* `reason`: A detailed reason string for explainability and logs

---

## Why This Matters

By having rules that adapt to **spike count**, **magnitude**, and **battery safety**, we:

* Avoid emptying the battery too early
* Capture truly high-value export opportunities
* Stay ready for multiple spikes in a row

This style of rule can complement others like:

* Day vs Night strategies
* SOC protection
* Negative price buying
