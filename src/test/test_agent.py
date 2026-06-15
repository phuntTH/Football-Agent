import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from langchain_core.messages import (
    AIMessage,
    ToolMessage
)

from agent.simple_agent import agent


THREAD_ID = "user_1"


# =====================================================
# EXTRACT TEXT
# =====================================================

def extract_text(content):

    if isinstance(content, str):
        return content

    if isinstance(content, list):

        texts = []

        for item in content:

            if isinstance(item, dict):

                texts.append(
                    item.get(
                        "text",
                        ""
                    )
                )

            else:
                texts.append(str(item))

        return "\n".join(texts)

    return str(content)


# =====================================================
# SOURCES
# =====================================================

def print_sources(messages):

    urls = set()

    for msg in messages:

        if not isinstance(msg, ToolMessage):
            continue

        artifact = getattr(
            msg,
            "artifact",
            None
        )

        if not artifact:
            continue

        results = artifact.get(
            "results",
            []
        )

        for item in results:

            url = item.get("url")

            if url:
                urls.add(url)

    if not urls:
        return

    print("\n📚 SOURCES")

    for url in sorted(urls):

        print(f"- {url}")


# =====================================================
# TOOL CALLS
# =====================================================

def print_tool_calls(messages):

    found = False

    for msg in messages:

        if (
            isinstance(msg, AIMessage)
            and msg.tool_calls
        ):

            if not found:

                print("\n🔧 TOOL CALLS")
                found = True

            for tool in msg.tool_calls:

                print(
                    f"- {tool['name']}"
                )

                if tool.get("args"):

                    print(
                        f"  Args: {tool['args']}"
                    )


# =====================================================
# TOOL RESULTS
# =====================================================

def print_tool_results(messages):

    found = False

    for msg in messages:

        if not isinstance(msg, ToolMessage):
            continue

        if not found:

            print("\n🛠 TOOL RESULTS")
            found = True

        print(f"\nTool: {msg.name}")

        content = str(msg.content)

        if len(content) > 500:

            content = (
                content[:500]
                + "\n...(truncated)"
            )

        print(content)


# =====================================================
# CHAT
# =====================================================

def chat():

    config = {
        "configurable": {
            "thread_id": THREAD_ID
        }
    }

    print("=" * 100)
    print("FOOTBALL AGENT")
    print("Type 'exit' to quit")
    print("=" * 100)

    while True:

        question = input("\nUSER: ")

        if question.lower() == "exit":
            break

        result = agent.invoke(
            {
                "messages": [
                    (
                        "human",
                        question
                    )
                ]
            },
            config=config
        )

        messages = result["messages"]

        print("\n")
        print("=" * 100)
        print("AGENT TRACE")
        print("=" * 100)

        # --------------------------------------------------
        # ROUTE
        # --------------------------------------------------

        route = result.get(
            "route",
            "unknown"
        )

        print(
            f"\n🧭 ROUTE: {route}"
        )

        # --------------------------------------------------
        # TOOL CALLS
        # --------------------------------------------------

        print_tool_calls(messages)

        # --------------------------------------------------
        # TOOL RESULTS
        # --------------------------------------------------

        print_tool_results(messages)

        # --------------------------------------------------
        # MEMORY
        # --------------------------------------------------

        print(
            f"\n💾 MEMORY SIZE: {len(messages)}"
        )

        # --------------------------------------------------
        # SUMMARY
        # --------------------------------------------------

        summary = result.get(
            "summary",
            ""
        )

        if summary:

            print("\n📝 SUMMARY")

            print(
                summary[:500]
            )

        # --------------------------------------------------
        # FINAL ANSWER
        # --------------------------------------------------

        print("\n")
        print("=" * 100)
        print("FINAL ANSWER")
        print("=" * 100)

        final_answer = extract_text(
            messages[-1].content
        )

        print(final_answer)

        # --------------------------------------------------
        # SOURCES
        # --------------------------------------------------

        print_sources(messages)

        print("\n")


if __name__ == "__main__":

    chat()