import streamlit as st
import os
import pandas as pd


# 展示比赛信息卡片
def get_model_options_selectbox(key=None):
    # 模型
    return st.selectbox(
        label="Model",
        options=("ft:gpt-3.5-turbo-1106:personal:v2-0-1:9RL6qByn", 
        "Anlesey/ernie-3.0-mini-zh-finetuned-aut", 
        ),
        key=key
    )