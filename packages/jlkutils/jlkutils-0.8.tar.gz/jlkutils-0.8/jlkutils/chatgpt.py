from openai import OpenAI
client = OpenAI()

def chatgpt(input):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": input
            }
        ]
    )

    return completion.choices[0].message.content