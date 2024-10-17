from typing import Type
from pydantic import BaseModel
import json
import ast
import re

def pull_out_structured_output(
    response_raw: str, response_model: Type[BaseModel]
) -> BaseModel:
    assert isinstance(response_raw, str), f"Response raw is not a string: {type(response_raw)}"

    # Use regex to extract JSON content within ```json ... ```
    json_pattern = re.compile(r'```json\s*(\{.*\})\s*```', re.DOTALL)
    match = json_pattern.search(response_raw)
    if match:
        response_prepared = match.group(1).strip()
    else:
        # Fallback to existing parsing if no code fencing is found
        if "```" in response_raw:
            response_prepared = response_raw.split("```")[1].strip()
        else:
            response_prepared = response_raw.strip()

    # Replace "null" with '"None"' if needed (ensure this aligns with your data)
    response_prepared = response_prepared.replace("null", '"None"')

    try:
        response = json.loads(response_prepared)
        final = response_model(**response)
    except json.JSONDecodeError as e:
        # Attempt to parse using ast.literal_eval as a fallback
        response_prepared = response_prepared.replace('\n', '').replace('\\n', '')
        response_prepared = response_prepared.replace('\\"', '"')
        try:
            response = ast.literal_eval(response_prepared)
            final = response_model(**response)
        except Exception as inner_e:
            raise ValueError(
                f"Failed to parse response as {response_model}: {inner_e} - {response_prepared}"
            )
    except Exception as e:
        raise ValueError(
            f"Failed to parse response as {response_model}: {e} - {response_prepared}"
        )
    return final
