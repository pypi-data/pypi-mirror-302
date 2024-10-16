from typing import Any

import httpx
from bs4 import BeautifulSoup
from prefect import flow, task
from pydantic import BaseModel

from mtmai.deps import AsyncSessionDep, CurrentUser
from mtmai.flows import FlowBase, mtflow
from mtmai.models.search_index import SearchIndex
from mtmai.models.site import (
    Site,
    SiteCreateRequest,
)


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
    content_summary = site_info.description or "no_description"
    content_summary = content_summary[:100]  # Limit the summary to 500 characters

    search_index = SearchIndex(
        content_type="site",
        content_id=new_site.id,
        title=new_site.title or "no_title",
        owner_id=current_user.id,
        content_summary=content_summary,
        meta={
            # "author_id": str(new_blog_post.author_id),
            # "tags": [tag.name for tag in new_blog_post.tags],
        },
        # search_vector=generate_search_vector(post.title, post.content),
        # embedding=generate_embedding(post.title, post.content)
    )
    session.add(search_index)
    await session.commit()
    await session.refresh(search_index)
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
        return task1_result
