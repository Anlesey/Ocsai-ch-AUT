import io
import numpy as np
import pandas as pd
import json
import time
import streamlit as st
import requests

starting_system_prompt = "请你作为心理测量专家，为创造力测评-替代用途任务中被试的作答评分。分值为1~5：1分代表该用途不具备创造力，5分代表该用途极具创造力。评分需保留一位小数，不需要额外说明。"

def request_format_fewshot_batch_gpt(x, model_name, d_fewshot, use_target_prompt=True):
    prompt = x['prompt']
    if prompt in d_fewshot['prompt'].unique() and use_target_prompt:
        d_fewshot = d_fewshot[d_fewshot['prompt']==prompt]
    
    message = construct_few_shot_message(d_fewshot)
    
    message.append({
            "role": "user",
            "content": x['text']
        })
    
    return {
        "custom_id": str(x['ID']).zfill(6), 
        "method": "POST", 
        "url": "/v1/chat/completions", 
        "body": {
            "model": model_name, 
            "messages": message,
            "temperature":0,
            "max_tokens":3
        }
    }

get_request_format_message_openai = lambda text : [
        {"role": "system", "content": starting_system_prompt},
        {"role": "user", "content": text}
    ]

# 输出:分数;错误信息
def get_finturned_model_response_openai(client, messages, model_name, max_retries=5):
    retries = 0
    while retries < max_retries:
        # send a ChatCompletion request to count to 100
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0,
        )
        # print the time delay and text received
        reply_content = response.choices[0].message.content
        try:
            return float(reply_content), None
        except ValueError:
            retries += 1
            time.sleep(0.05)  # Optional: wait for a short period before retrying
    
    return None, response


def get_finturned_model_response_huggingface(API_URL, text):

    headers = {
        "Accept" : "application/json",
        "Authorization": "Bearer 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",
        "Content-Type": "application/json" 
    }

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    result_json = query({
        "inputs": text,
        "parameters": {}
    })

    # ------------------------- 展示 -------------------------

    if "error" in result_json:
        st.write(result_json)
        return None, result_json
    else:
        score = result_json[0]['score']
        return score, None
        