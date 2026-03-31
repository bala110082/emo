const API_BASE = 'http://localhost:5000/api';
let currentUser = null;
let webcamStream = null;
let webcamInterval = null;
let musicUpdateInterval = null;
let bgmCheckInterval = null;
let allEmotions = [];
let detectionCount = 0;
let emotionCounter = {};
let webcamStartTime = null;
let currentBGM = null;
let lastDominantEmotion = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    checkSession();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    // Tabs
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => switchTab(tab.dataset.tab));
    });

    // Auth
    document.getElementById('loginBtn').addEventListener('click', () => openModal('loginModal'));
    document.getElementById('registerBtn').addEventListener('click', () => openModal('registerModal'));
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    document.getElementById('registerForm').addEventListener('submit', handleRegister);

    // Image
    document.getElementById('imageUpload').addEventListener('click', () => document.getElementById('imageInput').click());
    document.getElementById('imageInput').addEventListener('change', handleImageSelect);
    document.getElementById('detectImageBtn').addEventListener('click', detectEmotion);

    // Webcam
    document.getElementById('startWebcam').addEventListener('click', startWebcam);
    document.getElementById('stopWebcam').addEventListener('click', stopWebcam);

    // Video
    document.getElementById('videoUpload').addEventListener('click', () => document.getElementById('videoInput').click());
    document.getElementById('videoInput').addEventListener('change', handleVideoSelect);
    document.getElementById('generateBGMBtn').addEventListener('click', generateVideoBGM);
}

// ============================================
// SESSION MANAGEMENT
// ============================================
async function checkSession() {
    try {
        const response = await fetch(`${API_BASE}/auth/check-session`, { credentials: 'include' });
        const data = await response.json();
        
        if (data.logged_in) {
            currentUser = data.user;
            updateUIForLoggedInUser();
        }
    } catch (error) {
        console.error('Session check failed:', error);
    }
}

function updateUIForLoggedInUser() {
    const userInfo = document.getElementById('userInfo');
    userInfo.innerHTML = `
        <span class="user-name">Welcome, ${currentUser.name}</span>
        <button class="btn" onclick="handleLogout()">Logout</button>
    `;
}

