
import streamlit as st
import importlib
import pandas as pd
from streamlit_option_menu import option_menu
import os

st.set_page_config(layout="wide")

equipment_tree = {
    "10G GES": ["V2724GC", "E5024H"],
    "UTP2": ["E50XXH", "E56XXR", "V27XXGB"],
    "VDSL(100M)": ["MVD100XX", "U30XX", "V5924"],
    "VDSL(50M)": ["EX1172LR", "CC8100"],
    "VDSL(20M)": ["WEL5200", "XV3000/3000K", "CVLD20/1048"],
    "ADSL": ["HAMX6000", "DX6524", "IRT800"],
    "FES": ["V1XXX", "V21XX", "V16/17XX", "V18XX", "V2808k", "P31XX", "P33XX", "P35XX"],
    "GES": ["MFS10XX", "MFS23/27XX", "E50XX", "MGS2824", "V2724G"]
}

equipment_alias = {
    "E50XXH": ["E5008R", "E5016R", "E5024R"],
    "E56XXR": ["E5608R", "E5616R", "E5624R"]
}

def load_selected_equipment_pages(equipment):
    display_name = equipment
    if equipment == "V16/17XX":
        module_key = "V1617XX"
    else:
        module_key = equipment.replace("/", "").replace("-", "")
    try:
        module = importlib.import_module(module_key)
        return {
            "Home": getattr(module, f"{module_key}_home_page", create_page(display_name, "Home")),
            "긴급복구": getattr(module, f"{module_key}_e_page", create_page(display_name, "긴급복구")),
            "조회명령": getattr(module, f"{module_key}_w_page", create_page(display_name, "조회명령")),
            "커맨드": getattr(module, f"{module_key}_command_page", create_page(display_name, "커맨드"))
        }
    except (ModuleNotFoundError, AttributeError) as e:
        st.error(f"'{equipment}' 모듈을 로드할 수 없습니다: {e}")
        return {
            "Home": create_page(display_name, "Home"),
            "긴급복구": create_page(display_name, "긴급복구"),
            "조회명령": create_page(display_name, "조회명령"),
            "커맨드": create_page(display_name, "커맨드")
        }

def create_page(region, page_name):
    def page_function():
        st.title(f"{region} - {page_name}")
    return page_function

def render_pages(equipment_option, selected_page):
    if equipment_option and equipment_option != "선택하세요":
        pages = load_selected_equipment_pages(equipment_option)
        if selected_page in pages:
            pages[selected_page]()

def update_equipment():
    st.session_state["equipment_option"] = st.session_state["equipment_select"]
    st.session_state["selected_page"] = "Home"
    st.session_state["rerun_flag"] = True

def render_sidebar():
    st.markdown("""
    <style>
    .css-1d391kg { width: 300px; background-color: #E0FFFF; }
    .css-1h1w2f8 { font-size: 14px; }
    .stButton>button { width: 100%; padding: 17px; font-size: 17px; margin: 10px 0; }
    .stButton>button:hover { background-color: #f1f1f1; color: black; border: 2px solid #888; }
    </style>
    """, unsafe_allow_html=True)

    if "equipment_option" not in st.session_state:
        st.session_state["equipment_option"] = "선택하세요"
    if "selected_page" not in st.session_state:
        st.session_state["selected_page"] = "Home"
    if "rerun_flag" not in st.session_state:
        st.session_state["rerun_flag"] = False

    equipment_groups = list(equipment_tree.keys())
    selected_group = st.sidebar.selectbox("## 장비 유형 선택", options=["선택하세요"] + equipment_groups)

    if selected_group != "선택하세요":
        options = equipment_tree[selected_group]
        idx = options.index(st.session_state["equipment_option"]) if st.session_state["equipment_option"] in options else 0
        st.sidebar.selectbox(
            "## 장비 선택",
            options=options,
            index=idx,
            key="equipment_select",
            on_change=update_equipment
        )
    else:
        st.session_state["equipment_option"] = "선택하세요"

    if st.session_state["equipment_option"] != "선택하세요":
        st.sidebar.markdown("## 페이지 선택")
        for page in ["Home", "긴급복구", "조회명령", "커맨드"]:
            if st.sidebar.button(page):
                st.session_state["selected_page"] = page

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

if __name__ == "__main__":
    option, page = render_sidebar()
    if st.session_state.get("rerun_flag", False):
        st.session_state["rerun_flag"] = False
        st.rerun()
    if option != "선택하세요":
        render_pages(option, page)
