# SnapScribe - Production-Ready Application

A refactored, modular implementation of SnapScribe following industry-standard clean architecture principles.

## 📁 Project Structure

```
snapscribe/
│
├── main.py                         # Application entry point
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── config/
│   ├── __init__.py
│   └── settings.py                 # Configuration & environment variables
│
├── frontend/
│   ├── __init__.py
│   ├── home.py                     # Landing page with tool selection
│   ├── deepread_page.py            # YouTube summarization
│   ├── video_visual_page.py        # Local video to PDF
│   ├── youtube_visual_page.py      # YouTube to visual summaries
│   ├── local_video_page.py         # Local video file processing
│   ├── pdf_merger_page.py          # PDF merging
│   └── image_to_pdf_page.py        # Image to PDF conversion
│
├── backend/
│   ├── __init__.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── youtube_service.py      # YouTube operations
│   │   ├── video_service.py        # Video frame extraction
│   │   ├── transcript_service.py   # YouTube transcript API
│   │   ├── summarization_service.py # HuggingFace summarization
│   │   ├── pdf_service.py          # PDF operations
│   │   └── image_service.py        # Image operations
│   │
│   └── utils/
│       ├── __init__.py
│       ├── file_utils.py           # File operations
│       └── validators.py           # Input validation
```

## 🎯 Architecture Principles

### Separation of Concerns
- **Frontend**: Pure Streamlit UI code only
- **Backend**: Business logic completely independent of Streamlit
- **Config**: Centralized configuration management
- **Utils**: Reusable helper functions

### SOLID Principles Applied
1. **Single Responsibility**: Each service handles one domain
2. **Open/Closed**: Services are extensible without modification
3. **Liskov Substitution**: Services can be replaced without breaking code
4. **Interface Segregation**: Clean service interfaces
5. **Dependency Inversion**: Services inject dependencies

### Key Improvements
✅ **Zero Streamlit in Backend** - All business logic is frontend-independent
✅ **Type Hints Everywhere** - Full type annotations for IDE support
✅ **Google-style Docstrings** - Comprehensive documentation
✅ **Proper Logging** - Replaced all print statements with logging
✅ **DRY Principle** - No code duplication
✅ **Error Handling** - Proper exception handling with logging
✅ **Configuration Management** - Centralized settings
✅ **Testable Code** - Services can be unit tested independently

## 🚀 Quick Start

### 1. Installation

```bash
cd snapscribe
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the project root:

```env
HF_TOKEN=your_huggingface_api_token
```

### 3. Run Application

```bash
streamlit run main.py
```

## 📦 Service Documentation

### YouTubeService
Handles all YouTube operations:
- Extract video metadata
- Download videos
- Handle playlists
- Extract video IDs

```python
from backend.services.youtube_service import youtube_service

video_id = youtube_service.get_video_id(url)
title = youtube_service.get_video_title(url)
video_path = youtube_service.download_video(url, output_path)
playlist_videos = youtube_service.get_playlist_videos(playlist_url)
```

### VideoService
Handles video processing:
- Extract unique frames using SSIM
- Get video duration
- Configurable frame sampling

```python
from backend.services.video_service import video_service

frames = video_service.extract_unique_frames(
    video_path,
    output_folder,
    frame_skip=100,
    similarity_threshold=1.0
)
```

### TranscriptService
Handles YouTube transcript extraction:
- Fetch transcripts
- Check transcript availability
- Format transcript data

```python
from backend.services.transcript_service import transcript_service

transcript = transcript_service.extract_transcript(youtube_url)
is_available = transcript_service.is_transcript_available(video_id)
```

### SummarizationService
Handles AI-powered summarization:
- Local BART model summarization
- HuggingFace Inference API
- Chunk-based processing for long texts

```python
from backend.services.summarization_service import summarization_service

summaries = summarization_service.summarize_text(
    transcript_text,
    method="local"  # or "api"
)
```

### PDFService
Handles all PDF operations:
- Create PDFs from image frames
- Create text PDFs
- Merge multiple PDFs

```python
from backend.services.pdf_service import pdf_service

# Create PDF from frames
pdf_service.frames_to_pdf(output_path, frame_files)

# Create text PDF
pdf_service.create_text_pdf(
    output_path,
    title="My Title",
    content="PDF content",
    footer="Optional footer"
)

