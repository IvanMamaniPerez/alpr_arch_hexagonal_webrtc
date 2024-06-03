from typing import Set, List, Dict, Any
from aiortc import RTCPeerConnection, MediaStreamTrack
from aiortc.contrib.media import MediaRelay
from src.PeerConnection.PeerConnectionData import PeerConnectionData
import asyncio

class PeerConnectionManager:

    def __init__(self) -> None:
        self.peer_connections: Set[PeerConnectionData] = set()
        self.relay = MediaRelay()

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
    
    def add_active_track(self, peer_connection: RTCPeerConnection, track: MediaStreamTrack) -> MediaStreamTrack|None:
        pc_info = self.get_peer_connection_info(peer_connection)
        if pc_info:
            relayed_track = self.relay.subscribe(track)
            pc_info.active_tracks.append(relayed_track)
            return relayed_track
        else:
            return None
    
    def remove_active_track(self, peer_connection: RTCPeerConnection, track: MediaStreamTrack) -> None:
        pc_info = self.get_peer_connection_info(peer_connection)
        if pc_info:
            pc_info.active_tracks = [t for t in pc_info.active_tracks if t != track]
            self.relay.unsubscribe(track)
            

    def get_active_tracks(self) -> List[MediaStreamTrack]:
        active_tracks = []
        for pc in self.peer_connections:
            active_tracks.extend(pc.active_tracks)
        return active_tracks
    
    async def close_all(self):
        coros = [pc.peer_connection.close() for pc in self.peer_connections]
        await asyncio.gather(*coros)
        self.peer_connections.clear()