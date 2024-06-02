from aiortc import RTCPeerConnection
from src.PeerConnection.PeerConnectionManager import PeerConnectionManager

class PeerConnectionCameraManager(PeerConnectionManager):

    def __init__(self) -> None:
        super().__init__()

