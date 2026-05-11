from pydantic import BaseModel, Field


class DescribeSceneRequest(BaseModel):
    image_base64: str = Field(..., min_length=1)


class DescribeSceneResponse(BaseModel):
    description: str
    confidence: float = 1.0
    processing_time_ms: float


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    device: str
    model_name: str
