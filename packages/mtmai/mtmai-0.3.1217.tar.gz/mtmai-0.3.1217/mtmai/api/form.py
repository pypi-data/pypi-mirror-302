from camelCasing import camelCasing
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from mtmai.core.logging import get_logger
from mtmai.deps import AsyncSessionDep, CurrentUser
from mtmai.flows.site_flows import FlowBase
from mtmai.mtlibs import aisdk
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


class SubmitSchemaFormRequest(BaseModel):
    form_name: str
    payload: dict


@router.post("/submit_schema_form")
async def submit_schema_form(
    req: SubmitSchemaFormRequest, session: AsyncSessionDep, current_user: CurrentUser
):
    """接受动态表单提交，触发工作流运行，并流式回传 http stream 事件"""
    flow_class = next(
        (
            cls
            for cls in FlowBase.__subclasses__()
            if cls.form_model.__name__ == req.form_name
        ),
        None,
    )
    if not flow_class:
        raise HTTPException(
            status_code=404, detail=f"Flow for form {req.form_name} not found"
        )

    async def stream():
        result = await flow_class.execute(session, current_user, req.payload)
        yield aisdk.data(result)
        yield aisdk.finish()

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={
            "Content-Type": "text/plain; charset=utf-8",
            "Cache-Control": "no-store, no-cache, must-revalidate, proxy-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
            "Surrogate-control": "no-store",
        },
    )
