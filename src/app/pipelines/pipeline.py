from pathlib import Path
from src.app.agents.agent import agent_manager
from src.app.schemas.schema import FeedbackState
# ---------- RUN THE WORKFLOW ----------

def customer_feedback_Analysis(feedback: str, customer_name: str) -> FeedbackState:
    graph = agent_manager();
    graph_path = Path("customer_feedback_graph.png")
    if not graph_path.exists():
        graph_png = graph.get_graph().draw_mermaid_png()
        graph_path.write_bytes(graph_png)
    else:
        print("Graph already exists. Skipping generation.")

    initial_state: FeedbackState = {
        "customer_name": customer_name,
        "customer_email": "mail2gopalphp@gmail.com",
        "feedback": feedback,
        "sentiment": None,
        "sentiment_reason": None,
        "analysis": None,
        "email_subject": None,
        "email_body": None,
        "email_status": None,
    }

    result = graph.invoke(initial_state)
    return result