
import os
import sys
import streamlit as st
import requests
from Utils import *
import time  # for measuring time duration of API calls
from openai import OpenAI
from Utils.Utils import request_for_model_score
from Utils.components import get_model_options_selectbox
import os

# _______________________________________________________________________
st.write("## 单例测试")
# 选择物品、模型、答案

# 模型
model_name = get_model_options_selectbox(key='singleton')

# 物品
prompt = st.text_input("物品", value='报纸')

# 答案
response = st.text_input("答案", value='读报纸')

text = prompt + "新颖的用途是：" + response




# -------------------------
if st.button("计算创造力得分"):
    result_json = {}
    st.write("输入:", text)
    st.write("输出:")

    # ------------------------- 打接口 -------------------------

    score, err = request_for_model_score(model_name=model_name, text=text)

    if err is not None:
        st.error(err)
    else:
        st.write(score)
    