#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import pyperclip
from PIL import Image
import streamlit.components.v1 as components


def HAMX6000_home_page():
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

    st.markdown('<div class="title">HAMX6000</div>', unsafe_allow_html=True)

    # V2724GB 장비 이미지 추가
    image_path = "C:\\Users\\이창렬\\Desktop\\l2\\0404\\장비사진\\HAMX.PNG"

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

def HAMX6000_e_page():
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
    data = """HAMX6000> mod bridgecfg
 <bridgecfg-shelf_id>[int,[M]|p(prev)]: 1
 <bridgecfg-slot_id>[int,[M]|p(prev)]: 16                  ☞DC형:16, AC형:12
 <bridgecfg-port>[int,[M]|p(prev)]: 2
 <bridgecfg-addr>[IP-addr,[O]|p(prev)]: 10.0.0.2           ☞장비 IP설정
 <bridgecfg-netmask>[IP-addr,[O]|p(prev)]: 255.255.255.0   ☞Netmask 설정
 <bridgecfg-gateway>[IP-addr,[O]|p(prev)]: 10.0.0.1        ☞DEFAULT G/W설정
 <bridgecfg-admin>[(up|down),[O]|p(prev)]: up              ☞인터페이스 활성화
 BRIDGE Set Success ...
 
HAMX6000> sh bridgecfg                                                            ☞설정확인
HAMX6000> ping 10.0.0.1
 PING 10.0.0.1 : 56 data bytes
 64 bytes from 10.0.0.1: icmp_seq=1 time= <10 ms
 64 bytes from 10.0.0.1: icmp_seq=1 time= <10 ms
 64 bytes from 10.0.0.1: icmp_seq=2 time= <10 ms"""

    #df = pd.DataFrame(data, columns=["명령어"])

#Hostname 및 Password 설정
    data1 = """DSLAM> conf prompt
 <prompt-prompt>[str,[M]|p(prev)]: HAMX6000             ☞장비명 HAMX6000 입력
 prompt change config. success .....
HAMX6000>                                ☞장비명 DSLAM에서 HAMX6000으로 변경됨
 
HAMX6000> mod user
 <users-name>[str,[M]|p(prev)]: root
 <users-level>[(user|admin),[M]|p(prev)]: admin
 Enter login password:
 New password: test                       ☞새로운 패스워드 입력(예:test)
 Re-enter New password: test
 login account modify successfully."""

    #df1 = pd.DataFrame(data1, columns=["명령어", "설명"])

#Filter 설정
    data2 = """HAMX6000> conf iwbrg
 <iwbrg-shelf>[int,[M]|p(prev)]: 1
 <iwbrg-slot>[int,[M]|p(prev)]: 14                 ☞CRUB 보드에 모두 설정
 <iwbrg-dhcp_filter>[(enable|disable)]: enable     ☞dhcp 필터기능 적용
 <iwbrg-net_bios_filer>[(enable|disable)]: enable  ☞netbios 필터기능 적용
 <iwbrg-vlan_mode>[(enable|disable),[O]|p(prev)]:
 <iwbrg-system_mode>[(stacking|direct_mapping|link_aggregatn),[O]|p(prev)]:
 <iwbrg-mac_access_timeout>[int,[O]|p(prev)]:
 <iwbrg-default_mac_cnt>[int,[O]|p(prev)]: 5       ☞MAC 갯수 5개로 일괄변경
 <iwbrg-max_igmp_response_time>[int,[O]|p(prev)]:
 mnet iwbrg config success...
 
HAMX6000> sh iwbrg                                            ☞dhcp,netbios 필터기능 설정 상태 확인"""

    #df2 = pd.DataFrame(data2, columns=["명령어", "설명"])

