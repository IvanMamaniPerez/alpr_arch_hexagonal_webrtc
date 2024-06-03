from typing import Set
from aiortc import RTCPeerConnection
from src.PeerConnection.PeerConnectionManager import PeerConnectionManager

class PeerConnectionViewerManager(PeerConnectionManager):

    def __init__(self) -> None:
        super().__init__()