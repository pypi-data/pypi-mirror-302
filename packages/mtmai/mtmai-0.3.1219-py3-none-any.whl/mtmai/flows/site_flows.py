from typing import Any

import httpx
from bs4 import BeautifulSoup
from prefect import flow, task
from pydantic import BaseModel

from mtmai.crud.curd_search import create_site_search_index
from mtmai.deps import AsyncSessionDep, CurrentUser
from mtmai.flows import FlowBase, mtflow
from mtmai.models.site import (
    Site,
    SiteCreateRequest,
)
from mtmai.mtlibs import aisdk


class SiteDetectInfo(BaseModel):
    title: str | None = None
    description: str | None = None


@task
async def site_info_detect(
    session: AsyncSessionDep, current_user: CurrentUser, item_in: SiteCreateRequest
):
    """获取远程站点基本信息"""
    async with httpx.AsyncClient() as client:
        resp = await client.get(item_in.url)

    soup = BeautifulSoup(resp.text, "html.parser")
    title = soup.title.string if soup.title else None
    meta_description = soup.find("meta", attrs={"name": "description"})
    description = meta_description["content"] if meta_description else None
    if description:
        description = description[:100]
    return SiteDetectInfo(title=title, description=description)


@task
async def create_site_task(
    session: AsyncSessionDep, current_user: CurrentUser, item_in: SiteCreateRequest
):
    site_info = await site_info_detect(session, current_user, item_in)
    new_site = Site.model_validate(item_in, update={"owner_id": current_user.id})
    new_site.title = site_info.title
    new_site.description = site_info.description
    session.add(new_site)
    await session.commit()
    await session.refresh(new_site)
    await create_site_search_index(session, new_site, current_user.id)
    await session.refresh(new_site)
    ret = new_site.model_dump()
    return ret


@mtflow(SiteCreateRequest)
class CreateSiteFlow(FlowBase):
    @classmethod
    @flow(name="CreateSiteFlow")
    async def execute(
        cls, session: AsyncSessionDep, current_user: CurrentUser, data: dict
    ) -> Any:
        item_in = cls.form_model(**data)
        task1_result = await create_site_task(session, current_user, item_in)
        yield aisdk.AiTextChunck("工作流完成")
