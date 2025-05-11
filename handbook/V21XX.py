#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pyperclip
from PIL import Image
import streamlit.components.v1 as components

def V21XX_home_page():
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

    st.markdown('<div class="title">V21XX 장비</div>', unsafe_allow_html=True)

    # V21XX 장비 이미지 추가
    image_path = "C:\\Users\\LG\\Desktop\\handbook\\장비사진\\V21XX.png"  # 이미지 경로를 수정
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

def V21XX_e_page():
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
            
    data = [
        ["V21XX# conf t", "컨피그 모드 진입"],
        ["V21XX(config)# int br1", "인터페이스 진입"],
        ["V21XX(config-if)# no shutdown", "인터페이스 활성화"],
        ["V21XX(config-if)# ip addr 10.0.0.2/24", "장비 IP 설정"],
        ["V21XX(config)# ip route 0.0.0.0/0 10.0.0.1", "DEFAULT G/W설정"],
        ["V21XX# show ip", "IP 설정 확인"]
    ]

    data1 = [
        ["SWITCH# conf t", "컨피그 모드 진입"],
        ["SWITCH(config)# hostname V21XX", "호스트 이름 변경"],
        ["V21XX(config)# passwd", "패스워드 설정"]
    ]

    data2 = [
        ["V21XX# conf t", "컨피그 모드 진입"],
        ["V21XX(config)# br", "브리지 모드 전환"],
        [f"V21XX(bridge)# set dhcp-filter {port_min}~{port_max}", f"DHCP 필터 적용 ({port_min}~{port_max}포트)"],
        [f"V21XX(bridge)# set netbios-filter {port_min}~{port_max}", f"NetBIOS 필터 적용 ({port_min}~{port_max}포트)"]
    ]

    data3 = [
        ["V21XX# conf t", "컨피그 모드 진입"],
        ["V21XX(config)# br", "브리지 모드 전환"],
        [f"V21XX(bridge)# set max-host {port_min}~{port_max} 1", "포트당 MAC 1개 제한"],
        ["V21XX(config)# set storm-control broadcast rate 3", "Broadcast를 3Mbps로 제한"],
        [f"V21XX(bridge)# set storm-control broadcast {port_min}~{port_max} enable", f"{port_min}~{port_max} 포트에 Broadcast 트래픽 폭주 제어 기능을 활성화"]
    ]
    data4 = [
        ["V21XX# conf t", "컨피그 모드 진입"],
        ["V21XX(config)# br", "bridge 모드 진입"],
        ["V21XX(bridge)# set loop-detect srcmac laa", "Loop 감지 방식으로 Source MAC(LAA) 사용 설정"],
        ["V21XX(bridge)# set loop-detect enable", "Loop 감지 기능 전체 활성화"],
        [f"V21XX(bridge)# set loop-detect {port_min}~{port_max}", f"{port_min}~{port_max} 포트에 Loop 감지 기능 적용"],
        [f"V21XX(bridge)# set loop-detect {port_min}~{port_max} block", "Loop 감지 시 해당 포트를 차단하도록 설정"],
        [f"V21XX(bridge)# set loop-detect {port_min}~{port_max} period 2", "Loop 감지 패킷을 2초 간격으로 전송"],
        [f"V21XX(bridge)# set loop-detect {port_min}~{port_max} timer 300", "Loop 발생 시 차단된 포트를 300초 후 자동 해제"],
        ["V21XX(bridge)# set storm-control broadcast rate 3", "브로드캐스트 트래픽 속도 제한 (rate: 3)"]
    ]

    # 🔽 명령어 테이블 출력
    st.markdown('<div class="title">장비 IP 및 Default-Gateway 설정</div>', unsafe_allow_html=True)
    components.html(generate_table_html(data, "table1"), height=400, scrolling=True)

    st.markdown('<div class="title">Hostname 및 Password 설정</div>', unsafe_allow_html=True)
    components.html(generate_table_html(data1, "table2"), height=400, scrolling=True)

    st.markdown('<div class="title">Filter 설정</div>', unsafe_allow_html=True)
    components.html(generate_table_html(data2, "table3"), height=400, scrolling=True)

    st.markdown('<div class="title">MAX-host 개수 제한 및 Storm-control 설정</div>', unsafe_allow_html=True)
    components.html(generate_table_html(data3, "table4"), height=400, scrolling=True)

    st.markdown('<div class="title">LOOP 방지 설정 (loop-detect 설정)</div>', unsafe_allow_html=True)
    components.html(generate_table_html(data3, "table4"), height=400, scrolling=True)


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
            vertical-align: top;
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
            z-index: 9999;
        }
        @keyframes fadeOut {
            0% { opacity: 1; }
            100% { opacity: 0; display: none; }
        }
        .copy-text {
            color: black;
            text-decoration: underline;
            cursor: pointer;
            white-space: pre-line;
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
        cmd_html = cmd.replace('\n', '<br>')  # 줄바꿈 HTML로 변환
        cmd_attr = cmd.replace('"', '&quot;')  # 복사 속성용 이스케이프
        html += f"""
        <tr>
            <td>
                <span class='copy-text' data-command="{cmd_attr}" onclick="copyToClipboard(this)">{cmd_html}</span>
            </td>
            <td>{desc}</td>
        </tr>
        """
    
    html += "</table>"
    return html


def V21XX_w_page():
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
    ["show system", "시스템 정보 확인"],
    ["show version", "OS버전 확인"],
    ["show port 1-18", "시스템이 각 모듈을 인식하는지 점검"],
    ["show running-config", "스위치의 설정 내용을 확인"],
    ["show syslog local volatile", "RAM에 저장된 시스템 로그메시지(휘발성)를 보여줌"],
    ["show syslog local non-volatile", "비휘발성 메모리(NVRAM)에 저장된 syslog 메시지를 확인"],
    ["show dhcp-filter", "DHCP 필터링 설정 확인"],
    ["show netbios-filter", "NetBIOS 필터링 설정 확인"],
    ["show max-hosts", "포트별 MAC 수 제한 설정값 확인"],

    ["conf t\nbridge\nset port disable 1", "1번 포트 비활성화 (리셋)"],
    ["conf t\nbridge\nset port enable 1", "1번 포트 활성화 (리셋)"],
    ["conf t\nbridge\nset max-hosts 1 3", "1번 포트 → MAC 제한 3개로 설정"],
    ["conf t\nbridge\nclear max-hosts 17", "17번 포트 → MAC 제한 해제 (uplink용)"],

    ["show mac br1 1", "특정 포트(1번)의 MAC address 확인"],
    ["show mac br1", "포트별 MAC address 및 링크 상태 확인"],
    ["ping 168.126.63.1", "PING TEST 수행"],
    ["sping 168.126.63.1 218.153.41.229", "SOURCE PING 수행 (source IP → destination IP)"],

    ["show interface br1", "각 포트의 collision 및 packet 상태 확인"],
    ["show port statistics avg-pkt 1", "1번 포트의 평균 트래픽 통계 (5초, 1분, 10분)"],
    ["show port statistics rmon 1", "1번 포트의 MIB, CRC 정보 확인"],
    ["conf t\nclear port statistics 1", "1번 포트 트래픽 통계 초기화"],
    ["show igmp", "멀티캐스트 서비스(IGMP) 정보 확인"],

    ["conf t\nrestore factory-defaults", "시스템 초기화 (공장출하 상태로 복원)"],
    ["reload", "시스템 리부팅"],
    ["conf t\npasswd", "패스워드 변경"]
]

    # HTML 테이블 생성
    st.markdown('<div class="title">네트워크 장비 조회 명령어</div>', unsafe_allow_html=True)
    components.html(generate_table_html_w(commands), height=2000)  # height를 설정하지 않고 테이블 크기를 자동으로 맞추도록 설정


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


def V21XX_command_page():
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
                result = f"""
end
conf t
int br1
no shutdown
ip address {ip}/{cidr}
exit
ip route 0.0.0.0/0 {gw}
end
wr m
"""
            st.text_area("생성된 커맨드:", value=result, height=300)
            if st.button("커맨드 복사"):
                pyperclip.copy(result)
                st.success("복사 완료!")
        else:
            st.error("CIDR 변환 실패: 서브넷 마스크 확인")

def main():
    st.sidebar.title("V21XX 장비 핸드북")
    menu = ["홈", "기본 설정", "커맨드 생성"]
    choice = st.sidebar.selectbox("메뉴", menu)

    if choice == "홈":
        V21XX_home_page()
    elif choice == "기본 설정":
        V21XX_basic_settings()
    elif choice == "커맨드 생성":
        V21XX_command_page()

if __name__ == "__main__":
    main()
