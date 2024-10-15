# base_analyzer.py

class BaseAnalyzer:
    """
    base class for root cause analyzer
    """
    def analyze(self, data):
        """
        analyze the data and return the root cause
        """
        raise NotImplementedError("Subclasses should implement this method.")
