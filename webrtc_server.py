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
from src.PeerConnection.PeerConnectionCameraManager import PeerConnectionCameraManager
from src.PeerConnection.PeerConnectionViewerManager import PeerConnectionViewerManager
import numpy as np
from datetime import datetime
import base64



peer_connection_camera_manager = PeerConnectionCameraManager()
peer_connection_viewer_manager = PeerConnectionViewerManager()

ROOT = os.path.dirname(__file__)

logger = logging.getLogger("pc")

class VideoTransformTrack(MediaStreamTrack):

    kind = "video"

    def __init__(self, track, token):
        super().__init__()  # don't forget this!
        self.track = track
        self.token = token

    async def recv(self):
        frame = await self.track.recv()
        return frame

async def index(request):
    content = json.dumps(
            peer_connection_camera_manager.to_json()
        )
    
    return web.Response(content_type="application/json", text=content)

async def process_frame(request):
    try: 
        params = await request.json()

        image = params["image"]
        print('Image: ', image)
        data_bytes = base64.b64decode(image)  # Decodificar de base64 a bytes

        nparr = np.frombuffer(data_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        storage_folder = 'storage'
        current_timestamp = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

        final_path = os.path.join(storage_folder, current_timestamp + '.jpg')

        if not os.path.exists(storage_folder):
            os.makedirs(storage_folder)
        
        cv2.imwrite(final_path, img)
    except Exception as e:
        print('Error: ', e)
        return web.Response(content_type="application/json", text=json.dumps({"status": "error"}))

    return web.Response(content_type="application/json", text=json.dumps({"status": "ok", "path": final_path}))


async def offer(request):
    params = await request.json()
    
    connection_type = params["type_conection"]

    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])
    print(f"Received offer SDP:\n{offer.sdp}")  

    pc = RTCPeerConnection()
    pc_id = "PeerConnection(%s)" % uuid.uuid4()

    if connection_type == 'camera': 
        peer_connection_camera_manager.add_peer_connection(pc, 'camera', 'camarilla', 'dispositivo','puerta 1');
    
    if connection_type == "viewer":
        peer_connection_viewer_manager.add_peer_connection(pc, 'viewer', 'camarilla', 'dispositivo','puerta 1');

        camera_active_tracks = peer_connection_camera_manager.get_active_tracks();
        print('Active tracks DEBUG: ', camera_active_tracks)
        if len(camera_active_tracks) > 0:
            for track in camera_active_tracks:
                pc.addTrack(track)
                print(f"Added track {track} to viewer connection {pc_id}")

    def log_info(msg, *args):
        logger.info(pc_id + " " + msg, *args)

    log_info("Created for %s", request.remote)

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
            peer_connection_camera_manager.remove_peer_connection(pc)
            peer_connection_viewer_manager.remove_peer_connection(pc)

    @pc.on("track")
    def on_track(track):
        log_info("Track %s received", track.kind)

        relayed_track = peer_connection_camera_manager.add_active_track(pc, track)
        pc_info = peer_connection_camera_manager.get_peer_connection_info(pc)
        
        if pc_info:
            for viewer_pc in peer_connection_viewer_manager.peer_connections:
                if isinstance(viewer_pc.peer_connection, RTCPeerConnection):
                    viewer_pc.peer_connection.addTrack(relayed_track)
                else:
                    print(f"Error: Objeto inesperado en viewer_pcs: {type(viewer_pc)}")

        @track.on("ended")
        async def on_ended():
            log_info("Track %s ended", track.kind)
            await recorder.stop()

    # handle offer
    await pc.setRemoteDescription(offer)
    await recorder.start()

    # await asyncio.sleep(3)

    # send answer
    answer = await pc.createAnswer()
    print(f"-----------Created answer SDP DEBUG {connection_type} -----------\n{answer.sdp}\n-----------Created answer SDP DEBUG {connection_type} -----------")
    await pc.setLocalDescription(answer)

    return web.Response(
        content_type="application/json",
        text=json.dumps(
            {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
        ),
    )


async def on_shutdown(app):
    # close peer connections
    print("Shutting down...")
    await peer_connection_camera_manager.close_all()
    await peer_connection_viewer_manager.close_all()
    print("Shutdown complete.")


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
    app.router.add_post("/process_frame", process_frame)
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
