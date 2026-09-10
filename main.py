"""
نظام إدارة المشاريع الهندسية المتكامل
Construction Project Management System
Version: 1.0.0
"""

import os
import sys
from pathlib import Path

# إضافة المسارات الأساسية
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# استيراد المكتبات الرئيسية
from src.core.project_manager import ProjectManager
from src.ui.menu import MainMenu
from src.utils.logger import setup_logger

# إعداد السجل
logger = setup_logger('main')

def main():
    """الدالة الرئيسية للبرنامج"""
    try:
        logger.info("بدء تشغيل برنامج إدارة المشاريع الهندسية")
        
        # إنشاء مدير المشروع
        project_manager = ProjectManager()
        
        # إنشاء القائمة الرئيسية
        menu = MainMenu(project_manager)
        
        # بدء البرنامج
        menu.run()
        
        logger.info("انتهاء البرنامج بنجاح")
        
    except Exception as e:
        logger.error(f"خطأ في البرنامج الرئيسي: {str(e)}")
        print(f"\n❌ خطأ: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
