from typing import Set, List, Dict, Any
from aiortc import RTCPeerConnection
from src.PeerConnection.PeerConnectionData import PeerConnectionData

class PeerConnectionManager:

    def __init__(self) -> None:
        self.peer_connections: Set[PeerConnectionData] = set()

    def add_peer_connection(self, peer_connection: RTCPeerConnection, type: str, camera: str, name_device: str, access_point: str) -> None:
        pc_data = PeerConnectionData(
            peer_connection = peer_connection,
            type            = type,
            camera          = camera,
            name_device     = name_device,
            access_point    = access_point
        )
        
        self.peer_connections.add(pc_data)

    def remove_peer_connection(self, peer_connection: RTCPeerConnection) -> None:
        pc_data = PeerConnectionData(peer_connection , '', '', '', '') 
        self.peer_connections.discard(pc_data)

    def get_peer_connection_info(self, peer_connection: RTCPeerConnection):
        pc_data = PeerConnectionData(peer_connection, '','', '', None)
        for pc in self.peer_connections:
            if pc == pc_data:
                return pc
        return None
    
    def to_json(self) -> Dict[str, Any]:
        return {
            "peer_connections": [
                {
                    "type"        : pc.type,
                    "camera"      : pc.camera,
                    "name_device" : pc.name_device,
                    "access_point": pc.access_point,
                } for pc in self.peer_connections
            ]
        }