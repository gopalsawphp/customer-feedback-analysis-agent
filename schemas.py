
from typing import Literal
from pydantic import BaseModel, Field


class SentimentResult(BaseModel):
    sentiment: Literal["positive", "negative"] = Field(
        description="Overall customer feedback sentiment"
    )
    reason: str = Field(
        description="Short explanation for the classification"
    )


class FeedbackAnalysis(BaseModel):
    issue_type: Literal[
        "product_quality",
        "delivery",
        "billing",
        "technical_support",
        "customer_service",
        "refund",
        "other",
    ]
    tone: Literal[
        "angry",
        "frustrated",
        "disappointed",
        "concerned",
        "neutral",
    ]
    severity: Literal["low", "medium", "high", "critical"]
    summary: str = Field(
        description="Concise summary of the customer's problem"
    )
    suggested_action: str = Field(
        description="Recommended next step; do not claim an action has happened"
    )


class EmailDraft(BaseModel):
    subject: str = Field(description="Email subject line")
    body: str = Field(description="Complete professional email body")