// ============================================
// AUTH FUNCTIONS
// ============================================
async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    try {
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            showAlert('loginAlert', 'Login successful!', 'success');
            currentUser = data.user;
            setTimeout(() => {
                closeModal('loginModal');
                updateUIForLoggedInUser();
            }, 1000);
        } else {
            showAlert('loginAlert', data.error, 'error');
        }
    } catch (error) {
        showAlert('loginAlert', 'Login failed. Please try again.', 'error');
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const name = document.getElementById('registerName').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;

    try {
        const response = await fetch(`${API_BASE}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ name, email, password })
        });

        const data = await response.json();

        if (response.ok) {
            showAlert('registerAlert', 'Registration successful!', 'success');
            currentUser = data.user;
            setTimeout(() => {
                closeModal('registerModal');
                updateUIForLoggedInUser();
            }, 1000);
        } else {
            showAlert('registerAlert', data.error, 'error');
        }
    } catch (error) {
        showAlert('registerAlert', 'Registration failed. Please try again.', 'error');
    }
}

async function handleLogout() {
    try {
        await fetch(`${API_BASE}/auth/logout`, { method: 'POST', credentials: 'include' });
        currentUser = null;
        location.reload();
    } catch (error) {
        console.error('Logout failed:', error);
    }
}

// ============================================
// IMAGE DETECTION
// ============================================
function handleImageSelect(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            document.getElementById('imagePreview').innerHTML = `
                <img src="${e.target.result}" alt="Preview" style="max-width: 100%; max-height: 400px;">
            `;
            document.getElementById('detectImageBtn').style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
}

async function detectEmotion() {
    const fileInput = document.getElementById('imageInput');
    if (!fileInput.files[0]) return;

    const generateBGM = document.getElementById('generateBGMCheckbox').checked;
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('generate_bgm', generateBGM);

    document.getElementById('imageLoading').classList.add('active');
    document.getElementById('imageResults').style.display = 'none';

    try {
        const response = await fetch(`${API_BASE}/emotion/detect-image`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            displayEmotionResults(data);
            await getMusicRecommendations(data.top_emotion, 'musicTracks');
            
            // Handle BGM if generated
            if (data.bgm && data.bgm.audio_url) {
                displayImageBGM(data.bgm);
            }
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Detection failed: ' + error.message);
    } finally {
        document.getElementById('imageLoading').classList.remove('active');
    }
}

function displayImageBGM(bgm) {
    const bgmCard = document.getElementById('imageBGMCard');
    const bgmPlayer = document.getElementById('imageBGMPlayer');
    
    bgmPlayer.innerHTML = `
        <p style="color: var(--text-secondary); margin-bottom: 1rem;">
            Emotion: ${bgm.emotion} | BPM: ${bgm.bpm} | Duration: ${bgm.duration}s
        </p>
        <audio id="imageBGMAudio" controls loop style="width: 100%;">
            <source src="${API_BASE.replace('/api', '')}${bgm.audio_url}" type="audio/wav">
        </audio>
        <button class="btn" onclick="downloadBGM('${bgm.audio_url}')" style="margin-top: 1rem; width: 100%;">
            Download BGM
        </button>
    `;
    
    bgmCard.style.display = 'block';
    
    // Auto-play
    setTimeout(() => {
        const audio = document.getElementById('imageBGMAudio');
        audio.play().catch(e => console.log('Auto-play blocked:', e));
    }, 500);
    
    console.log('✅ Image BGM ready to play');
}

function displayEmotionResults(data) {
    const emotionBars = document.getElementById('emotionBars');
    emotionBars.innerHTML = '';

    const emotions = Object.entries(data.emotions).sort((a, b) => b[1] - a[1]);

    emotions.forEach(([emotion, confidence]) => {
        const bar = document.createElement('div');
        bar.className = 'emotion-bar';
        bar.innerHTML = `
            <div class="emotion-label">
                <span>${emotion}</span>
                <span>${confidence.toFixed(1)}%</span>
            </div>
            <div class="emotion-progress">
                <div class="emotion-progress-bar" style="width: ${confidence}%"></div>
            </div>
        `;
        emotionBars.appendChild(bar);
    });

    document.getElementById('imageResults').style.display = 'block';
}

async function getMusicRecommendations(emotion, containerId) {
    try {
        const response = await fetch(`${API_BASE}/music/recommend`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ emotion, limit: 12 })
        });

        const data = await response.json();

        if (response.ok) {
            displayMusicTracks(data.tracks, containerId);
        }
    } catch (error) {
        console.error('Music recommendation failed:', error);
    }
}

function displayMusicTracks(tracks, containerId) {
    const musicTracks = document.getElementById(containerId);
    musicTracks.innerHTML = '';

    if (!tracks || tracks.length === 0) {
        musicTracks.innerHTML = '<p style="color: var(--text-secondary);">No recommendations found. Please check your Spotify API credentials.</p>';
        return;
    }

    tracks.forEach(track => {
        const card = document.createElement('div');
        card.className = 'track-card';
        card.innerHTML = `
            ${track.album_cover ? `<img src="${track.album_cover}" alt="${track.name}" class="track-cover">` : '<div class="track-cover" style="background: var(--bg-tertiary);"></div>'}
            <div class="track-info">
                <h3 title="${track.name}">${track.name}</h3>
                <p title="${track.artists}">${track.artists}</p>
            </div>
            ${track.preview_url ? `<audio controls class="track-preview"><source src="${track.preview_url}" type="audio/mpeg"></audio>` : '<p style="color: var(--text-secondary); font-size: 0.8rem; margin-top: 0.5rem;">No preview available</p>'}
            ${track.external_url ? `<a href="${track.external_url}" target="_blank" class="btn" style="margin-top: 1rem; width: 100%; display: block; text-align: center; text-decoration: none;">Open in Spotify</a>` : ''}
        `;
        musicTracks.appendChild(card);
    });
}

// ============================================
// WEBCAM FUNCTIONS
// ============================================
async function startWebcam() {
    try {
        webcamStream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 } });
        
        const video = document.getElementById('webcam');
        video.srcObject = webcamStream;
        
        document.getElementById('startWebcam').style.display = 'none';
        document.getElementById('stopWebcam').style.display = 'inline-block';
        document.getElementById('webcamResults').style.display = 'block';

        // Reset tracking
        allEmotions = [];
        emotionCounter = {};
        detectionCount = 0;
        lastDominantEmotion = null;
        webcamStartTime = Date.now();

        // Start emotion detection every 2 seconds
        webcamInterval = setInterval(captureAndDetect, 2000);
        
        // Update music recommendations every 10 seconds
        musicUpdateInterval = setInterval(updateWebcamMusic, 10000);
        
        // Check for BGM generation after 60 seconds, then every 2 minutes
        setTimeout(() => {
            generateWebcamBGM();
            bgmCheckInterval = setInterval(checkAndRegenerateBGM, 120000); // Every 2 minutes
        }, 60000);
        
        updateWebcamStatus('Detecting emotions...');
        console.log('✅ Webcam started');
    } catch (error) {
        alert('Could not access webcam: ' + error.message);
    }
}

async function stopWebcam() {
    console.log('🛑 Stopping webcam...');
    
    if (webcamStream) {
        webcamStream.getTracks().forEach(track => track.stop());
        webcamStream = null;
    }
    
    if (webcamInterval) {
        clearInterval(webcamInterval);
        webcamInterval = null;
    }
    
    if (musicUpdateInterval) {
        clearInterval(musicUpdateInterval);
        musicUpdateInterval = null;
    }
    
    if (bgmCheckInterval) {
        clearInterval(bgmCheckInterval);
        bgmCheckInterval = null;
    }

    const video = document.getElementById('webcam');
    video.srcObject = null;
    
    document.getElementById('startWebcam').style.display = 'inline-block';
    document.getElementById('stopWebcam').style.display = 'none';
    
    updateWebcamStatus('Webcam stopped');
}

function updateWebcamStatus(message) {
    document.getElementById('webcamStatus').textContent = message;
}

async function captureAndDetect() {
    const video = document.getElementById('webcam');
    const canvas = document.getElementById('webcamCanvas');
    const ctx = canvas.getContext('2d');

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0);

    const imageData = canvas.toDataURL('image/jpeg');

    try {
        const response = await fetch(`${API_BASE}/emotion/detect-live`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: imageData })
        });

        const data = await response.json();

        if (response.ok && data.emotions) {
            displayWebcamEmotions(data);
            
            const topEmotion = data.top_emotion;
            allEmotions.push(topEmotion);
            emotionCounter[topEmotion] = (emotionCounter[topEmotion] || 0) + 1;
            detectionCount++;
        }
    } catch (error) {
        console.error('❌ Live detection error:', error);
    }
}

function displayWebcamEmotions(data) {
    const emotionBars = document.getElementById('webcamEmotionBars');
    emotionBars.innerHTML = '';

    const emotions = Object.entries(data.emotions).sort((a, b) => b[1] - a[1]);

    emotions.forEach(([emotion, confidence]) => {
        const bar = document.createElement('div');
        bar.className = 'emotion-bar';
        bar.innerHTML = `
            <div class="emotion-label">
                <span>${emotion}</span>
                <span>${confidence.toFixed(1)}%</span>
            </div>
            <div class="emotion-progress">
                <div class="emotion-progress-bar" style="width: ${confidence}%"></div>
            </div>
        `;
        emotionBars.appendChild(bar);
    });
}

async function updateWebcamMusic() {
    if (allEmotions.length === 0) return;
    
    const dominant = calculateDominantEmotion(allEmotions);
    console.log('🎵 Updating music for:', dominant);
    await getMusicRecommendations(dominant, 'webcamMusicTracks');
}

async function generateWebcamBGM() {
    if (allEmotions.length === 0) return;
    
    const dominant = calculateDominantEmotion(allEmotions);
    lastDominantEmotion = dominant;
    
    console.log('🎵 Generating BGM for:', dominant);
    updateWebcamStatus(`Generating BGM for ${dominant}...`);
    
    try {
        const response = await fetch(`${API_BASE}/emotion/generate-bgm-for-emotion`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ emotion: dominant, duration: 20 })
        });
        
        const data = await response.json();
        
        if (response.ok && data.audio_url) {
            displayWebcamBGM(data);
            updateWebcamStatus(`Playing ${dominant} music`);
        }
    } catch (error) {
        console.error('❌ BGM generation failed:', error);
        updateWebcamStatus('BGM generation failed');
    }
}

async function checkAndRegenerateBGM() {
    if (allEmotions.length === 0) return;
    
    const currentDominant = calculateDominantEmotion(allEmotions);
    
    if (currentDominant !== lastDominantEmotion) {
        console.log('🔄 Emotion changed:', lastDominantEmotion, '→', currentDominant);
        await generateWebcamBGM();
    } else {
        console.log('✅ Same emotion, keeping current BGM');
    }
}

function displayWebcamBGM(bgm) {
    const bgmCard = document.getElementById('webcamBGMCard');
    const bgmPlayer = document.getElementById('webcamBGMPlayer');
    
    bgmPlayer.innerHTML = `
        <p style="color: var(--text-secondary); margin-bottom: 1rem;">
            Emotion: ${bgm.emotion} | BPM: ${bgm.bpm} | Duration: ${bgm.duration}s
        </p>
        <audio id="webcamBGMAudio" controls loop autoplay style="width: 100%;">
            <source src="${API_BASE.replace('/api', '')}${bgm.audio_url}" type="audio/wav">
        </audio>
    `;
    
    bgmCard.style.display = 'block';
    console.log('✅ Webcam BGM playing');
}

function calculateDominantEmotion(emotions) {
    const counts = {};
    emotions.forEach(e => counts[e] = (counts[e] || 0) + 1);
    return Object.keys(counts).reduce((a, b) => counts[a] > counts[b] ? a : b);
}

// ============================================
// VIDEO FUNCTIONS
// ============================================
function handleVideoSelect(e) {
    const file = e.target.files[0];
    if (file) {
        const url = URL.createObjectURL(file);
        document.getElementById('videoPreview').innerHTML = `
            <video src="${url}" controls style="max-width: 100%; max-height: 400px;"></video>
        `;
        document.getElementById('generateBGMBtn').style.display = 'block';
    }
}

async function generateVideoBGM() {
    const fileInput = document.getElementById('videoInput');
    if (!fileInput.files[0]) return;

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('duration', 20);

    document.getElementById('videoLoading').classList.add('active');
    document.getElementById('videoResults').style.display = 'none';

    try {
        const response = await fetch(`${API_BASE}/video/generate-bgm`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok && data.success) {
            displayVideoResults(data);
            await getMusicRecommendations(data.analysis.dominant_emotion, 'videoMusicTracks');
        } else {
            alert('Error: ' + (data.error || data.bgm_error));
        }
    } catch (error) {
        alert('BGM generation failed: ' + error.message);
    } finally {
        document.getElementById('videoLoading').classList.remove('active');
    }
}

function displayVideoResults(data) {
    const timeline = document.getElementById('emotionTimeline');
    
    if (data.analysis && data.analysis.emotion_distribution) {
        const dist = data.analysis.emotion_distribution;
        let html = '<h3>Dominant Emotion: ' + data.analysis.dominant_emotion + '</h3>';
        html += '<div class="emotion-bars">';
        
        Object.entries(dist).sort((a, b) => b[1] - a[1]).forEach(([emotion, count]) => {
            const percentage = (count / data.analysis.total_frames_analyzed * 100).toFixed(1);
            html += `
                <div class="emotion-bar">
                    <div class="emotion-label">
                        <span>${emotion}</span>
                        <span>${percentage}%</span>
                    </div>
                    <div class="emotion-progress">
                        <div class="emotion-progress-bar" style="width: ${percentage}%"></div>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        timeline.innerHTML = html;
    }

    if (data.bgm && data.bgm.audio_url) {
        displayVideoBGM(data.bgm);
    }

    document.getElementById('videoResults').style.display = 'block';
}

function displayVideoBGM(bgm) {
    const bgmCard = document.getElementById('videoBGMCard');
    const bgmPlayer = document.getElementById('videoBGMPlayer');
    
    bgmPlayer.innerHTML = `
        <p style="color: var(--text-secondary); margin-bottom: 1rem;">
            Emotion: ${bgm.emotion} | BPM: ${bgm.bpm} | Duration: ${bgm.duration}s
        </p>
        <audio id="videoBGMAudio" controls loop autoplay style="width: 100%;">
            <source src="${API_BASE.replace('/api', '')}${bgm.audio_url}" type="audio/wav">
        </audio>
        <button class="btn" onclick="downloadBGM('${bgm.audio_url}')" style="margin-top: 1rem; width: 100%;">
            Download BGM
        </button>
    `;
    
    bgmCard.style.display = 'block';
    console.log('✅ Video BGM ready to play');
}

// ============================================
// UI HELPER FUNCTIONS
// ============================================
function switchTab(tabName) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    document.getElementById(`${tabName}-tab`).classList.add('active');
}

function openModal(modalId) {
    document.getElementById(modalId).classList.add('active');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

function showAlert(elementId, message, type) {
    const alert = document.getElementById(elementId);
    alert.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
    setTimeout(() => {
        alert.innerHTML = '';
    }, 5000);
}

function downloadBGM(audioUrl) {
    window.open(API_BASE.replace('/api', '') + audioUrl, '_blank');
}

// Close modal on outside click
document.querySelectorAll('.modal').forEach(modal => {
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
        }
    });
});