import os
import sys

ROOT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

sys.path.append(ROOT_DIR)
sys.path.append(
    os.path.join(
        ROOT_DIR,
        "src"
    )
)

from agent.graph import graph

from langchain_core.messages import AIMessage

from ui.services.trace_handler import TraceHandler


class AgentService:

    @staticmethod
    def extract_text(content):

        if not content:
            return ""

        if isinstance(
            content,
            str
        ):
            return content

        if isinstance(
            content,
            list
        ):

            parts = []

            for item in content:

                if isinstance(
                    item,
                    str
                ):

                    parts.append(item)

                elif isinstance(
                    item,
                    dict
                ):

                    parts.append(
                        item.get(
                            "text",
                            ""
                        )
                    )

                elif hasattr(
                    item,
                    "text"
                ):

                    parts.append(
                        item.text
                    )

            return "".join(parts)

        return str(content)

    @staticmethod
    async def stream_chat(
        question: str,
        thread_id: str
    ):

        trace = TraceHandler()

        config = {
            "configurable": {
                "thread_id": thread_id
            },
            "callbacks": [
                trace
            ]
        }

        result = await graph.ainvoke(

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

        # ==========================
        # TOOL TRACE
        # ==========================

        for e in trace.events:

            yield e

        # ==========================
        # FINAL ANSWER
        # ==========================

        final_answer = ""

        for msg in reversed(
            result["messages"]
        ):

            if isinstance(
                msg,
                AIMessage
            ):

                final_answer = (
                    AgentService.extract_text(
                        msg.content
                    )
                )

                break

        yield {
            "type": "answer",
            "content": final_answer
        }

        yield {
            "type": "done"
        }