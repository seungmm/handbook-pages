#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import pyperclip
from PIL import Image
import streamlit.components.v1 as components


def IRT800_home_page():
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

    st.markdown('<div class="title">IRT800</div>', unsafe_allow_html=True)

    #IMG
    image_path = "C:\\Users\\이창렬\\Desktop\\l2\\0404\\장비사진\\IRT800.PNG"

    try:
        img = Image.open(image_path)

        # 이미지 중앙 배치
        # st.markdown('<img src="data:image/png;base64,{}" class="centered-image" width="1250" />'.format(
            # img_to_base64(img)), unsafe_allow_html=True)
        
        st.markdown('<div style="text-align: center;">'
            '<img src="data:image/png;base64,{}" style="width:65%; border-radius:10px;" />'
            '</div>'.format(img_to_base64(img)),
        unsafe_allow_html=True
    )
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

def IRT800_e_page():
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
    data = """IRT800> set-ip:
 [MEND] Node IP (Node IP address)  => 10.0.0.2              ☞장비 IP설정
 [OPT] Netmask (netmask)  => 255.255.255.0                  ☞Netmask 설정
 [OPT] Gateway (gateway)  => 10.0.0.1                       ☞DEFAULT G/W설정
 COMMAND] SET-IP: 10.0.0.2, 255.255.255.0, 10.0.0.1
 IRT800> [2002/11/08 20:52:27 SET SYSBASICIP INFOMATION] OK
        Node IP : 10.0.0.2
        NetMask : 255.255.255.0
        GateWay : 10.0.0.1
IRT800> system:                                          ☞설정 상태 확인
IRT800> ping:                                            ☞DNS로 ping test 실시"""

    #df = pd.DataFrame(data, columns=["명령어"])

#Hostname 및 Password 설정
    data1 = """IRT800> chg-pwd                                ☞패스워드 설정
  Enter Old Password : irts                    ☞기존 패스워드 입력 (예:irts)
  Enter new password : test                    ☞새로운 패스워드 입력 (예:test)
  ReEnter new password : test
 [2007/12/12 17:58:10 CHANGE
 PASSWOAD] OK"""

    #df1 = pd.DataFrame(data1, columns=["명령어", "설명"])

#DHCP Filter 설정
    data2 = """IRT800> set-dhcp:00FFFFFFFFFFFFF00                  ☞dhcp 필터기능 적용
IRT800> rtrv-dhcp                                   ☞dhcp 필터기능 확인"""

    #df2 = pd.DataFrame(data2, columns=["명령어", "설명"])

#NETBIOS Filter 설정
    data3 = """IRT800> set-netbeui:00FFFFFFFFFFFFF00                   ☞netbios 필터기능 적용
IRT800> rtrv-netbeui                                    ☞netbios 필터기능 확인"""

#SNMP COMMUNITY 설정
    data4 = """IRT800> set-community:
 [MEND] GET (get community)  => public                 ☞read 권한의 SNMP 설정
 [MEND] SET (set community)  => private                ☞write 권한의 SNMP 설정
 COMMAND] SET-COMMUNITY: PUBLIC, PRIVATE
IRT800> rtrv-community;                                ☞SNMP 설정된 상태 확인"""

#가입자 포트 활성화/비활성화
    data5 = """IRT800> set-block:3,1                   ☞가입자 2번 카드 1번 포트 비활성화
IRT800> set-unblock:3,1                 ☞가입자 2번 카드 1번 포트 비활성화 
 
※ 보드 번호 설명
     - SLOT 1번 : SWU 보드(Uplink 보드)
     - SLOT 2번 :  ACU 보드(가입자보드) 1번카드"""


#MAX-host 개수 제한
    data6 = """IRT800> set-mac:
 [MEND] SLOT ID  [1 .. 16] => 5         ☞4번 카드 1번포트 MAC갯수 3개로 설정
 [MEND] CHID  [1 .. 4] => 1
 [MEND] Action (add:1, del:2)  [1 .. 2] => 1
 [OPT] Type (static:1, dynamic:2)  [1 .. 2] => 2
 [OPT] LeaseTime (unit: minute)  => 0
 [OPT] FilterNo (off:0, no1:1, no2:2, no3:3, no4:4, no5:5 [0..5] => 3 ☞MAC갯수
 [OPT] macAddr 1 (mac addr1 : 20 0A 22 04 ff ac)  => Enter키
  COMMAND] SET-MAC: 5, 1, 1, 2, 0, 3"""

