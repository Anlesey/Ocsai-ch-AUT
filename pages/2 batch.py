import streamlit as st
import pandas as pd
from io import BytesIO
from Utils import *

def validate_file(df):
    required_columns = ['ID', '物品', '答案']
    if not all(column in df.columns for column in required_columns):
        return "文件必须包含以下三列：ID, 物品, 答案"
    if df['ID'].duplicated().any():
        return "ID列不能包含重复值"
    return None
import streamlit as st
import pandas as pd
from io import BytesIO
from Utils import *

@st.cache_data
def process_file(df):
    results = []
    for i, row in df.iterrows():
        text = f"{row['物品']} {row['答案']}"
        API_URL = "https://rvye4ejt0au1uole.us-east-1.aws.endpoints.huggingface.cloud"
        score, err = get_finturned_model_response_huggingface(API_URL, text)
        df.at[i, 'Score'] = score
        df.at[i, 'Error'] = err
        progress_bar.progress((i + 1) / len(df))
    return df

def main():
    st.write("## 文件批处理")
    st.markdown(
    '''
    列要求：
    - **ID**：唯一标识符，不能重复。
    - **物品**：描述项目或对象。
    - **答案**：对应的答案或信息。

    示例：
    | ID  | 物品  | 答案  |
    |-----|-------|-------|
    | 1   | 报纸 | 阅读 |
    | 2   | 报纸 | 擦拭 |

    ''')
    uploaded_file = st.file_uploader(label="请上传包含ID, 物品, 答案三列的文件", type=["csv", "xlsx"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)

        validation_error = validate_file(df)
        if validation_error:
            st.error(validation_error)
            return

        st.info("文件格式正确，开始处理数据...")
        global progress_bar  # 将进度条设为全局变量
        progress_bar = st.progress(0)
        
        processed_df = process_file(df)

        st.success("数据处理完成！")

        # 将 DataFrame 保存为 Excel 格式
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            processed_df.to_excel(writer, index=False, sheet_name='Sheet1')
        output.seek(0)

        # 创建下载按钮
        st.download_button(
            label="下载结果",
            data=output,
            file_name="processed_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()
