#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import pyperclip
from PIL import Image
import streamlit.components.v1 as components


def DX6524_home_page():
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

    st.markdown('<div class="title">E5624R 장비</div>', unsafe_allow_html=True)

    #IMG
    image_path = "C:\\Users\\이창렬\\Desktop\\l2\\0404\\장비사진\\DX6524.PNG"
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

def DX6524_e_page():
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
#장비 IP 및 Default-Gateway 설정
    data = """DX6524> pm
 Enter Privileged Command Mode Password : ******            ☞pm 패스워드 입력
 Privileged command mode is turned on.
DX6524$;
DX6524$ ip if delete bridge                                 ☞ip설정
 Change will have no effect until after config save and restart.
DX6524$ ip if add bridge 10.0.0.2  10.0.0.1 255.255.255.0   ☞ip G/W Netmask
 Change will have no effect until after config save and restart.
DX6524$ wr                                                  ☞시스템 설정 저장
 Saving configuration...
 Configuration saved.
DX6524$ sr
 Reboot now? (Y/N) y
 REBOOTING...."""

    #df = pd.DataFrame(data, columns=["명령어"])

#Hostname 및 Password 설정
    data1 = """DX6524> pm
 Enter Privileged Command Mode Password : ******
 Privileged command mode is turned on.
DX6524$ snmp sn TEST                           ☞시스템 이름 설정 (예: TEST)
 System name changed to Corecess
TEST$
 
DX6524$ st set 2001 10 17 wed 18 10 00         ☞날짜,시간 설정
 System Date: 2001.10.17 (wed) Time-18:10:00
DX6524$ pass                                   ☞패스워드 설정
 Changing console login password.
 Enter current password : ******
 Enter new password : ****
 Re-enter new password : ****
 Password changed.
 To save, execute 'WRite' at home
DX6524$ pmpass pass                            ☞ privileged mode 패스워드 설정
 Changing privileged mode password.
 Enter current password : ******
 Enter new password : ****
 Re-enter new password : ****
 Password changed.
 To save, execute 'WRite' at home
DX6524$ wr
 Saving configuration...
 Configuration saved."""

    #df1 = pd.DataFrame(data1, columns=["명령어", "설명"])

#Filter 설정
    data2 = """DX6524> pm
 Enter  privileged  Command  Mode  Password  : ******
 Privileged  command  mode  is  turned  on
DX6524$ ip                                            ☞ip 모드로 이동
DX6512 ip$ ipf ip on                                  ☞ip filtering기능 설정
 IP  Filtering  Control  setting  OK
DX6524 ip$ ipf netbios on                             ☞netbios 필터기능 설정
 IP Filtering Control setting OK
DX6524 ip$ ipf dhcp on                                ☞dhcp 필터기능 설정
 IP Filtering Control setting OK
DX6512 ip$ ipf  show                                  ☞필터기능 확인
 IP Only
 NetBIOS Deny
 DHCP Deny
DX6524 ip$ home  wr                                   ☞필터기능 설정 저장"""

    #df2 = pd.DataFrame(data2, columns=["명령어", "설명"])

#SNMP COMMUNITY 설정
    data3 = """DX6524$ snmp                                          ☞snmp 모드로 이동
DX6524 snmp$ ac read public                           ☞read 권한의 SNMP 설정
DX6524 snmp$ ac write private                         ☞write 권한 SNMP 설정
DX6524 snmp$ ac delete public                         ☞read 권한의 SNMP 삭제
DX6524 snmp$ ac                                       ☞SNMP 설정된 상태 확인"""

#가입자 포트 활성화/비활성화
    data4 = """DX6524$ chips                                         ☞chips 모드로 이동  
DX6524 chips$ spm 3 disable                           ☞3번 포트 비활성화
DX6524 chips$ spm 3 enable                            ☞3번 포트 활성화
DX6524 chips$ spm 3 reset
DX6524 chips$ spm show                                ☞설정 확인"""

#MAX-host 개수 제한
    data5 = """DX6524$ bridge                                  ☞bridge 모드로 이동
DX6524 bridge$ pom 1 4                          ☞1번 포트 MAC갯수 4개로 설정
DX6524 bridge$ pom all 5                        ☞전체 포트 MAC갯수 5개로 설정
DX6524 bridge$ pom                              ☞설정 확인"""

#가입자 포트에 속도 설정
    data6 = """DX6524$ chips                       ☞chips 모드로 이동  
DX6524 chips$ spm 3 4000 640        ☞3번 포트 속도 설정  Down(4000k)/Up(640k)
DX6524 chips$ spm all 8160 640      ☞전체 포트 속도 설정 Down(8160k)/Up(640k)
DX6524 chips$ spm show              ☞설정 확인"""

