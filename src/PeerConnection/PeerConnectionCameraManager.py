from typing import List
from aiortc import MediaStreamTrack
from src.PeerConnection.PeerConnectionManager import PeerConnectionManager

class PeerConnectionCameraManager(PeerConnectionManager):

    def __init__(self) -> None:
        super().__init__()