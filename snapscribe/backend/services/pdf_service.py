"""
PDF service module.

Handles:
- PDF generation from frames
- PDF merging
- PDF manipulation
"""

import logging
import tempfile
import os
from typing import List, Optional
from fpdf import FPDF
from PyPDF2 import PdfMerger

from backend.utils.file_utils import ensure_output_directory

logger = logging.getLogger(__name__)


class PDFService:
    """
    Service for PDF operations.
    
    Provides methods to:
    - Generate PDFs from image frames
    - Merge multiple PDFs
    - Add content to PDFs
    """

    @staticmethod
    def frames_to_pdf(
        output_pdf_path: str,
        frame_files: List[str],
        title: Optional[str] = None,
    ) -> bool:
        """
        Create PDF from list of image frames.
        
        Args:
            output_pdf_path: Path to output PDF file.
            frame_files: List of image file paths.
            title: Optional title for the PDF.
            
        Returns:
            bool: True if successful, False otherwise.
            
        Raises:
            IOError: If PDF creation fails.
        """
        logger.info(f"Creating PDF from {len(frame_files)} frames")
        logger.debug(f"Output path: {output_pdf_path}")
        
        if not frame_files:
            logger.warning("No frames provided for PDF creation")
            return False
        
        try:
            # Ensure output directory exists
            output_dir = os.path.dirname(output_pdf_path)
            if output_dir:
                ensure_output_directory(output_dir)
            
            pdf = FPDF()
            pdf.set_auto_page_break(auto=False)
            
            for i, frame_path in enumerate(frame_files):
                logger.debug(f"Adding frame {i + 1}/{len(frame_files)}: {frame_path}")
                
                try:
                    pdf.add_page()
                    # Image dimensions: 190x277 (A4 - margins)
                    pdf.image(frame_path, x=10, y=10, w=190)
                except Exception as e:
                    logger.warning(f"Failed to add frame {frame_path}: {e}")
                    continue
            
            pdf.output(output_pdf_path, "F")
            logger.info(f"PDF created successfully: {output_pdf_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create PDF: {e}", exc_info=True)
            return False

    @staticmethod
    def create_text_pdf(
        output_pdf_path: str,
        title: str,
        content: str,
        footer: Optional[str] = None,
    ) -> bool:
        """
        Create PDF from text content.
        
        Args:
            output_pdf_path: Path to output PDF file.
            title: PDF title.
            content: Text content for PDF.
            footer: Optional footer text.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        logger.info(f"Creating text PDF: {output_pdf_path}")
        
        try:
            # Ensure output directory exists
            output_dir = os.path.dirname(output_pdf_path)
            if output_dir:
                ensure_output_directory(output_dir)
            
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            
            # Title
            pdf.set_font("Helvetica", style="B", size=16)
            pdf.set_text_color(71, 118, 230)
            pdf.cell(0, 10, title, align="C")
            pdf.ln(5)
            
            # Separator line
            pdf.set_draw_color(71, 118, 230)
            pdf.line(10, pdf.y, 200, pdf.y)
            pdf.ln(5)
            
            # Content
            pdf.set_font("Helvetica", size=11)
            pdf.set_text_color(45, 52, 54)
            
            # Handle encoding for special characters
            try:
                safe_content = content.encode("latin-1", "ignore").decode("latin-1")
            except Exception:
                safe_content = content
            
            pdf.multi_cell(0, 6, safe_content)
            
            # Footer
            if footer:
                pdf.ln(10)
                pdf.set_font("Helvetica", style="I", size=9)
                pdf.set_text_color(150, 150, 150)
                pdf.cell(0, 10, footer, align="C")
            
            pdf.output(output_pdf_path, "F")
            logger.info(f"Text PDF created successfully: {output_pdf_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create text PDF: {e}", exc_info=True)
            return False

    @staticmethod
    def merge_pdfs(
        pdf_files: List[str],
        output_path: str,
    ) -> bool:
        """
        Merge multiple PDF files into one.
        
        Args:
            pdf_files: List of PDF file paths in order.
            output_path: Path to output merged PDF.
            
        Returns:
            bool: True if successful, False otherwise.
            
        Raises:
            IOError: If merge operation fails.
        """
        logger.info(f"Merging {len(pdf_files)} PDF files")
        logger.debug(f"Output path: {output_path}")
        
        if not pdf_files or len(pdf_files) < 2:
            logger.warning("Need at least 2 PDFs to merge")
            return False
        
        temp_files = []
        
        try:
            # Ensure output directory exists
            output_dir = os.path.dirname(output_path)
            if output_dir:
                ensure_output_directory(output_dir)
            
            merger = PdfMerger()
            
            # Copy PDFs to temp files and merge
            for pdf_file in pdf_files:
                logger.debug(f"Adding PDF to merge: {pdf_file}")
                
                try:
                    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=".pdf"
                    ) as tmp:
                        # Copy file content
                        with open(pdf_file, "rb") as f:
                            tmp.write(f.read())
                        tmp.flush()
                        temp_files.append(tmp.name)
                        merger.append(tmp.name)
                except Exception as e:
                    logger.warning(f"Failed to add PDF {pdf_file}: {e}")
                    continue
            
            # Write merged PDF
            merger.write(output_path)
            merger.close()
            
            logger.info(f"PDFs merged successfully: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"PDF merge failed: {e}", exc_info=True)
            return False
            
        finally:
            # Clean up temporary files
            for temp_file in temp_files:
                try:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                except Exception as e:
                    logger.warning(f"Failed to clean temp file {temp_file}: {e}")


# Singleton instance for global use
pdf_service = PDFService()
