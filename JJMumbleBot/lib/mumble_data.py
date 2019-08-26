class MumbleData:
    ip_address = None
    port = 0
    user_id = None
    password = None
    certificate = None

    def __init__(self, ip: str, port: int, uid: str, pwd: str, cert: str):
        self.ip_address = ip
        self.port = port
        self.user_id = uid
        self.password = pwd
        self.certificate = cert
