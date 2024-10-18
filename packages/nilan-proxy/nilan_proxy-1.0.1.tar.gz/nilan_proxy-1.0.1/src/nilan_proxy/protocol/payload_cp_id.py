from .payload import ProxyPayload, ProxyPayloadType

class ProxyPayloadCP_ID(ProxyPayload):
    
    requires_checksum = False
    payload_type = ProxyPayloadType.U_CP_ID
    email = ""

    def __init__(self) -> None:
        pass

    def set_email(self, email:str) -> None:
        self.email = email

    def build_payload(self) -> bytes: 
        length = 5 + len(self.email)
        return b"".join([
            self.payload_type,
            self.payload_flags,
            length.to_bytes(2, 'big'),
            b'\x01', # ID type email
            self.email.encode("ascii")
        ])