## Behaviour-Based FAQ

### 1. Why does Powston stay in auto instead of exporting?

Because exporting would reduce future self-consumption or require buying back energy later at a worse price.

Auto means the battery is being *intentionally conserved*.

---

### 2. Why is Powston importing while in auto?

Auto allows importing **to protect self-consumption later**, for example:

* Low SOC during solar hours on a weak forecast day
* Approaching evening with insufficient battery reserve
* Current prices are acceptable and future prices are worse

This is still self-consumption optimisation.

---

### 3. Why didn’t it charge the battery even though SOC was low?

SOC alone is not decisive.

Powston checks:

* Solar forecast
* Whether cheaper imports are coming
* Whether charging now would crowd out better opportunities later

---

### 4. Why does Powston block export even with high SOC?

High SOC does not mean surplus.

Powston reserves energy for:

* Evening peak self-consumption
* Overnight usage
* Known forecast deficits

Export is blocked if those needs are not covered.

---

### 5. Why does Powston export in the morning on some sunny days?

On strong solar days with high SOC and better buy prices ahead, Powston may:

* Export excess early
* Refill later at lower cost
* Avoid curtailment

This only happens when the forecast supports it.

---

### 6. Why does Powston ignore short price spikes?

Short spikes are ignored if:

* There are larger or multiple spikes forecast later
* Exporting now would reduce total daily value
* The battery would need to be bought back at a worse price

---

### 7. Why does the app show “final: import” but the mode is auto?

“Final” describes the **chosen action**, not the control mode.

Auto decided that importing best supported self-consumption and protection at that time.

---

### 8. Why does Powston sometimes discharge instead of charging on sunny days?

On good solar days, Powston may:

* Discharge excess now
* Charge later from cheaper grid or abundant solar
* Avoid curtailment

This improves total energy value, not just SOC.

---

### 9. Why does Powston delay charging even with low SOC?

If solar or cheaper prices are forecast soon, Powston will wait rather than charge prematurely.

---

### 10. Why does Powston stop exporting in the evening?

Evening export is restricted when:

* SOC approaches backup minimum
* Overnight reserve would be compromised
* Buy prices remain reasonable for self-use later

---

### 11. Why does Powston limit EV charging?

When not importing, Powston limits EV charging to protect battery self-consumption.

When importing is allowed, EV charging is released.

---

### 12. Why does Powston curtail exports during negative prices?

Negative wholesale prices trigger export curtailment to avoid paying the grid to take energy.

---

### 13. Why does Powston behave differently on “good sun days”?

Good sun days enable:

* Morning export opportunities
* Delayed charging
* Less aggressive importing

Poor sun days prioritise protection and reserve.

---

### 14. Why does Powston sometimes stay in auto for long periods?

Because conditions have not changed enough to justify a state change.

Repeated behaviour usually means the system is already in the optimal posture.

---

### 15. Is something wrong if Powston keeps saying “not selling” or “waiting”?

No. These messages indicate that thresholds were evaluated and intentionally not crossed.

---
