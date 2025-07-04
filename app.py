import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters
import os

# Create a StdioServerParameters object
server_params=StdioServerParameters(
    command="python", 
    args=["servers/serper_search.py"],
    env={"UV_PYTHON": "3.12", **os.environ},
)


llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.5,
    verbose=True
)

st.title(" 🤖 Crew AI Agent")
st.markdown("### Blog post generation agents")
st.markdown("---")

Topic = st.text_input("Enter the topic for the blog post:", placeholder="e.g., AI in Healthcare")


with MCPServerAdapter(server_params) as tools:
    print(f"Available tools from Stdio MCP server: {[tool.name for tool in tools]}")

    # Example: Using the tools from the Stdio MCP server in a CrewAI Agent
    researcher = Agent(
        role="Google Researcher",
        goal="Research {topic} data using a local Stdio-based tool.",
        backstory="An AI that leverages local scripts via MCP for specialized tasks.",
        llm=llm,
        tools=tools,
        reasoning=True,
        verbose=True,
    )
    writer = Agent(
        role="Blog Writer",
        goal='Narrate compelling tech stories about {topic}',
        backstory="An Specialist in writing blog posts about technology.",
        llm=llm,
        reasoning=True,
        verbose=True,
    )
    
    research_task = Task(
        description=("Identify the next big trend in {topic}."
        "Focus on identifying pros and cons and the overall narrative."
        "Your final report should clearly articulate the key points,"
        "its market opportunities, and potential risks."),
        expected_output='A comprehensive 4 paragraphs long report based on the {topic}, including key points, insights, and any relevant details that would be useful for writing a blog post.',
        agent=researcher,
        markdown=True
    )

    writing_task = Task(
        description=(
            "Compose an insightful article based on the research findings of the research agent."
        ),
        expected_output='A well-structured blog post that effectively communicates the key points and insights from the research findings of the research agent, with Proper heading and subheadings, and a conclusion, tailored for an audience interested in technology.',
        context=[research_task],
        agent=writer,
        markdown=True,
        output_file='blog_post.md'
    )
    
    crew = Crew(
        agents=[researcher,writer],
        tasks=[research_task,writing_task],
        verbose=True,
        process=Process.sequential 
    )

if Topic:
        with st.spinner("Researching..."):
            result=crew.kickoff(inputs={'topic':Topic})

        with st.spinner("Generating blog post..."):
            st.markdown("### Generated Blog Post")
            with open('blog_post.md', 'r', encoding='utf-8') as f:
                blog_content = f.read()
            st.markdown(blog_content)

# if Topic:
    
#     crew=Crew(
#     agents=[researcher,writer],
#     tasks=[research_task,write_task],
#     process=Process.sequential,
#     )
#     with st.spinner("Researching..."):
#         result=crew.kickoff(inputs={'topic':Topic})

#     with st.spinner("Generating blog post..."):
#         st.markdown("### Generated Blog Post")
#         with open('blog_post.md', 'r', encoding='utf-8') as f:
#             blog_content = f.read()
#         st.markdown(blog_content)
