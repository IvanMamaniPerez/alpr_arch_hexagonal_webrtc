from typing import Any, List
from aiortc import RTCPeerConnection, MediaStreamTrack

class PeerConnectionData:
    def __init__(self, peer_connection: RTCPeerConnection, type:str, camera: str, name_device: str, access_point: str):
        self.peer_connection = peer_connection
        self.type            = type
        self.camera          = camera
        self.access_point    = access_point
        self.name_device     = name_device
        self.active_tracks: List[MediaStreamTrack] = [] 

    def __eq__(self, other):
        if isinstance(other, PeerConnectionData):
            return self.peer_connection == other.peer_connection
        return False

    def __hash__(self):
        return hash(self.peer_connection)


