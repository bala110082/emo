const startWebcamBtn = document.getElementById('start-webcam-btn');
const stopWebcamBtn = document.getElementById('stop-webcam-btn');
const captureBtn = document.getElementById('capture-btn');
const webcam = document.getElementById('webcam');
const canvas = document.getElementById('canvas');
const webcamPlaceholder = document.getElementById('webcam-placeholder');
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const previewImage = document.getElementById('preview-image');
const dropZoneText = document.getElementById('drop-zone-text');
const uploadForm = document.getElementById('upload-form');

let stream = null;

startWebcamBtn.addEventListener('click', async () => {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                width: 640, 
                height: 480 
            } 
        });
        
        webcam.srcObject = stream;
        webcam.classList.remove('hidden');
        webcamPlaceholder.classList.add('hidden');
        
        startWebcamBtn.classList.add('hidden');
        stopWebcamBtn.classList.remove('hidden');
        captureBtn.classList.remove('hidden');
        
    } catch (error) {
        alert('Unable to access webcam. Please ensure you have granted camera permissions.');
        console.error('Error accessing webcam:', error);
    }
});

stopWebcamBtn.addEventListener('click', () => {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        webcam.srcObject = null;
        webcam.classList.add('hidden');
        webcamPlaceholder.classList.remove('hidden');
        
        startWebcamBtn.classList.remove('hidden');
        stopWebcamBtn.classList.add('hidden');
        captureBtn.classList.add('hidden');
    }
});

captureBtn.addEventListener('click', async () => {
    canvas.width = webcam.videoWidth;
    canvas.height = webcam.videoHeight;
    
    const context = canvas.getContext('2d');
    context.save();
    context.scale(-1, 1);
    context.drawImage(webcam, -canvas.width, 0, canvas.width, canvas.height);
    context.restore();
    
    const imageData = canvas.toDataURL('image/jpeg');
    
    captureBtn.disabled = true;
    captureBtn.innerHTML = '<span class="inline-block animate-spin mr-2">⏳</span>Analyzing...';
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image: imageData })
        });
        
        const data = await response.json();
        
        if (data.emotions) {
            const params = new URLSearchParams({
                emotions: JSON.stringify(data.emotions),
                disorder: data.disorder,
                confidence: data.confidence,
                image_url: data.image_url
            });
            window.location.href = `/results?${params.toString()}`;
        }
    } catch (error) {
        alert('Error analyzing image. Please try again.');
        console.error('Error:', error);
    } finally {
        captureBtn.disabled = false;
        captureBtn.innerHTML = '<i class="bi bi-camera-fill"></i> Capture & Analyze';
    }
});

dropZone.addEventListener('click', () => {
    fileInput.click();
});

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('border-blue-500', 'bg-blue-50');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('border-blue-500', 'bg-blue-50');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('border-blue-500', 'bg-blue-50');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        displayPreview(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        displayPreview(e.target.files[0]);
    }
});

function displayPreview(file) {
    const reader = new FileReader();
    
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        previewImage.classList.remove('hidden');
        dropZoneText.classList.add('hidden');
    };
    
    reader.readAsDataURL(file);
}

uploadForm.addEventListener('submit', (e) => {
    const submitBtn = document.getElementById('upload-btn');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="inline-block animate-spin mr-2">⏳</span>Analyzing...';
});