EmoRhythm - Project Structure & Integration Plan
Complete Project Directory Structure
emorhythm/
│
├── backend/
│   ├── app.py                          # Main Flask application
│   ├── config.py                       # Configuration settings
│   ├── requirements.txt                # Python dependencies
│   │
│   ├── models/                         # ML Models
│   │   ├── __init__.py
│   │   ├── emotion_model.py            # Emotion detection model class
│   │   ├── face_detector.py            # Face detection module
│   │   ├── video_analyzer.py           # Video emotion analysis
│   │   └── saved_models/
│   │       ├── best_emotion_model.pth  # Trained emotion model
│   │       └── model_info.json         # Model metadata
│   │
│   ├── services/                       # Business Logic
│   │   ├── __init__.py
│   │   ├── emotion_service.py          # Emotion detection service
│   │   ├── music_service.py            # Music recommendation service
│   │   ├── spotify_service.py          # Spotify API integration
│   │   ├── gemini_service.py           # Google Gemini music generation
│   │   └── video_service.py            # Video processing service
│   │
│   ├── routes/                         # API Endpoints
│   │   ├── __init__.py
│   │   ├── auth_routes.py              # Authentication endpoints
│   │   ├── emotion_routes.py           # Emotion detection endpoints
│   │   ├── music_routes.py             # Music recommendation endpoints
│   │   └── video_routes.py             # Video BGM generation endpoints
│   │
│   ├── utils/                          # Utility Functions
│   │   ├── __init__.py
│   │   ├── image_utils.py              # Image processing utilities
│   │   ├── video_utils.py              # Video processing utilities
│   │   ├── emotion_mapping.py          # Emotion-to-genre mappings
│   │   └── validators.py               # Input validation
│   │
│   ├── database/                       # Database
│   │   ├── __init__.py
│   │   ├── db.py                       # Database connection
│   │   ├── models.py                   # Database models
│   │   └── users.json                  # User data (temporary)
│   │
│   └── static/                         # Static files
│       ├── uploads/                    # Uploaded images/videos
│       ├── generated/                  # Generated music files
│       └── temp/                       # Temporary files
│
├── frontend/                           # Frontend application (optional)
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── assets/
│
=
├── notebooks/                          # Jupyter notebooks for training
│   ├── train_emotion_model.ipynb
│   └── data_analysis.ipynb
│


How the Projects Will Be Combined
1. Emotion Detection Module (From app.py)
app.py Components Used:
├── EfficientNet-B2 emotion model loading
├── Face detection (Haar Cascade + DeepFace)
├── Image preprocessing and transformation
├── Emotion prediction logic
├── GradCAM visualization
└── Webcam capture functionality

Integration Points:
→ Extract as emotion_service.py
→ Reuse model loading in emotion_model.py
→ Create unified face_detector.py
2. Music Recommendation Module (From main.py)
main.py Components Used:
├── Spotify API integration (Spotipy)
├── Emotion-to-genre mapping (combined_labels)
├── Artist genre detection
├── Track filtering and recommendations
├── Sentiment + Emotion combination
└── User authentication system

Integration Points:
→ Extract as music_service.py
→ Move Spotify logic to spotify_service.py
→ Reuse emotion_mapping in utils/
→ Merge user auth with Flask sessions
3. New BGM Generation Module (Google Gemini)
New Component:
├── Google Gemini Lyria API integration
├── Real-time music synthesis
├── Emotion-weighted prompt generation
├── BPM and temperature control
└── Audio streaming

Integration Points:
→ Create gemini_service.py
→ Link with video_analyzer.py
→ Store generated audio in static/generated/

