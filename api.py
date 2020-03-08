"""
Simple API server for comparing content from two URLs
"""

import os

import httpx
import pydantic
import spacy
from bs4 import BeautifulSoup
from fastapi import FastAPI

app = FastAPI()
nlp_en = spacy.load("en_core_web_lg")

mercury_api_url = os.environ.get("MERCURY_API_URL", "")


async def fetch_and_extract_text(url: pydantic.HttpUrl) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(mercury_api_url + "?url=" + url)
        response.raise_for_status()

    # parse article content with self-hosted mercury api parser
    body = response.json()
    html = body["content"]
    soup = BeautifulSoup(html, features="lxml")

    return soup.get_text()


def compare_documents(sample_text_a: str, sample_text_b: str) -> float:
    """Compares two documents using spacy's bow model"""

    doc_a = nlp_en(sample_text_a)
    doc_b = nlp_en(sample_text_b)

    return doc_a.similarity(doc_b)


class RequestShape(pydantic.BaseModel):
    url_a: pydantic.HttpUrl
    url_b: pydantic.HttpUrl


@app.post("/compare")
async def compare_articles(payload: RequestShape, include_text: bool = False):
    if not mercury_api_url:  # not robust
        return {"err": "missing MERCURY_API_URL from environment"}

    document_a = await fetch_and_extract_text(payload.url_a)
    document_b = await fetch_and_extract_text(payload.url_b)

    context = {
        "similarity": compare_documents(document_a, document_b),
    }

    if include_text:
        context.update(
            text={
                "a": {"text": document_a, "url": payload.url_a,},
                "b": {"text": document_b, "url": payload.url_b,},
            }
        )

    return context