#시스템 초기설정을 구성마법사로 설정시 (IP, DHCP, NETBIOS))
    data7 = """DX6524$ su
 All configuration will be cleared. Are you sure?(Y/N) y
 To abort setup, enter ESC!
 Bridge(0)/PPPoA(1) ? 0                                ☞Bridge mode
 VPI ? ( 0-15) 0                                       ☞VPI = 0
 VCI ? ( 1-255 ) 32                                    ☞VCI = 32
 Enable packets transfer between ADSL ports ?(Y/N) y
 DX6524TA IP ? (dhcp/<IP>/<None-ENTER> 10.0.0.2        ☞IP 10.0.0.2
 Subnet ? (255.255.255.00) 255.255.255.0               ☞subnet 255.255.255.0
 Default gateway IP ? (<IP>/<None-ENTER>) 10.0.0.1     ☞Gateway 10.0.0.1
 Filtering : IP Only ?(Y/N) y
 Filtering : Netbios over TCP/IP deny ?(Y/N) y         ☞netbios 필터기능 설정
 Filtering : CPE DHCP deny ?(Y/N) y                    ☞dhcp 필터기능 설정"""
    
#시스템 초기화(공장초기화)
    data8 = """DX6524> pm
 Enter Privileged Command Mode Password : ******
 Privileged command mode is turned on.
DX6524$ cdef
 Are you sure? (Y/N) y
 Saving configuration...Configuration saved.
 All configuration is changed to factory default Warning ! : After the system
 rebooting, changed configuration will be appliedUpdating flash filing system  ...done
 REBOOTING....""" 

    st.markdown('<div class="title">장비 IP 및 Default-Gateway 설정</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.code(data)  
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="title">Hostname 및 Password 설정</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.code(data1)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="title">Filter 설정</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.code(data2)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="title">SNMP COMMUNITY 설정</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.code(data3)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="title">가입자 포트 활성화/비활성화</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.code(data4)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="title">MAX-host 개수 제한</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.code(data5)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="title">가입자 포트에 속도 설정</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.code(data6)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="title">시스템 초기설정을 구성마법사로 설정시 (IP, DHCP, NETBIOS))</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.code(data7)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="title">시스템 초기화(공장초기화)</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.code(data8)
        st.markdown('</div>', unsafe_allow_html=True)

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


def DX6524_w_page():
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
        ["ut", "시스템 UPTIME 정보확인"],
        ["sl show", "발생한 각종 이벤트에 대한 기록(로그)을 출력"],
        ["su\nip", "장비 초기 setup <br>(ip,pvc,filtering 설정등) 장비 IP조회"],
        ["help", "각 명령어를 조회"],
        ["ip\nipf show", "필터링 설정상태 조회<br>(IP 패킷, NetBIOS패킷, DHCP 서버 패킷)"],
        ["chips\npc\npc c", "가입자 포트의 트래픽 통계 조회 트래픽 통계 초기화"],
        ["chips\nai", "각 포트에 설정된 상태 조회 <br>(각 포트의 트래픽 정보와 에러가 발생한 횟수를 출력)"],
        ["chips\ncs\n cs all", "각 포트에 설정된 상태 조회 (링크상태,CRC,NoiseMazin,Attenation(감쇄량)조회)"],
        ["chips\nspm show", "각 포트에 설정된 상태 조회 <br> (속도 및 포트 활성화/비활성화(active/deactive) 상태)"],
        ["bridge\npom 1 4\npom all 5\npom", "모든포트(or 포트별) MAC 갯수 제한 설정 <br> ☞1번 포트 MAC갯수 4개로 설정 <br> ☞전체 포트 MAC갯수 5개로 설정"],
        ["chips\nsm show\nsm all 1", "특정 포트의 MAC address확인 <br> ☞3번 포트 MAC address조회 <br> ☞모든 포트 MAC address조회"],
        ["chips\nspm 3 disable\nspm 3 enable\nspm 3 reset\nspm show", "Line Mode 조회(fast/interleaved) <br> 모든 포트의 라인모드를 interleaved방식으로 설정 <br> sm all(port) <0:fast mode><1:interleaved mode>"],
        ["chips\nspm 3 4000 640\nspm all 8160 640\nspm show", "포트 비활성화 '(예 : 3번 포트 disable)' <br> 포트 활성화 (예 : 3번 포트 enable) <br> 포트 리셋(Reset)"],
        ["chips\nnm 15 8 0 8 0", "포트별 다운,업 속도 변경 <br> SetPortMode<port><max_downstream><max_upstream> <br> (예: 전체 포트 속도 설정 Down(8160k)/Up(640k) )"],
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

def DX6524_command_page():
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
            cidr = subnet_mask
            if cidr:
                commands = f"""
pm
dx6524
ip if delete bridge
int vlan1
ip if add bridge {ip_address} {gateway} {cidr}
wr
sr
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
    st.sidebar.title("E5624R 장비 핸드북")
    menu = ["홈", "기본 설정", "조회 명령어", "커맨드 생성"]
    choice = st.sidebar.selectbox("메뉴", menu)

    if choice == "홈":
        DX6524_home_page()
    elif choice == "기본 설정":
        DX6524_e_page()
    elif choice == "조회 명령어":
        DX6524_w_page()
    elif choice == "커맨드 생성":
        DX6524_command_page()

if __name__ == "__main__":
    main()