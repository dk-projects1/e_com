const uploadBoxes = document.querySelectorAll('.upload-box');
const fileInput   = document.getElementById('fileInput');
const cropOverlay = document.getElementById('cropOverlay');
const cropImg     = document.getElementById('cropImg');
const cropConfirm = document.getElementById('cropConfirm');
const cropCancel  = document.getElementById('cropCancel');
const form        = document.getElementById('productForm');

let currentIndex  = null;
let cropper       = null;
const base64Imgs  = new Array(4);

uploadBoxes.forEach(box => {
  box.addEventListener('click', () => {
    currentIndex = +box.dataset.index;
    fileInput.click();
  });
});

fileInput.addEventListener('change', e => {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    cropImg.src = reader.result;
    cropOverlay.style.display = 'flex';
    if (cropper) cropper.destroy();
    cropper = new Cropper(cropImg, { aspectRatio: 1, viewMode: 1 });
  };
  reader.readAsDataURL(file);
});

cropConfirm.addEventListener('click', () => {
  if (!cropper) return;
  const canvas = cropper.getCroppedCanvas({ width: 600, height: 600 });
  const base64 = canvas.toDataURL('image/jpeg', 0.9);
  base64Imgs[currentIndex] = base64;
  uploadBoxes[currentIndex].innerHTML = `<img src="${base64}" alt="Preview" />`;
  closeCrop();
});

cropCancel.addEventListener('click', closeCrop);
function closeCrop(){
  cropOverlay.style.display = 'none';
  fileInput.value = '';
  if (cropper){ cropper.destroy(); cropper = null; }
}

form.addEventListener('submit', e => {
  base64Imgs.forEach((img, i) => {
    if (img) {
      const input = document.querySelector(`input[name="image_${i}"]`);
      if (input) input.value = img;
    }
  });
});