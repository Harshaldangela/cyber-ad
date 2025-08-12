"""
Setup script for SMS Spam Classifier with Cyber Awareness
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def download_nltk_data():
    """Download required NLTK data"""
    print("📚 Downloading NLTK data...")
    try:
        import nltk
        nltk.download('punkt')
        nltk.download('stopwords')
        print("✅ NLTK data downloaded successfully")
        return True
    except Exception as e:
        print(f"❌ Error downloading NLTK data: {e}")
        return False

def check_files():
    """Check if required files exist"""
    print("🔍 Checking required files...")
    required_files = ['model.pkl', 'vectorizer.pkl', 'spam.csv']
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} found")
        else:
            print(f"❌ {file} missing")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️ Missing files: {', '.join(missing_files)}")
        print("Please run 'python model_training.py' to generate the missing files.")
        return False
    
    return True

def main():
    """Main setup function"""
    print("🛡️ SMS Spam Classifier - Setup")
    print("=" * 40)
    
    # Install requirements
    if not install_requirements():
        return
    
    # Download NLTK data
    if not download_nltk_data():
        return
    
    # Check files
    if not check_files():
        return
    
    print("\n" + "=" * 40)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Get your Gemini API key from: https://makersuite.google.com/app/apikey")
    print("2. Run the app: streamlit run app.py")
    print("3. Enter your API key in the sidebar")
    print("4. Start classifying messages!")
    
    print("\n💡 Optional:")
    print("- Run 'python test_app.py' to test the installation")
    print("- Set GEMINI_API_KEY environment variable for automatic API key loading")

if __name__ == "__main__":
    main()
