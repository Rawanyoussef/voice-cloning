#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Voice Cloning Script using Coqui TTS
Generates Arabic speech using a reference voice sample
"""

import os
import sys
from pathlib import Path
from TTS.api import TTS

def main():
    print("=" * 60)
    print("🎙️  Voice Cloning - Coqui TTS")
    print("=" * 60)
    
    # Paths
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    
    # Check directories
    print(f"\n🔍 Checking directories...")
    print(f"📁 Input directory exists: {input_dir.exists()}")
    print(f"📁 Output directory exists: {output_dir.exists()}")
    
    # Create output directory if it does not exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # List input directory contents
    if input_dir.exists():
        all_files = list(input_dir.glob("*"))
        print(f"\n📋 Input directory contents:")
        if all_files:
            for f in all_files:
                print(f"   - {f.name} ({f.suffix})")
        else:
            print("   (Directory is empty)")
    
    # Search for WAV file in input directory
    audio_files = list(input_dir.glob("*.wav"))
    
    if not audio_files:
        print("\n❌ Error: No .wav file found in input directory")
        print("📝 Please place a WAV audio file inside the input folder")
        print("\n💡 Tips:")
        print("   1. File must be .wav (not .mp3 or .m4a)")
        print("   2. File must be inside input/ directory")
        print("   3. Ensure Docker volume mounting is correct")
        sys.exit(1)
    
    speaker_wav = str(audio_files[0])
    print(f"\n✅ Audio file found: {audio_files[0].name}")
    print(f"📊 File size: {audio_files[0].stat().st_size / 1024:.2f} KB")
    
    # Text to be converted to speech (عامية مصرية بدون تشكيل)
    text = """
مساء الخير، ازيك؟
خليني اقولك ان الكلام اللي سامعه دلوقتي معمول بهدوء، وبنبرة طبيعية جدا.
مفيش تمثيل، ولا ضغط على الصوت، كله كلام عادي زي أي مكالمة يومية.
الهدف بس اننا نسمع النبرة صح، ونطمئن ان الصوت واضح ومريح للأذن.
لو حاسس ان الصوت تمام، يبقى نكمل بعد كده بسهولة.
تمام؟ شكرا ليك.
"""
    
    print("\n📝 Text to synthesize:")
    print(text.strip())
    
    # Load model
    print("\n⏳ Loading model...")
    print("ℹ️  This may take several minutes on first run")
    print("📜 Automatically accepting non-commercial license (CPML)")
    
    try:
        os.environ['COQUI_TOS_AGREED'] = '1'
        
        tts = TTS(
            model_name="tts_models/multilingual/multi-dataset/xtts_v2",
            progress_bar=False,
            gpu=False
        )
        print("✅ Model loaded successfully")
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Generate speech
    output_file = output_dir / "generated_voice.wav"
    print(f"\n🎵 Generating speech...")
    print(f"⚙️  Processing text using reference voice...")
    
    try:
        tts.tts_to_file(
            text=text.strip(),
            file_path=str(output_file),
            speaker_wav=speaker_wav,
            language="ar",
            split_sentences=False,
            temperature=0.65,
            repetition_penalty=2.0,
            top_p=0.85,
            top_k=50,
            sound_norm_refs=True  # 🔹 مفيش تأثير على الـ API إلا تحسين جودة الصوت
        )
        if output_file.exists():
            print(f"✅ Audio file generated successfully!")
            print(f"📂 File saved at: output/generated_voice.wav")
            print(f"📊 File size: {output_file.stat().st_size / 1024:.2f} KB")
        else:
            print(f"⚠️  Warning: Output file was not created!")
            
    except Exception as e:
        print(f"❌ Error generating audio: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✨ Process completed successfully!")
    print("=" * 60)
    print("\n💡 To change the text, edit the 'text' variable in run_tts.py")
    print("💡 To use a different reference voice, replace the file in input/")

if __name__ == "__main__":
    main()