# Merge PDFs
pdf_service.merge_pdfs(pdf_files_list, output_path)
```

### ImageService
Handles image operations:
- Convert images to PDF
- Validate image files
- Get image dimensions

```python
from backend.services.image_service import image_service

pdf_bytes = image_service.images_to_pdf(image_files)
is_valid = image_service.validate_image_file(file_obj)
dimensions = image_service.get_image_dimensions(image_file)
```

## 🔧 Configuration (config/settings.py)

Centralized settings management:
- Directory paths
- Model configuration
- Default values
- HuggingFace token handling

```python
from config.settings import settings

# Access settings
output_dir = settings.OUTPUT_PDFS_DIR
model = settings.HF_SUMMARIZATION_MODEL
token = settings.get_hf_token()
```

## 📝 Frontend Pages

Each frontend page is completely independent and contains only Streamlit UI code:

- **home.py**: Landing page with animated tool selection cards
- **deepread_page.py**: YouTube to intelligent notes converter
- **video_visual_page.py**: Upload and process local videos
- **youtube_visual_page.py**: Download YouTube videos and extract key frames
- **local_video_page.py**: Process local video files
- **pdf_merger_page.py**: Merge multiple PDFs
- **image_to_pdf_page.py**: Convert images to PDF

All pages follow the same pattern:
```python
def render() -> None:
    """Render page UI."""
    st.set_page_config(...)
    # Page-specific UI code
```

## 🧪 Testing Backend Services

Since backend is completely independent of Streamlit, it can be easily tested:

```python
from backend.services.youtube_service import youtube_service
from backend.services.summarization_service import summarization_service

# Test YouTube service
video_id = youtube_service.get_video_id(url)
assert video_id is not None

# Test summarization
summaries = summarization_service.summarize_text(text)
assert len(summaries) > 0
```

## 🔐 Environment Variables

Required environment variables:

```env
HF_TOKEN=your_huggingface_api_token  # For Inference API (optional)
```

The application supports multiple token sources:
1. Environment variable (`HF_TOKEN`)
2. Streamlit secrets (`st.secrets["HF_TOKEN"]`)
3. Session state (user input)
4. Sidebar input prompt (for Streamlit Cloud)

## 📊 Logging

All modules use proper logging instead of print statements:

```python
import logging

logger = logging.getLogger(__name__)
logger.info("Processing started")
logger.debug("Debug information")
logger.warning("Warning message")
logger.error("Error occurred", exc_info=True)
```

Configure logging level in main.py:
```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
```

## 🚨 Error Handling

All services include proper error handling with logging:

```python
try:
    result = service.operation()
except Exception as e:
    logger.error(f"Operation failed: {e}", exc_info=True)
    return None
```

## 💡 Type Hints

All functions include type hints for better IDE support:

```python
def extract_unique_frames(
    video_path: str,
    output_folder: str,
    frame_skip: int = 100,
    similarity_threshold: float = 1.0,
) -> List[str]:
    """Extract unique frames from video."""
    ...
```

## 📚 Documentation

All functions include Google-style docstrings:

```python
def summarize_text(
    self,
    text: str,
    method: str = "local",
) -> Optional[List[str]]:
    """
    Summarize long text by splitting into chunks.
    
    Splits text into chunks of defined size and summarizes each chunk,
    then returns list of summaries.
    
    Args:
        text: Text to summarize.
        method: Summarization method ("local" or "api").
        
    Returns:
        Optional[List[str]]: List of summary texts or None if fails.
    """
```

## 🔄 Data Flow

```
Frontend UI (Streamlit)
        ↓
Services (Business Logic)
        ↓
Utilities (Helpers)
        ↓
External APIs (YouTube, HuggingFace)
```

Each layer is independent and can be tested/modified separately.

## 📈 Performance Considerations

- Frame extraction uses SSIM for efficient similarity detection
- Summarization splits long texts into chunks for better results
- Proper resource cleanup with tempfile management
- Streaming support for large file uploads

## 🔐 Security

- Input validation for all user inputs
- File path traversal prevention
- Environment variable isolation
- Secure token handling with Streamlit secrets

## 🎯 Future Improvements

- Add unit tests for all services
- Implement caching for repeated operations
- Add progress indicators for long operations
- Support for more video platforms
- Database for output history

## 📄 License

[Your License Here]

## 🤝 Contributing

[Contributing Guidelines]

---

**Built with ❤️ using clean architecture principles**
