import os
import pygame
import glob

def play_wav_file(filename):
    """Play a WAV file using pygame"""
    try:
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Load and play the audio
        pygame.mixer.music.load(filename)
        
        print(f"\n🎵 Now playing: {filename}")
        print("Press Ctrl+C to stop\n")
        
        pygame.mixer.music.play()
        
        # Wait until the music finishes
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        print("\n✅ Playback finished!")
        
    except Exception as e:
        print(f"❌ Error playing audio: {str(e)}")
    finally:
        pygame.mixer.quit()

def main():
    """Main function to play WAV files"""
    print("\n🎼 WAV FILE PLAYER")
    print("=" * 60)
    
    # Find all WAV files in current directory
    wav_files = glob.glob("test_music_*.wav")
    
    if not wav_files:
        print("❌ No test_music_*.wav files found in current directory")
        return
    
    # Sort by modification time (newest first)
    wav_files.sort(key=os.path.getmtime, reverse=True)
    
    print(f"\nFound {len(wav_files)} WAV file(s):\n")
    
    for i, file in enumerate(wav_files, 1):
        size_mb = os.path.getsize(file) / (1024 * 1024)
        mod_time = os.path.getmtime(file)
        print(f"{i}. {file} ({size_mb:.2f} MB)")
    
    print(f"\n{len(wav_files) + 1}. Enter custom filename")
    print("0. Exit")
    
    # Get user choice
    try:
        choice = int(input("\nSelect file to play: "))
        
        if choice == 0:
            print("👋 Goodbye!")
            return
        elif choice == len(wav_files) + 1:
            filename = input("Enter WAV filename: ").strip()
            if not filename.endswith('.wav'):
                filename += '.wav'
        elif 1 <= choice <= len(wav_files):
            filename = wav_files[choice - 1]
        else:
            print("❌ Invalid choice")
            return
        
        if not os.path.exists(filename):
            print(f"❌ File not found: {filename}")
            return
        
        play_wav_file(filename)
        
    except ValueError:
        print("❌ Invalid input")
    except KeyboardInterrupt:
        print("\n\n⏹️ Playback stopped by user")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    main()