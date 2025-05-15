from abc import ABC, abstractmethod
from typing import Dict, List, Any

class BaseAnalyzer(ABC):
    """Base class for all smart contract analyzers."""
    
    def __init__(self, name: str):
        self.name = name
        
    @abstractmethod
    async def analyze(self, contract_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analyze a contract and return list of findings.
        
        Args:
            contract_data: Dictionary containing contract details
            
        Returns:
            List of findings, each as a dictionary
        """
        pass
        
    @abstractmethod
    def get_analyzer_info(self) -> Dict[str, Any]:
        """Return information about this analyzer."""
        pass