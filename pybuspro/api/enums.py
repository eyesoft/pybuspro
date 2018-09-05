from enum import Enum


class DeviceType(Enum):
    NotSet = b'\x00'
    SB_DN_6B0_10v = b'\x00\x11'     # Rele varme
    SB_DN_SEC250K = b'\x0B\xE9'	    # Sikkerhetsmodul
    SB_CMS_12in1 = b'\x01\x34'      # 12i1
    SB_DN_Logic960 = b'\x04\x53'    # Logikkmodul
    SB_DLP2 = b'\x00\x86'		    # DLP
    SB_DLP = b'\x00\x95'		    # DLP
    SB_DLP_v2 = b'\x00\x9C'			# DLPv2
    SmartHDLTest = b'\xFF\xFD'
    SetupTool = b'\xFF\xFE'
    SB_WS8M = b'\x01\x2B'			# 8 keys panel
    SB_CMS_8in1 = b'\x01\x35'		# 8i1
    SB_DN_DT0601 = b'\x02\x60'		# 6ch Dimmer
    SB_DN_R0816 = b'\x01\xAC'		# Rele
    # SB_DN_DT0601 = 0x009E	        # Universaldimmer 6ch 1A
    # SB_DN_RS232N				    # RS232


class OnOff(Enum):
    OFF = 0
    ON = 255


class OperateCode(Enum):
    NotSet = 0x0

    SingleChannelLightingControl = 0x0031
    Response_SingleChannelLightingControl = 0x0032

    UniversalSwitch = 0xE01C
    Response_UniversalSwitch = 0xE01D

    Scene = 0x0002
    Response_Scene = 0x0003

    TIME_IF_FROM_LOGIC_OR_SECURITY = 0xDA44

    # 0x1947
    INFO_IF_FROM_12in1__1 = 0x1647
    INFO_IF_FROM_12in1__2 = 0xE3E5
    INFO_IF_FROM_RELE_10V = 0xEFFF
    # 0xF036

    QUERY_DLP_FROM_SETUP_TOOL_1 = 0xE0E4		    # Ingen data sendes svar sendes sender
    RESPONSE_QUERY_DLP_FROM_SETUP_TOOL_1 = 0xE0E5
    QUERY_DLP_FROM_SETUP_TOOL_2 = 0x1944		    # Ingen data sendes svar sendes sender			FLOOR HEATING WORKING STATUS
    RESPONSE_QUERY_DLP_FROM_SETUP_TOOL_2 = 0x1945
    QUERY_DLP_FROM_SETUP_TOOL_3 = 0x1940		    # Ingen data sendes svar sendes sender			FLOOR HEATING
    RESPONSE_QUERY_DLP_FROM_SETUP_TOOL_3 = 0x1941
    QUERY_DLP_FROM_SETUP_TOOL_4 = 0x1946			# 0 1 1 23 20 20 20										FLOOR HEATING WORKING STATUS CONTROL
    RESPONSE_QUERY_DLP_FROM_SETUP_TOOL_4 = 0x1947
    # 0x1948 Temperature request?
    # 0x1949 Temperature request?
    # 0xE3E5 GPRS control answer back

    QUERY_12in1_FROM_SETUP_TOOL_1 = 0x000E
    RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_1 = 0x000F
    QUERY_12in1_FROM_SETUP_TOOL_2 = 0xF003
    RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_2 = 0xF004
    QUERY_12in1_FROM_SETUP_TOOL_3 = 0xDB3E
    RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_3 = 0xDB3F
    QUERY_12in1_FROM_SETUP_TOOL_4 = 0x1666
    RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_4 = 0x1667
    QUERY_12in1_FROM_SETUP_TOOL_5 = 0x1645
    RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_5 = 0x1646
    QUERY_12in1_FROM_SETUP_TOOL_6 = 0x165E
    RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_6 = 0x165F
    QUERY_12in1_FROM_SETUP_TOOL_7 = 0x1641
    RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_7 = 0x1642
    QUERY_12in1_FROM_SETUP_TOOL_8 = 0x166E
    RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_8 = 0x166F
    QUERY_12in1_FROM_SETUP_TOOL_9 = 0x16A9
    RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_9 = 0x16AA
