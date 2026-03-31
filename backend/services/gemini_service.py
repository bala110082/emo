# # # import os
# # # import asyncio
# # # import sys
# # # from google import genai
# # # from google.genai import types
# # # from dotenv import load_dotenv
# # # import base64
# # # import time
# # # import wave

# # # load_dotenv()

# # # class GeminiMusicService:
# # #     def __init__(self):
# # #         api_key = os.getenv('GOOGLE_API_KEY') or 'AIzaSyD6Z1B4At-908dalV2ohCssF9t7RIPp3NU'
# # #         if not api_key:
# # #             raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
# # #         self.client = genai.Client(
# # #             api_key=api_key,
# # #             http_options={'api_version': 'v1alpha'}
# # #         )
        
# # #         # Emotion to music prompt mapping
# # #         self.emotion_prompts = {
# # #             'happy': 'upbeat cheerful pop music with positive energy',
# # #             'sad': 'melancholic slow piano ballad',
# # #             'angry': 'aggressive intense rock music',
# # #             'fear': 'dark suspenseful ambient music',
# # #             'disgust': 'dissonant industrial electronic',
# # #             'surprise': 'dynamic energetic electronic dance',
# # #             'neutral': 'minimal ambient techno'
# # #         }
        
# # #         # Emotion to BPM mapping
# # #         self.emotion_bpm = {
# # #             'happy': 120,
# # #             'sad': 70,
# # #             'angry': 150,
# # #             'fear': 100,
# # #             'disgust': 110,
# # #             'surprise': 130,
# # #             'neutral': 90
# # #         }
        
# # #         print("✅ Gemini Music Service initialized successfully")
    
# # #     def get_prompt_for_emotion(self, emotion):
# # #         """Get music prompt for emotion"""
# # #         emotion_lower = emotion.lower()
# # #         return self.emotion_prompts.get(emotion_lower, 'minimal ambient techno')
    
# # #     def get_bpm_for_emotion(self, emotion):
# # #         """Get BPM for emotion"""
# # #         emotion_lower = emotion.lower()
# # #         return self.emotion_bpm.get(emotion_lower, 90)
    
# # #     async def generate_bgm_async(self, emotion='neutral', bpm=None, temperature=1.0, duration=20):
# # #         """
# # #         Generate background music asynchronously (default 20 seconds)
        
# # #         Args:
# # #             emotion: Emotion to generate music for
# # #             bpm: Beats per minute (optional, will use emotion default)
# # #             temperature: Creativity parameter (0.0 - 2.0)
# # #             duration: Duration in seconds (default 20)
        
# # #         Returns:
# # #             dict with audio_data (base64), format, duration
# # #         """
# # #         start_time = time.time()
        
# # #         try:
# # #             prompt = self.get_prompt_for_emotion(emotion)
# # #             if bpm is None:
# # #                 bpm = self.get_bpm_for_emotion(emotion)
            
# # #             print(f"\n🎵 Generating {duration}s music for: {emotion}")
# # #             print(f"📝 Prompt: {prompt} | BPM: {bpm}")
            
# # #             audio_chunks = []
            
# # #             # Python 3.11+ version with TaskGroup
# # #             if sys.version_info >= (3, 11):
# # #                 async with self.client.aio.live.music.connect(
# # #                     model='models/lyria-realtime-exp'
# # #                 ) as session:
                    
# # #                     async def receive_audio():
# # #                         """Receive audio chunks from the server"""
# # #                         async for message in session.receive():
# # #                             if hasattr(message, 'server_content') and \
# # #                                hasattr(message.server_content, 'audio_chunks'):
# # #                                 for chunk in message.server_content.audio_chunks:
# # #                                     audio_chunks.append(chunk.data)
                    
# # #                     async with asyncio.TaskGroup() as tg:
# # #                         receive_task = tg.create_task(receive_audio())
                        
# # #                         await session.set_weighted_prompts(
# # #                             prompts=[types.WeightedPrompt(text=prompt, weight=1.0)]
# # #                         )
# # #                         await session.set_music_generation_config(
# # #                             config=types.LiveMusicGenerationConfig(
# # #                                 bpm=bpm,
# # #                                 temperature=temperature,
# # #                                 guidance=4.0,
# # #                                 density=0.7,
# # #                                 brightness=0.6
# # #                             )
# # #                         )
                        
# # #                         await session.play()
# # #                         await asyncio.sleep(duration)
# # #                         await session.stop()
# # #                         await asyncio.sleep(1)
     
# # #             else:
# # #                 # Python 3.10 and below
# # #                 async with self.client.aio.live.music.connect(
# # #                     model='models/lyria-realtime-exp'
# # #                 ) as session:
                    
# # #                     async def receive_audio():
# # #                         """Receive audio chunks from the server"""
# # #                         try:
# # #                             async for message in session.receive():
# # #                                 if hasattr(message, 'server_content') and \
# # #                                    hasattr(message.server_content, 'audio_chunks'):
# # #                                     for chunk in message.server_content.audio_chunks:
# # #                                         audio_chunks.append(chunk.data)
# # #                         except Exception as e:
# # #                             print(f"⚠️ Receive error: {e}")
                    
