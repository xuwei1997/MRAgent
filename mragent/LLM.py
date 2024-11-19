from openai import OpenAI
import google.generativeai as genai
import anthropic


# 调用GPT
def openAI_gpt(text, openAI_key, model_name='gpt-4-1106-preview', base_url=None):
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


# 调用Gemini
def gemini_chat(text, model_name='gemini-1.5-pro-latest', AI_key=None):
    # sleep 1s to avoid 429 error
    # time.sleep(10)
    genai.configure(api_key=AI_key)
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(text)
    return response.text


# 调用Anthropic
def anthropic_chat(text, model_name='claude-3-opus-20240229', AI_key=None):
    client = anthropic.Anthropic(api_key=AI_key, )
    message = client.messages.create(
        model=model_name,
        max_tokens=1000,
        messages=[{"role": "system", "content": "You are a helpful biomedical scientist."},
                  {"role": "user", "content": text}]
    )
    return message.content


def anthropic_chat_openai(text, AI_key, model_name='claude-3-opus-20240229'):
    client = OpenAI(api_key=AI_key, base_url="https://api.ai365vip.com/v1/")
    chat_response = client.chat.completions.create(
        model=model_name,
        seed=42,
        messages=[{"role": "system", "content": "You are a helpful biomedical scientist."},
                  {"role": "user", "content": text}]
    )
    print(chat_response)

    return chat_response.choices[0].message.content


def qwen_chat(text, AI_key, model_name='qwen-max-0403'):
    openai_api_key = AI_key
    client = OpenAI(api_key=openai_api_key, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

    chat_response = client.chat.completions.create(
        model=model_name,
        seed=42,
        messages=[
            {"role": "system", "content": "You are a helpful biomedical scientist."},
            {"role": "user", "content": text}, ]
    )

    return chat_response.choices[0].message.content


def llm_chat(text, model_name, AI_key=None, base_url=None):
    if base_url == None:
        if 'gpt' in model_name:
            return openAI_gpt(text, AI_key, model_name, base_url)
        elif 'gemini' in model_name:
            return gemini_chat(text, model_name, AI_key)
        elif 'claude' in model_name:
            return anthropic_chat(text, model_name, AI_key)
        elif 'qwen-max' in model_name:
            return qwen_chat(text, AI_key, model_name)
        else:
            return ollama_chat(text, model_name)
    else:
        return openAI_gpt(text, AI_key, model_name, base_url)
