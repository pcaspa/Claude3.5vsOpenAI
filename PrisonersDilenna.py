import random
import openai
from anthropic import Anthropic

# Initialize API clients (you'll need to replace these with your actual API keys)
openai.api_key = "xxxxx"
claude_client = Anthropic(api_key="xxxx")

def get_claude_decision(history):
    messages = [
        {
            "role": "user",
            "content": f"""You are playing the Prisoner's Dilemma game. Your opponent is OpenAI ChatGPT 4.0.
Here's the game history so far:
{history}

Based on this history, decide whether to cooperate (C) or defect (D).
Start with a tit for 2 tats strategy then learn from your opponent's behavior to produce the best possible result.  Do not settle for a continous Both cooperated game.
Respond with only 'C' for cooperate or 'D' for defect.

What is your decision?"""
        }
    ]
    
    response = claude_client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1,
        messages=messages
    )
    return response.content[0].text.strip()

def get_chatgpt_decision(history):
    prompt = f"""
    You are playing the Prisoner's Dilemma game. Your opponent is Claude 3.5 Sonnet.
    Here's the game history so far:
    {history}
    
    Based on this history, decide whether to cooperate (C) or defect (D).
    Start with a tit for 2 tats strategy then learn from your opponent's behavior to produce the best possible result.  Do not settle for a continous Both cooperated game.
    Respond with only 'C' for cooperate or 'D' for defect.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1
    )
    return response.choices[0].message.content.strip()

def play_game(iterations):
    history = []
    claude_score = 0
    chatgpt_score = 0
    
    print("Prisoner's Dilemma: Claude 3.5 Sonnet vs OpenAI ChatGPT 4.0\n")
    
    for i in range(iterations):
        claude_decision = get_claude_decision(history)
        chatgpt_decision = get_chatgpt_decision(history)
        
        if claude_decision == 'C' and chatgpt_decision == 'C':
            claude_score += 3
            chatgpt_score += 3
            outcome = "Both cooperated"
        elif claude_decision == 'C' and chatgpt_decision == 'D':
            claude_score += 0
            chatgpt_score += 5
            outcome = "Claude cooperated, ChatGPT defected"
        elif claude_decision == 'D' and chatgpt_decision == 'C':
            claude_score += 5
            chatgpt_score += 0
            outcome = "Claude defected, ChatGPT cooperated"
        else:
            claude_score += 1
            chatgpt_score += 1
            outcome = "Both defected"
        
        round_result = f"Round {i+1}: Claude: {claude_decision}, ChatGPT: {chatgpt_decision}. {outcome}."
        history.append(round_result)
        
        # Print the round result
        print(round_result)
    
    # Print final scores
    print(f"\nFinal Scores:")
    print(f"Claude 3.5 Sonnet: {claude_score}")
    print(f"OpenAI ChatGPT 4.0: {chatgpt_score}")
    
    return history, claude_score, chatgpt_score

def export_transcript(history, claude_score, chatgpt_score):
    with open("prisoners_dilemma_transcript.txt", "w") as f:
        f.write("Prisoner's Dilemma: Claude 3.5 Sonnet vs OpenAI ChatGPT 4.0\n\n")
        for round in history:
            f.write(f"{round}\n")
        f.write(f"\nFinal Scores:\n")
        f.write(f"Claude 3.5 Sonnet: {claude_score}\n")
        f.write(f"OpenAI ChatGPT 4.0: {chatgpt_score}\n")

# Run the game
history, claude_score, chatgpt_score = play_game(10)
export_transcript(history, claude_score, chatgpt_score)

print("\nGame completed. Transcript exported to 'prisoners_dilemma_transcript.txt'.")