# # #                     receive_task = asyncio.create_task(receive_audio())
                    
# # #                     try:
# # #                         await session.set_weighted_prompts(
# # #                             prompts=[types.WeightedPrompt(text=prompt, weight=1.0)]
# # #                         )
# # #                         await session.set_music_generation_config(
# # #                             config=types.LiveMusicGenerationConfig(
# # #                                 bpm=bpm,
# # #                                 temperature=temperature,
# # #                                 guidance=4.0,
# # #                                 density=0.7,
# # #                                 brightness=0.6
# # #                             )
# # #                         )
                        
# # #                         await session.play()
# # #                         await asyncio.sleep(duration)
# # #                         await session.stop()
# # #                         await asyncio.sleep(1)
                        
# # #                     finally:
# # #                         receive_task.cancel()
# # #                         try:
# # #                             await receive_task
# # #                         except asyncio.CancelledError:
# # #                             pass
            
# # #             # Check if we got audio
# # #             if not audio_chunks:
# # #                 elapsed = time.time() - start_time
# # #                 print(f"❌ No audio received ({elapsed:.2f}s)")
# # #                 return {'error': 'No audio data received'}
            
# # #             # Combine and encode
# # #             combined_audio = b''.join(audio_chunks)
# # #             audio_base64 = base64.b64encode(combined_audio).decode('utf-8')
            
# # #             elapsed = time.time() - start_time
# # #             size_mb = len(combined_audio) / (1024 * 1024)
            
# # #             print(f"✅ Generated {size_mb:.2f}MB in {elapsed:.2f}s")
            
# # #             return {
# # #                 'success': True,
# # #                 'audio_data': audio_base64,
# # #                 'format': 'audio/wav',
# # #                 'duration': duration,
# # #                 'emotion': emotion,
# # #                 'bpm': bpm,
# # #                 'prompt': prompt,
# # #                 'file_size_mb': round(size_mb, 2),
# # #                 'elapsed_time': round(elapsed, 2)
# # #             }
        
# # #         except Exception as e:
# # #             elapsed = time.time() - start_time
# # #             print(f"❌ Error: {str(e)}")
# # #             return {'error': str(e), 'elapsed_time': elapsed}
    
# # #     def generate_bgm_sync(self, emotion='neutral', bpm=None, temperature=1.0, duration=20):
# # #         """
# # #         Synchronous wrapper for BGM generation (default 20 seconds)
# # #         """
# # #         try:
# # #             loop = asyncio.new_event_loop()
# # #             asyncio.set_event_loop(loop)
            
# # #             result = loop.run_until_complete(
# # #                 self.generate_bgm_async(emotion, bpm, temperature, duration)
# # #             )
            
# # #             loop.close()
# # #             return result
        
# # #         except Exception as e:
# # #             print(f"❌ Sync error: {str(e)}")
# # #             return {'error': str(e)}
    
# # #     def save_bgm_to_file(self, audio_data_base64, filepath):
# # #         """
# # #         Save base64 audio to WAV file with proper format
        
# # #         Gemini Lyria outputs:
# # #         - Raw 16-bit PCM Audio
# # #         - Sample rate: 48kHz
# # #         - Channels: 2 (stereo)
# # #         """
# # #         try:
# # #             audio_bytes = base64.b64decode(audio_data_base64)
            
# # #             with wave.open(filepath, 'wb') as wav_file:
# # #                 wav_file.setnchannels(2)  # Stereo
# # #                 wav_file.setsampwidth(2)  # 16-bit
# # #                 wav_file.setframerate(48000)  # 48kHz
# # #                 wav_file.writeframes(audio_bytes)
            
# # #             print(f"💾 Saved: {filepath}")
# # #             return True
            
# # #         except Exception as e:
# # #             print(f"❌ Save error: {str(e)}")
# # #             return False

# # # # Global instance
# # # gemini_service = GeminiMusicService()


# # import os
# # import asyncio
# # import sys
# # from google import genai
# # from google.genai import types
# # from dotenv import load_dotenv
# # import base64
# # import time
# # import wave
# # import subprocess
# # import platform

# # load_dotenv()

# # class GeminiMusicService:
# #     def __init__(self):
# #         api_key = os.getenv('GOOGLE_API_KEY') or 'AIzaSyD6Z1B4At-908dalV2ohCssF9t7RIPp3NU'
# #         if not api_key:
# #             raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
# #         self.client = genai.Client(
# #             api_key=api_key,
# #             http_options={'api_version': 'v1alpha'}
# #         )
        
# #         # Emotion to music prompt mapping
# #         self.emotion_prompts = {
# #             'happy': 'upbeat cheerful pop music with positive energy',
# #             'sad': 'melancholic slow piano ballad',
# #             'angry': 'aggressive intense rock music',
# #             'fear': 'dark suspenseful ambient music',
# #             'disgust': 'dissonant industrial electronic',
# #             'surprise': 'dynamic energetic electronic dance',
# #             'neutral': 'minimal ambient techno'
# #         }
        
