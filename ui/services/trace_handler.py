from langchain_core.callbacks import BaseCallbackHandler


class TraceHandler(BaseCallbackHandler):
    def __init__(self):
        self.events = []

    def on_tool_start(self, serialized, input_str, **kwargs):

        self.events.append(
            {
                "type": "tool_call",
                "tool": serialized.get(
                    "name",
                    "Unknown Tool"
                )
            }
        )

    def on_tool_end(self, output, **kwargs):
        self.events.append(
            {
                "type": "tool_result"
            }
        )