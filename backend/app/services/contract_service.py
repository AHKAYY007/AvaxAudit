from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.contract import Contract
from typing import Optional, Dict, Any

class ContractService:
    async def store_contract(self, contract_dict, db: AsyncSession):
        # Check if contract already exists
        query = select(Contract).where(
            Contract.address == contract_dict["address"],
            Contract.chain == contract_dict["chain"]
        )
        result = await db.execute(query)
        existing = result.scalar_one_or_none()
        if existing:
            return existing.id  # Return existing contract's ID

        # If not exists, insert new
        contract = Contract(**contract_dict)
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