from pydantic import BaseModel

class State(BaseModel):
    """
    State class to hold the state of the blog generator.
    """
    # user input
    topic : str =""
    audience : str ="general audience "

    #researcher output
    research : str =""
    research_feedback : str =""

    #writer output
    writer : str =""
    writer_feedback : str =""

    #final output
    final : str =""

    #metadata
    revision_count: int = 0
