# contract upload/fetch

from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form
from pydantic import BaseModel, field_validator
import re
from typing import Optional, List
from app.avalanche.contract import ContractHandler
from app.services.contract_service import ContractService
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_async_session
from app.schemas.contract import ContractOut

router = APIRouter(
    prefix="/contracts",
    tags=["contracts"],
)

contract_service = ContractService()

class ContractAddress(BaseModel):
    address: str
    network: str = "mainnet"
    
    @field_validator('address')
    @classmethod
    def validate_address(cls, v):
        if not re.fullmatch(r'^0x[a-fA-F0-9]{40}$', v):
            raise ValueError('Invalid Ethereum address format')
        return v

@router.post("/fetch")
async def fetch_contract(
    contract_data: ContractAddress,
    db: AsyncSession = Depends(get_async_session)
):
    """Fetch contract by address from Avalanche network and store in DB."""
    try:
        handler = ContractHandler(network=contract_data.network)
        contract_details = handler.get_contract_details(contract_data.address)
        contract_dict = {
            "address": contract_data.address,
            "chain": contract_data.network,
            "source_code": contract_details.get("source_code"),
            "bytecode": contract_details.get("bytecode"),
        }
        contract_id = await contract_service.store_contract(contract_dict, db)
        return {
            "contract_id": contract_id,
            "address": contract_data.address,
            "network": contract_data.network,
            "has_source": contract_details.get("source_code"),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/upload")
async def upload_contract(
    address: Optional[str] = Form(None), 
    network: str = Form("mainnet"),
    file: UploadFile = File(...),
    contract_name: str = Form(...),
    db: AsyncSession = Depends(get_async_session)
):
    """Upload contract source code directly and store in DB."""
    try:
        if address == "":
            address = None
        if address:
            if not re.fullmatch(r'^0x[a-fA-F0-9]{40}$', address):
                raise HTTPException(status_code=400, detail="Invalid Ethereum address format")
        content = await file.read()
        if not file.filename.endswith('.sol'):
            raise HTTPException(status_code=400, detail="File must be a Solidity (.sol) file")
        contract_dict = {
            "address": address,
            "chain": network,
            "contract_name": contract_name,
            "source_code": content.decode('utf-8'),
            "bytecode": None,
        }
        contract_id = await contract_service.store_contract(contract_dict, db)
        return {
            "contract_id": contract_id,
            "contract_name": contract_name,
            "network": network,
            "address": address,
            "file_name": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[ContractOut])
async def list_contracts(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_async_session)
):
    """List all contracts."""
    contracts = await contract_service.list_contracts(db, skip=skip, limit=limit)
    return contracts