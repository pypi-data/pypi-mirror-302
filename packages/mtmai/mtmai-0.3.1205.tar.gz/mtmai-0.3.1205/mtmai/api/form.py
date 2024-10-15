import os
from functools import lru_cache

import httpx
from fastapi import APIRouter
from pydantic import BaseModel

from mtmai.core.config import settings
from mtmai.core.logging import get_logger
from mtmai.models.form import MtForm, MtFormsConfig
from mtmai.mtlibs import yaml

logger = get_logger()

router = APIRouter()


@lru_cache(maxsize=1)
def get_form_by_name(name: str):
    if not os.path.exists(settings.graph_config_path):
        raise Exception(f"未找到mtforms配置文件: {settings.graph_config_path}")
    config_dict = yaml.load_yaml_file(settings.mtforms_config_path) or {}

    sub = config_dict.get("mtforms")
    mtforms = MtFormsConfig.model_validate(sub)
    for form in mtforms.mtforms:
        if form.name == name:
            return form
    return None


class OpenFormRequest(BaseModel):
    formName: str


@router.get("/open_form", response_model=MtForm)
def open_form(req: OpenFormRequest):
    mtform = get_form_by_name(req.formName)
    if not mtform:
        raise httpx.HTTPStatusError(
            status_code=404, message=f"Form '{req.formName}' not found"
        )
    return mtform
