from pydantic import BaseModel, Field


class EvalRequest(BaseModel):
    dataset_path: str = Field(..., min_length=1)
    load_demo_data: bool = Field(default=True)