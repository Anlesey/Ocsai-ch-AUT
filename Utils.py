import io
import numpy as np
import pandas as pd
import json
import time
import streamlit as st
import requests


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
        