import streamlit as st
import os
import pandas as pd


# 展示比赛信息卡片
def get_details_card_div(match, with_border=True, with_button=True):
    project_root = os.path.dirname(os.path.abspath(__file__))

    home_team_image = os.path.join(project_root, 'image', f'{match["home_team"]}.png')
    away_team_image = os.path.join(project_root, 'image', f'{match["away_team"]}.png')

    with st.container(border=with_border):
        st.write(match["datetime"])
        col0, col1, col2, col3, col4 = st.columns([1,2,2,2,1])
        col1.image(home_team_image, width=75, caption=match['home_team_cn'])
        col2.write(':vs:')
        col2.write(' ')
        col2.write(' ')
        col3.image(away_team_image, width=75, caption=match['away_team_cn'])
        # col0.write('主场')
        # col4.write('客场')

        if with_button:
            if st.button('Let me see see!', key=match['match_id'], use_container_width=True):
                st.switch_page("pages/比赛详情.py")



# 展示历史战绩
# use_data_cnt: 展示数据条数
def display_history_battles(home_team, use_data_cnt=10, container=st):
    df_countries = pd.read_excel('Data/country_names.xlsx')
    home_team_cn = df_countries[df_countries['team']==home_team]['team_cn'].values[0]

    results_final = pd.read_csv('Data/results_final.csv', encoding='latin1')
    history_battles = results_final[(results_final['home_team']==home_team)|(results_final['away_team']==home_team)]\
        .dropna(subset=['home_score'])\
        .sort_values(by='date', ascending=False)\
        .head(use_data_cnt)\
        .set_index('date')
    history_battles = history_battles[['home_team','home_score','away_score','away_team','winner']]
    history_battles['is_victory'] = history_battles['winner']==home_team

    winning_times = history_battles[history_battles['winner']==home_team].shape[0]
    draw_times = history_battles[history_battles['winner'].isna()].shape[0]
    lose_times = history_battles[history_battles['winner'].isna()].shape[0]

    # display
    history_battles.columns = ['主场队','主场队得分','客场队得分','客场队','胜利队','是否胜利']
    container.subheader(f'{home_team_cn}队历史战绩')
    container.metric(label=f"近{use_data_cnt}场比赛胜率", value=f"{winning_times*10}%", delta=f'{winning_times}胜 {draw_times}平 {lose_times}负', delta_color='off')
    container.dataframe(history_battles, use_container_width = True)




