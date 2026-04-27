"""
DeepRead page for YouTube video summarization.

Handles:
- YouTube transcript extraction
- AI-powered text summarization
- PDF generation of summaries
"""

import logging
import os
import streamlit as st

from backend.services.transcript_service import transcript_service
from backend.services.summarization_service import summarization_service
from backend.services.pdf_service import pdf_service
from backend.services.youtube_service import youtube_service
from backend.utils.validators import validate_youtube_url
from config.settings import settings

logger = logging.getLogger(__name__)


def render() -> None:
    """
    Render DeepRead page for YouTube video summarization.
    
    Allows users to:
    - Input YouTube video URL
    - Extract transcript
    - Generate AI summary
    - Download summary as PDF
    """
    st.set_page_config(
        page_title="DeepRead - Notes Generator",
        page_icon="📝",
        layout="wide",
    )

    # CSS styling
    st.markdown(
        """
    <style>
        .stApp {
            background: linear-gradient(120deg, #f8f9fa 0%, #e9ecef 100%);
            color: #2d3436;
        }
        
        .logo-container {
            text-align: center;
            margin-bottom: 2rem;
            animation: float 6s ease-in-out infinite;
        }
        
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }
        
        .modern-card {
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
            border: 1px solid rgba(255,255,255,0.4);
        }
        
        .modern-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        }
        
        .stButton button {
            background: linear-gradient(45deg, #4776E6, #8E54E9) !important;
            color: white !important;
            border: none !important;
            padding: 12px 24px !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 5px 15px rgba(71, 118, 230, 0.2) !important;
        }
        
        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 20px rgba(71, 118, 230, 0.3) !important;
        }
        
        .stTextInput input {
            border-radius: 12px !important;
            padding: 15px !important;
            font-size: 16px !important;
            transition: all 0.3s ease !important;  
            box-shadow: 0 0 0 3px white !important;
            background: white !important;
            color: black !important;
        }
        
        .feature-pill {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            background: rgba(71, 118, 230, 0.1);
            color: #4776E6;
            margin: 5px;
            font-size: 14px;
        }
        
        .stDownloadButton button {
            background: linear-gradient(45deg, #00b09b, #96c93d) !important;
            color: white !important;
            border: none !important;
            padding: 12px 24px !important;
            border-radius: 12px !important;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Enhanced Header with Animation
    st.markdown(
        """
        <div class='logo-container'>
            <h1 style='font-size: 3rem; font-weight: 800; background: linear-gradient(45deg, #4776E6, #8E54E9); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                📚 DeepRead
            </h1>
            <p style='font-size: 1.2rem; color: #666; margin-top: 10px;'>
                Transform Youtube Video Learning into Smart Summarized Notes
            </p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Feature Pills
    st.markdown(
        """
        <div style='text-align: center; margin-bottom: 2rem;'>
            <div class='feature-pill'>✨ Smart Summarization</div>
            <div class='feature-pill'>📝 Detailed Notes</div>
            <div class='feature-pill'>💾 PDF Export</div>
            <div class='feature-pill'>🎯 Key Points</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Two-column layout
    col1, col2 = st.columns([2, 1])

    youtube_link = None
    with col1:
        youtube_link = st.text_input(
            "🎥 Paste YouTube Video Link:",
            placeholder="https://www.youtube.com/watch?v=...",
        )
        out_pdf_name = st.text_input(
            "📄 Output PDF Name (without extension):",
            placeholder="My_Smart_Notes"
        )
        if youtube_link:
            video_id = youtube_service.get_video_id(youtube_link)
            if video_id:
                st.video(f"https://www.youtube.com/watch?v={video_id}")

    with col2:
        st.markdown(
            """
            <div style='background: rgba(71, 118, 230, 0.05); padding: 20px; border-radius: 12px;'>
                <h3 style='color: #4776E6; font-size: 1.2rem; margin-bottom: 10px;'>✨ How it works</h3>
                <ol style='color: #666; font-size: 0.9rem; margin-left: 20px;'>
                    <li>Paste your YouTube video link</li>
                    <li>Click "Generate Smart Notes"</li>
                    <li>Get instant notes & summary</li>
                    <li>Download as PDF for offline use</li>
                </ol>
            </div>
        """,
            unsafe_allow_html=True,
        )

    # Process Button
    if youtube_link:
        if not validate_youtube_url(youtube_link):
            st.error("Please enter a valid YouTube URL")
            return

        if st.button("🎯 Generate Smart Notes"):
            with st.spinner("🤓 Processing your video..."):
                # Results in tabs
                tab1, tab2 = st.tabs(["📝 Summary", "📚 Full Transcript"])

                # Extract transcript
                transcript_text = transcript_service.extract_transcript(youtube_link)

                with tab2:
                    st.markdown(
                        "<div style='background: white; padding: 20px; border-radius: 12px;color :black'>",
                        unsafe_allow_html=True,
                    )
                    if transcript_text:
                        st.write(transcript_text)
                    else:
                        st.error(
                            "❌ Video does not have a transcript. Please check the video link."
                        )
                    st.markdown("</div>", unsafe_allow_html=True)

                if transcript_text:
                    # Create transcript PDF
                    os.makedirs(settings.OUTPUT_DEEPREAD_DIR, exist_ok=True)

                    pdf_service.create_text_pdf(
                        f"{settings.OUTPUT_DEEPREAD_DIR}/f{out_pdf_name}_transcript.pdf",
                        "Video Transcript",
                        transcript_text,
                    )

                    # Summarize text
                    progress_bar = st.progress(0)
                    for i in range(100):
                        progress_bar.progress(i + 1)

                    summaries = summarization_service.summarize_text(
                        transcript_text, "local"
                    )

                    if summaries:
                        summary_text = " ".join(summaries)

                        # Create summary PDF
                        pdf_service.create_text_pdf(
                            f"{settings.OUTPUT_DEEPREAD_DIR}/f{out_pdf_name}_summary.pdf",
                            "Video Summary & Notes",
                            summary_text,
                            footer="Generated by DeepRead - SnapScribe",
                        )

                        with tab1:
                            st.markdown(
                                "<div style='background: white; padding: 20px; border-radius: 12px;color :black'>",
                                unsafe_allow_html=True,
                            )
                            st.write(summary_text)
                            st.markdown("</div>", unsafe_allow_html=True)

                        # Download buttons in columns
                        col_dl1, col_dl2 = st.columns(2)
                        with col_dl1:
                            with open(
                                f"{settings.OUTPUT_DEEPREAD_DIR}/output_summary.pdf", "rb"
                            ) as f:
                                st.download_button(
                                    "📥 Download Summary PDF",
                                    data=f.read(),
                                    file_name="summary_notes.pdf",
                                    mime="application/pdf",
                                )
                        with col_dl2:
                            with open(
                                f"{settings.OUTPUT_DEEPREAD_DIR}/output_transcript.pdf",
                                "rb",
                            ) as f:
                                st.download_button(
                                    "📥 Download Transcript PDF",
                                    data=f.read(),
                                    file_name="transcript.pdf",
                                    mime="application/pdf",
                                )
                    else:
                        st.error("Failed to summarize transcript")

    # Footer
    st.markdown(
        """
        <div style="text-align:center; margin-top:38px; color:black; font-size:15px;">
            Made with ❤️ by <b>SnapScribe</b> • Secure • Fast • Beautiful<br>
            <span style="font-size:13px;opacity:0.8;color:black;">Your files are never stored. All processing is done securely.</span>
        </div>
    """,
        unsafe_allow_html=True,
    )
