import streamlit as st
import os
import pandas as pd


# 展示比赛信息卡片
def get_model_options_selectbox(key=None):
    # 模型
    return st.selectbox(
        label="Model",
        options=("ft:gpt-4o-mini-2024-07-18:personal:aut-v3-1-1:A1ywguFJ", 
        # "Anlesey/ernie-3.0-mini-zh-finetuned-aut", 
        ),
        key=key
    )
