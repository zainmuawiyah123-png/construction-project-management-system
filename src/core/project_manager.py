"""
مدير المشاريع الرئيسي
"""
import os
from pathlib import Path
from datetime import datetime
import pandas as pd
from typing import List, Optional

from src.core.models import Project, WorkItem, FinancialReport
from src.utils.file_handler import FileHandler
from src.utils.logger import setup_logger
from src.core.work_items_data import WORK_ITEMS_CATEGORIES

logger = setup_logger('ProjectManager')

class ProjectManager:
    """فئة إدارة المشاريع"""
    
    def __init__(self):
        """تهيئة مدير المشاريع"""
        self.projects = {}
        self.data_dir = Path('data')
        self.reports_dir = Path('reports')
        self.projects_file = self.data_dir / 'projects.xlsx'
        
        # إنشاء المجلدات الأساسية
        FileHandler.create_directory(self.data_dir)
        FileHandler.create_directory(self.reports_dir)
        FileHandler.create_directory('logs')
        
        logger.info("تم تهيئة مدير المشاريع")
    
    def create_project(self, name: str, location: str, client_name: str, 
                      start_date: datetime, end_date: datetime, 
                      budget: float = 0.0, description: str = "") -> Project:
        """إنشاء مشروع جديد"""
        project_id = f"PRJ_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        project = Project(
            id=project_id,
            name=name,
            location=location,
            client_name=client_name,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            description=description
        )
        self.projects[project_id] = project
        logger.info(f"تم إنشاء المشروع: {name} (ID: {project_id})")
        return project
    
    def add_work_item_to_project(self, project_id: str, work_item: WorkItem):
        """إضافة بند عمل إلى المشروع"""
        if project_id not in self.projects:
            raise ValueError(f"المشروع {project_id} غير موجود")
        
        self.projects[project_id].add_work_item(work_item)
        logger.info(f"تم إضافة بند عمل: {work_item.name} للمشروع {project_id}")
    
    def import_quote_items(self, project_id: str, file_path: str) -> bool:
        """استيراد بنود العطاء من ملف Excel"""
        try:
            if project_id not in self.projects:
                raise ValueError(f"المشروع {project_id} غير موجود")
            
            df = FileHandler.read_excel(file_path)
            
            for idx, row in df.iterrows():
                item = WorkItem(
                    id=f"ITEM_{idx}",
                    name=row.get('الاسم', f'بند_{idx}'),
                    category=row.get('الفئة', ''),
                    unit=row.get('الوحدة', ''),
                    quote_quantity=float(row.get('كمية_العطاء', 0)),
                    unit_price=float(row.get('سعر_الوحدة', 0)),
                    notes=row.get('ملاحظات', '')
                )
                self.add_work_item_to_project(project_id, item)
            
            logger.info(f"تم استيراد {len(df)} بند من ملف العطاء")
            return True
        except Exception as e:
            logger.error(f"خطأ في استيراد العطاء: {str(e)}")
            raise
    
    def import_plan_items(self, project_id: str, file_path: str) -> bool:
        """استيراد كميات المخطط من ملف Excel"""
        try:
            if project_id not in self.projects:
                raise ValueError(f"المشروع {project_id} غير موجود")
            
            df = FileHandler.read_excel(file_path)
            project = self.projects[project_id]
            
            for idx, row in df.iterrows():
                item_name = row.get('الاسم', '')
                plan_qty = float(row.get('كمية_المخطط', 0))
                
                # البحث عن البند المطابق وتحديث الكمية
                for work_item in project.work_items:
                    if work_item.name == item_name:
                        work_item.plan_quantity = plan_qty
                        work_item.total_cost = work_item.quote_quantity * work_item.unit_price
                        break
            
            logger.info(f"تم استيراد كميات المخطط للمشروع {project_id}")
            return True
        except Exception as e:
            logger.error(f"خطأ في استيراد المخطط: {str(e)}")
            raise
    
    def get_project(self, project_id: str) -> Optional[Project]:
        """الحصول على مشروع"""
        return self.projects.get(project_id)
    
    def get_all_projects(self) -> dict:
        """الحصول على جميع المشاريع"""
        return self.projects
    
    def delete_project(self, project_id: str) -> bool:
        """حذف مشروع"""
        if project_id in self.projects:
            del self.projects[project_id]
            logger.info(f"تم حذف المشروع: {project_id}")
            return True
        return False
    
    def save_project_to_excel(self, project_id: str) -> bool:
        """حفظ بيانات المشروع في Excel"""
        try:
            project = self.get_project(project_id)
            if not project:
                raise ValueError(f"المشروع {project_id} غير موجود")
            
            # إعداد البيانات
            data = []
            for item in project.work_items:
                data.append({
                    'معرف': item.id,
                    'الاسم': item.name,
                    'الفئة': item.category,
                    'الوحدة': item.unit,
                    'كمية_العطاء': item.quote_quantity,
                    'كمية_المخطط': item.plan_quantity,
                    'الفرق': item.calculate_variance(),
                    'نسبة_الفرق': item.get_variance_percentage(),
                    'سعر_الوحدة': item.unit_price,
                    'إجمالي_التكلفة': item.total_cost,
                    'ملاحظات': item.notes
                })
            
            df = pd.DataFrame(data)
            
            # حفظ الملف
            output_file = self.reports_dir / f"project_{project_id}.xlsx"
            FileHandler.save_excel(df, output_file)
            
            logger.info(f"تم حفظ المشروع في: {output_file}")
            return True
        except Exception as e:
            logger.error(f"خطأ في حفظ المشروع: {str(e)}")
            raise
