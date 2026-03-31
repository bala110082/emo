import os
import asyncio
import sys
from google import genai
from google.genai import types
import base64
import time
import wave
import struct
import subprocess
import platform

# Your API key
API_KEY = 'AIzaSyD6Z1B4At-908dalV2ohCssF9t7RIPp3NU'

async def test_music_generation(emotion='happy', duration=10):
    """
    Simple test to check if Gemini music generation works
    """
    print(f"\n{'='*60}")
    print(f"🧪 TESTING GEMINI MUSIC GENERATION")
    print(f"{'='*60}")
    print(f"Emotion: {emotion}")
    print(f"Duration: {duration} seconds")
    print(f"{'='*60}\n")
    
    start_time = time.time()
    
    try:
        # Initialize client
        print("🔌 Connecting to Gemini API...")
        client = genai.Client(
            api_key=API_KEY,
            http_options={'api_version': 'v1alpha'}
        )
        print("✅ Connected!\n")
        
        # Music prompts
        prompts_map = {
            'happy': 'upbeat cheerful pop music',
            'sad': 'melancholic piano ballad',
            'angry': 'aggressive rock music',
            'neutral': 'minimal ambient techno'
        }
        
        bpm_map = {
            'happy': 120,
            'sad': 70,
            'angry': 150,
            'neutral': 90
        }
        
        prompt = prompts_map.get(emotion, 'minimal ambient techno')
        bpm = bpm_map.get(emotion, 90)
        
        print(f"🎵 Prompt: {prompt}")
        print(f"🎼 BPM: {bpm}\n")
        
        audio_chunks = []
        
        # Generate music
        print("🎵 Starting music generation...")
        
        async with client.aio.live.music.connect(
            model='models/lyria-realtime-exp'
        ) as session:
            
            async def receive_audio():
                """Receive audio chunks"""
                chunk_count = 0
                try:
                    async for message in session.receive():
                        if hasattr(message, 'server_content') and \
                           hasattr(message.server_content, 'audio_chunks'):
                            for chunk in message.server_content.audio_chunks:
                                audio_chunks.append(chunk.data)
                                chunk_count += 1
                                if chunk_count % 10 == 0:
                                    print(f"📦 Received {chunk_count} audio chunks...")
                except Exception as e:
                    print(f"⚠️ Receive error: {e}")
            
            # Start receiving audio
            receive_task = asyncio.create_task(receive_audio())
            
            try:
                # Configure music generation
                print("⚙️ Configuring generation parameters...")
                await session.set_weighted_prompts(
                    prompts=[types.WeightedPrompt(text=prompt, weight=1.0)]
                )
                await session.set_music_generation_config(
                    config=types.LiveMusicGenerationConfig(
                        bpm=bpm,
                        temperature=1.0
                    )
                )
                
                # Start playing
                print("▶️ Playing music...\n")
                await session.play()
                
                # Wait for duration
                for i in range(duration):
                    await asyncio.sleep(1)
                    print(f"⏱️ {i+1}/{duration} seconds...")
                
                # Stop
                print("\n⏹️ Stopping...")
                await session.stop()
                
                # Wait for remaining chunks
                await asyncio.sleep(2)
                
            finally:
                receive_task.cancel()
                try:
                    await receive_task
                except asyncio.CancelledError:
                    pass
        
        elapsed_time = time.time() - start_time
        
        # Check results
        print(f"\n{'='*60}")
        if not audio_chunks:
            print("❌ FAILED: No audio chunks received")
            print(f"⏱️ Time taken: {elapsed_time:.2f}s")
            print(f"{'='*60}\n")
            return None
        
        # Save audio file
        print(f"✅ SUCCESS: Received {len(audio_chunks)} audio chunks")
        
        combined_audio = b''.join(audio_chunks)
        file_size_mb = len(combined_audio) / (1024 * 1024)
        
        filename = f'test_music_{emotion}_{int(time.time())}.wav'
        with open(filename, 'wb') as f:
            f.write(combined_audio)
        
        print(f"💾 Saved to: {filename}")
        print(f"📊 File size: {file_size_mb:.2f} MB")
        print(f"⏱️ Time taken: {elapsed_time:.2f}s")
        print(f"{'='*60}\n")
        
        return filename
    
    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"\n{'='*60}")
        print(f"❌ ERROR: {str(e)}")
        print(f"⏱️ Time taken: {elapsed_time:.2f}s")
        print(f"{'='*60}\n")
        return None

