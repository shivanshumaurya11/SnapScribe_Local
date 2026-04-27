"""
Image service module.

Handles:
- Image loading and validation
- Image to PDF conversion
- Image format handling
"""

import logging
import io
from typing import List, Optional
from PIL import Image

logger = logging.getLogger(__name__)


class ImageService:
    """
    Service for image operations.
    
    Provides methods to:
    - Convert images to properly formatted images
    - Create PDFs from image lists
    - Handle various image formats
    """

    SUPPORTED_FORMATS = {"png", "jpg", "jpeg"}

    @staticmethod
    def images_to_pdf(image_files: List) -> Optional[io.BytesIO]:
        """
        Convert list of images to PDF.
        
        Opens images, converts them to RGB if needed, and creates
        a single PDF with images as pages.
        
        Args:
            image_files: List of image file objects (from st.file_uploader).
            
        Returns:
            Optional[io.BytesIO]: PDF bytes or None if conversion fails.
            
        Raises:
            IOError: If image processing fails.
        """
        logger.info(f"Converting {len(image_files)} images to PDF")
        
        if not image_files:
            logger.warning("No images provided for conversion")
            return None
        
        try:
            pil_images = []
            
            for i, img_file in enumerate(image_files):
                logger.debug(f"Processing image {i + 1}/{len(image_files)}")
                
                try:
                    # Open image from uploaded file
                    img = Image.open(img_file)
                    
                    # Convert to RGB if needed (for RGBA, grayscale, etc.)
                    if img.mode != "RGB":
                        logger.debug(f"Converting image {i + 1} from {img.mode} to RGB")
                        img = img.convert("RGB")
                    
                    pil_images.append(img)
                    logger.debug(f"Successfully processed image {i + 1}")
                    
                except Exception as e:
                    logger.warning(f"Failed to process image {i + 1}: {e}")
                    continue
            
            if not pil_images:
                logger.error("No images were successfully processed")
                return None
            
            # Create PDF from images
            logger.info(f"Creating PDF from {len(pil_images)} processed images")
            pdf_bytes = io.BytesIO()
            
            pil_images[0].save(
                pdf_bytes,
                format="PDF",
                save_all=True,
                append_images=pil_images[1:] if len(pil_images) > 1 else [],
                quality=95,
            )
            pdf_bytes.seek(0)
            
            logger.info("PDF created successfully from images")
            return pdf_bytes
            
        except Exception as e:
            logger.error(f"Image to PDF conversion failed: {e}", exc_info=True)
            return None

    @staticmethod
    def validate_image_file(file_obj) -> bool:
        """
        Validate if file is a supported image format.
        
        Args:
            file_obj: File object from uploader.
            
        Returns:
            bool: True if valid image, False otherwise.
        """
        try:
            if not hasattr(file_obj, "name"):
                return False
            
            file_extension = file_obj.name.split(".")[-1].lower()
            
            if file_extension not in ImageService.SUPPORTED_FORMATS:
                logger.warning(
                    f"Unsupported image format: {file_extension}"
                )
                return False
            
            # Try to open image to verify it's valid
            img = Image.open(file_obj)
            img.verify()
            
            logger.debug(f"Validated image: {file_obj.name}")
            return True
            
        except Exception as e:
            logger.warning(f"Image validation failed: {e}")
            return False

    @staticmethod
    def get_image_dimensions(image_file) -> Optional[tuple]:
        """
        Get image dimensions (width, height).
        
        Args:
            image_file: File object or path.
            
        Returns:
            Optional[tuple]: (width, height) or None if fails.
        """
        try:
            img = Image.open(image_file)
            dimensions = img.size
            logger.debug(f"Image dimensions: {dimensions}")
            return dimensions
        except Exception as e:
            logger.warning(f"Failed to get image dimensions: {e}")
            return None


# Singleton instance for global use
image_service = ImageService()
