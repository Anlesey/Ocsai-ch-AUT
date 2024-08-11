
import os
import sys
import streamlit as st
import requests
from Utils import *
import time  # for measuring time duration of API calls
from openai import OpenAI
from Utils import get_finturned_model_response_openai, get_finturned_model_response_huggingface

import os

# _______________________________________________________________________
# 选择物品、模型、答案
# 物品
prompt = st.text_input("物品", value='报纸')

# 答案
response = st.text_input("答案", value='读报纸')

# 模型
option = st.selectbox(
    "Model",
    ("ft:gpt-3.5-turbo-1106:personal:v2-0-1:9RL6qByn", 
    "Anlesey/ernie-3.0-mini-zh-finetuned-aut", 
    ),
)

text = prompt + "新颖的用途是：" + response




# -------------------------
if st.button("计算创造力得分"):
    result_json = {}
    st.write("输入:", text)
    st.write("输出:")

    # ------------------------- 打接口 -------------------------
    if option=="ft:gpt-3.5-turbo-1106:personal:v2-0-1:9RL6qByn":
        OPENAI_API_KEY=st.secrets["OPENAI_API_KEY"]
        
        client = OpenAI(api_key=OPENAI_API_KEY)
        model_name = option
        score, err = get_finturned_model_response_openai(client, text, model_name)

        if err is not None:
            st.error(err)
        else:
            st.write(score)
        
    elif option=="Anlesey/ernie-3.0-mini-zh-finetuned-aut":
        # https://ui.endpoints.huggingface.co/Anlesey/endpoints/ernie-3-0-mini-zh-finetuned--sxo
        API_URL = "https://rvye4ejt0au1uole.us-east-1.aws.endpoints.huggingface.cloud"
        score, err = get_finturned_model_response_huggingface(text)

        if err is not None:
            st.error(err)
        else:
            st.write(score)