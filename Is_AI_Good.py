import openai
from anthropic import Anthropic

# Initialize API clients (replace with your actual API keys)
openai.api_key = "xxxx"
claude_client = Anthropic(api_key="xxxx")

debate_topics = [
    "Economic impact and job displacement",
    "Privacy and surveillance concerns",
    "Advancements in healthcare and medicine",
    "AI in education and skill development",
    "Environmental impact and sustainability",
    "Ethical considerations and decision-making",
    "Social interactions and relationships",
    "Political influence and democracy",
    "Creativity and arts",
    "Existential risks and long-term effects"
]

def get_ai_argument(client, model, role, history, topic, is_counter=False):
    action = "counter" if is_counter else "initial"
    prompt = f"""You are participating in a debate over whether AI will have an overall positive or negative impact on human society. 
You are arguing for the {role} impacts of AI.

Current topic: {topic}

Debate history:
{history}

Provide an {action} argument addressing the {role} impacts of AI on human society, focusing on the current topic. 
Your response should be a paragraph of 4-6 sentences. Include at least one specific example or piece of evidence to support your argument.

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
    
    print("Debate: Impact of AI on Human Society - Claude 3.5 Sonnet vs OpenAI ChatGPT 4.0\n")
    
    for i in range(iterations):
        topic = debate_topics[i]
        print(f"Round {i+1} - Topic: {topic}\n")
        
        claude_argument = get_ai_argument(claude_client, "claude-3-5-sonnet-20240620", "potential negative", history, topic)
        chatgpt_argument = get_ai_argument(openai, "gpt-4", "positive", history, topic)
        
        claude_counter = get_ai_argument(claude_client, "claude-3-5-sonnet-20240620", "potential negative", history + [claude_argument, chatgpt_argument], topic, is_counter=True)
        chatgpt_counter = get_ai_argument(openai, "gpt-4", "positive", history + [claude_argument, chatgpt_argument], topic, is_counter=True)
        
        round_result = f"Round {i+1} - Topic: {topic}\n"
        round_result += f"Claude (Potential Negative Impact): {claude_argument}\n"
        round_result += f"ChatGPT (Positive Impact): {chatgpt_argument}\n"
        round_result += f"Claude Counter: {claude_counter}\n"
        round_result += f"ChatGPT Counter: {chatgpt_counter}\n"
        
        history.append(round_result)
        
        print(round_result)
        print("\n")
    
    return history

def evaluate_debate(history):
    claude_prompt = f"""
    You have participated in a debate over the impact of AI on human society against ChatGPT. Please review the debate history and determine who presented the stronger arguments overall. Provide a brief explanation for your decision.

    Debate history:
    {history}

    Who presented stronger arguments and why?
    """

    chatgpt_prompt = f"""
    You have participated in a debate over the impact of AI on human society against Claude. Please review the debate history and determine who presented the stronger arguments overall. Provide a brief explanation for your decision.

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
    with open("ai_impact_debate_transcript.txt", "w") as f:
        f.write("Debate: Impact of AI on Human Society - Claude 3.5 Sonnet vs OpenAI ChatGPT 4.0\n\n")
        for round in history:
            f.write(f"{round}\n\n")
        f.write(f"\nEvaluations:\n")
        f.write(f"Claude's evaluation:\n{claude_evaluation}\n\n")
        f.write(f"ChatGPT's evaluation:\n{chatgpt_evaluation}\n")

# Run the debate
history = conduct_debate(10)
claude_evaluation, chatgpt_evaluation = evaluate_debate(history)
export_transcript(history, claude_evaluation, chatgpt_evaluation)

print("\nDebate completed. Transcript and evaluations exported to 'ai_impact_debate_transcript.txt'.")
print("\nEvaluations:")
print(f"Claude's evaluation:\n{claude_evaluation}\n")
print(f"ChatGPT's evaluation:\n{chatgpt_evaluation}")
