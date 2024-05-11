// Listar camaras

let select = document.getElementById("video-input");
let startButton = document.getElementById("start-button");
let container = document.getElementById("container");
let devicesFiltered = [];
let devicesConected = [];
const totalGrids = 4;

function enumerateInputDevices() {
  navigator.mediaDevices
    .enumerateDevices()
    .then((devices) => {
      devicesFiltered = devices.filter((device) => device.kind == "videoinput");
      let counter = 1;
      devicesFiltered.forEach((device) => {
        console.log(device);
        const option = document.createElement("option");
        option.value = device.deviceId;
        option.text = device.label || "Camara #" + counter;
        select.appendChild(option);
        counter++;
      });
    })
    .catch((e) => {
      alert(e);
    });
}

enumerateInputDevices();

function startCamera() {
  let videoInput = select.value;
  let label = select.options[select.selectedIndex].text;
  if (devicesConected.find((device) => device.deviceId == videoInput)){
    alert("Esta cámara ya está conectada");
    return;
  }

  devicesConected.push({
    deviceId: videoInput,
    label: label,
  });

  /* let constraints = {
    video: {
      deviceId: videoInput,
    },
    audio: false,
  }; */

  startConection(videoInput, label);

/*   navigator.mediaDevices
    .getUserMedia(constraints)
    .then((stream) => {
  
    })
    .catch((e) => {
      alert(e);
    }); */
}

startButton.addEventListener("click", () => {
  startCamera();
});