#MAX-host 개수 제한
    data3 = """HAMX6000> mod bind
 <bind-shelf>[int,[M]|p(prev)]: 1
 <bind-slot>[int,[M]|p(prev)]: 1
 <bind-port>[int,[M]|p(prev)]: 1
 <bind-vpi>[int,[M]|p(prev)]: 0
 <bind-vci>[int,[M]|p(prev)]: 32
 <bind-enet_port>[int,[O]|p(prev)]: enter(default) 
 <bind-max_access_cnt>[int]: 5    ☞가입자보드 1번의 1포트 MAC 5 설정
 
HAMX6000> sh bind                 ☞가입자보드 1번의 1포트 MAC count 설정 확인
HAMX6000> sh bindlist             ☞전체 가입자 보드에 설정 확인
 <bindlist-shelf>[int,[M]|p(prev)]: 1
 <bindlist-slot>[int,[M]|p(prev)]: 11
 <bindlist-port>[int,[M]|p(prev)]: 1
 <bindlist-vpi>[int|l(list),[M]|p(prev)]: l"""

#가입자 포트에 프로파일 설정
    data4 = """HAMX6000> conf adslline
 <adslline-shelf>[int,[M]|p(prev)]: 1
 <adslline-slot>[int,[M]|p(prev)]: 1        
 <adslline-port>[int,[M]|p(prev)]: 5                                ☞설정할 가입자 포트 입력
 <adslline-cnf_name>[str,[M]|p(prev)]: lite             ☞적용할 프로파일명 입력
 <adslline-alarm_name>[str,[M]|p(prev)]: default
 <adslline-trans_enble>[(yes|no),[M]|p(prev)]: y
 ADSL line config. success .....
 
HAMX6000> sh adslline                                                       ☞프로파일 설정 상태 확인
HAMX6000> sh dsllink                                                         ☞전체 포트 상태 확인"""

#SNMP COMMUNITY 설정
    data5 = """HAMX6000> mod comm                            
 <community-index>[int,[M]|p(prev)]: 1
 <community-community>[str,[O]|p(prev)]: private         ☞write 권한의 SNMP
 <community-ipaddr>[IP-addr,[O]|p(prev)]:
 <community-access>[(read|write),[O]|p(prev)]: write
 Community Modify Success ...
HAMX6000> mod comm                            
 <community-index>[int,[M]|p(prev)]: 2
 <community-community>[str,[O]|p(prev)]: public          ☞read 권한의 SNMP
 <community-ipaddr>[IP-addr,[O]|p(prev)]:
 <community-access>[(read|write),[O]|p(prev)]: read 
 Community Modify Success ...
 
HAMX6000> show comm                                     ☞SNMP 설정된 상태 확인                             ☞설정 확인"""


#긴급복구(장비교체시)
    data6 = """※ 장치 하드웨어 부팅 보드를 탈장 후 다시 장착한다
       ☞ 예비 장치 또는 보드로 교체
 
HAMX6000> reset board                                       ☞ SEIRAL 또는 TELNET으로 장치 재부팅
<board-shelf_id>[int,[M]|p(prev)] : 1
<board-slot_id>[int,[M]|p(prev)]  : 1                 ☞  해당장치 슬롯
<board-reset>[(reset),[M]|p(prev)]: reset
 Board config. success ....."""

