"""
Simple AI agent using Groq (openai/gpt-oss-120b) with two tools:
  1. web_search  -> uses Tavily API
  2. calculate   -> evaluates basic math expressions safely

Setup:
  pip install groq tavily-python python-dotenv

.env file should contain:
  GROQ_API_KEY=your_groq_key
  TAVILY_API_KEY=your_tavily_key

Run:
  python agent.py
"""

import os
import json
import ast
import operator

from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found in environment (.env file)")
if not TAVILY_API_KEY:
    raise RuntimeError("TAVILY_API_KEY not found in environment (.env file)")

groq_client = Groq(api_key=GROQ_API_KEY)
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

MODEL = "openai/gpt-oss-120b"


# ---------------------------------------------------------------------------
# Tool 1: Web search (Tavily)
# ---------------------------------------------------------------------------

def web_search(query: str) -> str:
    """
    Searches the web using Tavily and returns a concise answer/summary.
    """
    try:
        response = tavily_client.search(
            query=query,
            search_depth="basic",
            include_answer=True,
        )

        # Tavily gives a direct synthesized answer when include_answer=True
        answer = response.get("answer")
        if answer:
            return answer

        # Fallback: stitch together top result snippets
        results = response.get("results", [])
        if not results:
            return "No results found."

        snippets = []
        for r in results[:3]:
            title = r.get("title", "")
            content = r.get("content", "")
            snippets.append(f"{title}: {content}")

        return "\n".join(snippets)

    except Exception as e:
        return f"Web search failed: {e}"


# ---------------------------------------------------------------------------
# Tool 2: Calculator (safe arithmetic expression evaluator)
# ---------------------------------------------------------------------------

# Only allow these operators - no function calls, no name access, no attribute
# access -> prevents arbitrary code execution via eval().
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _eval_node(node):
    if isinstance(node, ast.Constant):  # numbers
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric constants are allowed")

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Operator {op_type} not allowed")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Operator {op_type} not allowed")
        operand = _eval_node(node.operand)
        return _ALLOWED_OPERATORS[op_type](operand)

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")


def calculate(expression: str) -> str:
    """
    Safely evaluates a basic arithmetic expression string, e.g. "2*2", "(3+4)/7".
    Supports + - * / // % ** and parentheses. No names, calls, or attribute
    access are permitted, so it cannot execute arbitrary code.
    """
    try:
        parsed = ast.parse(expression, mode="eval")
        result = _eval_node(parsed.body)
        return str(result)
    except Exception as e:
        return f"Calculation failed: {e}"


# ---------------------------------------------------------------------------
# Tool schema (OpenAI/Groq function-calling format)
# ---------------------------------------------------------------------------

tools = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": (
                "Search the web for up-to-date information, facts, news, or "
                "anything that requires current/external knowledge. Use this "
                "when the answer is not something that can be computed."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to look up on the web.",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": (
                "Evaluate a basic arithmetic expression, e.g. '2*2', '(5+3)/2', "
                "'10 ** 2'. Use this whenever the user asks a math question."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A math expression to evaluate, e.g. '2*2'.",
                    }
                },
                "required": ["expression"],
            },
        },
    },
]

# Map tool name -> actual python function, used to dispatch calls
AVAILABLE_TOOLS = {
    "web_search": web_search,
    "calculate": calculate,
}


# ---------------------------------------------------------------------------
# Agent loop
# ---------------------------------------------------------------------------

def run_agent(user_query: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant with access to two tools: "
                "web_search (for factual/current info) and calculate (for "
                "arithmetic). Decide which tool (if any) to use based on the "
                "user's question, call it, and then answer clearly using the "
                "tool's result."
            ),
        },
        {"role": "user", "content": user_query},
    ]

    # Keep calling the model until it stops requesting tools (it may need
    # more than one round: e.g. call a tool, look at the result, call another
    # tool, then finally answer). Cap the number of rounds as a safety net.
    max_rounds = 5

    for round_num in range(1, max_rounds + 1):
        response = groq_client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if not tool_calls:
            # Model answered directly - guard against empty/None content
            return response_message.content or "(The model returned an empty response.)"

        # Append the assistant's tool-call message to the conversation
        messages.append(response_message)

        # Execute each requested tool call and append results
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            print(f"[round {round_num}] calling {function_name}({function_args})")

            function_to_call = AVAILABLE_TOOLS.get(function_name)
            if function_to_call is None:
                result = f"Error: unknown tool '{function_name}'"
            else:
                result = function_to_call(**function_args)

            print(f"[round {round_num}] {function_name} -> {str(result)[:200]}")

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": str(result),
                }
            )

    return "(Reached max tool-call rounds without a final answer.)"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    query = input("Enter your query: ")
    answer = run_agent(query)
    print("\nAnswer:\n" + answer)