from .payload import ProxyPayload, ProxyPayloadType

class ProxyPayloadCrypt(ProxyPayload):
    
    requires_checksum:bool = True
    payload_type:bytes = ProxyPayloadType.U_CRYPT
    data:bytes = b''

    def __init__(self) -> None:
        pass

    def set_data(self, data:bytes) -> None:
        self.data = data

    def build_payload(self) -> bytes:
        return b"".join([
            self.payload_type,
            self.payload_flags,
            (6+len(self.data)+3).to_bytes(2, 'big'), # Header + Crypto code + data length + padding and checksum to be inserted by packet builder.
            b'\x00\x0a', # Crypto code for the payload
            self.data,
            b'\x02' # Padding??
        ])