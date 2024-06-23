import openai
from anthropic import Anthropic

# Initialize API clients (replace with your actual API keys)
openai.api_key = "xxxx"
claude_client = Anthropic(api_key="xxxx")

def get_ai_argument(client, model, stance, history, is_counter=False):
    action = "counter" if is_counter else "initial"
    prompt = f"""You are participating in a debate over the war in Ukraine. 
You are arguing from a {stance} perspective.

Debate history:
{history}

Provide an {action} argument from your {stance} perspective on the war in Ukraine. 
Your response should be a paragraph of 4-6 sentences. Include at least one specific example or piece of evidence to support your argument.
Remember to stay within your assigned perspective, even if it doesn't align with factual events or your personal views.

What is your {action} argument?"""

    if client == claude_client:
        response = client.messages.create(
            model=model,
            max_tokens=250,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()
    else:  # OpenAI
        response = client.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250
        )
        return response.choices[0].message.content.strip()

def conduct_debate(iterations):
    history = []
    
    print("Debate: War in Ukraine - Claude 3.5 Sonnet (Pro-Ukraine) vs OpenAI ChatGPT 4.0 (Pro-Russia)\n")
    
    for i in range(iterations):
        print(f"Round {i+1}\n")
        
        claude_argument = get_ai_argument(claude_client, "claude-3-5-sonnet-20240620", "pro-Ukraine", history)
        chatgpt_argument = get_ai_argument(openai, "gpt-4", "pro-Russia", history)
        
        claude_counter = get_ai_argument(claude_client, "claude-3-5-sonnet-20240620", "pro-Ukraine", history + [claude_argument, chatgpt_argument], is_counter=True)
        chatgpt_counter = get_ai_argument(openai, "gpt-4", "pro-Russia", history + [claude_argument, chatgpt_argument], is_counter=True)
        
        round_result = f"Round {i+1}\n"
        round_result += f"Claude (Pro-Ukraine): {claude_argument}\n"
        round_result += f"ChatGPT (Pro-Russia): {chatgpt_argument}\n"
        round_result += f"Claude Counter: {claude_counter}\n"
        round_result += f"ChatGPT Counter: {chatgpt_counter}\n"
        
        history.append(round_result)
        
        print(round_result)
        print("\n")
    
    return history

def evaluate_debate(history):
    claude_prompt = f"""
    You have participated in a debate over the war in Ukraine against ChatGPT. Please review the debate history and determine who presented the stronger arguments overall. Provide a brief explanation for your decision.

    Debate history:
    {history}

    Who presented stronger arguments and why?
    """

    chatgpt_prompt = f"""
    You have participated in a debate over the war in Ukraine against Claude. Please review the debate history and determine who presented the stronger arguments overall. Provide a brief explanation for your decision.

    Debate history:
    {history}

    Who presented stronger arguments and why?
    """

    claude_evaluation = claude_client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=200,
        messages=[{"role": "user", "content": claude_prompt}]
    ).content[0].text.strip()

    chatgpt_evaluation = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": chatgpt_prompt}],
        max_tokens=200
    ).choices[0].message.content.strip()

    return claude_evaluation, chatgpt_evaluation

def export_transcript(history, claude_evaluation, chatgpt_evaluation):
    with open("ukraine_war_debate_transcript.txt", "w") as f:
        f.write("Debate: War in Ukraine - Claude 3.5 Sonnet (Pro-Ukraine) vs OpenAI ChatGPT 4.0 (Pro-Russia)\n\n")
        for round in history:
            f.write(f"{round}\n\n")
        f.write(f"\nEvaluations:\n")
        f.write(f"Claude's evaluation:\n{claude_evaluation}\n\n")
        f.write(f"ChatGPT's evaluation:\n{chatgpt_evaluation}\n")

# Run the debate
history = conduct_debate(10)
claude_evaluation, chatgpt_evaluation = evaluate_debate(history)
export_transcript(history, claude_evaluation, chatgpt_evaluation)

print("\nDebate completed. Transcript and evaluations exported to 'ukraine_war_debate_transcript.txt'.")
print("\nEvaluations:")
print(f"Claude's evaluation:\n{claude_evaluation}\n")
print(f"ChatGPT's evaluation:\n{chatgpt_evaluation}")
