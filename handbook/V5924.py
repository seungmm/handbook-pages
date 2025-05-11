#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import pyperclip
from PIL import Image
import streamlit.components.v1 as components


def V5924_home_page():
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
        .title3 {
            font-size: 15px;
            font-weight: soft;
            color: #0000FF;
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
    ### V5924 장비
    st.markdown('<div class="title">V5924 장비</div>', unsafe_allow_html=True)
        
    ### V5924 스위치 콘솔 접속방법    
    st.markdown('<div class="title2">■ V5924SB/B 스위치 콘솔 접속방법</div>', unsafe_allow_html=True)
    data = [["9600", "8", "N", "1", "없음", "admin", "password"]]
    columns = ["SPEED", "DATA BIT", "PARITY BIT", "STOP BIT", "FLOW CONTROL", "초기 LOGIN ID","Password"]
    df = pd.DataFrame(data, columns=columns)
    # 정적 테이블(수정 불가)
    st.dataframe(df, hide_index=True)
    
    ### V5924 장비 형상
    st.markdown('<div class="title2">■ V5924B 장비 형상도</div>', unsafe_allow_html=True)
    image_path = "C:\\Users\\Ohseungmin\\handbook\\장비사진\\V5924.png"  # 이미지 경로를 수정
    try:
        img = Image.open(image_path)
        
        # 이미지 중앙 배치
        st.markdown('<img src="data:image/png;base64,{}" class="centered-image" width="850" />'.format(
            img_to_base64(img)), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"이미지를 로드하는 데 실패했습니다: {e}")
    st.markdown('<div class="title3">※ V5924B는 V5924SB에서 hardware 적으로 개량 개선된 장비임 ※</div>', unsafe_allow_html=True)
    
    ### V5924 광커넥터 사양
    st.markdown('<div class="title2">■ V5924 광커넥터 사양</div>', unsafe_allow_html=True)
    image_path = "C:\\Users\\Ohseungmin\\handbook\\장비사진\\V5924_광.png"  # 이미지 경로를 수정
    try:
        img = Image.open(image_path)
        
        # 이미지 중앙 배치
        st.markdown('<img src="data:image/png;base64,{}" class="centered-image" width="750" />'.format(
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

def V5924_e_page():
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
    ### V5924 초기 설정    
    st.markdown('<div class="title2">■ V5924 초기 설정 명령</div>', unsafe_allow_html=True)
    image_path = "C:\\Users\\Ohseungmin\\handbook\\장비사진\\V5924_초기설정.png"  # 이미지 경로를 수정
    try:
        img = Image.open(image_path)
        
        # 이미지 중앙 배치
        st.markdown(
    '<img src="data:image/png;base64,{}" style="display: block; margin-left: auto; margin-right: auto;" width="650" />'.format(
        img_to_base64(img)),unsafe_allow_html=True)
    except Exception as e:
        st.error(f"이미지를 로드하는 데 실패했습니다: {e}")
    
    # ▶ 한 줄 정렬: 왼쪽 최대 포트 수, 오른쪽 포트 범위 슬라이더    
    st.markdown('<div class="title">🛠 포트 설정 옵션</div>', unsafe_allow_html=True)
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
        ["SWITCH# conf t", "컨피그 모드 진입"],
        ["V5924B(config)# int noshutdown default 또는 \n V5924B(config)# int noshutdown 1", "☞인터페이스 활성화"],
        ["V5924B(config)# int default 또는 \nV5924B(config)# int 1", ""],
        ["V5924B(config-if)# no shutdown", "☞인터페이스 활성화"],
        ["V5924B(config-if)# ip addr 10.0.0.2/24", "☞장비 IP설정"],
        ["V5924B(config)# ip route 0.0.0.0/0 10.0.0.1", "☞DEFAULT G/W설정"],
        ["V5924B# show ip", "☞장비 IP설정 확인"]
    ]
    ### Hostname 및 Password 설정
    data1 = [
        ["SWITCH# conf t",""],
        ["SWITCH(config)# hostname V5924B", "☞장비명 변경"],
        ["V5924B(config)# passwd", "☞패스워드 설정"],
        ["V5924B(config)# passwd enable test", "☞enable 패스워드 설정"],
        ["V5924B(config)# no passwd enable", "enable 패스워드 초기화"]
    ]
    ### Filter 설정
    data2 = [
        ["V5924B# conf t",""],
        ["V5924B(config)# br", ""],
        [f"V5924B(bridge)# dhcp-server-filter {port_min}-{port_max}", f"☞dhcp 필터기능을 번포트 적용"],
        ["V5924B(bridge)# netbios-filter 1-26", "☞netbios 필터기능을 전체 포트에 적용"],
        ["★UPLINK 또는 STACK된 장비와 연결된 포트에는 설정하지 않도록 주의 ★"]
    ]
    ### MAX-host 개수 제한 
    data3 = [
        ["V5924B# conf t", ""],
        ["V5924B(config)# br", ""],
        [f"V5924B(bridge)# max-host {port_min}-{port_max} 1", f"☞{port_min}-{port_max}번 포트의 MAC을 1개로 설정"],
        ["V5924B(bridge)# no max-hosts 25", "☞25번 포트 MAC 수 제한 해제"],
        ["★UPLINK 또는 STACK된 장비와 연결된 포트에는 설정하지 않도록 주의 ★"]
    ]
    ### MLOOP 방지 설정 (loop-detect 설정)
    data4 = [
        ["V5924B# conf t", ""],
        ["V5924B(config)# br", ""],
        ["V5924B(bridge)# set loop-detect srcmac laa", ""],
        ["V5924B(bridge)# set loop-detect enable", ""],
        ["V5924B(bridge)# set loop-detect 1-24", ""],
        ["V5924B(bridge)# set loop-detect 1-24 block", ""],
        ["V5924B(bridge)# set loop-detect 1-24 period 2", ""],
        ["V5924B(bridge)# set loop-detect 1-24 timer 300", "☞loop 감지를 위한 패킷을 2초단위로 전송후 loop 감지시 해당 포트를\nblock 시킨후 block 된 포트는 300초후 자동 해제됨"],
        ["★UPLINK 또는 STACK된 장비와 연결된 포트에는 설정하지 않도록 주의 ★"]
    ]
    ### 24번 포트를 Port  Stacking으로 구성시 주의해야 할 설정
    data5 = [
        ["V5924B# conf t", ""],
        ["V5924B(config)# br", ""],
        ["V5924B(bridge)# no storm-control broadcast 24", ""],
        ["V5924B(bridge)# no storm-control multicast 24", ""],
        ["V5924B(bridge)# no storm-control dlf 24", ""],
        ["V5924B(bridge)# no mac-flood-guard 24", ""],
        ["V5924B(bridge)# no loop-detect 24", ""],
        ["V5924B(bridge)# no loop-detect 24 block", ""],
        ["V5924B(bridge)# no dhcp-server-filter 24", ""],
        ["V5924B(bridge)# no max-hosts 24", ""],
        ["V5924B(config)# no ip igmp filter port 24 packet_type", ""],
        ["V5924B(config)# no cpu-flood-guard 24 ", ""],
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
    
    st.markdown('<div class="title">MLOOP 방지 설정 (loop-detect 설정)</div>', unsafe_allow_html=True)
    components.html(generate_table_html(data4, "table5"), height=400, scrolling=True)
    
    st.markdown('<div class="title">24번 포트를 Port Stacking으로 구성시 주의해야 할 설정</div>', unsafe_allow_html=True)
    components.html(generate_table_html(data5, "table6"), height=400, scrolling=True)

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


def V5924_w_page():
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
        ["show cpuload\nshow cpu-trueload", "CPU 부하율을 확인(5초,1분,10분단위)"],
        ["show vlan", "Vlan정보확인"],
        ["show running-config", "스위치의 설정 내용을 확인"],
        ["show flash", "FLASH 메모리 상태 확인"],
        ["show syslog local volatile", "RAM에 저장된시스템 로고메세지(휘발성)를 보여줌\n☞RESET 되기전 까지의 내용출력"],
        ["show syslog local non-volatile", "비휘발성 메모리(NVRAM)에 저장된 syslog 메시지를 확인"],
        ["show mac", "전포트 가입자 MAC 어드레스 조회"],
        ["show interface", ""],
        ["show arp", ""],
        ["show clock", ""],
        ["show port 1-26", ""],
        ["conf t\nbridge\nport disable 1(포트번호)\nport enable 1(포트번호)", "특정 포트 리셋 (활성화/ 비활성화)\n\n☞예: 1번포트 비활성화\n☞예: 1번포트 활성화"],
        ["show port statistics avg\nshow port statistics avg-pkt 1(포트 번호)", "포트트래픽통계\n☞지정포트의 평균 트래픽을 출력\n포트번호(1~24:이더넷,25번:WAN)\n지정포트에 대한5초,1분,10분에 대한 트래픽량에 대한 통계값"],
        ["show port statistics avg-type 1(포트 번호)", "포트 패킷유형별 트래픽통계\n☞지정포트의 패킷유형별 평균 트래픽을 출력\n패킷유형(unicast,multicast,broadcast), 단위: pps\n지정포트에 대한5초,1분,10분에 대한 트래픽량에 대한 통계값"],
        ["show port statistics rmon 25(포트번호)", "포트별 인터페이스 MIB,CRC정보를 확인"],
        ["conf t\nclear port statistics all(포트번호)", "포트통계초기화"],
        ["show ip route", "라우팅 경로 확인"],
        ["show loop-detct", "포트별 looping 상태 감지 확인"],
        ["show mac-flood-guard macs", "Mac flood-guard에 적용되어 차단된 MAC 확인"],
        ["show  ip igmp snooping\nshow  ip igmp snooping group\nshow  ip igmp snooping mrouter\nshow  ip igmp snooping querier", "IGMP Snooping 기능을 활성화 되어 있는지 확인\n가입자의 multicast 그룹 확인\nmulticast router 확인\nsnooping querier 포트 확인"],
        ["show ip dhcp snooping binding", "사용중인 가입자 IP, MAC 확인"],
        ["show netbios-filter ", "NetBIOS 필터링 설정 조회"],
        ["show dhcp-server-filter", "DHCP 필터링 설정 조회"],
        ["show max-hosts ", "MAC Address 개수 제한 조회"],
        ["conf t\nbridge\nmax-hosts 1 3\nno max-hosts 25", "MAC수 제한설정\n\n☞예:1번포트->Mac 제한 3개로 설정\n☞uplink 포트 Mac제한 무제한설정"],
        ["show lre line-config-profile\nconf t\nbridge\nset line-config-profile lite50_0 add 3\nset line-config-profile lite50_0 del 3", "가입자 포트에 적용된 프로파일 확인\n\n가입자포트에 프로파일 적용\n(예:3번포트->프로파일 lite50_0 설정)\n(예:3번포트에 적용된  프로파일 lite50_0 해제) "],
        ["show lre line-config-profile\nshow lre 1(포트번호)\nshow lre profile 1(포트번호)", "가입자 포트에 적용된 프로파일 확인\n가입자 포트에 대한 정보 확인\n☞link, speed, snr margin,감쇄, 프로파일등"],
        ["show lre stat-correctable-crc 3 (포트번호)\nshow lre stat-uncorrectable-crc 3(포트번호)\nshow lre stat-count-all \nshow lre stat-lof 3 (포트번호)\nshow lre stat-los 3 (포트번호)\nshow lre stat-lol 3 (포트번호)", "가입자 포트의 수정이 가능한 CRC 개수 확인\n가입자 포트의 수정이 불가능한 CRC 개수 확인\n가입자 포트의 link 상태 확인\n☞손실된 frame 개수 \n☞손실된 signal 갯수\n☞link가 끊어진 횟수"],
        ["conf t\nbridge\nrate 5 8", "\n가입자 포트에 일정한 대역 폭을 설정 하는 기능\n(예:5번포트->8Mbps 대역폭 설정)"],
        ["show cpe 1 (포트번호)", "가입자 모뎀 상태 확인"],
        ["show status fan", "FAN의 이원화 상태 확인"],
        ["show status temp", "시스템 온도 확인"],
        ["conf t \nrestore factory-defaults", "공장초기값 설정"],
        ["reload", "시스템 리부팅"]
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

def V5924_command_page():
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
int vlan 1
no shutdown
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
        V5924_home_page()
    elif choice == "기본 설정":
        V5924_e_page()
    elif choice == "조회 명령어":
        V5924_w_page()
    elif choice == "커맨드 생성":
        V5924_command_page()

if __name__ == "__main__":
    main()
# %%