#가입자 PVC 확인 및 Setting
    data7 = """※PVC 정보가 모두 지워지고 없을 경우 아래의 순서대로 작업한다.
 
1. PVC 확인
     ☞ PVC setting 확인 (vpvcrange 범위에 맞게 pvc를 setting 하여야 함)
HAMX6000> sh pvcc
 <pvcc-index>[int|l(list),[M]|p(prev)]: l
 ----------------------------------------------------------------
   id  lPort  lVpi lVci  hPort  hVpi hVci tUpc rUpc dir l2h  h2l
 ----------------------------------------------------------------
   1 01-11-01   1   32 01-12-02   0   32   0    0   bi   up   up   (관리용 PVC)
   2 01-01-01   0   32 01-11-01  11  101   0    0   bi down down   (가입자용 PVC)
 
2. 관리용 PVC Setting
    ☞PVC확인 후 PVC 정보가 없을경우 아래 PVC를 Setting 해야 함.
    ☞관리용 PVC가 Setting 되어 있어야 Telnet이 가능함
HAMX6000> add pvcc   (AC TYPE 기준)
 <pvcc-low_shelf>[int,[M]|p(prev)]: 1
 <pvcc-low_slot>[int,[M]|p(prev)]: 11         (DC Type 일 경우 15 입력)
 <pvcc-low_port>[int,[M]|p(prev)]: 1
 <pvcc-low_vpi>[int,[M]|p(prev)]: 1       
 <pvcc-low_vci>[int,[M]|p(prev)]: 32
 <pvcc-high_shelf>[int,[M]|p(prev)]: 1
 <pvcc-high_slot>[int,[M]|p(prev)]: 12        (DC Type 일 경우 16 입력)
 <pvcc-high_port>[int,[M]|p(prev)]: 2
 <pvcc-high_vpi>[int,[M]|p(prev)]: 0
 <pvcc-high_vci>[int,[M]|p(prev)]: 32
 <pvcc-tx_upc>[int,[M]|p(prev)]: 0
 <pvcc-rx_upc>[int,[M]|p(prev)]: 0
 <pvcc-aal_type>[(aal1|aal2|aal3|aal4|aal5|oth),[M]|p(prev)] : aal5
 <pvcc-tx_sdu>[int,[O]|p(prev)]: 1508
 <pvcc-rx_sdu>[int,[O]|p(prev)]: 1508
 <pvcc-ecap_t>[(route|bg8023|bg8025|bg8026|le8023|llc|frame),[O]|p(prev)]: llc
 <pvcc-direction>[(up-dir|down-dir|bi-dir),[M]|p(prev)]: bi
 <pvcc-admin_status>[(up|down),[M]|p(prev)] : up
 
3. 가입자 PVC 삭제
      ☞ 관리용 pvc를 제외한 모든 가입자 pvc가 삭제됨
HAMX6000>reset conn
  pass = conn@admin
 
4. 가입자 PVC 일괄 Setting
HAMX6000> batch mconn
 <mconn-wan_ub>[int,[M]|p(prev)]: 11                      (DC Type인 경우 15Slot)
 <mconn-port_type>[(16port|32port|64port),[M]|p(prev)]: 16port   (dslb 유형 선택)
 <mconn-target_shelf>[int,[M]|p(prev)]: 1                (변경할 시작 shelf 지정)
 <mconn-start_slot>[int,[M]|p(prev)]: 1                   (변경할 시작 slot 지정)
 <mconn-start_port>[int,[M]|p(prev)]: 1                   (변경할 시작 port 지정)
 <mconn-end_slot>[int,[M]|p(prev)]: 9                   (변경할 끝나는 slot 지정)
 <mconn-end_port>[int,[M]|p(prev)]: 16                  (변경할 끝나는 port 지정)
 <mconn-wan_vpi>[int,[M]|p(prev)]: 11    (11slot crub 1번 포트를 사용한다는 의미)
 <mconn-wan_vci>[int,[M]|p(prev)]: 101     (vpvcrange에서 setting한 start vci 값)
 <mconn-modem_vpi>[int,[M]|p(prev)]: 0                             (모뎀측 vpi값)
 <mconn-modem_vci>[int,[M]|p(prev)]: 32                            (모뎀측 vci값)"""
    
