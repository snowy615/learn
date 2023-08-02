import os
import openai
openai.api_key = os.getenv("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")

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)
print(completion.choices[0].message)





