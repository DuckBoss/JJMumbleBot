class MumbleData:
    ip_address = None
    port = 0
    user_id = None
    password = None
    certificate = None
    stereo = False

    def __init__(self, ip: str, port: int, uid: str, pwd: str, cert: str, stereo: bool):
        self.ip_address = ip
        self.port = port
        self.user_id = uid
        self.password = pwd
        self.certificate = cert
        self.stereo = stereo
