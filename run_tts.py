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
    
    # المسارات
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    
    # التحقق من وجود المجلدات
    print(f"\n🔍 التحقق من المجلدات...")
    print(f"📁 مجلد Input موجود: {input_dir.exists()}")
    print(f"📁 مجلد Output موجود: {output_dir.exists()}")
    
    # إنشاء مجلد output إذا لم يكن موجوداً
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # عرض محتويات مجلد input
    if input_dir.exists():
        all_files = list(input_dir.glob("*"))
        print(f"\n📋 محتويات مجلد input:")
        if all_files:
            for f in all_files:
                print(f"   - {f.name} ({f.suffix})")
        else:
            print("   (المجلد فارغ)")
    
    # البحث عن ملف صوتي في مجلد input
    audio_files = list(input_dir.glob("*.wav"))
    
    if not audio_files:
        print("\n❌ خطأ: لم يتم العثور على ملف .wav في مجلد input")
        print("📝 الرجاء وضع ملف صوتي بصيغة WAV في مجلد input")
        print("\n💡 نصيحة: تأكد من أن:")
        print("   1. الملف بصيغة .wav (وليس .mp3 أو .m4a)")
        print("   2. الملف موجود في مجلد input/ في نفس مجلد المشروع")
        print("   3. Docker قادر على الوصول للمجلد (تحقق من الـ volume mounting)")
        sys.exit(1)
    
    speaker_wav = str(audio_files[0])
    print(f"\n✅ تم العثور على الملف الصوتي: {audio_files[0].name}")
    print(f"📊 حجم الملف: {audio_files[0].stat().st_size / 1024:.2f} KB")
    
    # النص المراد تحويله لصوت
    text = """
    مرحباً، هذا اختبار لتقنية استنساخ الصوت باستخدام الذكاء الاصطناعي.
    النظام يقوم بتوليد صوت جديد بناءً على العينة الصوتية المرجعية.
    """
    
    print("\n📝 النص المراد تحويله:")
    print(text.strip())
    
    # تحميل الموديل
    print("\n⏳ جاري تحميل الموديل...")
    print("ℹ️  هذه العملية قد تستغرق عدة دقائق في المرة الأولى")
    print("📜 الموافقة التلقائية على الترخيص غير التجاري (CPML)")
    
    try:
        # تعيين متغير بيئة للموافقة التلقائية
        os.environ['COQUI_TOS_AGREED'] = '1'
        
        tts = TTS(
            model_name="tts_models/multilingual/multi-dataset/xtts_v2",
            progress_bar=False,  # تعطيل progress bar لتجنب مشاكل التفاعل
            gpu=False  # استخدام CPU (يمكن تغييره لـ True إذا كان GPU متاحاً)
        )
        print("✅ تم تحميل الموديل بنجاح")
    except Exception as e:
        print(f"❌ خطأ في تحميل الموديل: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # توليد الصوت
    output_file = output_dir / "generated_voice.wav"
    print(f"\n🎵 جاري توليد الصوت...")
    print(f"⚙️  معالجة النص باستخدام الصوت المرجعي...")
    
    try:
        tts.tts_to_file(
            text=text.strip(),
            file_path=str(output_file),
            speaker_wav=speaker_wav,
            language="ar"
        )
        
        # التحقق من إنشاء الملف
        if output_file.exists():
            print(f"✅ تم توليد الملف الصوتي بنجاح!")
            print(f"📂 الملف محفوظ في: output/generated_voice.wav")
            print(f"📊 حجم الملف: {output_file.stat().st_size / 1024:.2f} KB")
        else:
            print(f"⚠️  تحذير: الملف لم يتم إنشاؤه!")
            
    except Exception as e:
        print(f"❌ خطأ في توليد الصوت: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✨ اكتمل المشروع بنجاح!")
    print("=" * 60)
    print("\n💡 لتغيير النص، قم بتعديل متغير 'text' في ملف run_tts.py")
    print("💡 لاستخدام صوت مرجعي مختلف، استبدل الملف في مجلد input/")

if __name__ == "__main__":
    main()