#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import pyperclip
from PIL import Image
import streamlit.components.v1 as components


def EX1172LR_home_page():
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
            padding: 0px;
            border-radius: 0x;
            text-align: left;
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
    ### EX1172LR 장비
    st.markdown('<div class="title">EX1172LR 장비</div>', unsafe_allow_html=True)
        
    ### EX1172LR 스위치 콘솔 접속방법    
    st.markdown('<div class="title2">■ EX1172LR 스위치 콘솔 접속방법</div>', unsafe_allow_html=True)
    data = [["9600", "8", "N", "1", "없음", "root", "admin100"]]
    columns = ["SPEED", "DATA BIT", "PARITY BIT", "STOP BIT", "FLOW CONTROL", "초기 LOGIN ID","Password"]
    df = pd.DataFrame(data, columns=columns)
    # 정적 테이블(수정 불가)
    st.dataframe(df, hide_index=True)
    
    ### EX1172LR 장비 형상
    st.markdown('<div class="title2">■ EX1172LR 장비 형상도</div>', unsafe_allow_html=True)
    image_path = "C:\\Users\\Ohseungmin\\handbook\\장비사진\\EX1172LR.png"  # 이미지 경로를 수정
    try:
        img = Image.open(image_path)
        
        st.markdown('<img src="data:image/png;base64,{}" class="centered-image" width="850" />'.format(
            img_to_base64(img)), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"이미지를 로드하는 데 실패했습니다: {e}")
    st.markdown('<div class="title3">◈ 시스템 소요량 산출<br>&nbsp;&nbsp;&nbsp;-1 셀프 FULL 실장시 72회선 -> 스위치 보드당 24회선, VDSL 보드당 8회선</div>', unsafe_allow_html=True)
    
    ### EX1172LR 장비 형상
    st.markdown('<div class="title2">■ 장비구조(전체 실장시)</div>', unsafe_allow_html=True)
    image_path = "C:\\Users\\Ohseungmin\\handbook\\장비사진\\EX1172LR_structure.png"  # 이미지 경로를 수정
    
    try:
        img = Image.open(image_path)
        st.markdown('<img src="data:image/png;base64,{}" class="centered-image" width="1250" />'.format(
            img_to_base64(img)), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"이미지를 로드하는 데 실패했습니다: {e}")
        
    st.markdown('<div class="title3"><br>◈ PDU(Power Distribution Unit) x 2 유니트 (AC/DC,  DC/DC)</div>', unsafe_allow_html=True)
    st.markdown('<div class="title3">◈ VDL(VDSL Unit) x 9 유니트 : 각 유니트당 VDSL 8채널 수용</div>', unsafe_allow_html=True)
    st.markdown('<div class="title3">◈ LSW(Line Switching Unit) x 3 유니트 : 각 유니트당 24 VDSL 포트 지원<br>&nbsp;&nbsp;&nbsp;- LSW1번 VDL1~VDL3번 카드 지원<br>&nbsp;&nbsp;&nbsp;- LSW2번 VDL4~VDL6번 카드 지원<br>&nbsp;&nbsp;&nbsp;- LSW3번 VDL7~VDL9번 카드 지원<div>', unsafe_allow_html=True)
    st.markdown('<div class="title3">◈ MCP(Main Control Processor) x 1 유니트 :시스템 운용관리 및 제어</div>', unsafe_allow_html=True)
    
    
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

    html += """
            </table>
        </div>
    </div>
    """
    return html