#가입자 포트에 프로파일 설정
    data7 = """IRT800> set-subs:
  [MEND] SLOT ID  [1 .. 16] => 6           ☞설정할 가입자 카드 입력(예:ACU5번)
  [MEND] CH ID  [1 .. 4] => 1                    ☞설정할 가입자 포트 번호 입력
  [MEND] action (add:1, del:2, update:5)  => 1
  [OPT] Subs Address  => TEST        
  [OPT] LineType (vdsl:1, sdsl:2, adsl:3, g.shdsl:4)  => 3
  [OPT] ProfileName (Line Profile)  => LITE1     ☞적용할 프로파일명 입력
  [OPT] AlarmProfileName (Alarm Profile)  => DEFAULT
  [OPT] memo (some info. of subs)  => TESTUSER
   COMMAND] SET-SUBS: 6, 1, 1, TEST, 3, LITE1, DEFAULT, TEST
  IRT800> [2099/02/14 01:25:33 SET SUBS INFOMATION] OK, ADD"""
    
#정전후 백업값이 없어 졌을 때 조치방법
    data8 = """정전후 백업값이 없어졌을 때 초기값으로 재설정 해야한다.
   ☞ 이 명령어는 응급상황이 아닐때는 사용하지않도록 한다.
 
디폴트로 가입자를 설정하는 방법이다. 아래의 순서대로 작업한다.
 1. 디폴트값 속도(DOWN=8064k,UP=1024k)를 가입자 전 채널에 설정한다.
      IRT800> IHP:MAKESUBS     
 2. 한 채널씩PVC 값 0,32를 설정해 주어야 한다.
     PVC값이 설정이 끝나면 기본적으로 서비스 할 수 있다   
      IRT800> set-pvc:   """
    
