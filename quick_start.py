#!/usr/bin/env python3
"""
Quick start script for MARK L (Jarvis AI)
Runs pre-flight checks and launches the application
"""
import json
import sys
from pathlib import Path

def check_setup():
    """Verify all required components are in place"""
    base_dir = Path(__file__).parent
    config_file = base_dir / "config" / "api_keys.json"
    
    print("=" * 60)
    print("🚀 MARK L (Jarvis AI) - Pre-Flight Checks")
    print("=" * 60)
    
    # Check Python version
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"\n✅ Python {py_version}")
    
    if sys.version_info < (3, 10):
        print("❌ ERROR: Python 3.10+ required")
        return False
    
    # Check config file
    if not config_file.exists():
        print("❌ ERROR: config/api_keys.json not found")
        print("   Please run setup.py first or create the config file")
        return False
    print("✅ Configuration file found")
    
    # Check API key
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
            api_key = config.get("gemini_api_key", "").strip()
            
            if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
                print("❌ ERROR: Gemini API key not configured")
                print("   1. Get your key from: https://aistudio.google.com/apikey")
                print("   2. Edit config/api_keys.json and add your key")
                return False
            
            if len(api_key) < 16:
                print("❌ ERROR: API key appears invalid (too short)")
                return False
            
            print("✅ API key configured")
    except Exception as e:
        print(f"❌ ERROR reading config: {e}")
        return False
    
    # Check required modules
    modules = ["PyQt6", "google.genai", "sounddevice", "playwright"]
    missing = []
    for mod in modules:
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod)
    
    if missing:
        print(f"❌ ERROR: Missing modules: {', '.join(missing)}")
        print("   Run: python3 setup.py")
        return False
    print("✅ All required packages installed")
    
    # Check core files
    required_files = [
        "main.py",
        "ui.py",
        "core/llm_client.py",
        "core/stt.py",
        "core/tts.py",
        "core/prompt.txt",
        "memory/memory_manager.py",
        "memory/config_manager.py",
    ]
    
    for file in required_files:
        if not (base_dir / file).exists():
            print(f"❌ ERROR: Missing {file}")
            return False
    print("✅ All core files present")
    
    print("\n" + "=" * 60)
    print("✅ All checks passed! Starting MARK L...")
    print("=" * 60 + "\n")
    return True

if __name__ == "__main__":
    if not check_setup():
        print("\n❌ Setup check failed. Please fix the errors above.")
        sys.exit(1)
    
    # Import and run main
    from main import main
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 MARK L shutting down...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
