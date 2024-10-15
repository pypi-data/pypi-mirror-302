import uuid

from sqlmodel import Field, SQLModel


class FormField(SQLModel):
    name: str
    label: str | None = None
    type: str | None = None
    required: bool | None = None
    default: str | None = None
    description: str | None = None
    options: list[str] | None = None
    placeholder: str | None = None


class MtForm(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    title: str | None = None
    fields: list[FormField] | None = None
    layout: str | None = None
    submit_text: str | None = None
    action: str | None = None


class MtFormsConfig(SQLModel):
    class Config:
        arbitrary_types_allowed = True

    mtforms: list[MtForm]
