import pydantic
from typing_extensions import ClassVar
from fastapi.responses import JSONResponse


class BaseModel(pydantic.BaseModel):
    model_config: ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow")

    def e(self, prefix: str = "data: ", sep: str = "\n\n") -> str:
        return f"{prefix}{self.model_dump_json()}{sep}"


class BaseOutput(BaseModel):
    code: int = 200
    msg: str = "success"

    def r(self):
        return JSONResponse(self.dict(), status_code=self.code)

    class Config:
        extra = "allow"
