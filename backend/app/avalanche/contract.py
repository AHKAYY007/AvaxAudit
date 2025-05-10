import requests
from web3 import Web3
from app.avalanche.chain import AvaxChainConnection
import logging

logger = logging.getLogger(__name__)

class ContractHandler:
    def __init__(self, network="mainnet"):
        self.chain = AvaxChainConnection(network)
        self.web3 = self.chain.web3
        
    def get_contract_source(self, address):
        """
        Attempt to retrieve verified contract source from Snowtrace
        (Avalanche's block explorer)
        """
        api_url = "https://api.snowtrace.io/api"
        if self.chain.network == "fuji":
            api_url = "https://api-testnet.snowtrace.io/api"
            
        # Note: In a production app, you'd use an API key
        params = {
            "module": "contract",
            "action": "getsourcecode",
            "address": address,
        }
        
        try:
            response = requests.get(api_url, params=params)
            data = response.json()
            
            if data["status"] == "1" and data["result"]:
                return {
                    "source_code": data["result"][0]["SourceCode"],
                    "contract_name": data["result"][0]["ContractName"],
                    "compiler_version": data["result"][0]["CompilerVersion"],
                    "optimization": data["result"][0]["OptimizationUsed"],
                    "runs": data["result"][0]["Runs"]
                }
            else:
                logger.warning(f"Contract source not verified: {address}")
                return None
        except Exception as e:
            logger.error(f"Error fetching contract source: {str(e)}")
            return None
    
    def get_contract_details(self, address):
        """Get comprehensive contract details combining on-chain and explorer data."""
        # Verify valid contract
        code = self.chain.get_contract_code(address)
        if code == "0x":
            raise ValueError(f"No contract at address {address}")
        
        # Get source if available
        source_info = self.get_contract_source(address)
        
        # Return combined info
        return {
            "address": address,
            "bytecode": code,
            "source": source_info,
            "chain": self.chain.network,
            "block_number": self.web3.eth.block_number,
        }