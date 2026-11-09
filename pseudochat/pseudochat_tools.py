"""
Tool handlers for the PseudoChat use case.

Handlers are plain functions: they read and write the shared
agent state (data) and use engine services (context) - the
LLM, the config, and context.stop() to end the loop.
"""

import json

from pseudoagent.pseudoagent_tools_helper import extract_tool_call_arguments


def get_user_input(data, params, context):
    """
    Block on the user and store their message in
    data["user_input"]. exit / quit (or Ctrl+C / EOF) stops
    the loop.
    """

    try:
        text = input("You: ").strip()

    except (KeyboardInterrupt, EOFError):
        context.stop("user ended the chat")

    if text.lower() in {"exit", "quit"}:
        context.stop("user ended the chat")

    data["user_input"] = text

    return f"GET_USER_INPUT: {text}"


def respond(data, params, context):
    """
    Generate and print the reply to the pending user message,
    built from the persona and the profile.
    """

    user_text = data.get("user_input") or ""

    profile = data.get("profile") or {}

    prompt = f"""
        {data.get("persona", "")}
        
        What you know about the user:
        {json.dumps(profile, indent=4)}
        
        The user's latest message:
        {user_text}
        
        Write the reply to the user's latest message. Let the
        knowledge about the user shape the tone and content, but
        return only the reply.
    """

    reply = context.llm.generate(prompt).strip()

    print()
    print(f"PseudoAgent: {reply}")
    print()

    data["ai_response"] = reply

    return reply


def digest(data, context):
    """
    Have the LLM update the profile from the latest exchange
    (user_input + ai_response), store the parsed result, and
    clear the pending user_input / ai_response.
    """

    llm = context.llm

    user_input = data["user_input"]
    ai_response = data["ai_response"]

    if user_input and ai_response:

        print("Digesting this ...")
        print(json.dumps(data, indent= 4))

        prompt = f"""
        
            Here is the data: 
            {json.dumps(data, indent= 4)}
            
            Based on 'user_input' and 'ai_response' update all the fields in the 'profile':
            update 'user_sentiment'
            update 'feelings
            update 'preferences
            update 'open_goals
            update 'facts
            update 'relationship
            
            Print the updated data in json format. Only print the json, nothing else. Do not print your thought process or thinking. Just print the output which is a json. 
             
        
        """

        dgst = llm.generate(prompt)

        dgst_dict = json.loads(dgst)
        print(json.dumps(dgst_dict, indent=4))

        data['profile'] = dgst_dict["profile"]

        data["ai_response"] = None
        data["user_input"] = None

        print("to this ...")
        print(json.dumps(data, indent= 4))





