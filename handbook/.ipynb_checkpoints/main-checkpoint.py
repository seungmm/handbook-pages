#!/usr/bin/env python
# coding: utf-8

import streamlit as st

#레이아웃 wide
st.set_page_config(layout="wide")


import pandas as pd
from streamlit_option_menu import option_menu
import os
from E5024R import (
    E5024R_home_page, E5024R_e_page, E5024R_w_page,
    E5024R_command_page
)

# 공통 장비 목록
all_regions = [
    "E5008R", "E5016R", "E5024R",  # 기존 장비
    "V1XXX", "V21XX", "V16/17XX", "V18XX", "V2808X", "P31XX", "P33XX", "P35XX", "MFS10XX", "MFS23/27XX",
    "E5024", "MGS2824", "V2724G", "V2724GC", "E5024A",
    "E5624R", "V2724GB",
    "MVD100XX", "U3024B/48A", "V5924B/SB",
    "EX1172/LR", "CC8100",
    "WEL2500", "XV3000/3000K", "CVLD20/1048",
    "HAMX6000", "DX6524", "IRT800"
]

def load_pages_for_equipment():
    # 동적으로 각 장비에 맞는 페이지 함수들 생성
    equipment_pages = {}
    
    for equipment in all_regions:
        equipment_pages[equipment] = {
            "Home": globals().get(f"{equipment}_home_page", create_page(equipment, "Home")),
            "긴급복구": globals().get(f"{equipment}_e_page", create_page(equipment, "긴급복구")),
            "조회명령": globals().get(f"{equipment}_w_page", create_page(equipment, "조회명령")),
            "커맨드": globals().get(f"{equipment}_command_page", create_page(equipment, "커맨드"))
        }

    return equipment_pages

def create_page(region, page_name):
    def page_function():
        st.title(f"{region} - {page_name}")
    return page_function

def render_pages(equipment_option, selected_page):
    # 장비별로 페이지를 불러오는 코드
    equipment_pages = load_pages_for_equipment()
    
    if equipment_option and equipment_option != "선택하세요":
        pages = equipment_pages.get(equipment_option, {})
        if selected_page in pages:
            pages[selected_page]()


def update_equipment():
    st.session_state["equipment_option"] = st.session_state["equipment_select"]
    st.session_state["selected_page"] = "Home"  # 장비 선택 변경 시 페이지를 Home으로 설정
    st.session_state["rerun_flag"] = True

