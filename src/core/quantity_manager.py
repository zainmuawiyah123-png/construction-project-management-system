"""
مدير الكميات والمقارنات
"""
import pandas as pd
from typing import List, Dict, Tuple
from src.core.models import Project, WorkItem
from src.utils.logger import setup_logger

logger = setup_logger('QuantityManager')

class QuantityManager:
    """فئة إدارة الكميات والمقارنات"""
    
    def __init__(self, project: Project):
        """تهيئة مدير الكميات"""
        self.project = project
    
    def compare_quantities(self) -> pd.DataFrame:
        """مقارنة كميات العطاء مع المخطط"""
        data = []
        
        for item in self.project.work_items:
            variance = item.calculate_variance()
            variance_pct = item.get_variance_percentage()
            
            data.append({
                'معرف': item.id,
                'اسم_البند': item.name,
                'الفئة': item.category,
                'الوحدة': item.unit,
                'كمية_العطاء': item.quote_quantity,
                'كمية_المخطط': item.plan_quantity,
                'الفرق': variance,
                'نسبة_الفرق_%': round(variance_pct, 2),
                'الحالة': self._get_status(variance_pct)
            })
        
        df = pd.DataFrame(data)
        logger.info("تمت مقارنة الكميات بنجاح")
        return df
    
    def get_total_quantities(self) -> Dict:
        """الحصول على الكميات الإجمالية"""
        total_quote = sum(item.quote_quantity for item in self.project.work_items)
        total_plan = sum(item.plan_quantity for item in self.project.work_items)
        total_variance = total_quote - total_plan
        
        variance_pct = 0
        if total_plan != 0:
            variance_pct = (total_variance / total_plan) * 100
        
        return {
            'إجمالي_كمية_العطاء': total_quote,
            'إجمالي_كمية_المخطط': total_plan,
            'إجمالي_الفرق': total_variance,
            'نسبة_الفرق_%': round(variance_pct, 2)
        }
    
    def get_critical_items(self, threshold: float = 10.0) -> List[Dict]:
        """الحصول على البنود التي تجاوزت نسبة الفرق المسموحة"""
        critical = []
        
        for item in self.project.work_items:
            variance_pct = abs(item.get_variance_percentage())
            if variance_pct > threshold:
                critical.append({
                    'البند': item.name,
                    'نسبة_الفرق_%': variance_pct,
                    'الكمية_العطاء': item.quote_quantity,
                    'الكمية_المخطط': item.plan_quantity,
                    'الفرق': item.calculate_variance()
                })
        
        logger.info(f"تم العثور على {len(critical)} بنود حرجة")
        return critical
    
    def get_quantity_by_category(self) -> Dict:
        """الحصول على الكميات مجمعة حسب الفئة"""
        categories = {}
        
        for item in self.project.work_items:
            if item.category not in categories:
                categories[item.category] = {
                    'كمية_العطاء': 0,
                    'كمية_المخطط': 0,
                    'التكلفة': 0
                }
            
            categories[item.category]['كمية_العطاء'] += item.quote_quantity
            categories[item.category]['كمية_المخطط'] += item.plan_quantity
            categories[item.category]['التكلفة'] += item.total_cost
        
        return categories
    
    @staticmethod
    def _get_status(variance_pct: float) -> str:
        """تحديد حالة البند بناءً على نسبة الفرق"""
        abs_variance = abs(variance_pct)
        if abs_variance <= 5:
            return "ممتاز"
        elif abs_variance <= 10:
            return "جيد"
        elif abs_variance <= 15:
            return "تحذير"
        else:
            return "حرج"