# #         # Emotion to BPM mapping
# #         self.emotion_bpm = {
# #             'happy': 120,
# #             'sad': 70,
# #             'angry': 150,
# #             'fear': 100,
# #             'disgust': 110,
# #             'surprise': 130,
# #             'neutral': 90
# #         }
        
# #         print("✅ Gemini Music Service initialized successfully")
    
# #     def get_prompt_for_emotion(self, emotion):
# #         """Get music prompt for emotion"""
# #         emotion_lower = emotion.lower()
# #         return self.emotion_prompts.get(emotion_lower, 'minimal ambient techno')
    
# #     def get_bpm_for_emotion(self, emotion):
# #         """Get BPM for emotion"""
# #         emotion_lower = emotion.lower()
# #         return self.emotion_bpm.get(emotion_lower, 90)
    
# #     async def generate_bgm_async(self, emotion='neutral', bpm=None, temperature=1.0, duration=20):
# #         """
# #         Generate background music asynchronously (default 20 seconds)
        
# #         Args:
# #             emotion: Emotion to generate music for
# #             bpm: Beats per minute (optional, will use emotion default)
# #             temperature: Creativity parameter (0.0 - 2.0)
# #             duration: Duration in seconds (default 20)
        
# #         Returns:
# #             dict with audio_data (base64), format, duration
# #         """
# #         start_time = time.time()
        
# #         try:
# #             prompt = self.get_prompt_for_emotion(emotion)
# #             if bpm is None:
# #                 bpm = self.get_bpm_for_emotion(emotion)
            
# #             print(f"\n🎵 Generating {duration}s music for: {emotion}")
# #             print(f"📝 Prompt: {prompt} | BPM: {bpm}")
            
# #             audio_chunks = []
            
# #             # Python 3.11+ version with TaskGroup
# #             if sys.version_info >= (3, 11):
# #                 async with self.client.aio.live.music.connect(
# #                     model='models/lyria-realtime-exp'
# #                 ) as session:
                    
# #                     async def receive_audio():
# #                         """Receive audio chunks from the server"""
# #                         async for message in session.receive():
# #                             if hasattr(message, 'server_content') and \
# #                                hasattr(message.server_content, 'audio_chunks'):
# #                                 for chunk in message.server_content.audio_chunks:
# #                                     audio_chunks.append(chunk.data)
                    
# #                     async with asyncio.TaskGroup() as tg:
# #                         receive_task = tg.create_task(receive_audio())
                        
# #                         await session.set_weighted_prompts(
# #                             prompts=[types.WeightedPrompt(text=prompt, weight=1.0)]
# #                         )
# #                         await session.set_music_generation_config(
# #                             config=types.LiveMusicGenerationConfig(
# #                                 bpm=bpm,
# #                                 temperature=temperature,
# #                                 guidance=4.0,
# #                                 density=0.7,
# #                                 brightness=0.6
# #                             )
# #                         )
                        
# #                         await session.play()
# #                         await asyncio.sleep(duration)
# #                         await session.stop()
# #                         await asyncio.sleep(1)
     
# #             else:
# #                 # Python 3.10 and below
# #                 async with self.client.aio.live.music.connect(
# #                     model='models/lyria-realtime-exp'
# #                 ) as session:
                    
# #                     async def receive_audio():
# #                         """Receive audio chunks from the server"""
# #                         try:
# #                             async for message in session.receive():
# #                                 if hasattr(message, 'server_content') and \
# #                                    hasattr(message.server_content, 'audio_chunks'):
# #                                     for chunk in message.server_content.audio_chunks:
# #                                         audio_chunks.append(chunk.data)
# #                         except Exception as e:
# #                             print(f"⚠️ Receive error: {e}")
                    
# #                     receive_task = asyncio.create_task(receive_audio())
                    
# #                     try:
# #                         await session.set_weighted_prompts(
# #                             prompts=[types.WeightedPrompt(text=prompt, weight=1.0)]
# #                         )
# #                         await session.set_music_generation_config(
# #                             config=types.LiveMusicGenerationConfig(
# #                                 bpm=bpm,
# #                                 temperature=temperature,
# #                                 guidance=4.0,
# #                                 density=0.7,
# #                                 brightness=0.6
# #                             )
# #                         )
                        
# #                         await session.play()
# #                         await asyncio.sleep(duration)
# #                         await session.stop()
# #                         await asyncio.sleep(1)
                        
# #                     finally:
# #                         receive_task.cancel()
# #                         try:
# #                             await receive_task
# #                         except asyncio.CancelledError:
# #                             pass
            
# #             # Check if we got audio
# #             if not audio_chunks:
# #                 elapsed = time.time() - start_time
# #                 print(f"❌ No audio received ({elapsed:.2f}s)")
# #                 return {'error': 'No audio data received'}
            
