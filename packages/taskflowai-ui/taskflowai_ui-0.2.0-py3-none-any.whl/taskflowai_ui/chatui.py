from __future__ import annotations
import streamlit as st
from typing import Dict, Any, List, Literal, Optional, Union
from taskflowai import Task
from pydantic.v1 import BaseModel, Field
import json

class ToolCall(BaseModel):
    tool: str
    params: Dict[str, Any] = Field(default_factory=dict)
    result: Union[str, Dict[str, Any], None] = None

class Message(BaseModel):
    role: Literal["user", "assistant"]
    type: Literal["text", "tool_call"] 
    content: Union[str, ToolCall]

class ChatState(BaseModel):
    messages: List[Message] = Field(default_factory=list)
    conversation_history: List[Dict[str, str]] = Field(default_factory=list)

    def add_message(self, role: Literal["user", "assistant"], msg_type: Literal["text", "tool_call"], content: Union[str, ToolCall]):
        message = Message(role=role, type=msg_type, content=content)
        self.messages.append(message)
        if msg_type == "text":
            self.conversation_history.append({
                "role": role.capitalize(),
                "content": content if isinstance(content, str) else content.tool
            })
        elif msg_type == "tool_call":
            self.conversation_history.append({
                "role": role.capitalize(),
                "content": f"Tool Call: {content.tool}"
            })

class Response(BaseModel):
    tool_calls: List[ToolCall] = Field(default_factory=list)
    content: Optional[str] = None
    error: Optional[str] = None

def render_tool_call(tool_call: ToolCall):
    with st.expander(f"🛠️ Tool Call: {tool_call.tool}", expanded=False):
        st.markdown("**Request**")
        st.markdown(f"**Tool:** `{tool_call.tool}`")
        if tool_call.params:
            st.markdown("**Parameters:**")
            st.json(tool_call.params)
        else:
            st.markdown("No parameters provided")
        
        st.markdown("\n**Result**")
        if isinstance(tool_call.result, str):
            st.text(tool_call.result)
        elif isinstance(tool_call.result, dict):
            st.json(tool_call.result)
        else:
            st.code(json.dumps(tool_call.result, indent=2, default=str), language="json")

def respond_task(agent, message, conversation_history, additional_instruction=None, callback=None):
    response = Response()
    error_reported = False

    def task_callback(result: Dict[str, Any]):
        nonlocal error_reported
        if result["type"] == "tool_call":
            tool_call = ToolCall(**result)
            response.tool_calls.append(tool_call)
            callback({"type": "tool_call", "content": tool_call})
        elif result["type"] == "final_response":
            response.content = result["content"]
            callback({"type": "text", "content": result["content"]})
        elif result["type"] == "error" and not error_reported:
            response.error = result["content"]
            callback({"type": "text", "content": f"Error: {result['content']}"})
            error_reported = True

    context = "Conversation History: " + "\n".join([f"{entry['role']}: {entry['content']}" for entry in conversation_history]) + "\n---------\n"
    if additional_instruction:
        additional_instruction = additional_instruction + "\n\n"
        instruction = f"{additional_instruction}Now respond to the user message: {message}"
    else:
        instruction = f"Now respond to the user message: {message}"

    result = Task.create(
        agent=agent,
        context=context,
        instruction=instruction,
        callback=task_callback
    )

    if isinstance(result, Exception) and not error_reported:
        response.error = str(result)
        callback({"type": "text", "content": f"Error: {str(result)}"})
        error_reported = True
    elif not response.content and not response.error:
        response.content = result if isinstance(result, str) else str(result)

    return response

class ChatUI:
    def __init__(self, title: str, agent: Any, additional_instruction: Optional[str] = None):
        self.title = title
        self.agent = agent
        self.additional_instruction = additional_instruction
        if "chat_state" not in st.session_state:
            st.session_state.chat_state = ChatState()
        self.header_container = st.container()
        self.chat_container = st.container()
        self.spinner_container = st.empty()
        self.input_container = st.container()
        self.message_placeholders = []
        self.spinner_placeholder = st.empty()

    def render(self):
        with self.header_container:
            st.title(self.title)
            if st.button("Clear Chat"):
                st.session_state.chat_state = ChatState()
                self._clear_messages()
                st.rerun()

        self._render_new_messages()
        self._handle_user_input()

    def add_message(self, role: Literal["user", "assistant"], msg_type: Literal["text", "tool_call"], content: Union[str, ToolCall]):
        st.session_state.chat_state.add_message(role, msg_type, content)
        with self.chat_container:
            with st.chat_message(role):
                if msg_type == "text":
                    st.markdown(content)
                elif msg_type == "tool_call":
                    render_tool_call(content)

    def _render_new_messages(self):
        with self.chat_container:
            for idx, message in enumerate(st.session_state.chat_state.messages):
                if idx >= len(self.message_placeholders):
                    self.message_placeholders.append(st.empty())
                
                with self.message_placeholders[idx].container():
                    with st.chat_message(message.role):
                        if message.type == "text":
                            st.markdown(message.content)
                        elif message.type == "tool_call":
                            render_tool_call(message.content)

    def _handle_user_input(self):
        if prompt := st.chat_input("Type your message here..."):
            self.add_message("user", "text", prompt)

            with self.chat_container:
                with self.spinner_placeholder.container():
                    with st.spinner("Thinking..."):
                        response = respond_task(
                            self.agent,
                            prompt,
                            st.session_state.chat_state.conversation_history,
                            additional_instruction=self.additional_instruction,  # Pass the additional_instruction
                            callback=lambda result: self.add_message(
                                "assistant",
                                result["type"],
                                result["content"]
                            )
                        )

            self.spinner_placeholder.empty()

    def _clear_messages(self):
        for placeholder in self.message_placeholders:
            placeholder.empty()
        self.message_placeholders = []

def create_chat_ui(title: str, agent: Any, additional_instruction: Optional[str] = None) -> ChatUI:
    chatui = ChatUI(title, agent, additional_instruction)  # Pass the additional_instruction to ChatUI
    chatui.render()
    return chatui