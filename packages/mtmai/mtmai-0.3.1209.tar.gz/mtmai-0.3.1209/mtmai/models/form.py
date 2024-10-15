from pydantic import BaseModel
from pydantic import Field as PydanticField

from mtmlib.decorators.mtform.mtform import mtform

# class FormField(SQLModel):
#     name: str
#     label: str | None = None
#     type: str | None = None
#     required: bool | None = None
#     default: str | None = None
#     description: str | None = None
#     options: list[str] | None = None
#     placeholder: str | None = None


# class MtForm(SQLModel):
#     id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
#     name: str
#     title: str | None = None
#     fields: list[FormField] | None = None
#     layout: str | None = None
#     submit_text: str | None = None
#     action: str | None = None


# class MtFormsConfig(SQLModel):
#     class Config:
#         arbitrary_types_allowed = True

#     mtforms: list[MtForm]


@mtform(name="site_create")
class SiteCreateForm(BaseModel):
    name: str = PydanticField(default=None, description="站点名称")
    title: str = PydanticField(default=None, description="站点标题")
    description: str = PydanticField(default=None, description="站点描述")
    layout: str = PydanticField(default=None, description="站点布局")
    submit_text: str = PydanticField(default=None, description="站点提交文本")
    action: str = PydanticField(
        default=None,
        description="站点操作",
        json_schema_extra={
            "title": "Password",
            "description": "Password of the user",
            "examples": ["123456"],
        },
    )

    class Config:
        json_schema_extra = {
            "title": "站点创建234",
        }