def EX1172LR_e_page():
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
    
    ### EX1172LR 초기 설정    
    st.markdown('<div class="title2">■ EX1172LR 초기 설정 명령</div>', unsafe_allow_html=True)
    image_path = "C:\\Users\\Ohseungmin\\handbook\\장비사진\\EX1172LR_초기설정.png"  # 이미지 경로를 수정
    try:
        img = Image.open(image_path)
        
        # 이미지 중앙 배치
        st.markdown(
    '<img src="data:image/png;base64,{}" style="display: block; margin-left: auto; margin-right: auto;" width="650" />'.format(
        img_to_base64(img)),unsafe_allow_html=True)
    except Exception as e:
        st.error(f"이미지를 로드하는 데 실패했습니다: {e}")
        
    data = [
        ["LOGIN> act-user:root:admin100;", "☞로그인 방법(패스워드가 admin100인경우)"],
        ["EX1172> set-sys-net::10.0.0.2,255.255.255.0,10.0.0.1; ", "☞장비 IP설정 ( 명령어 =>set-sys-net::장비IP,netmask,장비G/W; )"],
        ["EX1172> rtrv-sys-net::;", "☞장비 IP 설정 확인"],
        ["EX1172> ping::168.126.63.1,5;", "☞장비 DNS까지 ping 시험\n( 명령어 => ping::IP입력,횟수; )"]
    ]

    data1 = [
        ["LOGIN> act-user:root:admin100;", "☞로그인"],
        ["DSLAM.0> set-sysname::EX1172;", "☞장비명 변경 ( 예 : EX1172로 변경 )"],
        ["EX1172> set-password::test;", "☞패스워드 변경 ( 예 : test로 변경 )"]
    ]
    data2 = [
        ["EX1172> set-net-filter::on;", "☞netbios 필터기능을 전체 포트에 적용"],
        ["EX1172> set-dhcp-filter::on;", "☞dhcp 필터기능을 전체 포트에 적용"],
        ["EX1172> rtrv-bridge-status::;", "☞설정 상태 확인"]
    ]
    data3 = [
        ["EX1172> rtrv-mac-limit:vdl:;", "☞가입자 보드 1번 보드(vdl1)의 mac 개수 확인"],
        ["EX1172> set-mac-limit-all::1;", "☞가입자 전체 MAC을 1개로 설정"],
        ["EX1172> set-mac-limit:vdl1-p7:4;", "☞vdl 1번 보드의 7번 포트 MAC 4개로 설정"]
    ]
    data4 = [
        ["EX1172> rtrv-community-list::;", "☞SNMP 설정된 상태 확인"],
        ["EX1172> add-community::\"public\",read_only;", "☞ read 권한의 SNMP 설정"],
        ["EX1172> add-community::\"private\",read_write;", "☞write 권한의 SNMP 설정"],
        ["EX1172> del-community::번호;", "☞ 설정된 community를 삭제"]
    ]
    data5 = [
        ["EX1172> rtrv-profile-list::config;", "☞시스템전체의 프로파일 확인"],
        ["EX1172> set-line-profile:vdl2-p3:config,LITE50_0", "☞vdl 2번 보드의 3번포트 LITE50_0 프로파일 적용"],
        ["EX1172> rtrv-port-status:vdl1:;", "☞vdl 1번 보드 상태 확인"],
    ]
    data6 = [
        ["EX1172> rtrv-port-status:vdl1:;", "☞vdl 1번 보드의 상태확인 (UP, 설정된 profile명)"],
        ["EX1172> rtrv-port-status:lsw1:;", ""],
        ["EX1172> set-unit-act:vdl1:act;", "☞vdl 1번 보드 활성화"],
        ["EX1172> set-unit-act:vdl1:deact;", "☞vdl 1번 보드 비활성화"],
        ["EX1172> set-port-act:vdl1-p1:act;", "☞vdl 1번 보드의 1번포트 활성화"],
        ["EX1172> set-port-act:vdl1-p1:deact;", "☞vdl 1번 보드의 1번포트 비활성화"]
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
    
    st.markdown('<div class="title">SNMP 설정 확인</div>', unsafe_allow_html=True)
    components.html(generate_table_html(data4, "table5"), height=400, scrolling=True)
    
    st.markdown('<div class="title">가입자 포트 프로파일 설정</div>', unsafe_allow_html=True)
    components.html(generate_table_html(data5, "table6"), height=400, scrolling=True)
    
    st.markdown('<div class="title">가입자 포트 활성화 / 비활성화</div>', unsafe_allow_html=True)
    components.html(generate_table_html(data6, "table7"), height=400, scrolling=True)

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


def EX1172LR_w_page():
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
        ["show sysinfo", "시스템 정보 확인(버전,Uptime)"],
        ["help::sys;","명령어에 대한 도움말 검색"],
        ["rtrv-sysinfo::;","시스템 정보 확인 (Uptime, 시스템명, 버전)"],
        ["rtrv-cpu-load::;","CPU 부하율을 확인(5초,10초,1분단위)"],
        ["rtrv-memory::;","시스템 Memory 사용율 확인"],
        ["rtrv-alarm::;\nEX1172> rtrv-alarm-log::;\nEX1172> init-alarm-log::;\nEX1172> rtrv-event-log::;","시스템 경보 확인\n시스템 경보 이력 확인\n시스템 경보 초기화\n시스템 Event 확인"],
        ["rtrv-sys-netinfo::;","시스템 IP주소, MAC주소, Gateway주소 확인"],
        ["set-sys-net::10.0.0.2,255.255.255.0,10.0.0.1;","장비 IP설정 (set-sys-net::[장비IP],[netmask],[장비G/W];)"],
        ["ping::168.126.63.1,10;","시스템의 네트워크 상태 확인"],
        ["rtrv-port-status:vdl1:;\nEX1172> rtrv-port-status:lsw1:;\nEX1172> rtrv-port-status-all:;","가입자보드 1번의 상태확인 ( UP, 설정된 profile명)\nUplink보드 1번의 상태확인\n전체 가입자 포트 상태 확인"],
        ["set-unit-act:vdl1:act;\nEX1172> set-unit-act:vdl1:deact;\nEX1172> set-port-act:vdl1-p1:act;\nEX1172> set-port-act:vdl1-p1:deact;","가입자보드(vdl) 1번 보드 활성화\n가입자보드(vdl) 1번 보드 비활성화\n가입자보드(vdl) 1번 보드의 1번포트 활성화\n가입자보드(vdl) 1번 보드의 1번포트 비활성화"],
        ["rtrv-bridge-status::;\nEX1172> set-net-filter::on;\nEX1172> set-dhcp-filter::on;","필터링 조회 ( DHCP, NETBIOS, IGMP등 )\nnetbios 필터기능을 전체 포트에 적용\ndhcp 필터기능을 전체 포트에 적용"],
        ["rtrv-mac-limit:vdl:;","가입자 보드 1번 보드(vdl1)의 mac 개수 확인"],
        ["set-mac-limit-all::1;\nEX1172> set-mac-limit:vdl1-p7:4;","MAC수 제한설정 (가입자 전체 MAC을 1개로 설정)\n☞예:가입자카드 1번 보드의 7번 포트 가입자 MAC 4개설정"],
        ["rtrv-mac-table:vdl-p1~vdl9-p8:;\nEX1172> rtrv-mac-table:vd3-p4:;","전체 가입자의 mac address 확인\n☞예:3번가입자 카드 4번포트 MAC Address 확인"],
        ["rtrv-modem-status:vdl1-p1:;\nEX1172> rtrv-vdsl-linerate-all::;\nEX1172> rtrv-vdsl-linerate:vdl1:;","가입자 모뎀 상태 확인(예: 가입자 1번보드 1번 포트)\n전체 가입자 포트의 Link 속도 확인\n가입자 보드 1번의 Link 속도 확인"],
        ["rtrv-profile-list::config;\nEX1172> set-line-profile:vdl2-p3:config,LITE50_0;\nEX1172> rtrv-port-status:vdl1:;","시스템전체의 프로파일 확인\n가입자보드(vdl) 2번 보드의 3번포트에 LITE50_0 프로파일 적용\n☞예: vdl-1번 보드 상태 확인"],
        ["rtrv-traffic-load:vdl1:;\nEX1172> rtrv-traffic-load:lsw1:;","가입자 포트 트래픽 확인 (예:가입자 보드 1번)\nUplink 보드의 트래픽 상태 확인"],
        ["rtrv-community-list::;\nEX1172> add-community::\"public\",read_only;\nEX1172> add-community::\"private\",read_write;\nEX1172> del-community::번호;","시스템의 SNMP 설정 상태 확인\n시스템의 읽기(read) 권한의 SNMP community 설정\n시스템의 쓰기(write) 권한의 SNMP community 설정\n설정된 community를 삭제"],
        ["rtrv-mcast-status::;\nEX1172> set-igmp-snoop::on;\nEX1172> set-mcast-aging::query,on;\nEX1172> set-igmp-proxy::on;","시스템의 Multicast 설정 상태 확인\nIGMP Snooping 활성화\nMulticast Aging 설정\nIGMP Proxy 활성화"],
        ["init-system::cold;\n","공장초기값 설정 (장비 IP 설정만 유지됨)"],
        ["init-system::warm;","시스템 리부팅"]
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

def EX1172LR_command_page():
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
    if "id" not in st.session_state:
        st.session_state["id"] = ""
    if "password" not in st.session_state:
        st.session_state["password"] = ""
        
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
        
    col5, col6 = st.columns(2)
    with col5:
        id = st.text_input("로그인 ID 입력", value=st.session_state["id"], key="id_input")
    with col6:
        password = st.text_input("로그인 PASSWORD 입력", value=st.session_state["password"], key="password_input")
        
    # 값 변경 시 자동으로 session_state 업데이트
    if ip_address != st.session_state["ip_address"]:
        st.session_state["ip_address"] = ip_address
    if subnet_mask != st.session_state["subnet_mask"]:
        st.session_state["subnet_mask"] = subnet_mask
    if gateway != st.session_state["gateway"]:
        st.session_state["gateway"] = gateway
    if id != st.session_state["id"]:
        st.session_state["id"] = id
    if password != st.session_state["password"]:
        st.session_state["password"] = password

    # 버튼을 누를 때 새로고침 없이 상태를 유지하도록 session_state에 저장
    if st.button("커맨드 생성"):
        if ip_address and subnet_mask and gateway:
            cidr = subnet_mask_to_cidr(subnet_mask)
            if cidr:
                commands = f"""
act-user:{id}:{password};
set-sys-net:: {ip_address},{subnet_mask},{gateway};
rtrv-sys-net;;
ping::{ip_address}
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
        EX1172LR_home_page()
    elif choice == "기본 설정":
        EX1172LR_e_page()
    elif choice == "조회 명령어":
        EX1172LR_w_page()
    elif choice == "커맨드 생성":
        EX1172LR_command_page()

if __name__ == "__main__":
    main()
# %%
