"""
مدير التقارير المالية والدراسات
"""
import pandas as pd
from datetime import datetime
from typing import List, Dict
from src.core.models import Project, FinancialReport, WorkItem
from src.utils.logger import setup_logger

logger = setup_logger('FinancialManager')

class FinancialManager:
    """فئة إدارة التقارير المالية"""
    
    def __init__(self, project: Project):
        """تهيئة مدير التقارير المالية"""
        self.project = project
    
    def calculate_costs(self) -> Dict:
        """حساب التكاليف الإجمالية"""
        total_quote_cost = sum(item.total_cost for item in self.project.work_items)
        
        # حساب التكلفة الفعلية (بناءً على كميات المخطط)
        total_actual_cost = sum(
            item.plan_quantity * item.unit_price 
            for item in self.project.work_items
        )
        
        variance = total_actual_cost - total_quote_cost
        variance_pct = 0
        if total_quote_cost != 0:
            variance_pct = (variance / total_quote_cost) * 100
        
        return {
            'إجمالي_تكلفة_العطاء': round(total_quote_cost, 2),
            'إجمالي_التكلفة_الفعلية': round(total_actual_cost, 2),
            'الانحراف': round(variance, 2),
            'نسبة_الانحراف_%': round(variance_pct, 2)
        }
    
    def get_cost_by_category(self) -> pd.DataFrame:
        """الحصول على التكاليف مجمعة حسب الفئة"""
        categories = {}
        
        for item in self.project.work_items:
            if item.category not in categories:
                categories[item.category] = {
                    'عدد_البنود': 0,
                    'كمية_العطاء': 0,
                    'كمية_المخطط': 0,
                    'تكلفة_العطاء': 0,
                    'التكلفة_الفعلية': 0,
                    'الانحراف': 0
                }
            
            actual_cost = item.plan_quantity * item.unit_price
            variance = actual_cost - item.total_cost
            
            categories[item.category]['عدد_البنود'] += 1
            categories[item.category]['كمية_العطاء'] += item.quote_quantity
            categories[item.category]['كمية_المخطط'] += item.plan_quantity
            categories[item.category]['تكلفة_العطاء'] += item.total_cost
            categories[item.category]['التكلفة_الفعلية'] += actual_cost
            categories[item.category]['الانحراف'] += variance
        
        # تحويل إلى DataFrame
        data = []
        for category, info in categories.items():
            data.append({
                'الفئة': category,
                'عدد_البنود': info['عدد_البنود'],
                'كمية_العطاء': info['كمية_العطاء'],
                'كمية_المخطط': info['كمية_المخطط'],
                'تكلفة_العطاء': round(info['تكلفة_العطاء'], 2),
                'التكلفة_الفعلية': round(info['التكلفة_الفعلية'], 2),
                'الانحراف': round(info['الانحراف'], 2),
                'نسبة_الانحراف_%': round(
                    (info['الانحراف'] / info['تكلفة_العطاء'] * 100) 
                    if info['تكلفة_العطاء'] != 0 else 0,
                    2
                )
            })
        
        df = pd.DataFrame(data)
        logger.info("تم حساب التكاليف حسب الفئات")
        return df
    
    def generate_financial_report(self) -> FinancialReport:
        """إنشاء تقرير مالي شامل"""
        costs = self.calculate_costs()
        
        report = FinancialReport(
            project_id=self.project.id,
            report_date=datetime.now(),
            total_quote_cost=costs['إجمالي_تكلفة_العطاء'],
            total_actual_cost=costs['إجمالي_التكلفة_الفعلية']
        )
        
        # إضافة التوصيات
        report.recommendations = self._generate_recommendations(report, costs)
        
        logger.info("تم إنشاء التقرير المالي")
        return report
    
    def _generate_recommendations(self, report: FinancialReport, costs: Dict) -> List[str]:
        """إنشاء التوصيات بناءً على البيانات المالية"""
        recommendations = []
        variance_pct = abs(costs['نسبة_الانحراف_%'])
        
        if variance_pct > 20:
            recommendations.append("⚠️ تحذير حرج: الانحراف المالي كبير جداً، يجب مراجعة فورية")
            recommendations.append("🔍 ضرورة إجراء تدقيق شامل على جميع البنود المالية")
        elif variance_pct > 10:
            recommendations.append("⚠️ تحذير: الانحراف المالي مرتفع، يجب المتابعة الدقيقة")
            recommendations.append("📊 التركيز على البنود ذات الانحرافات الكبيرة")
        elif variance_pct > 5:
            recommendations.append("✓ الانحراف المالي مقبول، تابع المراقبة العادية")
        else:
            recommendations.append("✓ الأداء المالي ممتاز، تم الالتزام بالميزانية")
        
        # توصيات إضافية
        if costs['الانحراف'] > 0:
            recommendations.append(f"💰 التكلفة الفعلية أزيد من العطاء بمقدار: {abs(costs['الانحراف'])}")
            recommendations.append("📈 يجب البحث عن أسباب الزيادة وتطبيق إجراءات تصحيحية")
        else:
            recommendations.append(f"💰 الاقتصاد في التكاليف: {abs(costs['الانحراف'])}")
            recommendations.append("✅ تم تحقيق توفير اقتصادي")
        
        # توصيات حسب الحالة
        if report.status == "Critical":
            recommendations.append("🚨 إجراء اجتماع طارئ مع الإدارة العليا")
        elif report.status == "Warning":
            recommendations.append("📋 إعداد خطة عمل لتصحيح الانحرافات")
        
        return recommendations
    
    def get_price_analysis(self) -> pd.DataFrame:
        """تحليل الأسعار ومقارنتها"""
        data = []
        
        for item in self.project.work_items:
            actual_unit_price = item.unit_price if item.quote_quantity != 0 else 0
            
            data.append({
                'البند': item.name,
                'الوحدة': item.unit,
                'سعر_الوحدة_العطاء': item.unit_price,
                'كمية_العطاء': item.quote_quantity,
                'إجمالي_العطاء': item.total_cost,
                'كمية_الفعلية': item.plan_quantity,
                'الإجمالي_الفعلي': item.plan_quantity * item.unit_price
            })
        
        df = pd.DataFrame(data)
        logger.info("تم تحليل الأسعار")
        return df
