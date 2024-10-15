from camelCasing import camelCasing
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from mtmai.core.logging import get_logger
from mtmlib.decorators.mtform.mtform import MtForm, get_form_by_name

logger = get_logger()

router = APIRouter()


class OpenFormRequest(BaseModel):
    formName: str


class SchemaFormRequest(BaseModel):
    formName: str


@router.get("/schema_form/{name}", response_model=MtForm)
async def schema_form(name: str):
    name = camelCasing.toCamelCase(name)

    names = [name, name + "Form"]

    for name in names:
        form_class = get_form_by_name(name)
        if form_class is not None:
            break
    if form_class is None:
        raise HTTPException(status_code=404, detail=f"Form '{name}' not found")
    return MtForm(**form_class.model_json_schema())
