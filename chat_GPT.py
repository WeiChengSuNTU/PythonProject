import openai

def GPT_func(api_key, prompt):
    try:
        openai.api_key = api_key
        model_engine = "text-davinci-003"

        response = openai.Completion.create(engine = model_engine, 
                                            prompt = prompt, 
                                            max_tokens = 1024,
                                            temperature = 0.8)
        generated_text = response.choices[0].text.strip()

    except Exception as e:
        return f"Error: {e}"
    return generated_text

