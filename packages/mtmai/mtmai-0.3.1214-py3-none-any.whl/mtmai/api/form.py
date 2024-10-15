from camelCasing import camelCasing
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from mtmai.core.logging import get_logger
from mtmlib.decorators.mtform.mtform import FormFieldSchema, MtForm, get_form_by_name

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

    schema = form_class.model_json_schema()
    properties = schema.get("properties", {})

    mtform_properties = {}
    for k, v in properties.items():
        field_schema = FormFieldSchema(
            name=k,
            placeholder=v.get("placeholder"),
            valueType=v.get("type"),
            defaultValue=v.get("default"),
            description=v.get("description"),
            label=v.get("title"),
            type=v.get("format") or v.get("type"),
        )
        mtform_properties[k] = field_schema

    mtform_instance = MtForm(
        properties=mtform_properties,
        title=schema.get("title", ""),
        type=schema.get("type", "object"),
        variant="default",
    )

    return mtform_instance
