# MSNRootCauseAnalyzer

MSNRootCauseAnalyzer is a Python library for performing root cause analysis.

## Installation

```bash
pip install MSNRootCauseAnalyzer
```

## Usage
```python
from root_cause_analyzer import get_analyzer

analyzer = get_analyzer('adtributor')
result = analyzer.analyze(data={})
print(result)
``` 