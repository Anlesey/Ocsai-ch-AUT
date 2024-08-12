import io
import numpy as np
import pandas as pd
import json
import time
import streamlit as st
import requests
from openai import OpenAI

starting_system_prompt = "请你作为心理测量专家，为创造力测评-替代用途任务中被试的作答评分。分值为1~5：1分代表该用途不具备创造力，5分代表该用途极具创造力。评分需保留一位小数，不需要额外说明。"


# 输出:分数;错误信息
def get_finturned_model_response_openai(client, text, model_name, max_retries=5):
    retries = 0
    while retries < max_retries:
        # send a ChatCompletion request to count to 100
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": starting_system_prompt},
                {"role": "user", "content": text}
            ],
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
    HUGGFACE_AUTH_KEY=st.secrets["HUGGFACE_AUTH_KEY"]
    
    headers = {
        "Accept" : "application/json",
        "Authorization": f"Bearer {HUGGFACE_AUTH_KEY}",
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


def request_for_model_score(model_name, text):
    if model_name=="ft:gpt-3.5-turbo-1106:personal:v2-0-1:9RL6qByn":
        OPENAI_API_KEY=st.secrets["OPENAI_API_KEY"]
        client = OpenAI(api_key=OPENAI_API_KEY)
        score, err = get_finturned_model_response_openai(client, text, model_name)

    # 为了省钱，先Pause了服务
    # elif model_name=="Anlesey/ernie-3.0-mini-zh-finetuned-aut":
    #     # https://ui.endpoints.huggingface.co/Anlesey/endpoints/ernie-3-0-mini-zh-finetuned--sxo
    #     API_URL = "https://rvye4ejt0au1uole.us-east-1.aws.endpoints.huggingface.cloud"
    #     score, err = get_finturned_model_response_huggingface(API_URL, text)

    else:
        st.error('Model is not available!')
        return None, None
    return score, err