def play_audio_file(filename):
    """Play audio file using system default player"""
    if not filename or not os.path.exists(filename):
        print("❌ File not found")
        return False
    
    try:
        print(f"\n🎵 Playing: {filename}")
        print("Opening with default audio player...\n")
        
        system = platform.system()
        
        if system == 'Windows':
            os.startfile(filename)
        elif system == 'Darwin':  # macOS
            subprocess.run(['open', filename])
        else:  # Linux
            subprocess.run(['xdg-open', filename])
        
        print("✅ Audio player opened!")
        print("If audio doesn't play, try VLC Media Player or another audio player\n")
        return True
        
    except Exception as e:
        print(f"❌ Error opening audio player: {str(e)}")
        print("💡 Try opening the file manually with VLC or Windows Media Player\n")
        return False

def main():
    """Run the test"""
    print("\n🚀 GEMINI MUSIC GENERATION TEST")
    print("This will test if your Gemini API is working\n")
    
    # Choose emotion to test
    emotion = input("Enter emotion (happy/sad/angry/neutral) [default: happy]: ").strip().lower() or 'happy'
    duration = input("Enter duration in seconds [default: 10]: ").strip() or '10'
    
    try:
        duration = int(duration)
    except:
        duration = 10
    
    # Run test
    filename = asyncio.run(test_music_generation(emotion, duration))
    
    if filename:
        print("🎉 Test completed successfully!")
        print("✅ Your Gemini API is working!")
        
        # Ask if user wants to play the audio
        play = input("\n▶️ Do you want to play the audio? (y/n) [default: y]: ").strip().lower()
        
        if play != 'n':
            play_audio_file(filename)
        else:
            print(f"💡 You can manually play the file: {filename}")
    else:import os
import asyncio
import sys
from google import genai
from google.genai import types
import time
import wave
import struct
import subprocess
import platform

# Your API key
API_KEY = 'AIzaSyD6Z1B4At-908dalV2ohCssF9t7RIPp3NU'

def save_pcm_as_wav(audio_chunks, filename, sample_rate=48000, channels=2, sample_width=2):
    """
    Convert raw PCM audio chunks to proper WAV file
    
    According to Gemini docs:
    - Output format: Raw 16-bit PCM Audio
    - Sample rate: 48kHz
    - Channels: 2 (stereo)
    """
    try:
        print(f"\n🔧 Converting raw PCM to WAV format...")
        
        # Combine all audio chunks
        combined_audio = b''.join(audio_chunks)
        
        # Create WAV file with proper headers
        with wave.open(filename, 'wb') as wav_file:
            wav_file.setnchannels(channels)  # Stereo
            wav_file.setsampwidth(sample_width)  # 16-bit = 2 bytes
            wav_file.setframerate(sample_rate)  # 48kHz
            wav_file.writeframes(combined_audio)
        
        file_size_mb = os.path.getsize(filename) / (1024 * 1024)
        duration_seconds = len(combined_audio) / (sample_rate * channels * sample_width)
        
        print(f"✅ WAV file created successfully!")
        print(f"📊 File size: {file_size_mb:.2f} MB")
        print(f"⏱️ Duration: {duration_seconds:.2f} seconds")
        print(f"🎼 Format: {sample_rate}Hz, {channels} channels, {sample_width*8}-bit")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating WAV file: {str(e)}")
        return False

