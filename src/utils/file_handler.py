"""معالج الملفات"""
import os
import shutil
from pathlib import Path
import pandas as pd
from openpyxl import load_workbook

class FileHandler:
    """فئة معالجة الملفات"""
    
    @staticmethod
    def create_directory(dir_path):
        """إنشاء مجلد"""
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        return True
    
    @staticmethod
    def read_excel(file_path, sheet_name=0):
        """قراءة ملف Excel"""
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            return df
        except Exception as e:
            raise Exception(f"خطأ في قراءة الملف: {str(e)}")
    
    @staticmethod
    def save_excel(df, file_path, sheet_name='Sheet1'):
        """حفظ DataFrame في ملف Excel"""
        try:
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            return True
        except Exception as e:
            raise Exception(f"خطأ في حفظ الملف: {str(e)}")
    
    @staticmethod
    def read_csv(file_path):
        """قراءة ملف CSV"""
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
            return df
        except Exception as e:
            raise Exception(f"خطأ في قراءة الملف: {str(e)}")
    
    @staticmethod
    def save_csv(df, file_path):
        """حفظ DataFrame في ملف CSV"""
        try:
            df.to_csv(file_path, index=False, encoding='utf-8')
            return True
        except Exception as e:
            raise Exception(f"خطأ في حفظ الملف: {str(e)}")
    
    @staticmethod
    def copy_file(source, destination):
        """نسخ ملف"""
        try:
            shutil.copy2(source, destination)
            return True
        except Exception as e:
            raise Exception(f"خطأ في نسخ الملف: {str(e)}")
    
    @staticmethod
    def delete_file(file_path):
        """حذف ملف"""
        try:
            Path(file_path).unlink()
            return True
        except Exception as e:
            raise Exception(f"خطأ في حذف الملف: {str(e)}")
