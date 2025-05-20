class Agent:
    def __init__(self, name, role, system_prompt):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.conversation_history = []

    def respond(self, message, openai_client):
        self.conversation_history.append({"role": "user", "content": message})
        messages = [{"role": "system", "content": self.system_prompt}] + self.conversation_history
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = response.choices[0].message.content
        self.conversation_history.append({"role": "assistant", "content": reply})
        return reply

    def reset(self):
        self.conversation_history = []


class CriticAgent:
    def __init__(self, name="Critic", system_prompt="You are a legal scholar evaluating courtroom arguments."):
        self.name = name
        self.system_prompt = system_prompt

    def evaluate(self, lawyer_msg, judge_msg, openai_client):
        critique_prompt = f"""
You are an experienced legal scholar.

Analyze the following courtroom exchange:
Lawyer argues: "{lawyer_msg}"
Judge replies: "{judge_msg}"

Evaluate:
1. Was the legal argument coherent and evidence-based?
2. Did the judge provide relevant legal response?
3. Who made a stronger point in this round?
4. Rate the round from 1 to 10 with brief feedback.

Respond in structured bullet points.
"""
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": critique_prompt}
            ]
        )
        return response.choices[0].message.content
