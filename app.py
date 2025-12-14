import streamlit as st
from agent_graph import graph  # Import the graph we just built

st.set_page_config(page_title="AI Researcher", layout="wide")

st.title("🤖 Gemini Structured Researcher")
st.markdown("This agent performs two distinct steps: **Research** -> **Writing**.")

# Input Section
topic = st.text_input("Enter a topic to research:", placeholder="e.g., The future of Quantum Computing")

if st.button("Start Research & Write"):
    if not topic:
        st.warning("Please enter a topic first.")
    else:
        # Create columns for live visualization
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🕵️ Step 1: Researching")
            status_box = st.status("Agent is working...", expanded=True)
            
            # Run the Graph
            # We initialize the state with the user's topic
            initial_state = {"topic": topic}
            
            # Using .invoke() runs the whole chain
            # For complex apps, you can use .stream() to see steps live
            result = graph.invoke(initial_state)
            
            status_box.update(label="Research Complete!", state="complete", expanded=False)
            st.info("Gathered Notes:")
            st.markdown(result["research_notes"])

        with col2:
            st.subheader("✍️ Step 2: Final Article")
            st.success("Draft Generated:")
            st.markdown(result["final_blog_post"])