# Project Structure

```
powston/
├── LICENSE
├── README.md
├── CONTRIBUTING.md
├── .gitignore
├── setup.py
├── requirements.txt
├── docs/
│   ├── trading_strategies.md
│   └── system_explainability.md
├── src/
│   └── powston/
│       ├── __init__.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── battery.py
│       │   ├── solar.py
│       │   └── grid.py
│       ├── strategies/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── price_based.py
│       │   ├── time_based.py
│       │   └── forecast_based.py
│       └── utils/
│           ├── __init__.py
│           ├── logging.py
│           └── forecasting.py
└── tests/
    ├── __init__.py
    ├── test_battery.py
    ├── test_solar.py
    └── test_strategies.py
```

## Directory Structure Explanation

### Root Level
- `LICENSE`: MIT License file
- `README.md`: Project documentation and getting started guide
- `CONTRIBUTING.md`: Contribution guidelines
- `.gitignore`: Git ignore rules
- `setup.py`: Package installation configuration
- `requirements.txt`: Project dependencies

### docs/
- `trading_strategies.md`: Documentation for all trading strategies
- `system_explainability.md`: Guide for system logging and debugging

### src/powston/
Main package directory containing all source code

#### core/
Core system components:
- `battery.py`: Battery management functionality
- `solar.py`: Solar system interface
- `grid.py`: Grid interaction logic

#### strategies/
Trading strategy implementations:
- `base.py`: Base strategy class and interfaces
- `price_based.py`: Price-based trading strategies
- `time_based.py`: Time-based trading strategies
- `forecast_based.py`: Forecast-based trading strategies

#### utils/
Utility functions and helpers:
- `logging.py`: Logging and reason string utilities
- `forecasting.py`: Price and load forecasting utilities

### tests/
Unit tests for all components:
- `test_battery.py`: Battery management tests
- `test_solar.py`: Solar system tests
- `test_strategies.py`: Trading strategy tests

## Next Steps

1. Move existing code into appropriate modules
2. Add proper Python package structure
3. Implement missing components
4. Add unit tests
5. Update documentation to reflect new structure
