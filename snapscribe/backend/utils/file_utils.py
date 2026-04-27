"""
Utility functions for file operations.

Handles:
- Directory creation and management
- File path validation
- PDF file operations
"""

import os
from typing import List
from pathlib import Path


def ensure_output_directory(directory_path: str) -> None:
    """
    Ensure output directory exists.
    
    Args:
        directory_path: Path to the directory to create.
        
    Raises:
        OSError: If directory creation fails.
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
    except OSError as e:
        raise OSError(f"Failed to create directory {directory_path}: {e}") from e


def get_safe_filename(filename: str) -> str:
    """
    Sanitize filename for safe file system operations.
    
    Removes or replaces invalid file system characters.
    
    Args:
        filename: Original filename.
        
    Returns:
        str: Sanitized filename.
    """
    invalid_chars = r'<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, "-")
    return filename.strip(".")


def file_exists(file_path: str) -> bool:
    """
    Check if file exists.
    
    Args:
        file_path: Path to the file.
        
    Returns:
        bool: True if file exists, False otherwise.
    """
    return os.path.isfile(file_path)


def delete_file_if_exists(file_path: str) -> bool:
    """
    Delete file if it exists.
    
    Args:
        file_path: Path to the file.
        
    Returns:
        bool: True if file was deleted, False if it didn't exist.
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except OSError as e:
        raise OSError(f"Failed to delete file {file_path}: {e}") from e


def get_file_size(file_path: str) -> int:
    """
    Get file size in bytes.
    
    Args:
        file_path: Path to the file.
        
    Returns:
        int: File size in bytes.
    """
    try:
        return os.path.getsize(file_path)
    except OSError as e:
        raise OSError(f"Failed to get file size for {file_path}: {e}") from e


def join_paths(*paths: str) -> str:
    """
    Join multiple path segments safely.
    
    Args:
        *paths: Path segments to join.
        
    Returns:
        str: Joined path.
    """
    return os.path.join(*paths)
