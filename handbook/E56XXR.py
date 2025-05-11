#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import pyperclip
from PIL import Image
import streamlit.components.v1 as components


def E56XXR_home_page():
    # 페이지 배경 색 설정
    st.markdown(
        """
        <style>
        body {
            background-color: #F0F8FF;
        }
        .title {
            font-size: 24px;
            font-weight: bold;
            color: #ffffff;
            background-color: #4682B4;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 10px;
        }
        .card {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .centered-image {
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="title">E56XXR 장비</div>', unsafe_allow_html=True)

    # E56XXR 장비 이미지 추가
    image_path = "C:\\Users\\LG\\Desktop\\handbook\\장비사진\\E56XXR.png"  # 이미지 경로를 수정
    try:
        img = Image.open(image_path)

        # 이미지 중앙 배치
        st.markdown('<img src="data:image/png;base64,{}" class="centered-image" width="1250" />'.format(
            img_to_base64(img)), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"이미지를 로드하는 데 실패했습니다: {e}")

def img_to_base64(img):
    import base64
    import io
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def colorize_command(command):
    if "#" in command:
        parts = command.split("#", 1)
        return f"{parts[0]}#<span style='color:#1E90FF'>{parts[1]}</span>"
    return command

def generate_table_html(data, table_id):
    html = f"""
    <style>
        .table-wrapper {{
            width: 100%;
            overflow-x: auto; /* 테이블이 너무 넓어질 경우 가로 스크롤 */
            margin-bottom: 10px; /* 버튼과의 간격 조절 */
        }}
        .table-container {{
            width: 100%;
        }}
        table#{table_id} {{
            width: 100%;
            table-layout: fixed;
            border-collapse: collapse; /* 테두리 중복 제거 */
        }}
        table#{table_id} th, table#{table_id} td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        table#{table_id} th {{
            background-color: white;
            color: black;
        }}
        table#{table_id} td:first-child {{
            width: auto;
        }}
        .copy-alert {{
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            display: none;
            font-size: 14px;
            animation: fadeOut 2s ease-in-out forwards;
        }}
        @keyframes fadeOut {{
            0% {{ opacity: 1; }}
            100% {{ opacity: 0; display: none; }}
        }}
        .copy-text {{
            color: black;
            text-decoration: underline;
            cursor: pointer;
        }}
        .copy-all-button-wrapper {{
            text-align: right; /* 버튼을 오른쪽으로 정렬 */
            margin-top: 10px; /* 테이블과의 간격 조절 */
        }}
        .copy-all-button {{
            background-color: #5cb85c;
            color: white;
            padding: 8px 12px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            display: inline-block; /* 버튼을 내용에 맞게 표시 */
        }}
    </style>
    <script>
    function copyToClipboard_{table_id}(element) {{
        var text = element.getAttribute("data-command");
        var parts = text.split("#", 2);
        if (parts.length > 1) {{
            navigator.clipboard.writeText(parts[1]).then(function() {{
                showCopyAlert_{table_id}();
            }}).catch(function(err) {{
                console.error("복사 실패: ", err);
            }});
        }}
    }}

    function showCopyAlert_{table_id}() {{
        var alertBox = document.getElementById("copy-alert");
        alertBox.style.display = "block";
        setTimeout(function() {{
            alertBox.style.display = "none";
        }}, 2000);
    }}

    function copyAll_{table_id}() {{
        var commands = [];
        var table = document.getElementById("{table_id}");
        var rows = table.getElementsByTagName("tr");
        for (var i = 1; i < rows.length; i++) {{ // Skip header row
            var cell = rows[i].getElementsByTagName("td")[0];
            if (cell) {{
                var copyTextSpan = cell.querySelector(".copy-text");
                if (copyTextSpan) {{
                    var command = copyTextSpan.getAttribute("data-command");
                    var parts = command.split("#", 2);
                    if (parts.length > 1) {{
                        commands.push(parts[1]);
                    }}
                }} else {{
                    commands.push(cell.textContent);
                }}
            }}
        }}
        navigator.clipboard.writeText(commands.join("\\n")).then(function() {{
            showCopyAlert_{table_id}();
        }}).catch(function(err) {{
            console.error("전체 복사 실패: ", err);
        }});
    }}
    </script>
    <div class="table-container">
        <div class="table-wrapper">
            <table id="{table_id}">
                <tr><th>명령어</th><th>설명</th></tr>
    """
    for cmd, desc in data:
        # 명령어에 '#'이 포함되어 있으면, 복사 가능하게 스타일 적용
        if "#" in cmd:
            html += f"""
            <tr>
                <td>
                    <span class='copy-text' data-command="{cmd}" onclick="copyToClipboard_{table_id}(this)">{colorize_command(cmd)}</span>
                </td>
                <td>{desc}</td>
            </tr>
            """
        else:
            # '#'이 없으면 일반 텍스트로 표시 (스타일 없이)
            html += f"""
            <tr>
                <td>{cmd}</td>
                <td>{desc}</td>
            </tr>
            """
    html += f"""
            </table>
        </div>
        <div class="copy-all-button-wrapper">
            <button class="copy-all-button" onclick="copyAll_{table_id}()">전체 명령어 복사</button>
        </div>
    </div>
    <div id="copy-alert" class="copy-alert">📋 복사되었습니다!</div>
    """
    return html

def E56XXR_e_page():
    st.markdown("""
        <style>
        body {
            background-color: #F0F8FF;
        }
        .title {
            font-size: 24px;
            font-weight: bold;
            color: #ffffff;
            background-color: #4682B4;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 10px;
        }
        .card {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        </style>
        """, unsafe_allow_html=True
    )

   # 🔷 포트 설정 구간
    st.markdown('<div class="title">🛠 포트 설정 옵션</div>', unsafe_allow_html=True)

    # ▶ 한 줄 정렬: 왼쪽 최대 포트 수, 오른쪽 포트 범위 슬라이더
    col1, col2 = st.columns([1, 1])

    with col1:
        max_ports = st.selectbox("최대 포트 수 선택", options=[8, 16, 24, 48], index=2)

    with col2:
        port_min, port_max = st.slider(
            "포트 범위 설정 (예: giX)", 
            min_value=1, 
            max_value=max_ports, 
            value=(1, max_ports)
        )

    # 명령어 포맷
    range_cmd = f"{port_min}~{port_max}"
    gi_cmd = f"gi{port_min}"  # 기본 gi 포트는 최소값 기준

    
    # 🔸 장비 IP 설정 명령어
    data = [
        ["E56XXR# conf t", "컨피그 모드 진입"],
        ["E56XXR(config)# int vlan1", "업링크 인터페이스 진입"],
        ["E56XXR(config-if-vlan1)# no shutdown", "인터페이스 활성화"],
        ["E56XXR(config-if-vlan1)# ip addr 10.0.0.2/24", "장비 IP설정"],
        ["E56XXR(config-if-vlan1)# ip default-gateway 10.0.0.1", "DEFAULT G/W설정"],
        ["E56XXR# show ip int brief", "장비 IP설정 확인"]
    ]

    # 🔸 장비 이름 및 비밀번호 설정 명령어
    data1 = [
        ["SWITCH# conf t", "컨피그 모드 진입"],
        ["SWITCH(config)# hostname E56XXR", "장비명 변경"],
        ["E56XXR(config)# username root password test", "패스워드 설정"],
        ["E56XXR(config)# enable password test", "enable 패스워드 설정"],
        ["E56XXR(config)# no enable password", "enable 패스워드 삭제"]
    ]

    # 🔸 포트 설정 명령어 (입력 값 반영)
    data2 = [
        ["SWITCH# conf t", "컨피그 모드 진입"],
        ["E56XXR(config)# range port", "인터페이스 범위 설정모드 진입"],
        [f"E56XXR(config-range-port)# no shutdown {port_min}~{port_max}", f"{port_min}~{port_max}번 포트 개방"],
        [f"E56XXR(config-range-port)# mac-count 8 {port_min}~{port_max}", f"{port_min}~{port_max}번 포트 MAC 제한"],
        [f"E56XXR(config-range-port)# no mac-count {port_min}~{port_max}", f"{port_min}~{port_max} 포트 MAC 제한 해제"],
        ["E56XXR# sh mac-count", "MAC 허용 개수 및 사용 개수 확인"]
    ]

    # 🔽 명령어 테이블 출력
    st.markdown('<div class="title">장비 IP 및 Default-Gateway 설정</div>', unsafe_allow_html=True)
    components.html(generate_table_html(data, "table1"), height=400, scrolling=True)

    st.markdown('<div class="title">Hostname 및 Password 설정</div>', unsafe_allow_html=True)
    components.html(generate_table_html(data1, "table2"), height=400, scrolling=True)

    st.markdown('<div class="title">포트OPEN 및 MAX-host 개수 제한</div>', unsafe_allow_html=True)
    components.html(generate_table_html(data2, "table3"), height=400, scrolling=True)

def colorize_command_w(command):
    # '#' 없이 글자색을 검정색으로 처리
    return command

def generate_table_html_w(data):
    html = """
    <style>
        table {
            width: 100%;
            table-layout: auto;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: white;
            color: black;
        }
        td:first-child {
            width: auto;
        }
        .copy-alert {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            display: none;
            font-size: 14px;
            animation: fadeOut 2s ease-in-out forwards;
        }
        @keyframes fadeOut {
            0% { opacity: 1; }
            100% { opacity: 0; display: none; }
        }
        .copy-text {
            color: black;
            text-decoration: underline;
            cursor: pointer;
        }
    </style>
    <script>
    function copyToClipboard(element) {
        var text = element.getAttribute("data-command");
        navigator.clipboard.writeText(text).then(function() {
            showCopyAlert();
        }).catch(function(err) {
            console.error("복사 실패: ", err);
        });
    }

    function showCopyAlert() {
        var alertBox = document.getElementById("copy-alert");
        alertBox.style.display = "block";
        setTimeout(function() {
            alertBox.style.display = "none";
        }, 2000);
    }
    </script>
    <div id="copy-alert" class="copy-alert">📋 복사되었습니다!</div>
    <table>
        <tr><th>명령어</th><th>설명</th></tr>
    """
    
    for cmd, desc in data:
        html += f"""
        <tr>
            <td>
                <span class='copy-text' data-command="{cmd}" onclick="copyToClipboard(this)">{cmd}</span>
            </td>
            <td>{desc}</td>
        </tr>
        """
    
    html += "</table>"
    return html


def E56XXR_w_page():
    st.markdown("""
        <style>
        body {
            background-color: #F0F8FF;
        }
        .title {
            font-size: 24px;
            font-weight: bold;
            color: #ffffff;
            background-color: #4682B4;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 10px;
        }
        .card {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        table {
            width: 100%;
            table-layout: auto;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: white;
            color: black;
        }
        td:first-child {
            width: auto;
        }
        </style>
        """, unsafe_allow_html=True
    )

    commands = [
        ["show uptime", "시스템 가동 시간 확인"],
        ["show system", "시스템 정보 확인"],
        ["show version", "OS 버전 확인"],
        ["show cpuload", "CPU 사용률 확인"],
        ["show vlan", "VLAN 정보 확인"],
        ["show arp", "ARP 테이블 확인"],
        ["show ip interfaces brief", "IP 인터페이스 요약 정보 확인"],
        ["show ip route", "IP 라우팅 테이블 확인"],
        ["show port status", "포트 상태 확인"],
        ["show rate-limit", "속도 제한 설정 확인"],
        ["show ip dhcp snooping binding", "IP 할당 상태 확인"],
        ["show mac", "MAC 주소 테이블 확인"],
        ["show max-hosts", "포트별 최대 호스트 수 확인"],
        ["show syslog local volatile reverse", "휘발성 로컬 시스템 로그 (최신 순) 확인"],
        ["show syslog local non-volatile reverse", "비휘발성 로컬 시스템 로그 (최신 순) 확인"],
        ["show port statistics avg allports", "모든 포트의 평균 트래픽 통계 확인"],
        ["show port statistics avg gi1", "인터페이스 gi1의 평균 트래픽 통계 확인"],
        ["show port statistics avg type", "포트 유형별 평균 트래픽 통계 확인"],
        ["show port statistics avg type gi1", "인터페이스 gi1의 특정 유형 평균 트래픽 통계 확인"],
        ["show ip igmp snooping reporter", "IGMP 통계 확인"],
        ["show ip igmp snooping reporter | include gi1", "인터페이스 gi1의 IGMP 통계 확인"],
        ["show port phy-diag", "GIGA 가입자 cable 거리 확인"],
        ["show cpe sysinfo", "CPE 시스템 정보 확인"],
        ["show cpe port status", "CPE 포트 상태 확인"],
        ["show port cpe lan-port status", "CPE 가입자 포트 상태 확인"],
        ["show port cpe lan-port status gi1", "CPE 가입자 포트 상태 확인"],
        ["show cpe mac", "CPE MAC 주소 정보 확인"]
    ]

    # HTML 테이블 생성
    st.markdown('<div class="title">네트워크 장비 조회 명령어</div>', unsafe_allow_html=True)
    components.html(generate_table_html_w(commands), height=1300)  # height를 설정하지 않고 테이블 크기를 자동으로 맞추도록 설정


def subnet_mask_to_cidr(subnet_mask):
    """서브넷 마스크를 CIDR 표기법으로 변환합니다."""
    mapping = {
        "255.255.255.0": 24,
        "255.255.255.128": 25,
        "255.255.255.192": 26,
        "255.255.255.224": 27,
        "255.255.255.240": 28,
        "255.255.255.248": 29,
        "255.255.255.252": 30
    }
    return mapping.get(subnet_mask, "")

def E56XXR_command_page():
    st.markdown(
        """
        <style>
        body {
            background-color: #F0F8FF; /* 밝은 하늘색 */
        }
        .title {
            font-size: 24px;
            font-weight: bold;
            color: #ffffff;
            background-color: #4682B4;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 10px;
        }
        .card {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="title">커맨드 생성 페이지</div>', unsafe_allow_html=True)

    # session_state 초기화
    if "ip_address" not in st.session_state:
        st.session_state["ip_address"] = ""
    if "subnet_mask" not in st.session_state:
        st.session_state["subnet_mask"] = "255.255.255.0"
    if "gateway" not in st.session_state:
        st.session_state["gateway"] = ""

    # 입력 필드 유지 (한 줄 정렬)
    col1, col2, col3 = st.columns(3)
    with col1:
        ip_address = st.text_input("IP 주소 입력", value=st.session_state["ip_address"], key="ip_input")
    with col2:
        subnet_mask_options = [
            "255.255.255.0", "255.255.255.128", "255.255.255.192",
            "255.255.255.224", "255.255.255.240", "255.255.255.248", "255.255.255.252"
        ]
        subnet_mask = st.selectbox("서브넷 마스크 선택", subnet_mask_options, index=subnet_mask_options.index(st.session_state["subnet_mask"]))
    with col3:
        gateway = st.text_input("게이트웨이 입력", value=st.session_state["gateway"], key="gateway_input")

    # 값 변경 시 자동으로 session_state 업데이트
    if ip_address != st.session_state["ip_address"]:
        st.session_state["ip_address"] = ip_address
    if subnet_mask != st.session_state["subnet_mask"]:
        st.session_state["subnet_mask"] = subnet_mask
    if gateway != st.session_state["gateway"]:
        st.session_state["gateway"] = gateway

    # 버튼을 누를 때 새로고침 없이 상태를 유지하도록 session_state에 저장
    if st.button("커맨드 생성"):
        if ip_address and subnet_mask and gateway:
            cidr = subnet_mask_to_cidr(subnet_mask)
            if cidr:
                commands = f"""
end
conf t
logging console disable
int vlan1
no ip address dhcp
ip address {ip_address}/{cidr}
exit
ip default-gateway {gateway}
end
copy r s
yes
"""
                st.session_state["generated_command"] = commands  # 생성된 커맨드도 유지
            else:
                st.error("유효하지 않은 서브넷 마스크 형식입니다.")
        else:
            st.warning("모든 필드를 입력해주세요.")

    # 커맨드 유지해서 화면이 바뀌어도 사라지지 않도록 함
    if "generated_command" in st.session_state:
        st.text_area("생성된 커맨드:", value=st.session_state["generated_command"], height=300)

        # 복사 버튼
        if st.button("커맨드 복사"):
            pyperclip.copy(st.session_state["generated_command"])
            st.success("커맨드가 클립보드에 복사되었습니다.")

def main():
    st.sidebar.title("E56XXR 장비 핸드북")
    menu = ["홈", "기본 설정", "조회 명령어", "커맨드 생성"]
    choice = st.sidebar.selectbox("메뉴", menu)

    if choice == "홈":
        E56XXR_home_page()
    elif choice == "기본 설정":
        E56XXR_e_page()
    elif choice == "조회 명령어":
        E56XXR_w_page()
    elif choice == "커맨드 생성":
        E56XXR_command_page()

if __name__ == "__main__":
    main()
