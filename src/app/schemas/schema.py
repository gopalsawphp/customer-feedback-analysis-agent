from pydantic import BaseModel, Field
from typing import TypedDict, Optional, Literal

class FeedbackSentiment(BaseModel):
    sentiment: Literal["positive", "negative"] = Field(
        description="Overall customer feedback sentiment"
    )
    reason: str = Field(
        description="Short explanation for the classification"
    )

class FeedbackAnalysis(BaseModel):
    issue_type: Literal["product_quality", "delivery", "billing", "technical_support", "customer_service", "refund", "other",
        ] = Field("Customer issue type")
    
    tone: Literal["angry", "frustrated", "disappointed", "concerned", "neutral"] = Field(
        description="Customer feedback tone"
        )

    severity: Literal["low", "medium", "high", "critical"] = Field(
        description="Customer feedback severity"
    )
    summary: str = Field(
            description="Concise summary of the customer's problem"
        )
    suggested_action: str = Field(
            description="Recommended next step; do not claim an action has happened"
        )

class EmailDraft(BaseModel):
    subject: str = Field(description="Email subject line")
    body: str = Field(description="Complete professional email body")

class FeedbackState(TypedDict):
    customer_name: str
    customer_email: str
    feedback: str
    sentiment: Optional[str]
    sentiment_reason: Optional[str]
    analysis: Optional[dict]
    email_subject: Optional[str]
    email_body: Optional[str]
    email_status: Optional[str]

    