#패스워드 복구 및 장비 초기화
    data9 = """운용중인 장비는 반드시 기존 DATA를 BACK-UP을 해둔다.
  ☞ default로 password는 복구되지만 모든 데이터는 다 손실됨 ( 공장 초기화 됨)
        
아래의 순서대로 작업한다.
 1. CONSOLE접속후 REBOOT후 count초(5 4 3 2 1) 나올때 엔터키를 입력한다.
      Press any key to stop auto-boot...
      2
 2. VxWorks Boot창이 나온다
    [VxWorks Boot]: f0x30000000,0x20000,0x0              ☞장비 공장초기화됨
 3. rebooting 시킨다.
    [VxWorks Boot]: a                                    ☞Rebooting 명령
 4. 장비 MAC을 설정한다.
     ctrl 보드를 빼면 hanbit메모리칩에 메모리 숫자가 써져있다.(16-67)
     창으로 가서
     N
     A  (MAC을 늘수 있다)
     00- 00  (일륭 장비측 default mac으로 자동으로 올라옴)
     0a- 0a  (일륭 장비측 default mac으로 자동으로 올라옴)
     0f-  0f   (일륭 장비측 default mac으로 자동으로 올라옴)
     00- 03  (default값 무조건 넣어주어야 함)
     00- 16  (메모리 숫자)
     00- 67  (메모리 숫자)
     a   (rebooting 명령어)"""

    st.markdown('<div class="title">장비 IP 및 Default-Gateway 설정</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.code(data)  
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="title">Hostname 및 Password 설정</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.code(data1)
        st.image("C:/Users/이창렬/Desktop/l2/0404/장비사진/IRT.png", width=600)
        st.image("C:/Users/이창렬/Desktop/l2/0404/장비사진/IRT2.png", width=300)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="title">DHCP Filter 설정</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.code(data2)
        st.image("C:/Users/이창렬/Desktop/l2/0404/장비사진/IRT3.png", width=600)
        st.image("C:/Users/이창렬/Desktop/l2/0404/장비사진/IRT4.png", width=300)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="title">NETBIOS Filter 설정</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.code(data3)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="title">SNMP COMMUNITY 설정</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.code(data4)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="title">가입자 포트 활성화/비활성화</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.code(data5)
        st.markdown('</div>', unsafe_allow_html=True)   
    
    st.markdown('<div class="title">MAX-host 개수 제한</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.code(data6)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="title">가입자 포트에 프로파일 설정</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.code(data7)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<p style="font-weight:bold; font-size:18px;">긴급복구요령</p>', unsafe_allow_html=True)

    st.markdown('<div class="title">정전후 백업값이 없어 졌을 때 조치방법</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.code(data8)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="title">패스워드 복구 및 장비 초기화</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.code(data9)
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

def IRT800_w_page():
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
    ["help", "전체 사용가능한 명령어와 설명 조회"],
    ["rtrv-ip", "시스템의 IP 설정 상태 조회"],
    ["system\nver", "시스템의 IP 설정 상태 및 장비 UPTIME 확인 가능"],
    ["rtrv-shelf", "SHELF에 실장된 유니트 확인"],
    ["rtrv-slot:", "장비에 실장된 유니트의 버전 및 상태 확인"],
    ["rtrv-swu;1", "SWU 정보 조회"],
    ["rtrv-mcu", "장비 MCU 보드 상태 및 버젼 확인"],
    ["rtrv-community", "SNMP 사용을 위한 READ/ WRITE 권한 COMMUNITY값 확인"],
    ["rtrv-alarm", "경보 조회"],
    ["ping: 168.126.63.1, 5;", "PING TEST 실시 ( 예: 168.126.63.1로 5회 ping test 실시)"],
    ["rtrv-subs:\nrtrv-subs: 2,3", "가입자설정 상태 조회 ( 포트 Up/Down, 설정된 Profile 명 확인 가능)\n( 예: 1번 가입자 카드 (ACU 1번) 3포트 확인 )\n☞ SLOT 1번 : SWU 보드(Uplink 보드)\n☞ SLOT 2번 : ACU 보드(가입자보드) 1번카드"],
    ["set-block:2,3\nset-unblock:2,3", "가입자 포트 비활성화 ( 예: 1번 가입자 카드 (ACU 1번) 3포트 비활성화 )]\n가입자 포트 활성화 ( 예: 1번 가입자 카드 (ACU 1번) 3포트 활성화 )"],
    ["rtrv-mac", "가입자 포트 전체 설정된 MAC 갯수 확인"],
    ["rtrv-cu:2", "가입자카드 1번(ACU 1번) 상태 조회\n☞CH1 LED : 010 숫자는 ACT,LINK,SYNC값을 나타낸다.\n    \"0\"은 비활성화, \"1\"은 활성화 상태 의미한다."],
    ["rtrv-adsl-profile", "장비에 설정된 프로파일 조회"],
    ["rtrv-chconf:2,3", "각 포트별 설정된 프로파일 및 가입자가 할당받은 IP조회도 가능하다.\n☞모뎀 연결된 경우의 현재속도 조회 ( 예: 가입자카드 1번의 3번포트 )"],
    ["rtrv-pm:\nrtrv-pm:2,3,5", "각 포트별 성능 조회\n( 예: 가입자카드 1번의 3번포트의 total 트래픽 조회 )"],
    ["reboot", "MCU유니트만 리셋 된다.\n☞장비 전체를 리셋하고자 할 때는 전원을 스위치를 on/off 한다."],
    ["backup:show:subs", "IRT-800후면에 있는 CTRL카드 NVRAM에 정상적으로 가입자 정보가 저장이 되어있는지 확인\n☞주의: 저장된 내용이 없는 경우는 장비 전원 재부팅시 가입자 정보가 손실되어 초기화 됨"],
    ["backup:show:mac", "IRT-800후면에 있는 CTRL카드 NVRAM에 정상적으로 mac 수 정보가 저장이 되어있는지 확인\n☞주의: 저장된 내용이 없는 경우는 장비 전원 재부팅시 mac수 정보가 손실되어 초기화 됨"]
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

def IRT800_command_page():
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
set-ip:
{ip_address}
{subnet_mask}
{gateway}
system:
ping:
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
        IRT800_home_page()
    elif choice == "기본 설정":
        IRT800_e_page()
    elif choice == "조회 명령어":
        IRT800_w_page()
    elif choice == "커맨드 생성":
        IRT800_command_page()

if __name__ == "__main__":
    main()