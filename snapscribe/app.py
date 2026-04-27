"""
SnapScribe - Main Application Entry Point

A production-ready, modular Streamlit application for converting media
(videos, images, PDFs) into various formats and summaries.

Architecture:
- Modular design with separation of concerns
- Backend services independent of Streamlit
- Clean frontend layer with minimal logic
- Centralized configuration management
"""

import logging
import sys
from pathlib import Path

import streamlit as st

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Add config directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import frontend pages
from frontend import (
    home,
    deepread_page,
    video_visual_page,
    youtube_visual_page,
    local_video_page,
    pdf_merger_page,
    image_to_pdf_page,
)

# Import configuration
from config.settings import settings


def initialize_session_state() -> None:
    """
    Initialize Streamlit session state variables.
    
    Sets default values for:
    - Tool selection routing
    - HuggingFace token storage
    """
    if "selected_tool" not in st.session_state:
        st.session_state.selected_tool = "Home"
        logger.info("Initialized session state")


def render_back_button() -> None:
    """
    Render back to home button in sidebar.
    
    Only shown on non-home pages.
    """
    if st.session_state.selected_tool != "Home":
        if st.sidebar.button("← Back to Home"):
            st.session_state.selected_tool = "Home"
            st.rerun()


def route_page() -> None:
    """
    Route to the selected page based on session state.
    
    Dispatches to appropriate frontend page based on
    st.session_state.selected_tool value.
    """
    tool = st.session_state.selected_tool

    logger.debug(f"Routing to page: {tool}")

    if tool == "Home":
        home.render()

    elif tool == "Upload Video to PDF":
        video_visual_page.render()

    elif tool == "DeepRead":
        deepread_page.render()

    elif tool == "YouTube to PDF":
        youtube_visual_page.render()

    elif tool == "Local Video to PDF":
        local_video_page.render()

    elif tool == "Merge PDFs":
        pdf_merger_page.render()

    elif tool == "Image to PDF":
        image_to_pdf_page.render()

    else:
        st.error(f"Unknown tool: {tool}")
        st.session_state.selected_tool = "Home"
        st.rerun()


def main() -> None:
    """
    Main application entry point.
    
    Initializes session state, renders sidebar navigation,
    and routes to selected page.
    """
    # Initialize session state
    initialize_session_state()

    # Render back button on non-home pages
    render_back_button()

    # Route to selected page
    route_page()


if __name__ == "__main__":
    logger.info("SnapScribe application started")
    main()