# #             # Combine and encode
# #             combined_audio = b''.join(audio_chunks)
# #             audio_base64 = base64.b64encode(combined_audio).decode('utf-8')
            
# #             elapsed = time.time() - start_time
# #             size_mb = len(combined_audio) / (1024 * 1024)
            
# #             print(f"✅ Generated {size_mb:.2f}MB in {elapsed:.2f}s")
            
# #             return {
# #                 'success': True,
# #                 'audio_data': audio_base64,
# #                 'format': 'audio/wav',
# #                 'duration': duration,
# #                 'emotion': emotion,
# #                 'bpm': bpm,
# #                 'prompt': prompt,
# #                 'file_size_mb': round(size_mb, 2),
# #                 'elapsed_time': round(elapsed, 2)
# #             }
        
# #         except Exception as e:
# #             elapsed = time.time() - start_time
# #             print(f"❌ Error: {str(e)}")
# #             return {'error': str(e), 'elapsed_time': elapsed}
    
# #     def generate_bgm_sync(self, emotion='neutral', bpm=None, temperature=1.0, duration=20):
# #         """
# #         Synchronous wrapper for BGM generation (default 20 seconds)
# #         """
# #         try:
# #             loop = asyncio.new_event_loop()
# #             asyncio.set_event_loop(loop)
            
# #             result = loop.run_until_complete(
# #                 self.generate_bgm_async(emotion, bpm, temperature, duration)
# #             )
            
# #             loop.close()
# #             return result
        
# #         except Exception as e:
# #             print(f"❌ Sync error: {str(e)}")
# #             return {'error': str(e)}
    
# #     def save_bgm_to_file(self, audio_data_base64, filepath):
# #         """
# #         Save base64 audio to WAV file with proper format
        
# #         Gemini Lyria outputs:
# #         - Raw 16-bit PCM Audio
# #         - Sample rate: 48kHz
# #         - Channels: 2 (stereo)
# #         """
# #         try:
# #             audio_bytes = base64.b64decode(audio_data_base64)
            
# #             with wave.open(filepath, 'wb') as wav_file:
# #                 wav_file.setnchannels(2)  # Stereo
# #                 wav_file.setsampwidth(2)  # 16-bit
# #                 wav_file.setframerate(48000)  # 48kHz
# #                 wav_file.writeframes(audio_bytes)
            
# #             print(f"💾 Saved: {filepath}")
# #             return True
            
# #         except Exception as e:
# #             print(f"❌ Save error: {str(e)}")
# #             return False
    
# #     def play_audio_file(self, filepath):
# #         """
# #         Play audio file using system's default media player
        
# #         Args:
# #             filepath: Path to the audio file
        
# #         Returns:
# #             bool: Success status
# #         """
# #         try:
# #             system = platform.system()
            
# #             print(f"🎵 Playing audio: {filepath}")
            
# #             if system == 'Windows':
# #                 # Windows - use start command
# #                 os.startfile(filepath)
# #                 print("✅ Opened in Windows Media Player")
# #             elif system == 'Darwin':
# #                 # macOS - use open command
# #                 subprocess.Popen(['open', filepath])
# #                 print("✅ Opened in default macOS player")
# #             else:
# #                 # Linux - try multiple players
# #                 players = ['vlc', 'mpv', 'mplayer', 'xdg-open']
# #                 for player in players:
# #                     try:
# #                         subprocess.Popen([player, filepath])
# #                         print(f"✅ Opened in {player}")
# #                         return True
# #                     except FileNotFoundError:
# #                         continue
# #                 print("⚠️ No media player found on Linux")
# #                 return False
            
# #             return True
            
# #         except Exception as e:
# #             print(f"❌ Error playing audio: {str(e)}")
# #             return False

# # # Global instance
# # gemini_service = GeminiMusicService()

# import os
# import asyncio
# import sys
# from google import genai
# from google.genai import types
# from dotenv import load_dotenv
# import base64
# import time
# import wave
# import subprocess
# import platform
# import threading

# load_dotenv()

# class GeminiMusicService:
#     def __init__(self):
#         api_key = os.getenv('GOOGLE_API_KEY') or 'AIzaSyD6Z1B4At-908dalV2ohCssF9t7RIPp3NU'
#         if not api_key:
#             raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
#         self.client = genai.Client(
#             api_key=api_key,
#             http_options={'api_version': 'v1alpha'}
#         )
        
#         # Try to import pygame for looping audio
#         self.pygame = None
#         try:
#             import pygame
#             self.pygame = pygame
#             print("✅ Pygame available - will use for looping audio")
#         except ImportError:
#             print("⚠️ Pygame not available - audio will not loop automatically")
        
#         # Current playing audio
#         self.current_audio_thread = None
#         self.stop_audio_flag = False
        
