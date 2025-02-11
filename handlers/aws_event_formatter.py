import struct
import binascii
import json

# ✅ 오디오 데이터를 AWS Transcribe 요구 포맷으로 변환
def create_audio_event(payload):
    # AWS 요구 헤더 생성
    content_type_header = get_headers(":content-type", "application/octet-stream")
    event_type_header = get_headers(":event-type", "AudioEvent")
    message_type_header = get_headers(":message-type", "event")
    
    # 헤더 통합
    headers = content_type_header + event_type_header + message_type_header

    # ✅ 프렐루드(Prelude) 설정
    total_length = struct.pack('>I', len(headers) + len(payload) + 16)
    headers_length = struct.pack('>I', len(headers))
    prelude = total_length + headers_length

    # ✅ 프렐루드 CRC 체크섬
    prelude_crc = struct.pack('>I', binascii.crc32(prelude) & 0xffffffff)

    # ✅ 메시지 구성
    message = prelude + prelude_crc + headers + payload

    # ✅ 메시지 CRC 체크섬 추가
    message_crc = struct.pack('>I', binascii.crc32(message) & 0xffffffff)
    return message + message_crc

# ✅ AWS Transcribe의 응답 디코딩
def decode_event(message):
    prelude = message[:8]
    total_length, headers_length = struct.unpack('>II', prelude)
    prelude_crc = struct.unpack('>I', message[8:12])[0]
    headers = message[12:12+headers_length]
    payload = message[12+headers_length:-4]
    message_crc = struct.unpack('>I', message[-4:])[0]

    # ✅ CRC 무결성 검사
    assert prelude_crc == binascii.crc32(prelude) & 0xffffffff, "Prelude CRC check failed"
    assert message_crc == binascii.crc32(message[:-4]) & 0xffffffff, "Message CRC check failed"

    # ✅ 헤더 파싱
    headers_dict = {}
    while headers:
        name_len = headers[0]
        name = headers[1:1+name_len].decode('utf-8')
        value_type = headers[1+name_len]
        value_len = struct.unpack('>H', headers[2+name_len:4+name_len])[0]
        value = headers[4+name_len:4+name_len+value_len].decode('utf-8')
        headers_dict[name] = value
        headers = headers[4+name_len+value_len:]

    return headers_dict, json.loads(payload)

# ✅ AWS 헤더 생성 유틸리티
def get_headers(header_name, header_value):
    name = header_name.encode('utf-8')
    name_length = bytes([len(name)])
    value_type = bytes([7])  # 7 = 문자열 타입
    value = header_value.encode('utf-8')
    value_length = struct.pack('>H', len(value))

    return name_length + name + value_type + value_length + value