#장비IP 설정후 Gateway로 PING 무응답 발생시 조치방법
    data8 = """※ 집선스위치로 Ping 에 대한 응답이 없는 경우 아래의 순서로 조치한다.
 
1. show bridgecfg 명령을 수행하여 IP 주소가 정상적으로 설정되어 있는지 확인한다
       ☞ IP 주소가 설정되어 있지 않으면 다음과 같이 진행한다.
          1). del pvcc 명령을 수행하여 Bridge에 해당하는 PVC 연결 정보만 삭제한다.
          2). mod bridgecfg 명령을 수행하여 IP 주소를 다시 설정한다.
 
2. IP 주소 설정이 정상이나 계속 ping에 대한 응답이 없으면 Bridge에 해당하는 PVC
    연결 정보를 확인한다
        ☞ 연결 정보가 없는 경우에 add pvcc 명령을 수행하여 Bridge에 해당하는 PVC
            연결 정보를 생성한다.
DSLAM> show pvc                          ☞ 인터페이스용  연결 정보 확인
 <pvcc-index>[int|l(list),[M]|p(prev)]: l
 -------------------------------------------------------------------
 id  lPort   lVpi  lVci  hPort   hVpi  hVci tUpc rUpc dir  l2h  h2l
 -------------------------------------------------------------------
 1  01-15-01   1   32   01-16-02   0   32   0    0   bi   up   up
 2  01-01-01   0   32   01-15-01  11  101   0    0   bi   up   up
 3  01-01-02   0   32   01-15-01  11  102   0    0   bi   up   up
 4  01-01-03   0   32   01-15-01  11  103   0    0   bi down down
 5  01-01-04   0   32   01-15-01  11  104   0    0   bi   up   up
 6  01-01-05   0   32   01-15-01  11  105   0    0   bi down down
 7  01-01-06   0   32   01-15-01  11  106   0    0   bi   up   up
 8  01-01-07   0   32   01-15-01  11  107   0    0   bi down down
 9  01-01-08   0   32   01-15-01  11  108   0    0   bi down down
 Please [enter(next)/(a)all/(e)exit]...
 
DSLAM> add pvcc                          ☞ 연결 정보 설정
 <pvcc-low_shelf>[int,[M]|p(prev)]: 1
 <pvcc-low_slot>[int,[M]|p(prev)]: 15
 <pvcc-low_port>[int,[M]|p(prev)]: 1
 <pvcc-low_vpi>[int,[M]|p(prev)]: 1
 <pvcc-low_vci>[int,[M]|p(prev)]: 32
 <pvcc-high_shelf>[int,[M]|p(prev)]: 1
 <pvcc-high_slot>[int,[M]|p(prev)]: 16
 <pvcc-high_port>[int,[M]|p(prev)]: 2
 <pvcc-high_vpi>[int,[M]|p(prev)]: 0
 <pvcc-high_vci>[int,[M]|p(prev)]: 32
 <pvcc-tx_upc>[int,[M]|p(prev)]: 0
 <pvcc-rx_upc>[int,[M]|p(prev)]: 0
 <pvcc-aal_type>[(aal1|aal34|aal5|other),[M]|p(prev)]: aal5
 <pvcc-tx_sdu>[int,[O]|p(prev)]: 1508
 <pvcc-rx_sdu>[int,[O]|p(prev)]: 1508
 <pvcc-ecap_t>[(route|bg8023|bg8025|bg8026|le8023|le8025|llc),[O]|p(prev)]:llc
 <pvcc-direction>[(up-dir|down-dir|bi-dir),[M]|p(prev)]: bi
 <pvcc-admin_status>[(up|down),[M]|p(prev)]: up
 VCC Add success .....
DSLAM> ping 10.0.0.1
 PING 10.0.0.1 : 56 data bytes
 64 bytes from 10.0.0.1: icmp_seq=1 time= <10 ms
 64 bytes from 10.0.0.1: icmp_seq=1 time= <10 ms
 64 bytes from 10.0.0.1: icmp_seq=2 time= <10 ms
 
3. 위의 두 가지 모두 정상이면 전송로 구간을 점검한다.""" 

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

    st.markdown('<div class="title">MAX-host 개수 제한</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.code(data3)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="title">가입자 포트에 프로파일 설정</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.code(data4)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="title">SNMP COMMUNITY 설정</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.code(data5)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<p style="font-weight:bold; font-size:18px;">긴급복구요령</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="title">긴급복구(장비교체시)</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.code(data6)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="title">가입자 PVC 확인 및 Setting</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.code(data7)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="title">장비IP 설정후 Gateway로 PING 무응답 발생시 조치방법</div>', unsafe_allow_html=True)
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


