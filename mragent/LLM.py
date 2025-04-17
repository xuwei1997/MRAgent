from openai import OpenAI


# 调用GPT
def openai_gpt(text, openAI_key, model_name='gpt-4-1106-preview', base_url=None):
    openai_api_key = openAI_key
    if base_url is not None:
        client = OpenAI(api_key=openai_api_key, base_url=base_url)
    else:
        client = OpenAI(api_key=openai_api_key)

    chat_response = client.chat.completions.create(
        model=model_name,
        seed=42,
        messages=[
            {"role": "system", "content": "You are a helpful biomedical scientist."},
            {"role": "user", "content": text}, ]
    )

    return chat_response.choices[0].message.content


# 调用Ollama
def ollama_chat(text, model_name='llama2'):
    import ollama
    response = ollama.chat(
        model=model_name,
        messages=[{"role": "system", "content": "You are a helpful biomedical scientist."},
                  {"role": "user", "content": text}, ]
    )
    return response['message']['content']


def llm_chat(text, model_name, AI_key=None, base_url=None, model_type='openai'):
    if model_type=='openai':
        return openai_gpt(text, AI_key, model_name, base_url)
    elif model_type=='ollama':
        return ollama_chat(text, model_name)
    else:
        # 返回报错
        raise ValueError("Unsupported model type. Please use 'openai' or 'ollama'.")