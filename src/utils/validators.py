"""التحقق من صحة البيانات"""
import os
from pathlib import Path

class Validator:
    """فئة التحقق من صحة البيانات"""
    
    @staticmethod
    def validate_file_exists(file_path):
        """التحقق من وجود الملف"""
        return Path(file_path).exists()
    
    @staticmethod
    def validate_file_extension(file_path, allowed_extensions):
        """التحقق من امتداد الملف"""
        file_ext = Path(file_path).suffix.lower()
        return file_ext in allowed_extensions
    
    @staticmethod
    def validate_number(value, min_val=None, max_val=None):
        """التحقق من أن القيمة رقم صحيح"""
        try:
            num = float(value)
            if min_val is not None and num < min_val:
                return False
            if max_val is not None and num > max_val:
                return False
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_string(value, min_length=1, max_length=None):
        """التحقق من صحة النص"""
        if not isinstance(value, str):
            return False
        if len(value) < min_length:
            return False
        if max_length and len(value) > max_length:
            return False
        return True
