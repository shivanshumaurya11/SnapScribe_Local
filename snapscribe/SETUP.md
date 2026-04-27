# SnapScribe Setup Guide

## Step 1: Installation

### Prerequisites
- Python 3.8 or higher
- pip or conda package manager

### Clone/Download
```bash
# Navigate to the snapscribe directory
cd snapscribe
```

### Create Virtual Environment (Recommended)

**Using venv:**
```bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

**Using conda:**
```bash
conda create -n snapscribe python=3.10
conda activate snapscribe
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- **streamlit**: Web framework
- **yt-dlp**: YouTube downloading
- **opencv-python**: Video processing
- **numpy**: Numerical operations
- **pillow**: Image processing
- **PyPDF2**: PDF merging
- **fpdf2**: PDF generation
- **youtube-transcript-api**: Transcript extraction
- **transformers**: HuggingFace models
- **torch**: PyTorch deep learning
- **huggingface-hub**: HuggingFace API
- **scikit-image**: Image similarity
- **python-dotenv**: Environment variables

## Step 2: Configuration

### Create Environment File
Create a `.env` file in the project root:

```bash
cp .env.example .env
```

### Add HuggingFace Token
Edit `.env` and add your HuggingFace API token:

```env
HF_TOKEN=your_huggingface_api_token_here
```

**To get a HuggingFace token:**
1. Go to https://huggingface.co/
2. Click Profile → Settings
3. Go to "Access Tokens"
4. Create a new token
5. Copy and paste into `.env`

**Token not required for:**
- Local video to PDF (uses local frame extraction)
- YouTube to visual PDF (uses local frame extraction)
- Image to PDF (no AI needed)
- PDF merger (no external API needed)

## Step 3: Verify Installation

Test that all dependencies are installed:

```bash
python -c "import streamlit; import cv2; import yt_dlp; print('✓ All dependencies installed correctly')"
```

## Step 4: Run Application

### Start Streamlit App
```bash
streamlit run main.py
```

The app will open in your browser at `http://localhost:8501`

### Expected Output
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

## Common Issues & Solutions

### Issue: ModuleNotFoundError

**Solution:**
```bash
# Make sure you're in the snapscribe directory
cd snapscribe

# Verify virtual environment is activated
# (you should see (venv) in your prompt on Windows or source venv/bin/activate on Mac/Linux)

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: HuggingFace Token Not Found

**Solution:**
1. Verify `.env` file exists in project root
2. Check `.env` contains `HF_TOKEN=your_token`
3. Restart Streamlit app
4. Use sidebar prompt to enter token

### Issue: Video Download Fails

**Solution:**
- Check internet connection
- Try different YouTube URL
- Update yt-dlp: `pip install --upgrade yt-dlp`
- Some videos may have download restrictions

### Issue: Out of Memory During Summarization

**Solution:**
- Use smaller models
- Increase frame skip value to extract fewer frames
- Process shorter videos

### Issue: Port 8501 Already in Use

**Solution:**
```bash
streamlit run main.py --server.port 8502
```

## Directory Structure After Setup

```
snapscribe/
├── main.py
├── requirements.txt
├── .env                      # Create this file
├── README.md
├── ARCHITECTURE.md
├── SETUP.md
├── config/
│   ├── __init__.py
│   └── settings.py
├── frontend/
│   ├── __init__.py
│   ├── home.py
│   ├── deepread_page.py
│   ├── video_visual_page.py
│   ├── youtube_visual_page.py
│   ├── local_video_page.py
│   ├── pdf_merger_page.py
│   └── image_to_pdf_page.py
├── backend/
│   ├── __init__.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── youtube_service.py
│   │   ├── video_service.py
│   │   ├── transcript_service.py
│   │   ├── summarization_service.py
│   │   ├── pdf_service.py
│   │   └── image_service.py
│   └── utils/
│       ├── __init__.py
│       ├── file_utils.py
│       └── validators.py
├── output_pdfs/             # Created automatically
├── output_pdf_deepread/     # Created automatically
├── video_files/             # Created automatically
└── venv/                    # Virtual environment (optional)
```

## First Run Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with HF_TOKEN
- [ ] No errors in `streamlit run main.py`
- [ ] App opens in browser at localhost:8501
- [ ] Can see SnapScribe landing page with 6 tools

## Learning Resources

- **Streamlit Docs**: https://docs.streamlit.io/
- **yt-dlp Docs**: https://github.com/yt-dlp/yt-dlp
- **OpenCV Docs**: https://docs.opencv.org/
- **HuggingFace Docs**: https://huggingface.co/docs
- **PyPDF2 Docs**: https://pypdf.readthedocs.io/

## Next Steps

1. **Explore Features**: Test each tool in the application
2. **Read ARCHITECTURE.md**: Understand the modular design
3. **Check Backend Services**: Review service implementations
4. **Customize**: Modify settings in `config/settings.py`
5. **Deploy**: See deployment options below

## Deployment Options

### Streamlit Cloud (Recommended for Testing)
```bash
# Install Streamlit CLI
pip install streamlit

# In your GitHub repo, create streamlit app
# Then deploy at https://streamlit.io/cloud
```

### Docker Deployment
```bash
# Build image
docker build -t snapscribe .

# Run container
docker run -p 8501:8501 snapscribe
```

### Self-Hosted Server
- Deploy on AWS, Google Cloud, or DigitalOcean
- Use Gunicorn + Nginx as reverse proxy
- Configure persistent storage for outputs

## Performance Tips

1. **Increase Frame Skip**: Higher value = faster processing
2. **Lower Similarity Threshold**: Reduce number of frames extracted
3. **Use Local Models**: Faster than API calls
4. **Batch Processing**: Process multiple videos in sequence

## Troubleshooting Commands

```bash
# Check Python version
python --version

# Check Streamlit installation
streamlit --version

# Check package versions
pip list | grep -E "streamlit|opencv|yt-dlp"

# Clear Streamlit cache
streamlit cache clear

# Run with debugging
streamlit run main.py --logger.level=debug

# Run with specific Python interpreter
/path/to/python -m streamlit run main.py
```

## Support

For issues and questions:
1. Check this SETUP.md file
2. Review ARCHITECTURE.md for design details
3. Check backend service docstrings for API usage
4. Review logs for error details

---

**Ready to use SnapScribe! 🚀**
