#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import pyperclip
from PIL import Image
import streamlit.components.v1 as components


def U30XX_home_page():
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
        .title2 {
            font-size: 20px;
            font-weight: bold;
            color: #000000;
            padding: 10px;
            border-radius: 10px;
            text-align: left;
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
    ### U30XX 장비
    st.markdown('<div class="title">U30XX 장비</div>', unsafe_allow_html=True)
        
    ### U30XX 스위치 콘솔 접속방법    
    st.markdown('<div class="title2">■ U30XX 스위치 콘솔 접속방법</div>', unsafe_allow_html=True)
    data = [["9600", "8", "N", "1", "없음", "root", "premier"]]
    columns = ["SPEED", "DATA BIT", "PARITY BIT", "STOP BIT", "FLOW CONTROL", "초기 LOGIN ID","Password"]
    df = pd.DataFrame(data, columns=columns)
    # 정적 테이블(수정 불가)
    st.dataframe(df, hide_index=True)
    
    ### U30XX 장비 형상
    st.markdown('<div class="title2">■ U30XX 장비 형상도</div>', unsafe_allow_html=True)
    image_path = "C:\\Users\\Ohseungmin\\handbook\\장비사진\\U30XX.png"  # 이미지 경로를 수정

    try:
        img = Image.open(image_path)
        # 이미지 중앙 배치
        st.markdown('<img src="data:image/png;base64,{}" class="centered-image" width="850" />'.format(
            img_to_base64(img)), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"이미지를 로드하는 데 실패했습니다: {e}")
    
    ### U30XX 광커넥터 사양
    st.markdown('<div class="title2">■ U30XX 광커넥터 사양</div>', unsafe_allow_html=True)
    image_path = "C:\\Users\\Ohseungmin\\handbook\\장비사진\\U30XX_Uplink.png"
    try:
        img = Image.open(image_path)
        # 이미지 중앙 배치
        st.markdown('<img src="data:image/png;base64,{}" class="centered-image" width="650" />'.format(
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
            overflow-x: auto;
            margin-bottom: 10px;
        }}
        .table-container {{
            width: 100%;
        }}
        table#{table_id} {{
            width: 100%;
            table-layout: fixed;
            border-collapse: collapse;
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
            text-align: right;
            margin-top: 10px;
        }}
        .copy-all-button {{
            background-color: #5cb85c;
            color: white;
            padding: 8px 12px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            display: inline-block;
        }}
        table#{table_id} td[colspan="2"] {{
            text-align: center;
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
        for (var i = 1; i < rows.length; i++) {{
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
    <div id="copy-alert" class="copy-alert">📋 복사되었습니다!</div>
    <div class="table-container">
        <div class="table-wrapper">
            <table id="{table_id}">
                <tr><th>명령어</th><th>설명</th></tr>
    """

    for row in data:
        if len(row) == 2:
            cmd, desc = row
            html += f"""
            <tr>
                <td>
                    <span class='copy-text' data-command="{cmd}" onclick="copyToClipboard_{table_id}(this)">{cmd}</span>
                </td>
                <td>{desc}</td>
            </tr>
            """
        elif len(row) == 1:
            cmd = row[0]
            html += f"""
            <tr>
                <td colspan="2">
                    <span class='copy-text' data-command="{cmd}" onclick="copyToClipboard_{table_id}(this)">{cmd}</span>
                </td>
            </tr>
            """
        else:
            # 빈 행 등 예외 처리
            html += "<tr><td colspan='2'></td></tr>"

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

def U30XX_e_page():
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
        .title2 {
            font-size: 20px;
            font-weight: bold;
            color: #000000;
            padding: 10px;
            border-radius: 10px;
            text-align: left;
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
    ### U30XX 초기 설정    
    st.markdown('<div class="title2">■ U30XX 초기 설정 명령</div>', unsafe_allow_html=True)
    image_path = "C:\\Users\\Ohseungmin\\handbook\\장비사진\\U30XX_초기설정.png"  # 이미지 경로를 수정
    try:
        img = Image.open(image_path)
        
        # 이미지 중앙 배치
        st.markdown(
    '<img src="data:image/png;base64,{}" style="display: block; margin-left: auto; margin-right: auto;" width="650" />'.format(
        img_to_base64(img)),unsafe_allow_html=True)
    except Exception as e:
        st.error(f"이미지를 로드하는 데 실패했습니다: {e}")
    
    
    st.markdown('<div class="title">🛠 포트 설정 옵션</div>', unsafe_allow_html=True)

    # ▶ 한 줄 정렬: 왼쪽 최대 포트 수, 오른쪽 포트 범위 슬라이더
    col1, col2 = st.columns([1, 1])

    with col1:
        max_ports = st.selectbox("최대 포트 수 선택", options=[24], index=0)

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
    
    ### 장비 IP 및 Default-Gateway 설정    
    data = [
        ["U3024B# conf t", "컨피그 모드 진입"],
        ["U3024B(config)# int vlan1", "업링크 인터페이스 진입"],
        ["U3024B(config-if-vlan1)# no shutdown", "인터페이스 활성화"],
        ["U3024B(config-if-vlan1)# ip addr 10.0.0.2/24", "장비 IP설정"],
        ["U3024B(config)# ip default-gateway 10.0.0.1", "☞DEFAULT G/W설정"],
        ["U3024B(config)# ip default-gateway static-mac 1 gi3 0007.7020.0000", "☞DEFAULT G/W의 MAC (L3장비 MAC설정)"],
        ["U3024B# show ip int brief ", "☞장비 설정 확인"]
    ]
    ### Hostname 및 Password 설정
    data1 = [
        ["SWITCH# conf t", "컨피그 모드 진입"],
        ["SWITCH(config)# hostname U3024B", "장비명 변경"],
        ["U3024B(config)# username root password test", "패스워드 설정"],
        ["U3024B(config)# enable passwd test", "☞enable 패스워드 설정"],
        ["U3024B(config)# no enable passwd", "☞enable 패스워드 삭제"]
    ]
    ### Filter 설정
    data2 = [
        ["U3024B# conf t", "컨피그 모드 진입"],
        [f"U3024B(config)# interface range vdsl {port_min}-{port_max}", f"인터페이스 범위({port_min}-{port_max}) 설정모드 진입"],
        ["U3024B(config-ifrange)# filter netbios", "☞netbios 기능 1~24포트에 적용"],
        ["U3024B(config-ifrange)# filter dhcp", "☞dhcp 기능 1~24번 포트에 적용"],
        ["U3024B(config)# interface vd1", ""],
        ["U3024B(config-if-vd1)# no filter dhcp", "☞1번 포트에 dhcp 필터기능 해제"],
        ["★UPLINK 또는 STACK된 장비와 연결된 포트에는 설정하지 않도록 주의 ★"]
    ]
    ### MAX-host 개수 제한 
    data3 = [
        ["U3024B# conf t", ""],
        ["U3024B(config)# interface range vdsl 1-24", ""],
        ["U3024B(config-ifrange)# mac-count 1", "☞1~24번 포트의 MAC을 1개로 설정"],
        ["U3024B(config)# interface vd1", ""],
        ["U3024B(config-if-vd1)# no mac-count", ""],
        ["U3024B# sh mac-count", "☞1번 포트의 MAC을 제한 해제"],
        ["★UPLINK 또는 STACK된 장비와 연결된 포트에는 설정하지 않도록 주의 ★"]
    ]
    ### 24번 포트를 Port  Stacking으로 구성시 주의해야 할 설정
    data4 = [
        ["U3024B# conf t", ""],
        ["U3024B(config)# interface vd24", ""],
        ["U3024B(config-if-vd24)# no filter dhcp", "☞dhcp 필터기능 해제"],
        ["U3024B(config-if-vd24)# no filter netbios", ""],
        ["U3024B(config-if-vd24)# no service-line-profile", ""],
        ["U3024B(config-if-vd24)# no cpu-mac-filter enable", "☞24번 포트에 적용된 필터기능 해제"],
        ["U3024B(config-if-vd24)# no self-loop-detection", ""],
        ["U3024B(config-if-vd24)# no ip igmp snoop-filter 1", ""],
        ["U3024B(config-if-vd24)# no traffic-control pps all inbound", ""],
        ["U3024B(config)# no service-policy vd24", "☞24번포트 uplink용 service-policy 적용"],
        ["U3024B(config)# service-policy vd24 ingress up-rule", ""],
        ["★UPLINK 또는 STACK된 장비와 연결된 포트에는 설정하지 않도록 주의 ★"]
    ]

    st.markdown('<div class="title">장비 IP 및 Default-Gateway 설정</div>', unsafe_allow_html=True)
    components.html(generate_table_html(data, "table1"), height=400, scrolling=True)

    st.markdown('<div class="title">Hostname 및 Password 설정</div>', unsafe_allow_html=True)
    components.html(generate_table_html(data1, "table2"), height=400, scrolling=True)
    
    st.markdown('<div class="title">Filter 설정</div>', unsafe_allow_html=True)
    components.html(generate_table_html(data2, "table3"), height=400, scrolling=True)
    #st.markdown('<div class="title">Filter 설정</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="title">MAX-host 개수 제한</div>', unsafe_allow_html=True)
    components.html(generate_table_html(data3, "table4"), height=400, scrolling=True)
    
    st.markdown('<div class="title">24번 포트를 Port Stacking으로 구성시 주의해야 할 설정</div>', unsafe_allow_html=True)
    components.html(generate_table_html(data4, "table5"), height=400, scrolling=True)

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
        # 줄바꿈(\n) 기준으로 분리
        cmd_lines = cmd.split('\n')
        cmd_html = "<br>".join(
            f"<span class='copy-text' data-command=\"{line.strip()}\" onclick=\"copyToClipboard(this)\">{line.strip()}</span>"
            for line in cmd_lines if line.strip() != ""
        )
        desc_html = desc.replace('\n', '<br>')
        html += f"""
        <tr>
            <td>
                {cmd_html}
            </td>
            <td>{desc_html}</td>
        </tr>
        """

    html += """
        </table>
    </div>
    """
    return html


def U30XX_w_page():
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
        ["show version","OS버전 확인"],
        ["show memory usage","시스템 메모리 사용율 확인"],
        ["show cpu usage","시스템 CPU 부하율을 확인"],
        ["show running-config","스위치의 설정 내용을 확인"],
        ["show flash","FLASH 메모리 상태 확인"],
        ["show log","RAM에 저장된시스템 로고메세지(휘발성)를 보여줌\n☞Reset 되기전 까지의 내용출력"],
        ["show arp","Arp 테이블의저장내용 확인 (IP,MAC 등)"],
        ["show clock","현재 날짜, 시간을 조회"],
        ["show ip default-gateway","시스템의 gateway 정보 확인"],
        ["show ip interface brief","시스템 interface의 IP 확인"],
        ["copy running-config startup-config","시스템 설정 정보 저장"],
        ["show mac-address-table\nshow mac-address-table vd1(포트번호)","포트별  MAC 어드레스 조회\n특정 포트의 MAC 어드레스 확인"],
        ["show interface\now interface vd1(interface명)","Port별 collision과 packet 상태 확인"],
        ["show port status",""],
        ["conf t\nint vd1\nmac-count 3\nno mac-count","MAC수 제한설정\n\n☞예:1번포트->Mac 제한 3개로 설정\n☞예:1번포트->Mac 제한 무제한설정"],
        ["show filter",""],
        ["show port counter\nshow port statistics vd1(포트번호)\nshow port statistics rmon\nclear counters","포트트래픽통계\n☞지정포트(예:1번포트)의 평균 트래픽을 출력\n포트별 인터페이스 MIB, CRC 정보 확인\n포트통계 초기화"],
        ["show  ip igmp snooping\nshow  ip igmp snooping proxy-reporting group\nshow  ip igmp snooping mrouter\nshow  ip igmp snooping querier\nshow  ip igmp snooping mac-entry","IGMP Snooping 기능을 활성화 되어 있는지 확인\n가입자의 multicast 그룹 확인\nmulticast router 확인\nsnooping querier 포트 확인\nIPTV 서비스중인 가입자 포트 확인"],
        ["show  port line-profile\nshow  port line-rate\nshow  port line-ewl","1-24번 포트 링크상태 및 프로파일점검\n포트별 라인속도, Payload 속도 확인\n포트별 CO-CPE 사이의 거리 확인"],
        ["config\ninterface vd1\nservice-line-profile lite_10\napply line-profile","1번포트의 Profile을 lite_10 으로 설정"],
        ["show port cpe-status","모뎀과 PC Link 상태 확인"],
        ["show self-loop-detection","포트별 Looping 상태 확인"],
        ["erase startup-config\nrestore standard-config","공장초기값 설정\nKT 운용 표준 Config로 설정"],
        ["reload","시스템 리부팅"]
    ]

    # HTML 테이블 생성
    st.markdown('<div class="title">네트워크 장비 조회 명령어</div>', unsafe_allow_html=True)
    components.html(generate_table_html_w(commands), height=3000)  # height를 설정하지 않고 테이블 크기를 자동으로 맞추도록 설정


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

def U30XX_command_page():
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
conf
no ip default-gateway
interface vlan 1
no ip address
ip address {ip_address}/{cidr}
exit
ip default-gateway {gateway}
end
wr m
y
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
    st.sidebar.title("E5024R 장비 핸드북")
    menu = ["홈", "기본 설정", "조회 명령어", "커맨드 생성"]
    choice = st.sidebar.selectbox("메뉴", menu)

    if choice == "홈":
        U30XX_home_page()
    elif choice == "기본 설정":
        U30XX_e_page()
    elif choice == "조회 명령어":
        U30XX_w_page()
    elif choice == "커맨드 생성":
        U30XX_command_page()

if __name__ == "__main__":
    main()
# %%
