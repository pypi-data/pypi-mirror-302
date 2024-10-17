from datetime import datetime
from pydantic import BaseModel, Field
from typing import Annotated, Any, Optional


class T2SRequestOptions(BaseModel):
    temp: Optional[float] = Field(default=0.7, ge=0.0, le=1.0)
    top_k: Optional[Any] = None
    top_p: Optional[Any] = None
    silent: Optional[bool] = False
    min_eos_p: Optional[float] = Field(default=0.2, ge=0.0, le=1.0)
    max_gen_duration_s: Optional[Any] = None
    allow_early_stop: Optional[bool] = True
    use_kv_caching: Optional[bool] = False


class T2SRequest(BaseModel):
    text: str
    history_prompt: Optional[Any] = None
    options: T2SRequestOptions = T2SRequestOptions()

    def extract_options(self):
        return self.options.model_dump(exclude_unset=True) if self.options else {}


class T2SResponse(BaseModel):
    created_at: datetime
    response_file: Annotated[str, Field(min_length=1)] = Field(..., description="Base64-encoded string of the audio file to be transcribed.")
    response_file_format: Optional[str]
    done: bool
    done_reason: Optional[str] = None
    total_duration: Optional[int] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }