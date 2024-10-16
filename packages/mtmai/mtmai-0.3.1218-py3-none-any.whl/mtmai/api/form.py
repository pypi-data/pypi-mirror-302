import json
from typing import Type

from camelCasing import camelCasing
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from mtmai.core.logging import get_logger
from mtmai.deps import AsyncSessionDep, CurrentUser
from mtmai.flows.site_flows import FlowBase
from mtmai.mtlibs import aisdk
from mtmlib.decorators.mtform.mtform import FormFieldSchema, MtForm

logger = get_logger()

router = APIRouter()


class OpenFormRequest(BaseModel):
    formName: str


class SchemaFormRequest(BaseModel):
    formName: str


@router.get("/schema_form/{name}", response_model=MtForm)
async def schema_form(name: str):
    # 旧代码
    # name = camelCasing.toCamelCase(name)

    # names = [name, name + "Form", name + "Request"]

    # for name in names:
    #     form_class = get_form_by_name(name)
    #     if form_class is not None:
    #         break
    # if form_class is None:
    #     raise HTTPException(status_code=404, detail=f"Form '{name}' not found")

    # schema = form_class.model_json_schema()
    # properties = schema.get("properties", {})

    # mtform_properties = {}
    # for k, v in properties.items():
    #     field_schema = FormFieldSchema(
    #         name=k,
    #         placeholder=v.get("placeholder"),
    #         valueType=v.get("type"),
    #         defaultValue=v.get("default"),
    #         description=v.get("description"),
    #         label=v.get("title"),
    #         type=v.get("format") or v.get("type"),
    #     )
    #     mtform_properties[k] = field_schema

    # mtform_instance = MtForm(
    #     properties=mtform_properties,
    #     title=schema.get("title", ""),
    #     type=schema.get("type", "object"),
    #     variant="default",
    # )

    # return mtform_instance

    # 新代码
    name = camelCasing.toCamelCase(name)
    names = [name, name + "Form", name + "Request"]

    form_class: Type[BaseModel] = None
    for flow_class in FlowBase.__subclasses__():
        if hasattr(flow_class, "form_model"):
            form_name = flow_class.form_model.__name__
            if form_name in names or camelCasing.toCamelCase(form_name) in names:
                form_class = flow_class.form_model
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
    form_data: dict


@router.post("/submit_schema_form")
async def submit_schema_form(
    req: Request, session: AsyncSessionDep, current_user: CurrentUser
):
    """接受动态表单提交，触发工作流运行，并流式回传 http stream 事件"""
    request_data = await req.json()
    messages = request_data.get("messages")
    if not messages or len(messages) == 0:
        raise HTTPException(status_code=400, detail="No messages provided")
    latest_message = messages[-1]
    formReq = SubmitSchemaFormRequest(**json.loads(latest_message.get("content")))

    flow_class = next(
        (
            cls
            for cls in FlowBase.__subclasses__()
            if cls.form_model.__name__ == formReq.form_name
            or camelCasing.toCamelCase(cls.form_model.__name__) == formReq.form_name
            or camelCasing.toCamelCase(cls.form_model.__name__)
            == formReq.form_name + "Form"
            or camelCasing.toCamelCase(cls.form_model.__name__)
            == formReq.form_name + "Request"
        ),
        None,
    )
    if not flow_class:
        raise HTTPException(
            status_code=404, detail=f"Flow for form {formReq.form_name} not found"
        )

    async def stream():
        result = await flow_class.execute(session, current_user, formReq.form_data)
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
