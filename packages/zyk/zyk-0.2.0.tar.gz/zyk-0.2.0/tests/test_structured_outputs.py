import unittest
import asyncio
from typing import List
from pydantic import BaseModel, Field

from zyk.src.lms.core.main import LM


# Define example structured output models
class SimpleResponse(BaseModel):
    message: str
    confidence: float


class ComplexResponse(BaseModel):
    title: str
    tags: List[str]
    content: str


class NestedResponse(BaseModel):
    main_category: str
    subcategories: List[str]
    details: SimpleResponse


class TestLMStructuredOutputs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the LM once for all tests
        cls.lm = LM(
            model_name="gpt-4o-mini",
            formatting_model_name="gpt-4o-mini",
            temperature=0.7,
            max_retries="Few",
            structured_output_mode="forced_json",
        )

    def test_sync_simple_response(self):
        result = self.lm.respond_sync(
            system_message="You are a helpful assistant.",
            user_message="Give me a short greeting and your confidence level.",
            response_model=SimpleResponse,
        )
        self.assertIsInstance(result, SimpleResponse)
        self.assertIsInstance(result.message, str)
        self.assertIsInstance(result.confidence, float)
        self.assertGreaterEqual(result.confidence, 0)
        self.assertLessEqual(result.confidence, 1)

    def test_sync_complex_response(self):
        result = self.lm.respond_sync(
            system_message="You are a content creator.",
            user_message="Create a short blog post about AI.",
            response_model=ComplexResponse,
        )
        self.assertIsInstance(result, ComplexResponse)
        self.assertIsInstance(result.title, str)
        self.assertIsInstance(result.tags, list)
        self.assertIsInstance(result.content, str)

    async def async_nested_response(self):
        result = await self.lm.respond_async(
            system_message="You are a categorization expert.",
            user_message="Categorize 'Python' and provide a brief description.",
            response_model=NestedResponse,
        )
        self.assertIsInstance(result, NestedResponse)
        self.assertIsInstance(result.main_category, str)
        self.assertIsInstance(result.subcategories, list)
        self.assertIsInstance(result.details, SimpleResponse)

    def test_async_nested_response(self):
        asyncio.run(self.async_nested_response())


if __name__ == "__main__":
    unittest.main()