async def test_music_generation(emotion='happy', duration=10):
    """
    Test Gemini music generation with proper PCM to WAV conversion
    """
    print(f"\n{'='*60}")
    print(f"🧪 TESTING GEMINI MUSIC GENERATION")
    print(f"{'='*60}")
    print(f"Emotion: {emotion}")
    print(f"Duration: {duration} seconds")
    print(f"{'='*60}\n")
    
    start_time = time.time()
    
    try:
        # Initialize client
        print("🔌 Connecting to Gemini API...")
        client = genai.Client(
            api_key=API_KEY,
            http_options={'api_version': 'v1alpha'}
        )
        print("✅ Connected!\n")
        
        # Music prompts
        prompts_map = {
            'happy': 'upbeat cheerful pop music',
            'sad': 'melancholic piano ballad',
            'angry': 'aggressive rock music',
            'neutral': 'minimal ambient techno'
        }
        
        bpm_map = {
            'happy': 120,
            'sad': 70,
            'angry': 150,
            'neutral': 90
        }
        
        prompt = prompts_map.get(emotion, 'minimal ambient techno')
        bpm = bpm_map.get(emotion, 90)
        
        print(f"🎵 Prompt: {prompt}")
        print(f"🎼 BPM: {bpm}\n")
        
        audio_chunks = []
        
        # Generate music
        print("🎵 Starting music generation...")
        
        async with client.aio.live.music.connect(
            model='models/lyria-realtime-exp'
        ) as session:
            
            async def receive_audio():
                """Receive audio chunks"""
                chunk_count = 0
                try:
                    async for message in session.receive():
                        if hasattr(message, 'server_content') and \
                           hasattr(message.server_content, 'audio_chunks'):
                            for chunk in message.server_content.audio_chunks:
                                audio_chunks.append(chunk.data)
                                chunk_count += 1
                                if chunk_count % 10 == 0:
                                    print(f"📦 Received {chunk_count} audio chunks...")
                except Exception as e:
                    print(f"⚠️ Receive error: {e}")
            
            # Start receiving audio
            receive_task = asyncio.create_task(receive_audio())
            
            try:
                # Configure music generation
                print("⚙️ Configuring generation parameters...")
                await session.set_weighted_prompts(
                    prompts=[types.WeightedPrompt(text=prompt, weight=1.0)]
                )
                await session.set_music_generation_config(
                    config=types.LiveMusicGenerationConfig(
                        bpm=bpm,
                        temperature=1.0,
                        guidance=4.0,
                        density=0.7,
                        brightness=0.6
                    )
                )
                
                # Start playing
                print("▶️ Playing music...\n")
                await session.play()
                
                # Wait for duration
                for i in range(duration):
                    await asyncio.sleep(1)
                    print(f"⏱️ {i+1}/{duration} seconds...")
                
                # Stop
                print("\n⏹️ Stopping...")
                await session.stop()
                
                # Wait for remaining chunks
                await asyncio.sleep(2)
                
            finally:
                receive_task.cancel()
                try:
                    await receive_task
                except asyncio.CancelledError:
                    pass
        
        elapsed_time = time.time() - start_time
        
        # Check results
        print(f"\n{'='*60}")
        if not audio_chunks:
            print("❌ FAILED: No audio chunks received")
            print(f"⏱️ Time taken: {elapsed_time:.2f}s")
            print(f"{'='*60}\n")
            return None
        
        print(f"✅ SUCCESS: Received {len(audio_chunks)} audio chunks")
        print(f"⏱️ Generation time: {elapsed_time:.2f}s")
        
        # Save as proper WAV file
        filename = f'test_music_{emotion}_{int(time.time())}.wav'
        
        if save_pcm_as_wav(audio_chunks, filename):
            print(f"💾 Saved to: {filename}")
            print(f"{'='*60}\n")
            return filename
        else:
            return None
    
    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"\n{'='*60}")
        print(f"❌ ERROR: {str(e)}")
        print(f"⏱️ Time taken: {elapsed_time:.2f}s")
        print(f"{'='*60}\n")
        return None

def play_audio_file(filename):
    """Play audio file using system default player"""
    if not filename or not os.path.exists(filename):
        print("❌ File not found")
        return False
    
    try:
        print(f"\n🎵 Playing: {filename}")
        print("Opening with default audio player...\n")
        
        system = platform.system()
        
        if system == 'Windows':
            os.startfile(filename)
        elif system == 'Darwin':  # macOS
            subprocess.run(['open', filename])
        else:  # Linux
            subprocess.run(['xdg-open', filename])
        
        print("✅ Audio player opened!")
        print("🔊 You should hear the music playing now!")
        print("\nIf no sound, check:")
        print("  - Volume is not muted")
        print("  - Speakers/headphones are connected")
        print("  - Try VLC Media Player if default player doesn't work\n")
        return True
        
    except Exception as e:
        print(f"❌ Error opening audio player: {str(e)}")
        print("💡 Try opening the file manually with VLC or Windows Media Player\n")
        return False

def main():
    """Run the test"""
    print("\n🚀 GEMINI MUSIC GENERATION TEST")
    print("This will test if your Gemini API is working\n")
    
    # Choose emotion to test
    emotion = input("Enter emotion (happy/sad/angry/neutral) [default: happy]: ").strip().lower() or 'happy'
    duration = input("Enter duration in seconds [default: 10]: ").strip() or '10'
    
    try:
        duration = int(duration)
    except:
        duration = 10
    
    # Run test
    filename = asyncio.run(test_music_generation(emotion, duration))
    
    if filename:
        print("🎉 Test completed successfully!")
        print("✅ Your Gemini API is working!")
        
        # Ask if user wants to play the audio
        play = input("\n▶️ Do you want to play the audio? (y/n) [default: y]: ").strip().lower()
        
        if play != 'n':
            play_audio_file(filename)
        else:
            print(f"💡 You can manually play the file: {filename}")
    else:
        print("💔 Test failed!")
        print("❌ Check your API key and internet connection")

if __name__ == '__main__':
    main()
    print("💔 Test failed!")
    print("❌ Check your API key and internet connection")

if __name__ == '__main__':
    main()