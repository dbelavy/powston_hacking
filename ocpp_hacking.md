# OCPP Smart Charging Profiles

How to control EV charging via OCPP 1.6J smart charging profiles using Powston’s MQTT-based interface and OCPP server.

Powston lets you tune your own energy rules—whether for battery trading, smart appliance scheduling, or EV charging. This explains how to set charging power limits for your EVSE using MQTT to talk to the site’s OCPP server.

---

## Overview

We use MQTT to publish updates to the local OCPP server that manages the EVSE (electric vehicle supply equipment). These messages define a **Smart Charging Profile** by setting the max charging rate per phase (in Watts).

This gives you programmable control over how and when the EV can charge—either:

* **7000 W** for full-speed 3-phase charging (or the EVSE's actual limit),
* **100 W** to effectively "pause" charging and stop the car drawing from the house battery during export or discharge periods.
📘 For setup instructions and compatible charger info, see
Managing Grid Load and Costs with OCPP [Powston Blog](https://powston.com.au/blog/managing-grid-load-and-costs-with-ocpp)
---

## Why?

We want to prevent the EV from charging off the house battery when we're discharging to the grid, or doing a strategic export. Instead, car charging should only be allowed when we’re in:

* **charge mode** (topping up the house battery), or
* **import mode** (buying cheap grid power).

That way, you don't rob your battery arbitrage profits just to fill up your car.

---

## Sample Rule Snippet

Add this to your Powston ruleset:

```python
# OCPP hacking
if action in ['auto', 'discharge', 'export']:
    mqtt_topic_ocpp_max_charge = 100
    action = decisions.reason(action, 'OCPP update', mqtt_topic_ocpp_max_charge=mqtt_topic_ocpp_max_charge)
else:
    mqtt_topic_ocpp_max_charge = 7000
    action = decisions.reason(action, 'OCPP update', mqtt_topic_ocpp_max_charge=mqtt_topic_ocpp_max_charge)
```

This snippet dynamically adjusts the charge rate:

* In **discharge**, **export**, or **auto** (balancing) modes → we limit EV charging to 100W.
* In **import** or **charge** modes → we allow full-speed EV charging at 7000W.

You can fine-tune the thresholds based on your EV charger, house phase setup, or car battery size.

---

## How It Works

Your site should have:

* A Powston controller with MQTT integration
* A local OCPP 1.6J server connected to your EVSE
* A config to accept smart charging profiles via MQTT

Once configured, this snippet:

* Publishes to the site's OCPP MQTT topic
* Adjusts the Smart Charging Profile with a simple per-phase power limit
* Ensures that car charging aligns with overall site energy strategy

---

## Tip for Charge Mode

If using `charge` or `import` to allow car charging, leave enough time at those states for the EV to meaningfully top up.

You can do this by:

* Holding `charge` longer when excess solar is available
* Delaying exports briefly to prioritise car charging, if that’s your intent

This balance is up to your goals—site credits vs. EV readiness.
