import json

def parse_gemini_planner_output(response_lines: list[str]) -> dict:
    # Join lines into a single string
    joined = "\n".join(response_lines).strip()
    
    # Remove surrounding markdown or stray backticks if they exist
    if joined.startswith("```json"):
        joined = joined.removeprefix("```json").strip()
    if joined.endswith("```"):
        joined = joined.removesuffix("```").strip()
    
    try:
        return json.loads(joined)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")

def parse_gemini_json_output(response: str) -> dict:
    # Join lines into a single string
    # Remove surrounding markdown or stray backticks if they exist
    if response.startswith("```json"):
        response = response.removeprefix("```json").strip()
    if response.endswith("```"):
        response = response.removesuffix("```").strip()
    
    try:
        return json.loads(response)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")