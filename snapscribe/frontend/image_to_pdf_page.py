"""
Image to PDF Converter page.

Handles:
- Image file uploads
- Image arrangement/reordering
- Image to PDF conversion
"""

import logging
import streamlit as st

from backend.services.image_service import image_service

logger = logging.getLogger(__name__)


def render() -> None:
    """
    Render image to PDF converter page.
    
    Allows users to:
    - Upload multiple image files
    - Arrange images in desired order
    - Convert images to PDF
    - Download PDF
    """
    # ---------------------- PAGE CONFIG ----------------------
    st.set_page_config(
        page_title="Image to PDF | SnapScribe",
        page_icon="🖼️",
        layout="centered",
    )

    # ---------------------- CUSTOM STYLES ----------------------
    st.markdown(
        """
        <style>
            body {
                background: #ffffff;
                color: black;
            }
            .glass-box {
                background: rgba(255, 255, 255, 0.18);
                border-radius: 24px;
                box-shadow: 0 8px 40px rgba(0, 0, 0, 0.18);
                backdrop-filter: blur(12px);
                border: 1.5px solid rgba(255, 255, 255, 0.35);
                padding: 48px 32px;
                text-align: center;
                max-width: 750px;
                margin: 48px auto;
            }
            div.stButton > button:first-child {
                background: linear-gradient(135deg, #ffb347, #ffcc33);
                color: #222;
                border-radius: 12px;
                height: 3.2em;
                font-weight: 700;
                font-size: 1.1em;
                border: none;
                box-shadow: 0 2px 8px rgba(255,179,71,0.15);
                transition: all 0.3s ease;
            }
            div.stButton > button:first-child:hover {
                background: linear-gradient(135deg, #ffe29f, #ffb347);
                transform: scale(1.07);
                box-shadow: 0 4px 16px rgba(255,179,71,0.22);
            }
            .uploadedFile {
                color: #222 !important;
            }
            @keyframes fadeInDown {
                from { opacity: 0; transform: translateY(-20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .animated-title {
                animation: fadeInDown 1.2s ease-out;
                font-size: 2.6em;
                font-weight: 800;
                letter-spacing: 1px;
                margin-bottom: 0.2em;
            }
            .subtitle {
                font-size: 1.25em;
                opacity: 0.92;
                margin-bottom: 1.2em;
            }
            .step {
                background: rgba(255,255,255,0.09);
                border-radius: 8px;
                padding: 10px 18px;
                margin: 10px 0;
                font-size: 1.05em;
                color: white;
                box-shadow: 0 1px 4px rgba(255,179,71,0.08);
            }
            .download-btn {
                margin-top: 18px;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # ---------------------- HEADER ----------------------
    st.markdown(
        """
        <div class="glass-box">
            <h1 class="animated-title">🖼️ Image to PDF Converter</h1>
            <div class="subtitle">Transform your images into a single, high-quality PDF document.<br>
            <span style="font-size:16px;opacity:0.9;">Upload, arrange, and convert with ease!</span></div>
            <div class="step" style="color:black;">1️⃣ <b>Upload</b> your images (PNG, JPG, JPEG)</div>
            <div class="step" style="color:black;">2️⃣ <b>Arrange</b> them in your preferred order</div>
            <div class="step" style="color:black;">3️⃣ <b>Convert</b> and <b>Download</b> your PDF</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # ---------------------- MAIN APP ----------------------
    uploaded_files = st.file_uploader(
        "🖼️ **Upload your images**",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
       help="Select one or more images to convert into a PDF.",
    )

    if uploaded_files and len(uploaded_files) >= 1:
        filenames = [file.name for file in uploaded_files]
        order = st.multiselect(
            "🔀 **Arrange your images in the order you want:**",
            options=filenames,
            default=filenames,
            help="**Select to reorder your images before converting.**",
        )

        if st.button("✨ Generate PDF"):
            if len(order) < len(filenames):
                st.warning(
                    "Please select all images in your preferred order before converting."
                )
                return

            with st.spinner("Converting images to PDF..."):
                file_map = {file.name: file for file in uploaded_files}
                ordered_files = [file_map[fname] for fname in order]

                pdf_bytes = image_service.images_to_pdf(ordered_files)

                if pdf_bytes:
                    st.success("✅ Your images have been converted to PDF successfully!")
                    st.download_button(
                        label="⬇️ Download PDF",
                        data=pdf_bytes,
                        file_name="images.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                        key="download-btn",
                    )
                else:
                    st.error("Failed to convert images to PDF")

    else:
        st.info("**Upload at least one image to start converting.**", icon="🖼️")

    # ---------------------- FOOTER ----------------------
    st.markdown(
        """
        <div style="text-align:center; margin-top:38px; color:black; font-size:15px;">
            Made with ❤️ by <b>SnapScribe</b> • Secure • Fast • Beautiful<br>
            <span style="font-size:13px;opacity:0.8;color:black;">Your files are never stored. All processing is done securely.</span>
        </div>
    """,
        unsafe_allow_html=True,
    )
