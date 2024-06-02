import argparse
import asyncio
import json
import logging
import os
import ssl
import uuid

import cv2
from aiohttp import web
import aiohttp_cors
from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder, MediaRelay
from av import VideoFrame
# import sys
# sys.path.append("src/PeerConnection")
from src.PeerConnection.PeerConnectionCameraManager import PeerConnectionCameraManager

peer_connection_camera_manager = PeerConnectionCameraManager()

ROOT = os.path.dirname(__file__)

logger = logging.getLogger("pc")
pcs = set()
relay = MediaRelay()

camera_pcs = {}
viewer_pcs = {}
active_tracks = []
class VideoTransformTrack(MediaStreamTrack):

    kind = "video"

    def __init__(self, track, token):
        super().__init__()  # don't forget this!
        self.track = track
        self.token = token

    async def recv(self):
        frame = await self.track.recv()
        return frame

def get_viewer_pcs():
    return viewer_pcs.values()

def handle_new_track(track):
    relayed_track = relay.subscribe(track)
    active_tracks.append(relayed_track)

async def index(request):
    content = json.dumps(
            peer_connection_camera_manager.to_json()
        )
    
    return web.Response(content_type="application/json", text=content)


async def offer(request):
    params = await request.json()
    
    connection_type = params["type_conection"]

    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pc_id = "PeerConnection(%s)" % uuid.uuid4()
    pcs.add(pc)
    if connection_type == 'camera': 
        peer_connection_camera_manager.add_peer_connection(pc, 'camera', 'camarilla', 'dispositivo','puerta 1');
    
    if connection_type == "viewer":
        viewer_pcs[pc_id] = pc  # Almacenar la conexión del viewer
        # Subscribir este viewer a todos los streams de cámara disponibles
        if len(active_tracks) > 0:
            for track in active_tracks:
                pc.addTrack(track)

    def log_info(msg, *args):
        logger.info(pc_id + " " + msg, *args)

    log_info("Created for %s", request.remote)

    # prepare local media
    
    if args.record_to:
        recorder = MediaRecorder(args.record_to)
    else:
        recorder = MediaBlackhole()

    @pc.on("datachannel")
    def on_datachannel(channel):
        @channel.on("message")
        def on_message(message):
            if isinstance(message, str) and message.startswith("ping"):
                channel.send("pong" + message[4:])

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        log_info("Connection state is %s", pc.connectionState)
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    @pc.on("track")
    def on_track(track):
        log_info("Track %s received", track.kind)

        relayed_track = relay.subscribe(track)

        pc.addTrack(
            VideoTransformTrack(
                relayed_track, token=params["token"]
            )
        )
        active_tracks.append(relayed_track)
        
        for viewer_pc in viewer_pcs.values():
            if isinstance(viewer_pc, RTCPeerConnection):
                viewer_pc.addTrack(VideoTransformTrack(relayed_track, token=params["token"]))
            else:
                print(f"Error: Objeto inesperado en viewer_pcs: {type(viewer_pc)}")


        if args.record_to:
            recorder.addTrack(relay.subscribe(track))

        @track.on("ended")
        async def on_ended():
            log_info("Track %s ended", track.kind)
            await recorder.stop()

    # handle offer
    await pc.setRemoteDescription(offer)
    await recorder.start()

    # send answer
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.Response(
        content_type="application/json",
        text=json.dumps(
            {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
        ),
    )


async def on_shutdown(app):
    # close peer connections
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()


if  __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="WebRTC audio / video / data-channels demo"
    )
    parser.add_argument("--cert-file", default='./cert.pem', help="SSL certificate file (for HTTPS)")
    parser.add_argument("--key-file", default='./key.pem', help="SSL key file (for HTTPS)")
    parser.add_argument(
        "--host", default="0.0.0.0", help="Host for HTTP server (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", type=int, default=8080, help="Port for HTTP server (default: 8080)"
    )
    parser.add_argument("--record-to", help="Write received media to a file.")
    parser.add_argument("--password", default="hola", help="Password for SSL key file")
    parser.add_argument("--verbose", "-v", action="count")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if args.cert_file:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(args.cert_file, args.key_file, password=args.password)
    else:
        ssl_context = None

    app = web.Application()
    app.on_shutdown.append(on_shutdown)
    app.router.add_get("/", index)
    app.router.add_post("/offer", offer)
    """ web.run_app(
        app, access_log=None, host=args.host, port=args.port, ssl_context=ssl_context
    ) """

# Configura CORS
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
                allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
            )
    })

    # Aplica la configuración de CORS a todas las rutas
    for route in list(app.router.routes()):
        cors.add(route)

    #web.run_app(
    #    app, access_log=None, host=args.host, port=args.port, ssl_context=ssl_context
    #)
    web.run_app(
        app, access_log=None, host=args.host, port=args.port
    )
