import os
from typing import TypedDict
from dotenv import load_dotenv

from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# 1. Define State
# This dict is the "memory" passed between nodes
class AgentState(TypedDict):
    topic: str
    research_notes: str
    final_blog_post: str

# 2. Initialize Model & Tools
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
search_tool = DuckDuckGoSearchRun()

# 3. Define Nodes ( The Workers )

def researcher_node(state: AgentState):
    """
    Worker 1: Takes the topic, searches for info, and summarizes findings.
    """
    topic = state["topic"]
    print(f"--- RESEARCHER: Searching for {topic} ---")
    
    # Simple search execution
    # In a real app, you might search multiple queries.
    search_results = search_tool.invoke(f"key facts and latest news about {topic}")
    
    # Ask Gemini to summarize the raw search data into clean notes
    prompt = ChatPromptTemplate.from_template(
        "You are a research assistant. Summarize the following raw search results about '{topic}' into 5 key bullet points: \n\n {data}"
    )
    chain = prompt | llm
    summary = chain.invoke({"topic": topic, "data": search_results})
    
    return {"research_notes": summary.content}

def writer_node(state: AgentState):
    """
    Worker 2: Takes the research notes and writes a blog post.
    """
    notes = state["research_notes"]
    topic = state["topic"]
    print(f"--- WRITER: Writing blog post on {topic} ---")
    
    prompt = ChatPromptTemplate.from_template(
        """You are a tech blogger. Write a short, engaging blog post (approx 200 words) based strictly on the following research notes.
        Use markdown formatting.
        
        Topic: {topic}
        Notes:
        {notes}
        """
    )
    chain = prompt | llm
    response = chain.invoke({"topic": topic, "notes": notes})
    
    return {"final_blog_post": response.content}

# 4. Build the Graph ( The Assembly Line )
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("researcher", researcher_node)
workflow.add_node("writer", writer_node)

# Add edges (First Research, Then Write)
workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", END)

# Compile
graph = workflow.compile()