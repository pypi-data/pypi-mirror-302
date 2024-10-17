import unittest
import asyncio
from typing import List
from pydantic import BaseModel, Field

from zyk.src.lms.core.main import LM

class SimpleResponse(BaseModel):
    message: str
    confidence_between_zero_one: float = Field(
        ..., description="Confidence level between 0 and 1"
    )


class NestedResponse(BaseModel):
    main_category: str
    subcategories: List[str]
    details: SimpleResponse

if __name__ == "__main__":
    lm = LM(
        model_name="gpt-4o-mini",
        formatting_model_name="gpt-4o-mini",
        temperature=0.7,
        max_retries="Few",
        structured_output_mode="stringified_json",
    )
    result = lm.respond_sync(
        system_message="You are a helpful assistant.",
        user_message="Give me a short greeting and your confidence level.",
        response_model=SimpleResponse,
    )
    print(result)
    result = lm.respond_sync(
        system_message="You are a helpful assistant.",
        user_message="Give me a short greeting and your confidence level.",
        response_model=NestedResponse,
    )
    print(result)