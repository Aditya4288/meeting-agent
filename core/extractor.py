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
        temperature=0.2,
    )


def invoke_with_retry(chain, transcript, max_retries=5):

    for attempt in range(max_retries):

        try:
            return chain.invoke(transcript)

        except Exception as e:

            error_text = str(e)

            if "429" not in error_text and "rate_limit" not in error_text.lower():
                raise

            if attempt == max_retries - 1:
                raise RuntimeError(
                    "Mistral API rate limit is still active. "
                    "Please wait and try again."
                ) from e

            wait_time = min(
                30,
                (2 ** attempt) + random.uniform(0, 1)
            )

            print(
                f"Mistral rate limit reached. "
                f"Retrying in {wait_time:.1f} seconds..."
            )

            time.sleep(wait_time)


def build_chain(system_prompt: str):

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{text}"),
    ])

    return prompt | llm | StrOutputParser()


def extract_action_items(transcript: str) -> str:

    chain = build_chain(
        "You are an expert meeting analyst. From the meeting transcript, "
        "extract all action items. For each provide:\n"
        "- Task description\n"
        "- Owner (who is responsible)\n"
        "- Deadline (if mentioned, else write 'Not specified')\n\n"
        "Format as a numbered list. If none found say "
        "'No action items found.'"
    )

    result = invoke_with_retry(chain, {"text": transcript})

    time.sleep(1)

    return result


def extract_key_decisions(transcript: str) -> str:

    chain = build_chain(
        "You are an expert meeting analyst. From the meeting transcript, "
        "extract all key decisions made. Format as a numbered list. "
        "If none found say 'No key decisions found.'"
    )

    result = invoke_with_retry(chain, {"text": transcript})

    time.sleep(1)

    return result


def extract_questions(transcript: str) -> str:

    chain = build_chain(
        "From the meeting transcript, extract all unresolved questions "
        "or topics needing follow-up. Format as a numbered list. "
        "If none found say 'No open questions found.'"
    )

    return invoke_with_retry(chain, {"text": transcript})