#         # Emotion to music prompt mapping
#         self.emotion_prompts = {
#             'happy': 'upbeat cheerful pop music with positive energy',
#             'sad': 'melancholic slow piano ballad',
#             'angry': 'aggressive intense rock music',
#             'fear': 'dark suspenseful ambient music',
#             'disgust': 'dissonant industrial electronic',
#             'surprise': 'dynamic energetic electronic dance',
#             'neutral': 'minimal ambient techno'
#         }
        
#         # Emotion to BPM mapping
#         self.emotion_bpm = {
#             'happy': 120,
#             'sad': 70,
#             'angry': 150,
#             'fear': 100,
#             'disgust': 110,
#             'surprise': 130,
#             'neutral': 90
#         }
        
#         print("✅ Gemini Music Service initialized successfully")
    
#     def get_prompt_for_emotion(self, emotion):
#         """Get music prompt for emotion"""
#         emotion_lower = emotion.lower()
#         return self.emotion_prompts.get(emotion_lower, 'minimal ambient techno')
    
#     def get_bpm_for_emotion(self, emotion):
#         """Get BPM for emotion"""
#         emotion_lower = emotion.lower()
#         return self.emotion_bpm.get(emotion_lower, 90)
    
#     async def generate_bgm_async(self, emotion='neutral', bpm=None, temperature=1.0, duration=20):
#         """
#         Generate background music asynchronously (default 20 seconds)
        
#         Args:
#             emotion: Emotion to generate music for
#             bpm: Beats per minute (optional, will use emotion default)
#             temperature: Creativity parameter (0.0 - 2.0)
#             duration: Duration in seconds (default 20)
        
#         Returns:
#             dict with audio_data (base64), format, duration
#         """
#         start_time = time.time()
        
#         try:
#             prompt = self.get_prompt_for_emotion(emotion)
#             if bpm is None:
#                 bpm = self.get_bpm_for_emotion(emotion)
            
#             print(f"\n🎵 Generating {duration}s music for: {emotion}")
#             print(f"📝 Prompt: {prompt} | BPM: {bpm}")
            
#             audio_chunks = []
            
#             # Python 3.11+ version with TaskGroup
#             if sys.version_info >= (3, 11):
#                 async with self.client.aio.live.music.connect(
#                     model='models/lyria-realtime-exp'
#                 ) as session:
                    
#                     async def receive_audio():
#                         """Receive audio chunks from the server"""
#                         async for message in session.receive():
#                             if hasattr(message, 'server_content') and \
#                                hasattr(message.server_content, 'audio_chunks'):
#                                 for chunk in message.server_content.audio_chunks:
#                                     audio_chunks.append(chunk.data)
                    
#                     async with asyncio.TaskGroup() as tg:
#                         receive_task = tg.create_task(receive_audio())
                        
#                         await session.set_weighted_prompts(
#                             prompts=[types.WeightedPrompt(text=prompt, weight=1.0)]
#                         )
#                         await session.set_music_generation_config(
#                             config=types.LiveMusicGenerationConfig(
#                                 bpm=bpm,
#                                 temperature=temperature,
#                                 guidance=4.0,
#                                 density=0.7,
#                                 brightness=0.6
#                             )
#                         )
                        
#                         await session.play()
#                         await asyncio.sleep(duration)
#                         await session.stop()
#                         await asyncio.sleep(1)
     
#             else:
#                 # Python 3.10 and below
#                 async with self.client.aio.live.music.connect(
#                     model='models/lyria-realtime-exp'
#                 ) as session:
                    
#                     async def receive_audio():
#                         """Receive audio chunks from the server"""
#                         try:
#                             async for message in session.receive():
#                                 if hasattr(message, 'server_content') and \
#                                    hasattr(message.server_content, 'audio_chunks'):
#                                     for chunk in message.server_content.audio_chunks:
#                                         audio_chunks.append(chunk.data)
#                         except Exception as e:
#                             print(f"⚠️ Receive error: {e}")
                    
#                     receive_task = asyncio.create_task(receive_audio())
                    
#                     try:
#                         await session.set_weighted_prompts(
#                             prompts=[types.WeightedPrompt(text=prompt, weight=1.0)]
#                         )
#                         await session.set_music_generation_config(
#                             config=types.LiveMusicGenerationConfig(
#                                 bpm=bpm,
#                                 temperature=temperature,
#                                 guidance=4.0,
#                                 density=0.7,
#                                 brightness=0.6
#                             )
#                         )
                        
#                         await session.play()
#                         await asyncio.sleep(duration)
#                         await session.stop()
#                         await asyncio.sleep(1)
                        
#                     finally:
#                         receive_task.cancel()
#                         try:
#                             await receive_task
#                         except asyncio.CancelledError:
#                             pass
            
#             # Check if we got audio
#             if not audio_chunks:
#                 elapsed = time.time() - start_time
#                 print(f"❌ No audio received ({elapsed:.2f}s)")
#                 return {'error': 'No audio data received'}
            
#             # Combine and encode
#             combined_audio = b''.join(audio_chunks)
#             audio_base64 = base64.b64encode(combined_audio).decode('utf-8')
            
