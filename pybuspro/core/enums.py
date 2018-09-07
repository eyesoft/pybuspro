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
    # SB_DN_DT0601 = b'\x00\x9E'    # Universaldimmer 6ch 1A
    # SB_DN_RS232N				    # RS232


class OnOff(Enum):
    OFF = 0
    ON = 255


class OperateCode(Enum):
    NotSet = b'\x00'

    SingleChannelLightingControl = b'\x00\x31'
    Response_SingleChannelLightingControl = b'\x00\x32'

    UniversalSwitch = b'\xE0\x1C'
    Response_UniversalSwitch = b'\xE0\x1D'

    Scene = b'\x00\x02'
    Response_Scene = b'\x00\x03'

    TIME_IF_FROM_LOGIC_OR_SECURITY = b'\xDA\x44'

    # b'\x1947'
    INFO_IF_FROM_12in1__1 = b'\x16\x47'
    INFO_IF_FROM_12in1__2 = b'\xE3\xE5'
    INFO_IF_FROM_RELE_10V = b'\xEF\xFF'
    # b'\xF036'

    QUERY_DLP_FROM_SETUP_TOOL_1 = b'\xE0\xE4'		    # Ingen data sendes svar sendes sender
    RESPONSE_QUERY_DLP_FROM_SETUP_TOOL_1 = b'\xE0\xE5'
    QUERY_DLP_FROM_SETUP_TOOL_2 = b'\x19\x44'		    # Ingen data sendes svar sendes sender			FLOOR HEATING WORKING STATUS
    RESPONSE_QUERY_DLP_FROM_SETUP_TOOL_2 = b'\x19\x45'
    QUERY_DLP_FROM_SETUP_TOOL_3 = b'\x19\x40'		    # Ingen data sendes svar sendes sender			FLOOR HEATING
    RESPONSE_QUERY_DLP_FROM_SETUP_TOOL_3 = b'\x19\x41'
    QUERY_DLP_FROM_SETUP_TOOL_4 = b'\x19\x46'			# 0 1 1 23 20 20 20										FLOOR HEATING WORKING STATUS CONTROL
    RESPONSE_QUERY_DLP_FROM_SETUP_TOOL_4 = b'\x19\x47'
    # b'\x19\x48' Temperature request?
    # b'\x19\x49' Temperature request?
    # b'\xE3\xE5' GPRS control answer back

    QUERY_12in1_FROM_SETUP_TOOL_1 = b'\x00\x0E'
    RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_1 = b'\x00\x0F'
    QUERY_12in1_FROM_SETUP_TOOL_2 = b'\xF0\x03'
    RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_2 = b'\xF0\x04'
    QUERY_12in1_FROM_SETUP_TOOL_3 = b'\xDB\x3E'
    RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_3 = b'\xDB\x3F'
    QUERY_12in1_FROM_SETUP_TOOL_4 = b'\x16\x66'
    RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_4 = b'\x16\x67'
    QUERY_12in1_FROM_SETUP_TOOL_5 = b'\x16\x45'
    RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_5 = b'\x16\x46'
    QUERY_12in1_FROM_SETUP_TOOL_6 = b'\x16\x5E'
    RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_6 = b'\x16\x5F'
    QUERY_12in1_FROM_SETUP_TOOL_7 = b'\x16\x41'
    RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_7 = b'\x16\x42'
    QUERY_12in1_FROM_SETUP_TOOL_8 = b'\x16\x6E'
    RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_8 = b'\x16\x6F'
    QUERY_12in1_FROM_SETUP_TOOL_9 = b'\x16\xA9'
    RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_9 = b'\x16\xAA'
