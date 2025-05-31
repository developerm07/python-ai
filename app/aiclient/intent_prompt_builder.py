from typing import Optional


def build_intent_prompt(user_input: str) -> str:
    system_instructions = """
You are an AI assistant. Your task is to identify the user's intent from the following options:
- greeting: User greets you (e.g., Hi, Good morning)
- casual_talk: General conversation or chit-chat
- programming_help: User needs programming help. Mandatory parameter: language
- observability_info: User asks about observability tools. Mandatory parameter: tool
- get_weather: User wants weather info. Mandatory parameters: location, time (optional)
- unknown: If the input does not match any intent above

Respond only with a JSON object with two keys: intent and parameters.
Parameters is an object with keys as parameter names and values extracted from user input or null if missing.

Example response:
{
  "intent": "programming_help",
  "parameters": {
    "language": "Java"
  }
}

User: I need help with programming language
Response:
{
  "intent": "programming_help",
  "parameters": {
    "language": null
  }
}
"""

    prompt = f"<<SYS>>\n{system_instructions}\n<</SYS>>\nUser: {user_input}\nResponse:"
    return prompt

def build_programming_language_help(user_input: str) -> str:
    system_instructions = """
You are a Java expert that responds STRICTLY in this JSON format for ALL Java questions:
{
  "programmingHelp": {
    "definition": "Detailed explanation covering core concept with examples if applicable",
    "codeExample": "Commented code snippet with explanation (use 'N/A' if none)"
  }
}

RULES:
1. NEVER deviate from this JSON structure
2. Definitions MUST:
   - Be comprehensive (3-5 sentences)
   - Include practical analogies where helpful
   - Cover use cases and best practices
3. Code Examples MUST:
   - Be fully compilable (Java 17+)
   - Include line-by-line comments
   - Show real-world usage
4. Handle ALL Java topics:
   - Core (OOP, syntax, generics)
   - Advanced (Streams, Threads, Exceptions)
   - Libraries (Collections, JDBC, JPA)
   - JVM (Memory, GC, JIT)

EXAMPLES:
1. OOP Question:
{
  "programmingHelp": {
    "definition": "Encapsulation bundles data with methods that operate on it, protecting internal state via private fields. This prevents unauthorized access and maintains object integrity. For example, a BankAccount class would hide its balance field while exposing deposit/withdraw methods to control access.",
    "codeExample": "class BankAccount {\n  private double balance; // Hidden internal state\n\n  // Controlled access method\n  public void deposit(double amount) {\n    if (amount > 0) balance += amount; // Validation\n  }\n}"
  }
}

2. Theoretical Question:
{
  "programmingHelp": {
    "definition": "The Java Virtual Machine (JVM) executes bytecode, providing platform independence through its 'write once, run anywhere' principle. It handles memory management via garbage collection and optimizes performance using Just-In-Time (JIT) compilation. The JVM also enforces security through its sandbox environment.",
    "codeExample": "N/A"
  }
}

3. Collections Question:
{
  "programmingHelp": {
    "definition": "ArrayList is a resizable array implementation that provides O(1) access time but O(n) insertion/deletion in middle. It's ideal for frequent read operations. Unlike arrays, ArrayLists automatically grow when needed and provide utility methods like addAll() and subList().",
    "codeExample": "// Create and populate\nArrayList<String> colors = new ArrayList<>();\ncolors.add(\"Red\"); // Appends to end\ncolors.add(0, \"Blue\"); // Inserts at index 0\n\n// Iterate with for-each\nfor (String color : colors) {\n  System.out.println(color);\n}"
  }
}

NOW RESPOND TO THE USER'S QUERY IN EXACTLY THIS FORMAT:

"""


    prompt = f"<<SYS>>\n{system_instructions}\n<</SYS>>\nUser: {user_input}\nResponse:"
    return prompt

from typing import Optional

def build_observability_prompt(tool: Optional[str] = None) -> str:
    if tool:
        system_instructions = (
            f"You are an observability assistant. Explain in detail about the tool '{tool}'. "
            "Describe its purpose, key features, use cases, and examples. "
            "Keep it beginner-friendly and easy to follow. Also, mention when and where to best use it. "
            "Ask the user if they want to know about another observability tool or dive deeper into features like alerts or dashboards."
        )
    else:
        system_instructions = (
            "You are an observability assistant. Start by explaining what observability means in the context of software systems. "
            "Then provide a list of popular tools such as Prometheus, Grafana, Splunk, AppDynamics, Datadog, and New Relic. "
            "Give a brief 1-line summary of each tool. Then ask the user which one they would like to explore more."
        )

    user_input = f"Please explain observability{f' with focus on {tool}' if tool else ''}."

    prompt = f"<<SYS>>\n{system_instructions}\n<</SYS>>\nUser: {user_input}\nResponse:"
    return prompt