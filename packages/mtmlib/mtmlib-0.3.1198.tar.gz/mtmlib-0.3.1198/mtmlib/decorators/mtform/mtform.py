from pydantic import BaseModel, Field

# 存储注册的表单
registered_forms: dict[str, type[BaseModel]] = {}


def get_form_by_name(name: str) -> type[BaseModel]:
    return registered_forms.get(name)


class FormAttributes(BaseModel):
    name: str
    title: str | None = None
    method: str = "POST"
    action: str | None = None
    enctype: str | None = None
    target: str | None = None


def mtform(**kwargs):
    """
    表单装饰器，用于注册表单并设置表单属性
    """
    form_attrs = FormAttributes(**kwargs)

    def decorator(cls: type[BaseModel]):
        if form_attrs.name in registered_forms:
            msg = f"Form with name '{form_attrs.name}' already exists"
            raise ValueError(msg)
        registered_forms[form_attrs.name] = cls
        # cls.model_fields["form_attributes"] = Field(default=form_attrs)
        return cls

    return decorator


class FormFieldSchema(BaseModel):
    default: str | None = None
    description: str | None = None
    title: str
    type: str
    examples: list[str] | None = None


class MtForm(BaseModel):
    properties: dict[str, FormFieldSchema]
    title: str
    type: str = Field(default="object")
    # form_attributes: FormAttributes | None = None  # 可能没用

    class Config:  # noqa: D106
        arbitrary_types_allowed = True
