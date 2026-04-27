"""
PDF Merger page.

Handles:
- PDF file uploads
- PDF arrangement/reordering
- PDF merging
"""

import logging
import streamlit as st

from backend.services.pdf_service import pdf_service

logger = logging.getLogger(__name__)


def render() -> None:
    """
    Render PDF merger page.
    
    Allows users to:
    - Upload multiple PDF files
    - Arrange PDFs in desired order
    - Merge PDFs into single document
    - Download merged PDF
    """
    # PAGE CONFIG
    st.set_page_config(
        page_title="PDF Merger | SnapScribe",
        page_icon="📄",
        layout="centered",
    )

    # CUSTOM STYLES
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
                box-shadow: 0 8px 40px rgba(0, 0, 0, 0.25);
                backdrop-filter: blur(12px);
                border: 1.5px solid rgba(255, 255, 255, 0.35);
                padding: 48px 32px;
                text-align: center;
                max-width: 750px;
                margin: 48px auto;
            }
            div.stButton > button:first-child {
                background: linear-gradient(135deg, #4F8BF9, #1C67E3);
                color: white;
                border-radius: 12px;
                height: 3.2em;
                font-weight: 700;
                font-size: 1.1em;
                border: none;
                box-shadow: 0 2px 8px rgba(79,139,249,0.15);
                transition: all 0.3s ease;
            }
            div.stButton > button:first-child:hover {
                background: linear-gradient(135deg, #5AA2FF, #4F8BF9);
                transform: scale(1.07);
                box-shadow: 0 4px 16px rgba(79,139,249,0.22);
            }
            .uploadedFile {
                color: white !important;
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
                color: #e3e3e3;
                box-shadow: 0 1px 4px rgba(79,139,249,0.08);
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
            <h1 class="animated-title">📄 PDF Merger</h1>
            <div class="subtitle">Effortlessly combine multiple PDF files into one beautiful document.<br>
            <span style="font-size:16px;opacity:0.9;">Upload, arrange, and merge with a single click.</span></div>
            <div class="step" style="color:black;">1️⃣ <b>Upload</b> your PDF files</div>
            <div class="step" style="color:black;">2️⃣ <b>Arrange</b> them in your preferred order</div>
            <div class="step" style="color:black;">3️⃣ <b>Merge</b> and <b>Download</b> your new PDF</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # ---------------------- MAIN APP ----------------------
    uploaded_files = st.file_uploader(
        "**📂 Upload your PDF files**",
        type="pdf",
        accept_multiple_files=True,
        help="**Select two or more PDFs to merge.**",
    )

    if uploaded_files and len(uploaded_files) >= 2:
        filenames = [file.name for file in uploaded_files]
        order = st.multiselect(
            "**🧩 Arrange your PDFs in the order you want:**",
            options=filenames,
            default=filenames,
            help="Select to reorder your PDFs before merging.",
        )

        if st.button("**✨ Merge PDFs**"):
            if len(order) < len(filenames):
                st.warning(
                    "Please select all PDFs in your preferred order before merging."
                )
                return

            with st.spinner("Merging PDFs..."):
                file_map = {file.name: file for file in uploaded_files}

                # Create list of PDF paths for merging
                import tempfile
                import os

                temp_files = []
                pdf_paths = []

                try:
                    for fname in order:
                        pdf_file = file_map[fname]
                        with tempfile.NamedTemporaryFile(
                            delete=False, suffix=".pdf"
                        ) as tmp:
                            tmp.write(pdf_file.read())
                            tmp.flush()
                            temp_files.append(tmp.name)
                            pdf_paths.append(tmp.name)

                    # Merge PDFs
                    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=".pdf"
                    ) as out_tmp:
                        success = pdf_service.merge_pdfs(pdf_paths, out_tmp.name)

                        if success:
                            st.success("✅ Your PDFs have been merged successfully!")

                            with open(out_tmp.name, "rb") as f:
                                st.download_button(
                                    label="⬇️ Download Merged PDF",
                                    data=f.read(),
                                    file_name="merged.pdf",
                                    mime="application/pdf",
                                    use_container_width=True,
                                    key="download-btn",
                                )
                        else:
                            st.error("Failed to merge PDFs")

                        try:
                            os.unlink(out_tmp.name)
                        except Exception as e:
                            logger.warning(f"Failed to clean temp file: {e}")

                except Exception as e:
                    logger.error(f"Merge operation failed: {e}", exc_info=True)
                    st.error(f"Merge operation failed: {e}")

                finally:
                    # Clean up temporary files
                    for temp_file in temp_files:
                        try:
                            if os.path.exists(temp_file):
                                os.unlink(temp_file)
                        except Exception as e:
                            logger.warning(f"Failed to clean temp file: {e}")

    else:
        st.info("Upload at least two PDF files to start merging.", icon="📘")

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
