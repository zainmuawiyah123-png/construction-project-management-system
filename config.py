"""
ملف الإعدادات الرئيسية
"""

# إعدادات المشروع
PROJECT_SETTINGS = {
    'default_currency': 'SAR',  # الريال السعودي
    'decimal_places': 2,
    'date_format': '%Y-%m-%d',
}

# إعدادات الكميات
QUANTITY_SETTINGS = {
    'critical_threshold': 10.0,  # النسبة المئوية لتحديد البنود الحرجة
    'warning_threshold': 5.0,    # نسبة التحذير
}

# إعدادات التقارير
REPORT_SETTINGS = {
    'include_charts': True,
    'include_recommendations': True,
    'report_format': 'both',  # 'pdf', 'excel', 'both'
}

# إعدادات الملفات
FILE_SETTINGS = {
    'data_dir': 'data',
    'reports_dir': 'reports',
    'logs_dir': 'logs',
    'allowed_extensions': ['.xlsx', '.xls', '.csv'],
}

# معايير التقييم
PERFORMANCE_CRITERIA = {
    'excellent': {'min': 0, 'max': 5, 'label': 'ممتاز'},
    'good': {'min': 5, 'max': 10, 'label': 'جيد'},
    'warning': {'min': 10, 'max': 15, 'label': 'تحذير'},
    'critical': {'min': 15, 'max': 100, 'label': 'حرج'},
}
