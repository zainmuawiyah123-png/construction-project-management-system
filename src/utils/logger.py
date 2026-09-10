"""نظام السجل والتسجيل"""
import logging
import os
from datetime import datetime
from pathlib import Path

def setup_logger(name):
    """إعداد نظام السجل"""
    # إنشاء مجلد السجلات
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)
    
    # إنشاء Logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # معالج الملف
    log_file = logs_dir / f"{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # معالج الكونسول
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # صيغة التسجيل
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