def HAMX6000_w_page():
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
    ["show identity", "시스템의 Identification 정보 (시스템명, 버전, 장비 MAC)"],
    ["show shelf", "시스템의 Shelf 에 대한 정보"],
    ["show board", "각 보드의 상태"],
    ["show port", "각 port 의 유형, 상태 등의 정보"],
    ["show connect", "각 shelf 나 보드 단위의 연결정보"],
    ["show pvcc", "시스템의 ATM VC connection table"],
    ["show enet", "ethernet port 의 상태 정보"],
    ["show enetsts", "ethernet port 의 통계 정보"],
    ["show users", "현재 시스템에 등록되어 있는 Craft interface의 사용자 정보"],
    ["show loginlist", "사용자가 장비에 login 한 시간 목록과 이력 정보"],
    ["show adslprof", "ADSL 포트의 profile"],
    ["show adslalarm", "ADSL 포트에서 발생되는 alarm 의 threshold 값"],
    ["show adslchan", "ADSL 포트의 Channel Layer Parameters 값"],
    ["show adslchpef", "Channel Layer 에서 수집되는 performance 통계정보"],
    ["show adslphy", "ADSL 포트의 Physical Layer Parameters 값"],
    ["show adslpef", "ADSL 포트의 Physical Layer 에서 수집되는 통계정보"],
    ["show bridgecfg", "BRIDGE(IN-BAND 로 연결)에 대한 설정 값"],
    ["show iproute", "IP 도메인에 대한 라우팅 정보"],
    ["show events", "시스템에서 저장하고 있는 event information"],
    ["show community", "시스템의 SNMP Community 를 보여준다."],
    ["show vpvcrange", "CRUB 보드에 VPVP 와 VPVC 의 범위"],
    ["show iwbrg", "CRUB 보드의 control 정보"],
    ["show bind", "vpi/vci 값이 bind 된 항목, MAC count 확인(1개 가입자별로 확인)"],
    ["show bindlist", "vpi/vci 값이 bind 된 항목,MAC count 확인(전체 가입자 확인)"],
    ["show mac", "ATM connection 의 PVC 에 해당하는 단말 MAC 주소 (1개 가입자별로 확인)"],
    ["show maclist", "CRUB에 연결된 전체 가입자 MAC 주소(전체 가입자 확인)"],
    ["show vlan", "VLAN 이 설정된 연결의 VLAN 정보"],
    ["show vlannamet", "VLAN name table 의 정보"],
    ["show dsllink", "ADSL line 상의 상태 정보"],
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

def HAMX6000_command_page():
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
    if "device_type" not in st.session_state:
        st.session_state["device_type"] = "AC형"

    # 입력 필드 유지 (한 줄 정렬)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        ip_address = st.text_input("IP 주소 입력", value=st.session_state["ip_address"], key="ip_input")
    with col2:
        subnet_mask_options = [
            "255.255.255.0", "255.255.255.128", "255.255.255.192",
            "255.255.255.224", "255.255.255.240", "255.255.255.248", "255.255.255.252"
        ]
        subnet_mask = st.selectbox("서브넷 마스크 선택", subnet_mask_options,
                                   index=subnet_mask_options.index(st.session_state["subnet_mask"]))
    with col3:
        gateway = st.text_input("게이트웨이 입력", value=st.session_state["gateway"], key="gateway_input")
    with col4:
        device_type = st.selectbox("장비 유형", ["AC형", "DC형"], index=["AC형", "DC형"].index(st.session_state["device_type"]))

    # 값 변경 시 자동으로 session_state 업데이트
    st.session_state["ip_address"] = ip_address
    st.session_state["subnet_mask"] = subnet_mask
    st.session_state["gateway"] = gateway
    st.session_state["device_type"] = device_type

    # 버튼을 누를 때 커맨드 생성
    if st.button("커맨드 생성"):
        if ip_address and subnet_mask and gateway:
            slot_number = "12" if device_type == "AC형" else "16"
            commands = f"""mod bridgecfg
1
{slot_number}
2
{ip_address}
{subnet_mask}
{gateway}
sh bridgecfg
ping {gateway}
"""
            st.session_state["generated_command"] = commands
        else:
            st.warning("모든 필드를 입력해주세요.")

    # 생성된 커맨드 출력 및 복사 버튼
    if "generated_command" in st.session_state:
        st.text_area("생성된 커맨드:", value=st.session_state["generated_command"], height=300)

        if st.button("커맨드 복사"):
            pyperclip.copy(st.session_state["generated_command"])
            st.success("커맨드가 클립보드에 복사되었습니다.")

      

def main():
    st.sidebar.title("E5624R 장비 핸드북")
    menu = ["홈", "기본 설정", "조회 명령어", "커맨드 생성"]
    choice = st.sidebar.selectbox("메뉴", menu)

    if choice == "홈":
        HAMX6000_home_page()
    elif choice == "기본 설정":
        HAMX6000_e_page()
    elif choice == "조회 명령어":
        HAMX6000_w_page()
    elif choice == "커맨드 생성":
        HAMX6000_command_page()

if __name__ == "__main__":
    main()