from pydantic import BaseModel, Field

class ImagesPostData(BaseModel):
    """
    Images post data type used in `[POST] /api/images/`
    """
    filename: str | None = None
    tags: list[str] = Field(default_factory=list)