def render_sidebar():
    st.markdown(
        """
        <style>
        .css-1d391kg {
            width: 300px;
        }
        .css-1h1w2f8 {
            font-size: 14px;
        }
        .css-1d391kg {
            background-color: #E0FFFF;
        }

        /* 사이드바 내 버튼 스타일링 */
        .stButton>button {
            display: block;
            width: 100%;
            padding: 17px;
            font-size: 17px;
            text-align: center;
            background-color: white; /* 흰색 배경 */
            color: black; /* 검은색 글씨 */
            border: 1px solid black; /* 검은색 테두리 */
            border-radius: 5px;
            margin: 10px 0;
        }

        .stButton>button:hover {
            background-color: #f1f1f1; /* 버튼 호버시 밝은 회색 배경 */
            color: black; /* 글씨색 검정 */
            border: 2px solid #888; /* 호버 시 테두리 색상 */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    all_areas = ["충청", "호남", "부산", "대구"]

    # 세션 상태 초기화
    if "equipment_option" not in st.session_state:
        st.session_state["equipment_option"] = "선택하세요"
    if "area_option" not in st.session_state:
        st.session_state["area_option"] = "선택하세요"
    if "selected_page" not in st.session_state:
        st.session_state["selected_page"] = "Home"
    if "rerun_flag" not in st.session_state:
        st.session_state["rerun_flag"] = False  # rerun을 위한 flag 추가

    # 지역 선택
    def update_area():
        st.session_state["area_option"] = st.session_state["area_select"]

    area_select_index = 0 if st.session_state["area_option"] == "선택하세요" else all_areas.index(st.session_state["area_option"]) + 1
    area_select = st.sidebar.selectbox(
        "지역 선택 (검색 가능)",
        options=["선택하세요"] + all_areas,
        index=area_select_index,
        format_func=lambda x: "" if x == "선택하세요" else x,
        key="area_select",
        on_change=update_area  # 변경 시 지역 상태 업데이트
    )

    # 장비 선택
    equipment_select_index = all_regions.index(st.session_state["equipment_option"]) + 1 if st.session_state["equipment_option"] != "선택하세요" else 0
    equipment_option = st.sidebar.selectbox(
        "장비 선택 (검색 가능)",
        options=["선택하세요"] + all_regions,
        index=equipment_select_index,
        format_func=lambda x: "" if x == "선택하세요" else x,
        key="equipment_select",
        on_change=update_equipment
    )

    

    # 페이지 선택 버튼
    st.sidebar.markdown("페이지 선택")
    pages = ["Home", "긴급복구", "조회명령", "커맨드"]
    for page in pages:
        if st.sidebar.button(page):
            st.session_state["selected_page"] = page

    # 유관 부서 전화번호 표시
    if st.session_state["area_option"] != "선택하세요":
        st.sidebar.markdown("유관 부서 전화번호")

        common_numbers = {
            "OSP 관제센터": "02-500-6150",
            "IP망 관제센터": "042-478-1600",
            "전원관제": "042-478-1800",
            "과천 제1관제센터(교환)": "02-500-6080",
        }

        unique_numbers = {
            "충청": {"name": "교환기술부(충청)", "number": "042-255-2470"},
            "호남": {"name": "교환기술부(호남)", "number": "062-513-1200"},
            "부산": {"name": "교환기술부(부산)", "number": "051-464-4699"},
            "대구": {"name": "교환기술부(대구)", "number": "053-477-3010"},
        }
        enter_numbers = {
            "충청": {"name": "분기국사출입(충청)", "number": "042-478-7550, 7540"},
            "호남": {"name": "분기국사출입(호남)", "number": "062-230-3355~7"},
            "부산": {"name": "분기국사출입(부산)", "number": "051-464-2300"},
            "대구": {"name": "분기국사출입(대구)", "number": "053-477-1984~5"},
        }

        phone_numbers = list(common_numbers.values()) + [unique_numbers[st.session_state["area_option"]]["number"]] + [enter_numbers[st.session_state["area_option"]]["number"]]
        phone_names = list(common_numbers.keys()) + [unique_numbers[st.session_state["area_option"]]["name"]] + [enter_numbers[st.session_state["area_option"]]["name"]]

        for name, number in zip(phone_names, phone_numbers):
            st.sidebar.markdown(f"- {name}: {number}")

    # URL Navigation 추가
    st.sidebar.header("URL Navigation")
    urls = {
        "기상레이더센터_낙뢰": "https://radar.kma.go.kr/lightning/area_lightning.do",
        "날씨누리_레이더": "https://www.weather.go.kr/w/image/radar.do",
        "windy.com": "https://www.windy.com/?37.475,126.957,5",
        "KBS 재난포털_CCTV": "https://d.kbs.co.kr/special/cctv",
        "카카오맵": "https://map.kakao.com/",
        "네이버지도": "https://map.naver.com/"
    }
    for name, url in urls.items():
        st.sidebar.markdown(f"[{name}]({url})")

    return st.session_state["equipment_option"], st.session_state["selected_page"]

def main():
    equipment_option, selected_page = render_sidebar()

    # 화면 새로 고침 여부 체크
    if st.session_state["rerun_flag"]:
        st.session_state["rerun_flag"] = False  # 새로 고침 후 다시 플래그를 False로 설정
        st.rerun()

    render_pages(equipment_option, selected_page)

if __name__ == "__main__":
    main()