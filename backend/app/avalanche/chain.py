from web3 import Web3
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

class AvaxChainConnection:
    def __init__(self, network="mainnet"):
        """Initialize connection to Avalanche C-Chain."""
        self.network = network
        
        if network == "mainnet":
            self.rpc_url = os.getenv('AVALANCHE_MAINNET_URL')
        elif network == "fuji":
            self.rpc_url = os.getenv('AVALANCHE_FUJI_URL')
        else:
            raise ValueError(f"Unsupported network: {network}")
            
        self.web3 = Web3(Web3.HTTPProvider(self.rpc_url))
        
        # Verify connection
        if not self.web3.is_connected():
            logger.error(f"Failed to connect to Avalanche {network}")
            raise ConnectionError(f"Could not connect to Avalanche {network}")
        
        logger.info(f"Connected to Avalanche {network} at block {self.web3.eth.block_number}")
    
    def get_contract(self, address, abi=None):
        """Get contract instance at specified address."""
        # Validate address
        if not self.web3.is_address(address):
            raise ValueError(f"Invalid address: {address}")
            
        if abi:
            return self.web3.eth.contract(address=address, abi=abi)
        else:
            # For verification only
            return address
    
    def get_contract_code(self, address):
        """Get contract bytecode at address."""
        code = self.web3.eth.get_code(address)
        return code.hex()
    
    def get_transaction_count(self, address):
        """Get transaction count for address."""
        return self.web3.eth.get_transaction_count(address)