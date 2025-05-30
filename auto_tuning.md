# Auto Tuning with Backtesting and Variable Optimisation

---

## Overview

The Powston Auto Tuning feature introduces a mechanism to optimise script variables based on historical performance data. By embedding specific annotations within your scripts and utilising machine learning techniques, the system can automatically backtest and adjust variables to enhance efficiency and accuracy, aiming to minimise retail energy bills.

---

## Opt-In Mechanism

To enable Auto Tuning in your script:

1. **Script Name**: Ensure the name of your active script starts with `PowstonAutoTuned:`. This designation is set within the Powston Rules interface, not within the script's content.

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

1. **Detection**: Identifies the presence of the `PowstonAutoTuned:` prefix in the script's name to confirm that Auto Tuning is enabled.

2. **Parsing Annotations**: Scans for all `# CICD:` annotations to extract the specified timestamps and expected actions.

3. **Variable Identification**: Detects all variables in the script that match the following regular expression, targeting all-uppercase variable names assigned numeric values:

   ```python
   r"^[A-Z_0-9]+\s*=\s*\d+(\.\d+)?"
   ```



4. **Optimization Process**:

   * **Simulation Environment**: Utilises a virtual environment (or "gym") to model different scenarios based on historical data.

   * **Machine Learning Model**: Employs a machine learning model to simulate various configurations of the identified variables, aiming to determine the combination that results in the lowest retail energy bill.

   * **Reward Function**: Evaluates each configuration with the goal of minimizing the retail energy bill.

   * **Variable Adjustment**: Iteratively adjusts and tests variables within the simulation to identify the optimal set.

5. **Validation**:

   * **Backtesting**: For each annotation:

     * Retrieves historical data corresponding to the specified timestamp.

     * Applies the current set of tuned variables to simulate the system's behaviour at that time.

     * Compares the simulated action against the expected action.

   * **Outcome**:

     * If the simulated action matches the expected action for all annotations, the tuned variables are considered valid and are applied.

     * If any discrepancy is found, the system retains the previous set of variables to ensure reliability.

---

## Benefits

* **Enhanced Accuracy**: Validates tuned variables against historical data to ensure effective optimisations.

* **Cost Reduction**: Optimised variables lead to lower energy bills by enhancing the efficiency of energy consumption and storage.

* **Reliability**: Prevents the deployment of unverified changes that could degrade system performance.

* **Transparency**: Provides clear documentation within scripts about the expected behaviour at specific times.

* **Automation**: Requires minimal manual intervention, streamlining the optimisation workflow.

---

## Usage Example

```python
# CICD: '2025-05-19 17:30:00+10', 'export'
# CICD: '2025-05-20 09:00:00+10', 'import'

MAX_CHARGE_RATE = 5.0
BATTERY_CAPACITY = 10.0
# Additional script logic follows...
```



---

## Notes

* **Time Format**: Ensure that timestamps are in ISO 8601 format with the appropriate timezone offset.

* **Action Labels**: Use consistent and valid actions (e.g., 'export', 'import') to avoid misinterpretation during backtesting.

* **Annotation Placement**: Place all `# CICD:` annotations near the top of the script for better visibility and maintenance.

---

By following the above guidelines, you can leverage the Auto Tuning feature to maintain optimal performance and reliability in your scripts.