#             elapsed = time.time() - start_time
#             size_mb = len(combined_audio) / (1024 * 1024)
            
#             print(f"✅ Generated {size_mb:.2f}MB in {elapsed:.2f}s")
            
#             return {
#                 'success': True,
#                 'audio_data': audio_base64,
#                 'format': 'audio/wav',
#                 'duration': duration,
#                 'emotion': emotion,
#                 'bpm': bpm,
#                 'prompt': prompt,
#                 'file_size_mb': round(size_mb, 2),
#                 'elapsed_time': round(elapsed, 2)
#             }
        
#         except Exception as e:
#             elapsed = time.time() - start_time
#             print(f"❌ Error: {str(e)}")
#             return {'error': str(e), 'elapsed_time': elapsed}
    
#     def generate_bgm_sync(self, emotion='neutral', bpm=None, temperature=1.0, duration=20):
#         """
#         Synchronous wrapper for BGM generation (default 20 seconds)
#         """
#         try:
#             loop = asyncio.new_event_loop()
#             asyncio.set_event_loop(loop)
            
#             result = loop.run_until_complete(
#                 self.generate_bgm_async(emotion, bpm, temperature, duration)
#             )
            
#             loop.close()
#             return result
        
#         except Exception as e:
#             print(f"❌ Sync error: {str(e)}")
#             return {'error': str(e)}
    
#     def save_bgm_to_file(self, audio_data_base64, filepath):
#         """
#         Save base64 audio to WAV file with proper format
        
#         Gemini Lyria outputs:
#         - Raw 16-bit PCM Audio
#         - Sample rate: 48kHz
#         - Channels: 2 (stereo)
#         """
#         try:
#             audio_bytes = base64.b64decode(audio_data_base64)
            
#             with wave.open(filepath, 'wb') as wav_file:
#                 wav_file.setnchannels(2)  # Stereo
#                 wav_file.setsampwidth(2)  # 16-bit
#                 wav_file.setframerate(48000)  # 48kHz
#                 wav_file.writeframes(audio_bytes)
            
#             print(f"💾 Saved: {filepath}")
#             return True
            
#         except Exception as e:
#             print(f"❌ Save error: {str(e)}")
#             return False
    
#     def stop_current_audio(self):
#         """Stop currently playing audio"""
#         self.stop_audio_flag = True
#         if self.pygame and self.pygame.mixer.get_init():
#             try:
#                 self.pygame.mixer.music.stop()
#                 print("⏹️ Stopped previous audio")
#             except:
#                 pass
    
#     def play_audio_looped_pygame(self, filepath):
#         """Play audio file in a loop using pygame (background thread)"""
#         def play_loop():
#             try:
#                 if not self.pygame:
#                     print("⚠️ Pygame not available for looping")
#                     return
                
#                 # Initialize pygame mixer
#                 if not self.pygame.mixer.get_init():
#                     self.pygame.mixer.init(frequency=48000, size=-16, channels=2)
                
#                 # Load and play with infinite loop
#                 self.pygame.mixer.music.load(filepath)
#                 self.pygame.mixer.music.play(loops=-1)  # -1 = infinite loop
                
#                 print(f"🔁 Playing in loop: {os.path.basename(filepath)}")
                
#                 # Keep thread alive while playing
#                 while self.pygame.mixer.music.get_busy() and not self.stop_audio_flag:
#                     time.sleep(0.1)
                    
#             except Exception as e:
#                 print(f"❌ Pygame playback error: {str(e)}")
        
#         # Stop previous audio
#         self.stop_current_audio()
#         self.stop_audio_flag = False
        
#         # Start new playback thread
#         self.current_audio_thread = threading.Thread(target=play_loop, daemon=True)
#         self.current_audio_thread.start()
    
#     def play_audio_file(self, filepath):
#         """
#         Play audio file using system's default media player OR pygame loop
        
#         Args:
#             filepath: Path to the audio file
        
#         Returns:
#             bool: Success status
#         """
#         try:
#             # First, try pygame for looping
#             if self.pygame:
#                 self.play_audio_looped_pygame(filepath)
#                 return True
            
#             # Fallback to system player (won't loop)
#             system = platform.system()
            
#             print(f"🎵 Playing audio: {filepath}")
            
#             if system == 'Windows':
#                 # Windows - use start command
#                 os.startfile(filepath)
#                 print("✅ Opened in Windows Media Player (Note: Won't loop automatically)")
#             elif system == 'Darwin':
#                 # macOS - use open command
#                 subprocess.Popen(['open', filepath])
#                 print("✅ Opened in default macOS player")
#             else:
#                 # Linux - try VLC with repeat flag
#                 try:
#                     subprocess.Popen(['vlc', '--repeat', filepath])
#                     print("✅ Opened in VLC with repeat")
#                     return True
#                 except FileNotFoundError:
#                     # Try other players
#                     players = ['mpv', 'mplayer', 'xdg-open']
#                     for player in players:
#                         try:
#                             subprocess.Popen([player, filepath])
#                             print(f"✅ Opened in {player}")
#                             return True
#                         except FileNotFoundError:
#                             continue
#                     print("⚠️ No media player found on Linux")
#                     return False
            
