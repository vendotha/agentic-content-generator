import os
import traceback  # We'll leave this for safety
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.prompts import ChatPromptTemplate
# --- IMPORT CHANGES ---
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub  # We need this to pull the agent's prompt


# --- END IMPORT CHANGES ---

def create_blog_agent():
    """Initializes and returns the blog generation agent using Gemini."""

    # 1. Load .env file
    load_dotenv()
    if not os.getenv("GOOGLE_API_KEY"):
        raise EnvironmentError("GOOGLE_API_KEY not found in .env file.")

    # 2. Initialize the Gemini LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
        convert_system_message_to_human=True
    )

    # 3. Define the tools
    search_tool = DuckDuckGoSearchRun()
    wiki_api = WikipediaAPIWrapper()
    wiki_tool = WikipediaQueryRun(api_wrapper=wiki_api)
    tools = [search_tool, wiki_tool]

    # --- AGENT PROMPT CHANGES ---
    # 4. Get the ReAct prompt template
    # This is a pre-built prompt designed to make models "think" step-by-step
    prompt = hub.pull("hwchase17/react")

    # 5. Modify the prompt template
    # We will prepend our detailed blog writing instructions to the
    # existing ReAct prompt, which provides the Thought/Action/Observation
    # framework.
    blog_instructions = """
    **YOUR PRIMARY GOAL:** You are an expert content creator and professional blog writer.
    Your task is to generate a high-quality, well-structured, and engaging 
    blog post on the user's given "Question".

    You must use your tools (DuckDuckGo Search and Wikipedia) to conduct 
    thorough research.

    **FINAL ANSWER FORMAT:**
    When you have gathered enough information, you MUST stop using tools and provide your
    "Final Answer". This answer *must* be a complete blog post, formatted 
    exactly as shown below using Markdown. Do not add any other text around it.

    # [Blog Post Heading: Your Engaging Title Here]

    ## Introduction
    [Your engaging introduction here. It should be 1-2 paragraphs, hook the 
    reader, and state the blog's purpose.]

    ## Content
    [Your detailed, informative content here. This should be the main body, 
    supported by facts from your research. Use paragraphs, and if appropriate, 
    bullet points. It should be well-researched and comprehensive.]

    ## Summary
    [Your concise summary here. It should be one paragraph and recap the 
    main points of the blog.]

    ---
    **AGENT FRAMEWORK INSTRUCTIONS (Follow these for your thoughts):**
    """

    # Prepend our new instructions to the existing template
    prompt.template = blog_instructions + "\n" + prompt.template
    # --- END AGENT PROMPT CHANGES ---

    # 6. Create the Agent
    # We now use create_react_agent
    agent = create_react_agent(llm, tools, prompt)

    # 7. Create the Agent Executor (This part is identical and verbose=True works!)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True
    )

    return agent_executor


def main():
    """Main function to run the blog generation."""
    try:
        agent_executor = create_blog_agent()

        # Get topic from user
        topic = input("Enter the blog topic: ")

        if not topic:
            print("No topic provided. Exiting.")
            return

        print(f"\nGenerating blog on: '{topic}'... This may take a moment.\n")

        # Invoke the agent
        response = agent_executor.invoke({"input": topic})

        # Extract and print the final output
        final_blog_post = response['output']

        print("\n--- Generated Blog Post ---")
        print(final_blog_post)
        print("---------------------------\n")

        # Save the output to a file
        output_filename = "blog_output.md"
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(final_blog_post)

        print(f"Blog post saved to {output_filename}")

    except EnvironmentError as e:
        print(f"Error: {e}")
    except Exception as e:
        # We'll keep the full traceback just in case
        print(f"An unexpected error occurred. Printing full traceback:")
        traceback.print_exc()


if __name__ == "__main__":
    main()