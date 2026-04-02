import os
import httpx
from dotenv import load_dotenv

load_dotenv()

LM_STUDIO_URL=os.getenv("LM_STUDIO_URL", "http://localhost:1234/api/v1/chat")
LM_STUDIO_MODEL=os.getenv("LM_STUDIO_MODEL", "local-model")

async def call_lm_studio(prompt_str) -> str:
    """Helper function for calling LM studio API"""
    payload = {
        "model": LM_STUDIO_MODEL,
        "input": prompt_str,
        "temperature": 0.3,
        "max_output_tokens": 300,
        "reasoning": "off"
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(LM_STUDIO_URL, json=payload)
            response.raise_for_status()
            data = response.json()

            outputs = data.get("output", [])
            for item in outputs:
                if item.get("type") == "message":
                    return item.get("content", "").strip()

            return "No answer from AI model"

    except httpx.RequestError as e:
        print(f"Connection error with LM studio: {e}")
        return "AI trainer is unavailable. Check if LM Studio is running."
    except Exception as e:
        print(f"Error parsing LM studio response: {e}")
        return "Error processing tactical advice"