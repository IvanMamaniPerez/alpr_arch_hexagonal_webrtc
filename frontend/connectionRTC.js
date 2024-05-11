// Crear un objeto para almacenar las conexiones
let connections = [];
let streams = [];
const API_TOKEN = "98943522-64fd-449b-80ff-87bcf18a157f";
let config = {
  sdpSemantics: "unified-plan",
  iceServers: [{ urls: ["stun:stun.l.google.com:19302"] }],
};
// Función para crear una nueva conexión

function createConnection(idCamera, nameCamera) {
  let peerConnection = new RTCPeerConnection(config);
  let dataConnection = {
    id: idCamera,
    peerConnection: peerConnection,
    label: nameCamera,
  };

  peerConnection.onconnectionstatechange = () => {
    console.log(
      "Connection State Change: " + nameCamera,
      peerConnection.connectionState
    );
    if (peerConnection.connectionState === "failed") {
      /* TODO poner en ui que se perdio la conexion con el servidor */
      showOverlay(idCamera, true)
      let actualStream = streams.find((stream) => stream.id === idCamera);
      actualStream.stream.getTracks().forEach((track) => {
        track.stop();
      });
    }
  };

  connections.push(dataConnection);
  return dataConnection;
}

function negotiate(pc, idCamera, nameCamera) {
  return pc
    .createOffer()
    .then((offer) => {
      console.log("offer.sdp", offer.sdp);
      return pc.setLocalDescription(offer);
    })
    .then(() => {
      // wait for ICE gathering to complete
      return new Promise((resolve) => {
        if (pc.iceGatheringState === "complete") {
          resolve();
        } else {
          function checkState() {
            if (pc.iceGatheringState === "complete") {
              pc.removeEventListener("icegatheringstatechange", checkState);
              resolve();
            }
          }
          pc.addEventListener("icegatheringstatechange", checkState);
        }
      });
    })
    .then(() => {
      let offer = pc.localDescription;
      let codec = "H264/90000";

      offer.sdp = sdpFilterCodec("video", codec, offer.sdp);

      return fetch("/offer", {
        body: JSON.stringify({
          sdp: offer.sdp,
          type: offer.type,
          type_conection: "camera",
          token: API_TOKEN,
          idCamera: idCamera,
          nameCamera: nameCamera,
        }),
        headers: {
          "Content-Type": "application/json",
        },
        method: "POST",
      });
    })
    .then((response) => {
      return response.json();
    })
    .then((answer) => {
      console.log("answer.sdp", answer.sdp);
      return pc.setRemoteDescription(answer);
    })
    .catch((e) => {
      alert(e);
    });
}

function startConection(idCamera, nameCamera) {
  let dataConnection = createConnection(idCamera, nameCamera);
  let pc = dataConnection.peerConnection;
  // let parameters = { ordered: true };

  const constraints = {
    video: false,
  };

  const videoConstraints = {};

  videoConstraints.deviceId = { exact: idCamera };

  /* const resolution = document.getElementById("video-resolution").value;
  if (resolution) {
    const dimensions = resolution.split("x");
    videoConstraints.width = parseInt(dimensions[0], 0);
    videoConstraints.height = parseInt(dimensions[1], 0);
    console.log('dimensions');
    console.log(dimensions);
    console.log('dimensions');

  } */

  constraints.video = videoConstraints;

  navigator.mediaDevices.getUserMedia(constraints).then(
    (stream) => {
      streams.push({ id: idCamera, stream: stream });
      let containerVideo = document.createElement("div");
      containerVideo.id = "container-video-" + idCamera;
      containerVideo.classList.add(
        "col-span-" + totalGrids / devicesConected.length, "relative"
      );
      let overlayVideo = document.createElement("div");
      overlayVideo.id = "overlay-video-" + idCamera;
      overlayVideo.classList.add(
        "absolute",
        "inset-0",
        "bg-black",
        "bg-opacity-50",
        "flex",
        "justify-center",
        "items-center",
        "text-white",
        "text-lg",
        "w-full",
        "h-full",
        "hidden"
      );
      overlayVideo.innerHTML = "Error en la conexión";
      let video = document.createElement("video");
      video.id = "video-" + idCamera;
      video.classList.add("w-full", "h-full", "object-cover");
      video.autoplay = true;
      containerVideo.appendChild(video);
      containerVideo.appendChild(overlayVideo);
      container.appendChild(containerVideo);
      video.srcObject = stream;
      // video.play();

      console.log("Media acquired. con el track");
      stream.getTracks().forEach((track) => {
        pc.addTrack(track, stream);
      });
      return negotiate(pc, idCamera, nameCamera);
    },
    (err) => {
      alert("Could not acquire media: " + err);
    }
  );
}

function showOverlay(idCamera, active) {
  let overlay = document.getElementById("overlay-video-" + idCamera);
  if (active) {
    overlay.classList.remove("hidden");
  }else {
    overlay.classList.add("hidden");
  }
}




function sdpFilterCodec(kind, codec, realSdp) {
  var allowed = [];
  var rtxRegex = new RegExp("a=fmtp:(\\d+) apt=(\\d+)\r$");
  var codecRegex = new RegExp("a=rtpmap:([0-9]+) " + escapeRegExp(codec));
  var videoRegex = new RegExp("(m=" + kind + " .*?)( ([0-9]+))*\\s*$");

  var lines = realSdp.split("\n");

  var isKind = false;
  for (var i = 0; i < lines.length; i++) {
    if (lines[i].startsWith("m=" + kind + " ")) {
      isKind = true;
    } else if (lines[i].startsWith("m=")) {
      isKind = false;
    }

    if (isKind) {
      var match = lines[i].match(codecRegex);
      if (match) {
        allowed.push(parseInt(match[1]));
      }

      match = lines[i].match(rtxRegex);
      if (match && allowed.includes(parseInt(match[2]))) {
        allowed.push(parseInt(match[1]));
      }
    }
  }

  var skipRegex = "a=(fmtp|rtcp-fb|rtpmap):([0-9]+)";
  var sdp = "";

  isKind = false;
  for (var i = 0; i < lines.length; i++) {
    if (lines[i].startsWith("m=" + kind + " ")) {
      isKind = true;
    } else if (lines[i].startsWith("m=")) {
      isKind = false;
    }

    if (isKind) {
      var skipMatch = lines[i].match(skipRegex);
      if (skipMatch && !allowed.includes(parseInt(skipMatch[2]))) {
        continue;
      } else if (lines[i].match(videoRegex)) {
        sdp += lines[i].replace(videoRegex, "$1 " + allowed.join(" ")) + "\n";
      } else {
        sdp += lines[i] + "\n";
      }
    } else {
      sdp += lines[i] + "\n";
    }
  }

  return sdp;
}

function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); // $& means the whole matched string
}
