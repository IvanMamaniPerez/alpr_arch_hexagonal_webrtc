from aiohttp import web
import aiohttp_cors
import argparse
import json
import logging
import os
import ssl
import uuid
import cv2
import numpy as np
from datetime import datetime
import base64

async def test_connect(request):
    return web.Response(content_type="application/json", text=json.dumps({"status": "ok"}))

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
    app.router.add_post("/process_frame", process_frame)
    app.router.add_get("/test_connect", test_connect)

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
