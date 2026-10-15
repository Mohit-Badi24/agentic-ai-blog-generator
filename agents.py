import os

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# llm 

def llm (model_name : str ="openai/gpt-oss-20b", temperature: float = 0.50):
    api_key = os.getenv("GROQ_API_KEY")

    llm = ChatGroq(model=model_name,temperature=temperature,api_key=api_key)
    return llm


#researcher agent 

research_prompt = ChatPromptTemplate([
    {"role":"system","content":"""
    You are a Research Agent. Given a blog topic and target audience, produce a clear,
    "structured research outline. Include: \n"
    "1. 5-7 key points the blog should cover\n"
    "2. Important facts, stats, or examples for each point\n"
    "3. Suggested angle or hook\n"
    "Be concise. Use bullet points. Do NOT write the full blog yet."
    """},
    {"role":"user", "content":"Topic:{topic}, Audience:{audience},{revision_hints}, Write the research outline now "}
])


def researcher_agent(llm:ChatGroq ,topic:str ,audience: str ,feedback: str =""):
    revision_hints = f"the human provided this feedback based on your previous reseach please address it :{feedback}"

    if not feedback:
        revision_hints =" this is your first attempt"

    chain = research_prompt | llm

    response = chain.invoke({
        "topic":topic,
        "audience":audience,
        "revision_hints":revision_hints
    })

    return response.content

# writer agent 

writer_prompt = ChatPromptTemplate([
    {"role": "system", "content": """
        You are a Blog Writer Agent. Using the research notes provided, write a complete
        engaging blog post.
        Rules:
        - Length: 500-800 words
        - Structure: catchy title, intro hook, 3-5 sections with H2 headings, conclusion
        - Tone: clear, friendly, suited to the target audience
        - Use markdown formatting
        - Do NOT add a 'word count' line at the end
    """},
    {"role": "user", "content": """
        Topic: {topic}
        Audience: {audience}
        Research Notes: {research}
        {revision_hints}
        Write the full blog post now.
    """}
])

def writer_agent(llm:ChatGroq ,topic:str ,audience: str ,feedback: str ="",research_notes: str =""):
    revision_hints = f"the human provided this feedback based on your previous reseach :{feedback}, based on this feedback make the changes in the blog "

    if not feedback:
        revision_hints =" this is your first attempt"

    chain = writer_prompt | llm

    response = chain.invoke({
        "topic":topic,
        "audience":audience,
        "research":research_notes,
        "revision_hints":revision_hints
    })

    return response.content

## editor agent 

editor_prompt = ChatPromptTemplate([
    {"role": "system", "content": """
        "You are an Editor Agent - the final quality gate before publishing. \n"
        "Take the draft and produce the FINAL polished version. Specifically: \n"
        "- Fix grammar, spelling, and awkward phrasing\n"
        "- Tighten wordy sentences\n"
        "- Improve flow and transitions between sections\n"
        "- Make the title and intro more compelling if needed\n"
        "- Keep the same structure and markdown formatting\n"
        "- Blog Wordings should look like human, not a AI, and don't use any special chars and complex / fancy words. \n"
        "Output only the final polished blog post - no commentary."""},
        {"role": "user",
        "content": """
        Topic: {topic},
        Draft: {draft},
        Return the published blog post."""}
])

def editor_agent(llm:ChatGroq ,topic:str ,draft: str =""):


    chain = editor_prompt | llm

    response = chain.invoke({
        "topic":topic,
        "draft":draft
    })

    return response.content