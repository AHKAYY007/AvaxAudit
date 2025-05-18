from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.contract import Contract
from typing import Optional, Dict, Any

class ContractService:
    async def store_contract(self, contract_details: Dict[str, Any], db: AsyncSession) -> int:
        """
        Store a contract in the database.
        Expects contract_details to include:
        - address (str)
        - chain (str)
        - source_code (str, optional)
        - bytecode (str, optional)
        """
        contract = Contract(
            address=contract_details.get("address"),
            chain=contract_details.get("chain"),
            source_code=contract_details.get("source_code"),
            bytecode=contract_details.get("bytecode"),
        )
        db.add(contract)
        await db.commit()
        await db.refresh(contract)
        return contract.id

    async def get_contract_by_id(self, contract_id: int, db: AsyncSession) -> Optional[Contract]:
        return await db.get(Contract, contract_id)

    async def get_contract_by_address(self, address: str, chain: str, db: AsyncSession) -> Optional[Contract]:
        result = await db.execute(
            select(Contract).where(Contract.address == address, Contract.chain == chain)
        )
        return result.scalars().first()

    async def list_contracts(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(select(Contract).offset(skip).limit(limit))
        return result.scalars().all()