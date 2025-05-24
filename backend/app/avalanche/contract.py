import requests
from web3 import Web3
from app.avalanche.chain import AvaxChainConnection
import logging
import os
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

logger = logging.getLogger(__name__)

class ContractHandler:
    def __init__(self, network="mainnet"):
        self.chain = AvaxChainConnection(network)
        self.web3 = self.chain.web3
        self.api_key = os.getenv("SNOWTRACE_API_KEY")
        if not self.api_key:
            raise EnvironmentError("Missing SNOWTRACE_API_KEY in environment variables.")

    def get_api_url(self):
        return "https://api-testnet.snowtrace.io/api" if self.chain.network == "fuji" else "https://api.routescan.io/v2/network/mainnet/evm/43114/etherscan/api"

    @lru_cache(maxsize=128)
    def get_contract_source(self, address):
        """
        Attempt to retrieve verified contract source from Snowtrace
        (Avalanche's block explorer)
        """
        api_url = self.get_api_url()
        params = {
            "module": "contract",
            "action": "getsourcecode",
            "address": address,
            "apikey": self.api_key,
        }

        try:
            response = requests.get(api_url, params=params)
            data = response.json()

            if data["status"] != "1":
                logger.warning(f"Snowtrace API returned error: {data}")
                return None

            if not data["result"]:
                logger.warning(f"Contract not verified or not found: {data.get('message', '')}")
                return None

            # print({'file': data['result'][0]})
            return {
                "source_code": data["result"][0]["SourceCode"],
                "contract_name": data["result"][0]["ContractName"],
                "compiler_version": data["result"][0]["CompilerVersion"],
                "optimization": data["result"][0]["OptimizationUsed"],
                "runs": data["result"][0]["Runs"]
            }
        except Exception as e:
            logger.error(f"Error fetching contract source: {str(e)}")
            return None

    def get_contract_details(self, address):
        code = self.chain.get_contract_code(address)
        if code == "0x":
            raise ValueError(f"No contract at address {address}")

        source_info = self.get_contract_source(address)
        
        result = {
            "address": address,
            "bytecode": code,
            "chain": self.chain.network,
            "block_number": self.web3.eth.block_number,
            "source_code": source_info,
            "contract_name": None,
            "compiler_version": None,
            "optimization": None,
            "runs": None,
        }
        if source_info:
            result.update(source_info)
        return result