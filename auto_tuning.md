# Auto Tuning with Backtesting
---

**Overview**

The Powston Auto Tuning feature introduces a mechanism to optimise script variables based on historical performance data. By embedding specific annotations within your scripts, the system can automatically backtest and adjust variables to enhance efficiency and accuracy.

---

## Opt-In Mechanism

To enable Auto Tuning in your script:

1. **Script Name**: Start your script name of your active script with `PowstonAutoTuned: `


2. **CICD Annotations**: Include comment lines that specify the desired action and the corresponding timestamp for backtesting. Use the following format:

   ```python
   # CICD: 'YYYY-MM-DD HH:MM:SS+TZ', 'expected_action'
   ```



* **Example**: To indicate that the expected action at 5:30 PM AEST on May 19, 2025, is 'export':

  ```python
  # CICD: '2025-05-19 17:30:00+10', 'export'
  ```

---

## Functionality

Upon execution, the Auto Tuning system performs the following steps:

1. **Detection**: Identifies the presence of the `PowstonAutoTuned:` in the name to confirm that Auto Tuning is enabled for the script.

2. **Parsing Annotations**: Scans for all `# CICD:` annotations to extract the specified timestamps and expected actions.

3. **Backtesting**: For each annotation:

   * Retrieves historical data corresponding to the specified timestamp.
   * Applies the current set of tuned variables to simulate the system's behavior at that time.
   * Compares the simulated action against the expected action.

4. **Validation**: If the simulated action matches the expected action for all annotations, the tuned variables are considered valid and are applied. If any discrepancy is found, the system retains the previous set of variables to ensure reliability.

---

# Benefits

* **Enhanced Accuracy**: By validating tuned variables against historical data, the system ensures that only effective optimizations are applied.
* **Reliability**: Prevents the deployment of unverified changes that could degrade system performance.
* **Transparency**: Provides clear documentation within scripts about the expected behavior at specific times.

---

## Usage Example

```python
# CICD: '2025-05-19 17:30:00+10', 'export'
# CICD: '2025-05-20 09:00:00+10', 'import'
# Additional script logic follows...
```

---

**Notes**

* **Time Format**: Ensure that timestamps are in ISO 8601 format with the appropriate timezone offset.
* **Action Labels**: Use consistent and valid actions (e.g., 'export', 'import') to avoid misinterpretation during backtesting.
* **Annotation Placement**: Place all `# CICD:` annotations near the top of the script for better visibility and maintenance.

---

By following the above guidelines, you can leverage the Auto Tuning feature to maintain optimal performance and reliability in your scripts.
