from openai import OpenAI
import ollama
import google.generativeai as genai
import anthropic
import time
import dashscope


# 调用GPT
def openAI_gpt(text, openAI_key, model_name='gpt-4-1106-preview'):
    openai_api_key = openAI_key
    client = OpenAI(api_key=openai_api_key)

    chat_response = client.chat.completions.create(
        model=model_name,
        seed=42,
        messages=[
            {"role": "system", "content": "You are a helpful biomedical scientist."},
            {"role": "user", "content": text}, ]
    )

    return chat_response.choices[0].message.content


def openAI_gpt_2(text, AI_key, model_name='gpt-4o'):
    openai_api_key = AI_key
    client = OpenAI(api_key=openai_api_key, base_url="https://api.gpt.ge/v1/")

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


# 调用claude
# def anthropic_chat_openai(text, AI_key, model_name='claude-3-opus-20240229'):
#     client = OpenAI(api_key=AI_key, base_url="https://suno.lmzh.top/v1")
#     chat_response = client.chat.completions.create(
#         model=model_name,
#         seed=42,
#         messages=[{"role": "system", "content": "You are a helpful biomedical scientist."},
#                   {"role": "user", "content": text}]
#     )
#
#     return chat_response.choices[0].message.content


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


# def qwen_chat(text, AI_key, model_name='qwen-max-0403'):
#     response = dashscope.Generation.call(
#         model=model_name,
#         api_key=AI_key,
#         messages=[{"role": "system", "content": "You are a helpful biomedical scientist."},
#                   {"role": "user", "content": text}],
#         result_format='message', )
#     return response.output.choices[0].message.content

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


#
# def llm_chat(text, model_name, AI_key=None):
#     if model_name == 'gpt-4-turbo-preview' or model_name == 'gpt-3.5-turbo' or model_name == 'gpt-4-1106-preview':
#         return openAI_gpt(text, AI_key, model_name)
#     elif model_name == 'gemini-pro':
#         return gemini_chat(text, model_name, AI_key)
#     elif model_name == 'claude-3-opus-20240229':
#         return anthropic_chat(text, model_name, AI_key)
#     else:
#         return ollama_chat(text, model_name)


def llm_chat(text, model_name, AI_key=None):
    if 'gpt' in model_name:
        return openAI_gpt(text, AI_key, model_name)
        # return openAI_gpt_2(text, AI_key, model_name)
    elif 'gemini' in model_name:
        return gemini_chat(text, model_name, AI_key)
    elif 'claude' in model_name:
        return anthropic_chat(text, model_name, AI_key)
        # return anthropic_chat_openai(text, AI_key, model_name)
    elif 'qwen-max' in model_name:
        return qwen_chat(text, AI_key, model_name)
    else:
        return ollama_chat(text, model_name)


if __name__ == '__main__':
    text = '鲁迅为什么暴打周树人？'
    # out = llm_chat(text, 'qwen-max', 'sk-afac4adcb4974723a26f4a05ee586dbc')
    out = llm_chat(text, 'gpt-4o', '')
    print(out)