Integration Architecture
┌─────────────────────────────────────────────────────────────────┐
│                         FLASK BACKEND                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────┐       ┌─────────────────┐                  │
│  │  User Request   │──────▶│  Flask Routes   │                  │
│  │  (API Calls)    │       │  (auth, emotion,│                  │
│  └─────────────────┘       │   music, video) │                  │
│                             └────────┬────────┘                  │
│                                      │                            │
│                                      ▼                            │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    SERVICES LAYER                         │  │
│  ├───────────────────────────────────────────────────────────┤  │
│  │                                                            │  │
│  │  ┌──────────────────┐  ┌──────────────────┐             │  │
│  │  │ Emotion Service  │  │  Music Service   │             │  │
│  │  │                  │  │                  │             │  │
│  │  │ • Face Detection │  │ • Spotify API    │             │  │
│  │  │ • Emotion Predict│  │ • Recommendations│             │  │
│  │  │ • DeepFace/Custom│  │ • Playlist Create│             │  │
│  │  └─────────┬────────┘  └─────────┬────────┘             │  │
│  │            │                      │                       │  │
│  │            └──────────┬───────────┘                       │  │
│  │                       │                                   │  │
│  │                       ▼                                   │  │
│  │            ┌─────────────────────┐                       │  │
│  │            │  Emotion Mapping    │                       │  │
│  │            │  (Combined Labels)  │                       │  │
│  │            └─────────────────────┘                       │  │
│  │                       │                                   │  │
│  │       ┌───────────────┴───────────────┐                 │  │
│  │       ▼                               ▼                  │  │
│  │  ┌────────────────┐         ┌────────────────┐         │  │
│  │  │ Spotify Tracks │         │ Gemini BGM Gen │         │  │
│  │  └────────────────┘         └────────────────┘         │  │
│  │                                                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    VIDEO PROCESSING                       │  │
│  ├───────────────────────────────────────────────────────────┤  │
│  │                                                            │  │
│  │  Video Upload → Frame Extraction → Emotion Detection      │  │
│  │       ↓              ↓                    ↓               │  │
│  │  Store Temp    Batch Process      Aggregate Emotions      │  │
│  │       ↓              ↓                    ↓               │  │
│  │  OpenCV        Face Detect         Dominant Emotion       │  │
│  │                     ↓                     ↓               │  │
│  │              Emotion Timeline    Generate BGM (Gemini)    │  │
│  │                                           ↓               │  │
│  │                                    Return Audio Stream     │  │
│  │                                                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

Data Flow: Complete User Journey
Scenario 1: Image Upload → Emotion Detection → Music Recommendation
User Action:
├── Upload Image via Frontend
└── Click "Detect Emotion"

Backend Processing:
├── 1. Receive image at /api/detect-emotion
├── 2. Save image to static/uploads/
├── 3. Load image with PIL
├── 4. Face Detection (Haar Cascade)
│    ├── If face found → Crop face
│    └── If no face → Return error
├── 5. Emotion Prediction (Custom Model)
│    ├── Preprocess image (resize, normalize)
│    ├── Forward pass through EfficientNet-B2
│    ├── Get emotion probabilities
│    └── Get top emotion
├── 6. Emotion-to-Genre Mapping
│    ├── Get emotion (e.g., "Happy")
│    ├── Map to genres (e.g., ["pop", "dance", "happy"])
│    └── Optional: Combine with sentiment
├── 7. Spotify Music Recommendation
│    ├── Query Spotify API with genres
│    ├── Filter tracks by popularity/relevance
│    ├── Get top 10 tracks
│    └── Return track details (name, artist, preview URL, cover)
├── 8. Return Response to Frontend
│    └── {
│          "emotion": "Happy",
│          "confidence": 85.3,
│          "all_emotions": {...},
│          "music_recommendations": [...]
│        }

Frontend Display:
├── Show emotion probabilities (bar chart)
├── Display music recommendations
└── Enable Spotify preview playback
Scenario 2: Webcam Live Detection → Real-time Music
User Action:
├── Enable webcam
└── Start live detection

Backend Processing:
├── 1. Receive frame stream at /api/detect-live
├── 2. Convert base64 to image
├── 3. Face Detection (DeepFace for real-time)
│    └── Faster processing for live feed
├── 4. Emotion Prediction (DeepFace)
│    └── Real-time emotion analysis
├── 5. Return emotion every frame
│    └── { "emotion": "Happy", "confidence": 78.5 }
├── 6. Frontend aggregates emotions
│    └── Get dominant emotion over 3 seconds
├── 7. Request music recommendations
│    └── POST /api/recommend-music
└── 8. Update music playlist dynamically

