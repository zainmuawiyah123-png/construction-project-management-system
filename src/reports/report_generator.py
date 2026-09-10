"""
مولد التقارير الشاملة
"""
import os
from pathlib import Path
from datetime import datetime
import pandas as pd
from fpdf import FPDF
from src.core.models import Project
from src.core.quantity_manager import QuantityManager
from src.core.financial_manager import FinancialManager
from src.utils.logger import setup_logger
from src.utils.file_handler import FileHandler

logger = setup_logger('ReportGenerator')

class ReportGenerator:
    """فئة إنشاء التقارير الشاملة"""
    
    def __init__(self, project: Project):
        """تهيئة مولد التقارير"""
        self.project = project
        self.reports_dir = Path('reports')
        self.reports_dir.mkdir(exist_ok=True)
        self.qty_manager = QuantityManager(project)
        self.fin_manager = FinancialManager(project)
    
    def generate_pdf_report(self) -> str:
        """إنشاء تقرير PDF شامل"""
        try:
            pdf = FPDF(orientation='P', unit='mm', format='A4')
            pdf.add_page()
            pdf.set_font('Arial', 'B', 16)
            
            # العنوان
            pdf.cell(0, 10, 'تقرير المشروع الهندسي الشامل', 0, 1, 'C')
            pdf.set_font('Arial', '', 12)
            
            # معلومات المشروع
            pdf.ln(5)
            pdf.cell(0, 8, f'اسم المشروع: {self.project.name}', 0, 1)
            pdf.cell(0, 8, f'الموقع: {self.project.location}', 0, 1)
            pdf.cell(0, 8, f'العميل: {self.project.client_name}', 0, 1)
            pdf.cell(0, 8, f'تاريخ التقرير: {datetime.now().strftime("%Y-%m-%d")}', 0, 1)
            
            # ملخص الكميات
            pdf.ln(10)
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 8, 'ملخص الكميات', 0, 1)
            pdf.set_font('Arial', '', 11)
            
            totals = self.qty_manager.get_total_quantities()
            pdf.cell(0, 7, f'إجمالي كمية العطاء: {totals["إجمالي_كمية_العطاء"]}', 0, 1)
            pdf.cell(0, 7, f'إجمالي كمية المخطط: {totals["إجمالي_كمية_المخطط"]}', 0, 1)
            pdf.cell(0, 7, f'الفرق: {totals["إجمالي_الفرق"]}', 0, 1)
            pdf.cell(0, 7, f'نسبة الفرق: {totals["نسبة_الفرق_%"]}%', 0, 1)
            
            # ملخص التكاليف
            pdf.ln(5)
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 8, 'ملخص التكاليف', 0, 1)
            pdf.set_font('Arial', '', 11)
            
            costs = self.fin_manager.calculate_costs()
            pdf.cell(0, 7, f'إجمالي تكلفة العطاء: {costs["إجمالي_تكلفة_العطاء"]:,.2f}', 0, 1)
            pdf.cell(0, 7, f'إجمالي التكلفة الفعلية: {costs["إجمالي_التكلفة_الفعلية"]:,.2f}', 0, 1)
            pdf.cell(0, 7, f'الانحراف: {costs["الانحراف"]:,.2f}', 0, 1)
            pdf.cell(0, 7, f'نسبة الانحراف: {costs["نسبة_الانحراف_%"]}%', 0, 1)
            
            # التقرير المالي
            pdf.ln(5)
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 8, 'التقرير المالي والتوصيات', 0, 1)
            pdf.set_font('Arial', '', 11)
            
            report = self.fin_manager.generate_financial_report()
            for rec in report.recommendations:
                # تقسيم النص الطويل
                lines = pdf.multi_cell(0, 6, rec, 0, 'R')
            
            # حفظ ملف PDF
            output_path = self.reports_dir / f"report_{self.project.id}.pdf"
            pdf.output(str(output_path))
            
            logger.info(f"تم إنشاء تقرير PDF: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء تقرير PDF: {str(e)}")
            raise
    
    def generate_excel_report(self) -> str:
        """إنشاء تقرير Excel شامل"""
        try:
            output_path = self.reports_dir / f"report_{self.project.id}.xlsx"
            
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                # ورقة معلومات المشروع
                project_info = pd.DataFrame([
                    {'الحقل': 'اسم المشروع', 'القيمة': self.project.name},
                    {'الحقل': 'الموقع', 'القيمة': self.project.location},
                    {'الحقل': 'العميل', 'القيمة': self.project.client_name},
                    {'الحقل': 'تاريخ التقرير', 'القيمة': datetime.now().strftime("%Y-%m-%d")},
                ])
                project_info.to_excel(writer, sheet_name='معلومات المشروع', index=False)
                
                # ورقة مقارنة الكميات
                quantities = self.qty_manager.compare_quantities()
                quantities.to_excel(writer, sheet_name='مقارنة الكميات', index=False)
                
                # ورقة التكاليف
                costs = self.fin_manager.get_cost_by_category()
                costs.to_excel(writer, sheet_name='التكاليف حسب الفئة', index=False)
                
                # ورقة تحليل الأسعار
                prices = self.fin_manager.get_price_analysis()
                prices.to_excel(writer, sheet_name='تحليل الأسعار', index=False)
                
                # ورقة ملخص النتائج
                totals = self.qty_manager.get_total_quantities()
                fin_costs = self.fin_manager.calculate_costs()
                
                summary = pd.DataFrame([
                    {'البيان': 'إجمالي كمية العطاء', 'القيمة': totals['إجمالي_كمية_العطاء']},
                    {'البيان': 'إجمالي كمية المخطط', 'القيمة': totals['إجمالي_كمية_المخطط']},
                    {'البيان': 'الفرق في الكميات', 'القيمة': totals['إجمالي_الفرق']},
                    {'البيان': 'نسبة الفرق %', 'القيمة': totals['نسبة_الفرق_%']},
                    {'البيان': '', 'القيمة': ''},
                    {'البيان': 'إجمالي تكلفة العطاء', 'القيمة': fin_costs['إجمالي_تكلفة_العطاء']},
                    {'البيان': 'إجمالي التكلفة الفعلية', 'القيمة': fin_costs['إجمالي_التكلفة_الفعلية']},
                    {'البيان': 'الانحراف المالي', 'القيمة': fin_costs['الانحراف']},
                    {'البيان': 'نسبة الانحراف %', 'القيمة': fin_costs['نسبة_الانحراف_%']},
                ])
                summary.to_excel(writer, sheet_name='الملخص', index=False)
                
                # ورقة التوصيات
                report = self.fin_manager.generate_financial_report()
                recommendations = pd.DataFrame([
                    {'التوصيات': rec} for rec in report.recommendations
                ])
                recommendations.to_excel(writer, sheet_name='التوصيات', index=False)
            
            logger.info(f"تم إنشاء تقرير Excel: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء تقرير Excel: {str(e)}")
            raise
    
    def generate_executive_summary(self) -> Dict:
        """إنشاء ملخص تنفيذي"""
        totals = self.qty_manager.get_total_quantities()
        costs = self.fin_manager.calculate_costs()
        report = self.fin_manager.generate_financial_report()
        critical = self.qty_manager.get_critical_items()
        
        return {
            'project_name': self.project.name,
            'report_date': datetime.now().isoformat(),
            'status': report.status,
            'quantity_summary': totals,
            'financial_summary': costs,
            'critical_items_count': len(critical),
            'recommendations': report.recommendations
        }
