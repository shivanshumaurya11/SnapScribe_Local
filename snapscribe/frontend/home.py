"""
Home page for SnapScribe application.

Displays landing page with tool cards for navigation.
"""

import streamlit as st


def render() -> None:
    """
    Render home page with tool selection cards.
    
    Displays animated hero section and tool selection buttons.
    """
    # PAGE CONFIG
    st.set_page_config(
        page_title="SnapScribe",
        page_icon="📚",
        layout="wide",
    )

    # CUSTOM STYLES
    st.markdown(
        """
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            background: #ffffff;
        }
        body {
            background: #ffffff;  
            color: black;
        }
        
        .landing-hero {
            min-height: 10vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            background: #ffffff;
            padding: 40px 20px;
            color: white;
        }
        
        .landing-content {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 30px;
            padding: 60px 90px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
            max-width: 900px;
            animation: slideInContent 1s ease-out;
            margin: 0 auto;
            width: 90%;
        }
        
        @keyframes slideInContent {
            from {
                opacity: 0;
                transform: scale(0.9);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }
        
        .landing-title {
            font-size: 3.5rem;
            font-weight: 800;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: slideDown 0.8s ease-out;
        }
        
        .landing-subtitle {
            font-size: 1.5rem;
            margin-bottom: 25px;
            color: #2d3436;
            font-weight: 700;
            animation: slideUp 0.8s ease-out 0.2s both;
        }
        
        .landing-description {
            font-size: 1.1rem;
            max-width: 700px;
            margin: 0 auto 30px;
            line-height: 1.8;
            color: #636e72;
            animation: slideUp 0.8s ease-out 0.4s both;
        }
        
        @keyframes slideDown {
            from { 
                opacity: 0; 
                transform: translateY(-30px); 
            }
            to { 
                opacity: 1; 
                transform: translateY(0); 
            }
        }
        
        @keyframes slideUp {
            from { 
                opacity: 0; 
                transform: translateY(30px); 
            }
            to { 
                opacity: 1; 
                transform: translateY(0); 
            }
        }
        
        .scroll-indicator {
            margin-top: 40px;
            animation: bounce 2s infinite;
            color: #636e72;
            font-weight: 600;
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-15px); }
        }
        
        .tools-section {
            padding: 100px 20px;
            background: #ffffff;
            animation: slideInSection 1.2s ease-out;
        }
        
        @keyframes slideInSection {
            from {
                opacity: 0;
                transform: translateY(50px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .section-title {
            text-align: center;
            font-size: 2.5rem;
            font-weight: 800;
            color: #2d3436;
            margin-bottom: 20px;
            animation: slideInSection 1s ease-out;
        }
        
        .section-subtitle {
            text-align: center;
            font-size: 1.1rem;
            color: #636e72;
            margin-bottom: 60px;
            animation: slideInSection 1.1s ease-out;
        }
        
        div[data-testid="stButton"] button {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.08), rgba(118, 75, 162, 0.08)) !important;
            border: 2.5px solid rgba(102, 126, 234, 0.3) !important;
            border-radius: 20px !important;
            padding: 45px 30px !important;
            text-align: center !important;
            transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
            cursor: pointer !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08) !important;
            min-height: 300px !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            align-items: center !important;
            color: #2d3436 !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            line-height: 2 !important;
            white-space: normal !important;
            word-wrap: break-word !important;
            background-color: white !important;
            user-select: none !important;
            -webkit-user-select: none !important;
            gap: 8px !important;
        }
        
        div[data-testid="stButton"] button::first-line {
            font-size: 3.5rem !important;
            line-height: 1 !important;
            margin-bottom: 10px !important;
        }
        
        div[data-testid="stButton"] button:hover {
            transform: translateY(-15px) scale(1.02) !important;
            box-shadow: 0 20px 50px rgba(102, 126, 234, 0.25) !important;
            border-color: rgba(142, 84, 233, 0.8) !important;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15)) !important;
            background-color: linear-gradient(135deg, #f0f2ff 0%, #f5f0ff 100%) !important;
        }
        
        div[data-testid="stButton"] button:active {
            transform: translateY(-8px) scale(0.99) !important;
        }
        
        .footer-section {
            background: white;
            padding: 50px 20px;
            color: black;
            animation: slideInSection 1.3s ease-out;
        }
        
        .footer-text {
            text-align: center;
            font-size: 15px;
            margin-bottom: 10px;
        }
        
        .footer-subtext {
            text-align: center;
            font-size: 13px;
            opacity: 0.8;
        }
        
        @media (max-width: 1024px) {
            .landing-content {
                padding: 50px 40px;
                border-radius: 25px;
                margin: 0 auto;
                width: 85%;
                max-width: 800px;
            }
            
            .landing-title {
                font-size: 3rem;
                margin-bottom: 15px;
            }
            
            .landing-subtitle {
                font-size: 1.3rem;
                margin-bottom: 20px;
            }
            
            .landing-description {
                font-size: 1rem;
                margin-bottom: 25px;
            }
            
            .section-title {
                font-size: 2.2rem;
                margin-bottom: 15px;
            }
            
            .section-subtitle {
                font-size: 1rem;
                margin-bottom: 50px;
            }
            
            .tools-section {
                padding: 80px 15px;
            }
            
            div[data-testid="stButton"] button {
                padding: 40px 25px !important;
                min-height: 280px !important;
                font-size: 0.9rem !important;
                line-height: 1.8 !important;
            }
            
            div[data-testid="stButton"] button::first-line {
                font-size: 3.2rem !important;
            }
        }
        
        @media (max-width: 768px) {
            .landing-hero {
                min-height: 90vh;
                padding: 30px 15px;
            }
            
            .landing-content {
                padding: 40px 25px;
                border-radius: 20px;
                box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
                margin: 0 auto;
                width: 90%;
                max-width: 600px;
            }
            
            .landing-title {
                font-size: 2.5rem;
                margin-bottom: 12px;
            }
            
            .landing-subtitle {
                font-size: 1.1rem;
                margin-bottom: 15px;
                font-weight: 600;
            }
            
            .landing-description {
                font-size: 0.95rem;
                line-height: 1.6;
                margin-bottom: 20px;
                padding: 0 5px;
            }
            
            .scroll-indicator {
                margin-top: 25px;
                font-size: 0.9rem;
            }
            
            .tools-section {
                padding: 60px 12px;
                color: #2d3436;
            }
            
            .section-title {
                font-size: 1.8rem;
                margin-bottom: 10px;
            }
            
            .section-subtitle {
                font-size: 0.95rem;
                margin-bottom: 40px;
            }
            
            div[data-testid="stButton"] button {
                padding: 35px 20px !important;
                min-height: 260px !important;
                font-size: 0.85rem !important;
                border-radius: 16px !important;
                line-height: 1.7 !important;
                margin-bottom: 20px !important;
            }
            
            div[data-testid="stButton"] button::first-line {
                font-size: 2.8rem !important;
            }
            
            div[data-testid="stButton"] button:hover {
                transform: translateY(-10px) scale(1.01) !important;
                box-shadow: 0 15px 40px rgba(102, 126, 234, 0.2) !important;
            }
            
            .footer-text {
                font-size: 14px;
            }
            
            .footer-subtext {
                font-size: 12px;
            }
        }
        
        @media (max-width: 480px) {
            .landing-hero {
                min-height: 85vh;
                padding: 25px 12px;
            }
            
            .landing-content {
                padding: 35px 20px;
                border-radius: 18px;
                max-width: 100%;
                margin: 0 auto;
                width: 95%;
            }
            
            .landing-title {
                font-size: 2rem;
                margin-bottom: 10px;
            }
            
            .landing-subtitle {
                font-size: 1rem;
                margin-bottom: 12px;
            }
            
            .landing-description {
                font-size: 0.9rem;
                line-height: 1.5;
                margin-bottom: 15px;
                max-width: 100%;
            }
            
            .scroll-indicator {
                margin-top: 20px;
                font-size: 0.85rem;
            }
            
            .tools-section {
                padding: 50px 10px;
            }
            
            .section-title {
                font-size: 1.5rem;
                margin-bottom: 8px;
            }
            
            .section-subtitle {
                font-size: 0.9rem;
                margin-bottom: 35px;
            }
            
            div[data-testid="stButton"] button {
                padding: 30px 18px !important;
                min-height: 240px !important;
                font-size: 0.8rem !important;
                border-radius: 15px !important;
                line-height: 1.6 !important;
                margin-bottom: 15px !important;
                border: 2px solid rgba(102, 126, 234, 0.3) !important;
            }
            
            div[data-testid="stButton"] button::first-line {
                font-size: 2.4rem !important;
            }
            
            div[data-testid="stButton"] button:hover {
                transform: translateY(-8px) scale(1.01) !important;
                box-shadow: 0 12px 30px rgba(102, 126, 234, 0.2) !important;
            }
            
            .footer-section {
                padding: 40px 15px;
            }
            
            .footer-text {
                font-size: 13px;
                margin-bottom: 8px;
            }
            
            .footer-subtext {
                font-size: 11px;
            }
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # ---------------------- LANDING SECTION ----------------------
    st.markdown(
        """
    <div class='landing-hero'>
        <div class='landing-content'>
            <h1 class='landing-title'>📚 SnapScribe</h1>
            <p class='landing-subtitle'>Your Ultimate Learning Companion</p>
            <p class='landing-description'>
                Welcome to SnapScribe, the all-in-one platform designed to enhance your learning experience for both Students, Educators and Professionals! 
                Whether you're looking to convert videos into summarized notes, extract images from videos, merge PDFs, or convert images to PDFs, 
                SnapScribe has got you covered.
            </p>
            <div class='scroll-indicator'>
                <p>Scroll Down to Explore Tools</p>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ---------------------- TOOLS SECTION ----------------------
    st.markdown(
        """
    <div class='tools-section'>
        <h2 class='section-title'>✨ Explore Something Powerful</h2>
        <p class='section-subtitle'>Choose anyone below to get started with your learning journey</p>
    """,
        unsafe_allow_html=True,
    )

    # Tools Grid - 2x3 (6 tools)
    col1, col2 = st.columns(2, gap="large")

    with col1:
        if st.button(
            """🎬

Video to Visual Summaries

Extract key frames from videos and create visual summaries as PDF documents.""",
            key="btn_video",
            use_container_width=True,
        ):
            st.session_state.selected_tool = "Upload Video to PDF"
            st.rerun()

    with col2:
        if st.button(
            """📚

DeepRead

Transform YouTube videos into intelligent, detailed notes using AI-powered summarization.""",
            key="btn_deepread",
            use_container_width=True,
        ):
            st.session_state.selected_tool = "DeepRead"
            st.rerun()

    col3, col4 = st.columns(2, gap="large")

    with col3:
        if st.button(
            """🎥

YouTube to Notes

Convert YouTube videos into summarized notes with timestamps and key points.""",
            key="btn_youtube",
            use_container_width=True,
        ):
            st.session_state.selected_tool = "YouTube to PDF"
            st.rerun()

    with col4:
        if st.button(
            """💻

Local Video Processor

Process local video files and generate PDF summaries from extracted frames.""",
            key="btn_local",
            use_container_width=True,
        ):
            st.session_state.selected_tool = "Local Video to PDF"
            st.rerun()

    col5, col6 = st.columns(2, gap="large")

    with col5:
        if st.button(
            """📄

Merge PDFs

Combine multiple PDF files into one organized document. Arrange files in your preferred order.""",
            key="btn_merge",
            use_container_width=True,
        ):
            st.session_state.selected_tool = "Merge PDFs"
            st.rerun()

    with col6:
        if st.button(
            """🖼️

Image to PDF

Convert your images into high-quality PDF documents. Arrange and organize images seamlessly.""",
            key="btn_image",
            use_container_width=True,
        ):
            st.session_state.selected_tool = "Image to PDF"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------- FOOTER ----------------------
    st.markdown(
        """
        <div class="footer-section">
            <p class="footer-text">
                Made with ❤️ by <b>SnapScribe</b> • Secure • Fast • Beautiful
            </p>
            <p class="footer-subtext">Your files are never stored. All processing is done securely on your device.</p>
        </div>
    """,
        unsafe_allow_html=True,
    )
