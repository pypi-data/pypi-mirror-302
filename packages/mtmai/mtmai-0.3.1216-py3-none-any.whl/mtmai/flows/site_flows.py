from typing import Any, Type

from prefect import flow, task
from pydantic import BaseModel

from mtmai.deps import AsyncSessionDep, CurrentUser
from mtmai.models.form import SiteCreateForm
from mtmai.models.site import (
    Site,
    SiteCreateRequest,
)


@task
async def create_site_task(
    session: AsyncSessionDep, current_user: CurrentUser, item_in: SiteCreateRequest
):
    item = Site.model_validate(item_in, update={"owner_id": current_user.id})
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


@flow
async def create_Site_flow(
    *, session: AsyncSessionDep, current_user: CurrentUser, item_in: SiteCreateRequest
) -> Any:
    """
    Create new site.
    """
    task1_result = await create_site_task(session, current_user, item_in)
    return task1_result


# ---------------------------------------------------------------------------------------------------------
class FlowBase:
    @classmethod
    async def execute(
        cls, session: AsyncSessionDep, current_user: CurrentUser, data: dict
    ) -> Any:
        raise NotImplementedError("Subclasses must implement this method")


def mtflow(form_model: Type[BaseModel]):
    def decorator(cls):
        cls.form_model = form_model
        return cls

    return decorator


@mtflow(SiteCreateForm)
class CreateSiteFlow(FlowBase):
    @classmethod
    @flow
    async def execute(
        cls, session: AsyncSessionDep, current_user: CurrentUser, data: dict
    ) -> Any:
        item_in = cls.form_model(**data)
        task1_result = await create_site_task(session, current_user, item_in)
        return task1_result
