from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from mtmai.core.logging import get_logger
from mtmlib.decorators.mtform.mtform import MyForm, get_form_by_name

logger = get_logger()

router = APIRouter()


class OpenFormRequest(BaseModel):
    formName: str


class SchemaFormRequest(BaseModel):
    formName: str


@router.get("/schema_form/{name}", response_model=MyForm)
async def schema_form(name: str):
    form_class = get_form_by_name(name)
    if form_class is None:
        raise HTTPException(status_code=404, detail=f"Form '{name}' not found")
    return MyForm(**form_class.model_json_schema())
