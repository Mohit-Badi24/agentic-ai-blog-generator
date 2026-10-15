from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt
from typing import Literal

from state import State
from agents import llm,researcher_agent,writer_agent,editor_agent

Max_revision = 3 

#nodes 

def researcher_node(state:State):
    """Researcher agent Generates (or Revises) the research outline"""
    model = llm()
    researched_data = researcher_agent(
        llm = model,
        topic = state.topic,
        audience = state.audience,
        feedback = state.research_feedback
    )
    state.research = researched_data
    state.research_feedback =""

    return state

def human_review_research_data(state:State):
    """Pause and ask the human to approve the research or send the feedback"""
    decision = interrupt({
    "stage": "researcher_review",
    "research": state.research,
    "instructions": (
        "Reply with 'approve' to continue to writing",
        "or describe what to change to send it back to the researcher."
        )
    })
    if isinstance(decision, dict):
        action = decision.get("action", "approve")
        feedback = decision.get("feedback", "")
    else:
        text = str (decision)
        action = "approve" if text.lower() in ["approve", "approved", "ok", "yes", "process", ""] else "revise"
        feedback = "" if action == "approve" else text

    state.research_feedback = feedback
    return state




def writer_node(state:State):
    """Writer agent Generates (or Revises) the blog from given research data"""
    model = llm()
    draft_data = writer_agent(
        llm = model,
        topic = state.topic,
        audience = state.audience,
        feedback = state.writer_feedback,
        research_notes=state.research
    )
    state.writer = draft_data
    state.writer_feedback =""

    return state

def human_review_draft_data(state:State):
    """Pause and ask the human to approve the draft or send the feedback"""
    decision = interrupt({
    "stage": "Draft_review",
    "research": state.writer,
    "instructions": (
        "Reply with 'approve' to continue to editor",
        "or describe what to change to send it back to the editor."
        )
    })
    if isinstance(decision, dict):
        action = decision.get("action", "approve")
        feedback = decision.get("feedback", "")
    else:
        text = str (decision)
        action = "approve" if text.lower() in ["approve", "approved", "ok", "yes", "process", ""] else "revise"
        feedback = "" if action == "approve" else text

    state.writer_feedback = feedback
    return state


#editor node

def editor_node(state:State):
    """editor agent Generates the final blog from given drafted data"""
    model = llm()
    final = editor_agent(
        llm = model,
        topic = state.topic,
        draft=state.writer
    )
    state.final = final

    return state


# condintional nodes 

def route_after_researcher_node(state:State) -> Literal["research","writer"]:
    if state.research_feedback:
        return "research"
    else:
        return "writer"

# def route_after_writer_node(state:State) -> Literal["editor","writer"]:
#     if state.writer_feedback and state.revision_count < Max_revision:
#         return "editor"
#     else:
#         return "writer"

def route_after_writer_node(state: State) -> Literal["editor", "writer"]:
    print("DEBUG feedback:", repr(state.writer_feedback))
    print("DEBUG revision_count:", state.revision_count)

    if state.writer_feedback and state.revision_count < Max_revision:
        return "writer"

    return "editor"

## Build Graph 

def build_blog_graph(state:State):
    builder = StateGraph(state)

    #build nodes
    builder.add_node("research",researcher_node)
    builder.add_node("review_research",human_review_research_data)
    builder.add_node("writer",writer_node)
    builder.add_node("review_writer",human_review_draft_data)
    builder.add_node("editor",editor_node)

    #build edges
    builder.add_edge(START,"research")
    builder.add_edge("research","review_research")
    builder.add_conditional_edges("review_research",route_after_researcher_node,{
        "research":"research","writer":"writer"
    })
    builder.add_edge("writer","review_writer")
    builder.add_conditional_edges("review_writer",route_after_writer_node,{
            "writer":"writer","editor":"editor"
        })
    builder.add_edge("editor",END)

    graph = builder.compile(checkpointer=InMemorySaver())
    return graph