#             return True
            
#         except Exception as e:
#             print(f"❌ Error playing audio: {str(e)}")
#             return False

# # Global instance
# gemini_service = GeminiMusicService()

import os
import asyncio
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
import base64
import time
import wave
import subprocess
import platform

load_dotenv()

class GeminiMusicService:
    def __init__(self):
        api_key = os.getenv('GOOGLE_API_KEY') or 'AIzaSyD6Z1B4At-908dalV2ohCssF9t7RIPp3NU'
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        self.client = genai.Client(
            api_key=api_key,
            http_options={'api_version': 'v1alpha'}
        )
        
        # Emotion to music prompt mapping
        self.emotion_prompts = {
            'happy': 'upbeat cheerful pop music with positive energy',
            'sad': 'melancholic slow piano ballad',
            'angry': 'aggressive intense rock music',
            'fear': 'dark suspenseful ambient music',
            'disgust': 'dissonant industrial electronic',
            'surprise': 'dynamic energetic electronic dance',
            'neutral': 'minimal ambient techno'
        }
        
        # Emotion to BPM mapping
        self.emotion_bpm = {
            'happy': 120,
            'sad': 70,
            'angry': 150,
            'fear': 100,
            'disgust': 110,
            'surprise': 130,
            'neutral': 90
        }
        
        print("✅ Gemini Music Service initialized successfully")
    
    def get_prompt_for_emotion(self, emotion):
        """Get music prompt for emotion"""
        emotion_lower = emotion.lower()
        return self.emotion_prompts.get(emotion_lower, 'minimal ambient techno')
    
    def get_bpm_for_emotion(self, emotion):
        """Get BPM for emotion"""
        emotion_lower = emotion.lower()
        return self.emotion_bpm.get(emotion_lower, 90)
    
    async def generate_bgm_async(self, emotion='neutral', bpm=None, temperature=1.0, duration=20):
        """
        Generate background music asynchronously (default 20 seconds)
        
        Args:
            emotion: Emotion to generate music for
            bpm: Beats per minute (optional, will use emotion default)
            temperature: Creativity parameter (0.0 - 2.0)
            duration: Duration in seconds (default 20)
        
        Returns:
            dict with audio_data (base64), format, duration
        """
        start_time = time.time()
        
        try:
            prompt = self.get_prompt_for_emotion(emotion)
            if bpm is None:
                bpm = self.get_bpm_for_emotion(emotion)
            
            print(f"\n🎵 Generating {duration}s music for: {emotion}")
            print(f"📝 Prompt: {prompt} | BPM: {bpm}")
            
            audio_chunks = []
            
            # Python 3.11+ version with TaskGroup
            if sys.version_info >= (3, 11):
                async with self.client.aio.live.music.connect(
                    model='models/lyria-realtime-exp'
                ) as session:
                    
                    async def receive_audio():
                        """Receive audio chunks from the server"""
                        async for message in session.receive():
                            if hasattr(message, 'server_content') and \
                               hasattr(message.server_content, 'audio_chunks'):
                                for chunk in message.server_content.audio_chunks:
                                    audio_chunks.append(chunk.data)
                    
                    async with asyncio.TaskGroup() as tg:
                        receive_task = tg.create_task(receive_audio())
                        
                        await session.set_weighted_prompts(
                            prompts=[types.WeightedPrompt(text=prompt, weight=1.0)]
                        )
                        await session.set_music_generation_config(
                            config=types.LiveMusicGenerationConfig(
                                bpm=bpm,
                                temperature=temperature,
                                guidance=4.0,
                                density=0.7,
                                brightness=0.6
                            )
                        )
                        
                        await session.play()
                        await asyncio.sleep(duration)
                        await session.stop()
                        await asyncio.sleep(1)
     
            else:
                # Python 3.10 and below
                async with self.client.aio.live.music.connect(
                    model='models/lyria-realtime-exp'
                ) as session:
                    
                    async def receive_audio():
                        """Receive audio chunks from the server"""
                        try:
                            async for message in session.receive():
                                if hasattr(message, 'server_content') and \
                                   hasattr(message.server_content, 'audio_chunks'):
                                    for chunk in message.server_content.audio_chunks:
                                        audio_chunks.append(chunk.data)
                        except Exception as e:
                            print(f"⚠️ Receive error: {e}")
                    
                    receive_task = asyncio.create_task(receive_audio())
                    
                    try:
                        await session.set_weighted_prompts(
                            prompts=[types.WeightedPrompt(text=prompt, weight=1.0)]
                        )
                        await session.set_music_generation_config(
                            config=types.LiveMusicGenerationConfig(
                                bpm=bpm,
                                temperature=temperature,
                                guidance=4.0,
                                density=0.7,
                                brightness=0.6
                            )
                        )
                        
                        await session.play()
                        await asyncio.sleep(duration)
                        await session.stop()
                        await asyncio.sleep(1)
                        
                    finally:
                        receive_task.cancel()
                        try:
                            await receive_task
                        except asyncio.CancelledError:
                            pass
            
            # Check if we got audio
            if not audio_chunks:
                elapsed = time.time() - start_time
                print(f"❌ No audio received ({elapsed:.2f}s)")
                return {'error': 'No audio data received'}
            
            # Combine and encode
            combined_audio = b''.join(audio_chunks)
            audio_base64 = base64.b64encode(combined_audio).decode('utf-8')
            
            elapsed = time.time() - start_time
            size_mb = len(combined_audio) / (1024 * 1024)
            
            print(f"✅ Generated {size_mb:.2f}MB in {elapsed:.2f}s")
            
            return {
                'success': True,
                'audio_data': audio_base64,
                'format': 'audio/wav',
                'duration': duration,
                'emotion': emotion,
                'bpm': bpm,
                'prompt': prompt,
                'file_size_mb': round(size_mb, 2),
                'elapsed_time': round(elapsed, 2)
            }
        
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"❌ Error: {str(e)}")
            return {'error': str(e), 'elapsed_time': elapsed}
    
    def generate_bgm_sync(self, emotion='neutral', bpm=None, temperature=1.0, duration=20):
        """
        Synchronous wrapper for BGM generation (default 20 seconds)
        """
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            result = loop.run_until_complete(
                self.generate_bgm_async(emotion, bpm, temperature, duration)
            )
            
            loop.close()
            return result
        
        except Exception as e:
            print(f"❌ Sync error: {str(e)}")
            return {'error': str(e)}
    
    def save_bgm_to_file(self, audio_data_base64, filepath, loop_count=6):
        """
        Save base64 audio to WAV file with proper format and loop it
        
        Gemini Lyria outputs:
        - Raw 16-bit PCM Audio
        - Sample rate: 48kHz
        - Channels: 2 (stereo)
        
        Args:
            audio_data_base64: Base64 encoded audio data
            filepath: Output file path
            loop_count: Number of times to repeat the audio (default 6 = 2 minutes from 20s)
        """
        try:
            audio_bytes = base64.b64decode(audio_data_base64)
            
            # Loop the audio by repeating the bytes
            looped_audio = audio_bytes * loop_count
            
            with wave.open(filepath, 'wb') as wav_file:
                wav_file.setnchannels(2)  # Stereo
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(48000)  # 48kHz
                wav_file.writeframes(looped_audio)
            
            duration_sec = loop_count * 20  # 20 seconds per loop
            file_size_mb = len(looped_audio) / (1024 * 1024)
            
            print(f"💾 Saved: {filepath}")
            print(f"🔁 Looped {loop_count}x = {duration_sec}s total ({file_size_mb:.2f}MB)")
            return True
            
        except Exception as e:
            print(f"❌ Save error: {str(e)}")
            return False
    
    def play_audio_file(self, filepath):
        """
        Play audio file using system's default media player
        Audio file is already looped 6x (2 minutes), so player just needs to repeat it
        
        Args:
            filepath: Path to the audio file
        
        Returns:
            bool: Success status
        """
        try:
            system = platform.system()
            
            print(f"🎵 Playing looped audio: {os.path.basename(filepath)}")
            
            if system == 'Windows':
                # Windows - use Windows Media Player with loop
                # Note: WMP doesn't support command-line loop, but file is already 2min looped
                os.startfile(filepath)
                print("✅ Opened in Windows Media Player (2 min looped file)")
            elif system == 'Darwin':
                # macOS - use afplay with loop or default player
                try:
                    # Try afplay with -t flag for infinite loop
                    subprocess.Popen(['afplay', '-t', str(999999), filepath])
                    print("✅ Playing with afplay (infinite loop)")
                except:
                    subprocess.Popen(['open', filepath])
                    print("✅ Opened in default macOS player")
            else:
                # Linux - VLC with repeat
                try:
                    subprocess.Popen(['vlc', '--loop', '--quiet', filepath])
                    print("✅ Opened in VLC with infinite loop")
                    return True
                except FileNotFoundError:
                    # Try MPV with loop
                    try:
                        subprocess.Popen(['mpv', '--loop=inf', filepath])
                        print("✅ Opened in MPV with infinite loop")
                        return True
                    except FileNotFoundError:
                        # Fallback to other players
                        players = ['mplayer', 'xdg-open']
                        for player in players:
                            try:
                                subprocess.Popen([player, filepath])
                                print(f"✅ Opened in {player} (2 min looped file)")
                                return True
                            except FileNotFoundError:
                                continue
                        print("⚠️ No media player found on Linux")
                        return False
            
            return True
            
        except Exception as e:
            print(f"❌ Error playing audio: {str(e)}")
            return False

# Global instance
gemini_service = GeminiMusicService()