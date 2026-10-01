import os
import time
import random

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def get_llm():
    return ChatMistralAI(
        model="mistral-small-latest",
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.3,
    )


def invoke_with_retry(chain, input_data, max_retries=3):
    """
    Invoke Mistral with exponential backoff when rate limited.
    """

    for attempt in range(max_retries):
        try:
            return chain.invoke(input_data)

        except Exception as e:
            error_text = str(e)

            if "429" not in error_text and "rate_limit" not in error_text.lower():
                raise

            if attempt == max_retries - 1:
                raise RuntimeError(
                    "Mistral API rate limit exceeded. "
                    "Please wait for the API rate limit to reset."
                ) from e

            wait_time = min(
                30,
                (2 ** attempt) + random.uniform(0.5, 1.5)
            )

            print(
                f"Mistral rate limit reached. "
                f"Retrying in {wait_time:.1f} seconds..."
            )

            time.sleep(wait_time)


def analyze_transcript(transcript: str) -> dict:
    """
    Generate title, summary, action items, decisions and
    open questions using ONE Mistral API call.
    """

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are an expert meeting analyst.

Analyze the meeting transcript and return the result using
EXACTLY this structure:

TITLE:
<short professional title, maximum 8 words>

SUMMARY:
- <important point>
- <important point>
- <important point>

ACTION ITEMS:
1. <task> | Owner: <person or Not specified> | Deadline: <deadline or Not specified>

KEY DECISIONS:
1. <decision>

OPEN QUESTIONS:
1. <unresolved question>

Rules:
- Base everything ONLY on the transcript.
- Do not invent information.
- Keep the summary concise.
- If there are no action items, write:
  No action items found.
- If there are no key decisions, write:
  No key decisions found.
- If there are no open questions, write:
  No open questions found.
""",
        ),
        ("human", "{transcript}"),
    ])

    chain = prompt | llm | StrOutputParser()

    print("Generating complete meeting analysis...")

    result = invoke_with_retry(
        chain,
        {"transcript": transcript}
    )

    return parse_analysis(result)


def parse_analysis(text: str) -> dict:
    """
    Convert the single LLM response into fields that
    the existing Streamlit UI can use.
    """

    sections = {
        "title": "",
        "summary": "",
        "action_items": "",
        "key_decisions": "",
        "open_questions": "",
    }

    current_section = None

    section_map = {
        "TITLE:": "title",
        "SUMMARY:": "summary",
        "ACTION ITEMS:": "action_items",
        "KEY DECISIONS:": "key_decisions",
        "OPEN QUESTIONS:": "open_questions",
    }

    for line in text.splitlines():

        stripped = line.strip()

        upper = stripped.upper()

        if upper in section_map:
            current_section = section_map[upper]
            continue

        if current_section:
            if sections[current_section]:
                sections[current_section] += "\n"

            sections[current_section] += stripped

    return {
        key: value.strip()
        for key, value in sections.items()
    }


def summarize(transcript: str) -> str:
    """
    Compatibility function for the existing app.

    NOTE:
    For the optimized pipeline, use analyze_transcript()
    instead of calling summarize() separately.
    """

    result = analyze_transcript(transcript)

    return result["summary"]


def generate_title(transcript: str) -> str:
    """
    Compatibility function for the existing app.

    NOTE:
    For the optimized pipeline, use analyze_transcript()
    instead of calling generate_title() separately.
    """

    result = analyze_transcript(transcript)

    return result["title"]