Frontend Display:
├── Live webcam with emotion overlay
├── Real-time emotion bar chart
└── Auto-update music recommendations
Scenario 3: Video Upload → BGM Generation
User Action:
├── Upload video file
└── Click "Generate BGM"

Backend Processing:
├── 1. Receive video at /api/analyze-video
├── 2. Save video to static/uploads/
├── 3. Extract frames (1 frame per second)
│    └── Using OpenCV
├── 4. Batch Emotion Detection
│    ├── For each frame:
│    │    ├── Detect face
│    │    ├── Predict emotion
│    │    └── Store emotion + timestamp
│    └── Create emotion timeline
├── 5. Aggregate Emotions
│    ├── Count emotion frequencies
│    ├── Determine dominant emotion (40% weight)
│    ├── Identify emotion transitions
│    └── Calculate average confidence
├── 6. Generate BGM with Google Gemini
│    ├── Create weighted prompt:
│    │    └── ["minimal techno": 0.3, "ambient": 0.7]
│    ├── Set BPM based on emotion:
│    │    ├── Happy → 120-140 BPM
│    │    ├── Sad → 60-80 BPM
│    │    └── Angry → 140-180 BPM
│    ├── Set temperature (creativity):
│    │    └── 1.0 for balanced generation
│    ├── Call Gemini Lyria API
│    ├── Stream audio chunks
│    └── Save as MP3 file
├── 7. Return Response
│    └── {
│          "dominant_emotion": "Happy",
│          "emotion_timeline": [...],
│          "bgm_url": "/static/generated/bgm_12345.mp3",
│          "duration": 30
│        }

Frontend Display:
├── Show emotion timeline (line chart)
├── Display dominant emotion
├── Video player with generated BGM
└── Download BGM option

API Integration Map
┌──────────────────────────────────────────────────────────────┐
│                    EMOTION DETECTION APIs                     │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  POST /api/detect-emotion                                    │
│  ├── Input: Image file (multipart/form-data)                │
│  ├── Process: Face detect → Emotion predict (Custom Model)  │
│  └── Output: Emotion probabilities + Top emotion            │
│                                                               │
│  POST /api/detect-live                                       │
│  ├── Input: Base64 encoded frame                            │
│  ├── Process: Face detect → Emotion predict (DeepFace)      │
│  └── Output: Real-time emotion                              │
│                                                               │
│  POST /api/analyze-video                                     │
│  ├── Input: Video file                                       │
│  ├── Process: Frame extraction → Batch emotion analysis     │
│  └── Output: Emotion timeline + Dominant emotion            │
│                                                               │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                    MUSIC RECOMMENDATION APIs                  │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  POST /api/recommend-music                                   │
│  ├── Input: { "emotion": "Happy", "limit": 10 }            │
│  ├── Process: Emotion → Genres → Spotify search             │
│  └── Output: Track list with Spotify details                │
│                                                               │
│  GET /api/emotion-to-genre                                   │
│  ├── Input: Query param ?emotion=Happy                       │
│  └── Output: Genre list                                      │
│                                                               │
│  POST /api/artist-recommendations                            │
│  ├── Input: { "emotion": "Happy", "artist": "Artist Name" } │
│  ├── Process: Get artist genres → Filter by emotion genre   │
│  └── Output: Filtered artist tracks                         │
│                                                               │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                    BGM GENERATION APIs                        │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  POST /api/generate-bgm                                      │
│  ├── Input: {                                                │
│  │    "emotion": "Happy",                                   │
│  │    "bpm": 120,                                           │
│  │    "temperature": 1.0,                                   │
│  │    "duration": 30                                        │
│  │  }                                                        │
│  ├── Process: Create prompt → Call Gemini → Generate music  │
│  └── Output: Audio file URL                                 │
│                                                               │
│  POST /api/generate-video-bgm                                │
│  ├── Input: Video file + emotion_timeline                   │
│  ├── Process: Multi-segment BGM generation                  │
│  └── Output: Composite BGM audio file                       │
│                                                               │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                    USER MANAGEMENT APIs                       │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  POST /api/register                                          │
│  POST /api/login                                             │
│  POST /api/logout                                            │
│  GET  /api/user-profile                                      │
│  GET  /api/user-history                                      │
│                                                               │
└──────────────────────────────────────────────────────────────┘