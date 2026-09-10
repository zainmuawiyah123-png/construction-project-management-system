"""
واجهة المستخدم الرئيسية
"""
import os
from datetime import datetime
from pathlib import Path
from src.core.project_manager import ProjectManager
from src.core.quantity_manager import QuantityManager
from src.core.financial_manager import FinancialManager
from src.reports.report_generator import ReportGenerator
from src.utils.logger import setup_logger

logger = setup_logger('MainMenu')

class MainMenu:
    """فئة القائمة الرئيسية"""
    
    def __init__(self, project_manager: ProjectManager):
        """تهيئة القائمة الرئيسية"""
        self.project_manager = project_manager
        self.current_project = None
    
    def run(self):
        """تشغيل البرنامج"""
        self.show_welcome()
        
        while True:
            self.show_main_menu()
            choice = input("\n👈 اختر من الخيارات (1-6): ").strip()
            
            if choice == '1':
                self.create_new_project()
            elif choice == '2':
                self.manage_project()
            elif choice == '3':
                self.view_projects()
            elif choice == '4':
                self.generate_reports()
            elif choice == '5':
                self.show_help()
            elif choice == '6':
                print("\n👋 شكراً لاستخدام البرنامج! وداعاً.")
                logger.info("انتهى البرنامج بشكل طبيعي")
                break
            else:
                print("\n❌ اختيار غير صحيح! يرجى المحاولة مجدداً.")
    
    def show_welcome(self):
        """عرض رسالة الترحيب"""
        print("\n" + "="*70)
        print("🏗️  نظام إدارة المشاريع الهندسية المتكامل")
        print("   Construction Project Management System")
        print("="*70)
        print("\n✨ مرحباً بك في برنامج إدارة المشاريع الهندسية")
        print("\nالإمكانيات الرئيسية:")
        print("  • إدارة بنود الأعمال الهندسية")
        print("  • رفع جداول كميات العطاء والمخططات")
        print("  • مقارنة الكميات والتكاليف")
        print("  • إنشاء التقارير المالية الشاملة")
        print("  • تحليل الانحرافات والتوصيات\n")
    
    def show_main_menu(self):
        """عرض القائمة الرئيسية"""
        print("\n" + "-"*70)
        print("📋 القائمة الرئيسية:")
        print("-"*70)
        print("1. ➕ إنشاء مشر��ع جديد")
        print("2. ✏️  إدارة مشروع")
        print("3. 📊 عرض المشاريع")
        print("4. 📈 إنشاء التقارير")
        print("5. ❓ المساعدة")
        print("6. 🚪 الخروج")
        print("-"*70)
    
    def create_new_project(self):
        """إنشاء مشروع جديد"""
        print("\n" + "="*70)
        print("➕ إنشاء مشروع جديد")
        print("="*70)
        
        try:
            name = input("\n📝 اسم المشروع: ").strip()
            if not name:
                print("❌ اسم المشروع مطلوب!")
                return
            
            location = input("📍 موقع المشروع: ").strip()
            client_name = input("👤 اسم العميل: ").strip()
            
            print("\n📅 تاريخ البداية (صيغة: YYYY-MM-DD):")
            start_date_str = input("   ").strip()
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            
            print("📅 تاريخ النهاية (صيغة: YYYY-MM-DD):")
            end_date_str = input("   ").strip()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            
            budget = input("💰 الميزانية (اختياري): ").strip()
            budget = float(budget) if budget else 0.0
            
            description = input("📄 وصف المشروع (اختياري): ").strip()
            
            # إنشاء المشروع
            project = self.project_manager.create_project(
                name=name,
                location=location,
                client_name=client_name,
                start_date=start_date,
                end_date=end_date,
                budget=budget,
                description=description
            )
            
            print(f"\n✅ تم إنشاء المشروع بنجاح!")
            print(f"   معرف المشروع: {project.id}")
            self.current_project = project
            logger.info(f"تم إنشاء المشروع: {name}")
            
        except ValueError as e:
            print(f"\n❌ خطأ في الإدخال: {str(e)}")
        except Exception as e:
            print(f"\n❌ حدث خطأ: {str(e)}")
            logger.error(f"خطأ في إنشاء المشروع: {str(e)}")
    
    def manage_project(self):
        """إدارة مشروع"""
        if not self.current_project:
            project_id = input("\n📋 أدخل معرف المشروع: ").strip()
            self.current_project = self.project_manager.get_project(project_id)
            
            if not self.current_project:
                print("❌ المشروع غير موجود!")
                return
        
        while True:
            print("\n" + "-"*70)
            print(f"✏️  إدارة المشروع: {self.current_project.name}")
            print("-"*70)
            print("1. 📤 استيراد بنود العطاء")
            print("2. 📤 استيراد كميات المخطط")
            print("3. 📊 عرض الكميات")
            print("4. 💰 عرض التكاليف")
            print("5. 💾 حفظ المشروع")
            print("6. ↩️  العودة للقائمة الرئيسية")
            print("-"*70)
            
            choice = input("\n👈 اختر من الخيارات (1-6): ").strip()
            
            if choice == '1':
                self.import_quote_items()
            elif choice == '2':
                self.import_plan_items()
            elif choice == '3':
                self.view_quantities()
            elif choice == '4':
                self.view_costs()
            elif choice == '5':
                self.save_project()
            elif choice == '6':
                break
            else:
                print("❌ اختيار غير صحيح!")
    
    def import_quote_items(self):
        """استيراد بنود العطاء"""
        file_path = input("\n📂 أدخل مسار ملف العطاء (Excel): ").strip()
        
        if not Path(file_path).exists():
            print("❌ الملف غير موجود!")
            return
        
        try:
            self.project_manager.import_quote_items(self.current_project.id, file_path)
            print(f"✅ تم استيراد {len(self.current_project.work_items)} بند من العطاء")
        except Exception as e:
            print(f"❌ خطأ في الاستيراد: {str(e)}")
    
    def import_plan_items(self):
        """استيراد كميات المخطط"""
        file_path = input("\n📂 أدخل مسار ملف المخطط (Excel): ").strip()
        
        if not Path(file_path).exists():
            print("❌ الملف غير موجود!")
            return
        
        try:
            self.project_manager.import_plan_items(self.current_project.id, file_path)
            print("✅ تم استيراد كميات المخطط بنجاح")
        except Exception as e:
            print(f"❌ خطأ في الاستيراد: {str(e)}")
    
    def view_quantities(self):
        """عرض الكميات والمقارنة"""
        try:
            qty_manager = QuantityManager(self.current_project)
            
            print("\n" + "="*70)
            print("📊 مقارنة الكميات")
            print("="*70)
            
            # الإجمالي العام
            totals = qty_manager.get_total_quantities()
            print("\n📈 الملخص الإجمالي:")
            print(f"   إجمالي كمية العطاء: {totals['إجمالي_كمية_العطاء']}")
            print(f"   إجمالي كمية المخطط: {totals['إجمالي_كمية_المخطط']}")
            print(f"   الفرق: {totals['إجمالي_الفرق']}")
            print(f"   نسبة الفرق: {totals['نسبة_الفرق_%']}%")
            
            # البنود الحرجة
            critical = qty_manager.get_critical_items()
            if critical:
                print(f"\n⚠️  البنود الحرجة ({len(critical)} بند):")
                for item in critical[:10]:  # عرض أول 10 بنود
                    print(f"   • {item['البند']}: {item['نسبة_الفرق_%']:.2f}%")
            else:
                print("\n✅ لا توجد بنود حرجة")
            
        except Exception as e:
            print(f"❌ خطأ: {str(e)}")
    
    def view_costs(self):
        """عرض التكاليف"""
        try:
            fm = FinancialManager(self.current_project)
            costs = fm.calculate_costs()
            
            print("\n" + "="*70)
            print("💰 تحليل التكاليف")
            print("="*70)
            print(f"\nإجمالي تكلفة العطاء: {costs['إجمالي_تكلفة_العطاء']:,.2f}")
            print(f"إجمالي التكلفة الفعلية: {costs['إجمالي_التكلفة_الفعلية']:,.2f}")
            print(f"الانحراف: {costs['الانحراف']:,.2f}")
            print(f"نسبة الانحراف: {costs['نسبة_الانحراف_%']:.2f}%")
            
        except Exception as e:
            print(f"❌ خطأ: {str(e)}")
    
    def save_project(self):
        """حفظ المشروع"""
        try:
            self.project_manager.save_project_to_excel(self.current_project.id)
            print("\n✅ تم حفظ المشروع بنجاح")
        except Exception as e:
            print(f"❌ خطأ في الحفظ: {str(e)}")
    
    def view_projects(self):
        """عرض المشاريع"""
        projects = self.project_manager.get_all_projects()
        
        if not projects:
            print("\n❌ لا توجد مشاريع بعد")
            return
        
        print("\n" + "="*70)
        print("📊 المشاريع المسجلة:")
        print("="*70)
        
        for project_id, project in projects.items():
            print(f"\n📌 {project.name}")
            print(f"   المعرف: {project_id}")
            print(f"   الموقع: {project.location}")
            print(f"   العميل: {project.client_name}")
            print(f"   عدد البنود: {len(project.work_items)}")
    
    def generate_reports(self):
        """إنشاء التقارير"""
        if not self.current_project:
            project_id = input("\n📋 أدخل معرف المشروع: ").strip()
            self.current_project = self.project_manager.get_project(project_id)
            
            if not self.current_project:
                print("❌ المشروع غير موجود!")
                return
        
        print("\n" + "-"*70)
        print("📈 إنشاء التقارير:")
        print("-"*70)
        print("1. 📄 تقرير PDF شامل")
        print("2. 📊 تقرير Excel")
        print("3. 🔙 عودة")
        print("-"*70)
        
        choice = input("\n👈 اختر نوع التقرير: ").strip()
        
        try:
            if choice == '1':
                report_gen = ReportGenerator(self.current_project)
                report_gen.generate_pdf_report()
                print("✅ تم إنشاء تقرير PDF بنجاح")
            elif choice == '2':
                report_gen = ReportGenerator(self.current_project)
                report_gen.generate_excel_report()
                print("✅ تم إنشاء تقرير Excel بنجاح")
            elif choice == '3':
                return
            else:
                print("❌ اختيار غير صحيح!")
        except Exception as e:
            print(f"❌ خطأ في إنشاء التقرير: {str(e)}")
            logger.error(f"خطأ في التقرير: {str(e)}")
    
    def show_help(self):
        """عرض المساعدة"""
        print("\n" + "="*70)
        print("❓ المساعدة والتعليمات")
        print("="*70)
        print("""
🎯 خطوات الاستخدام:

1️⃣  إنشاء مشروع:
   • اختر "إنشاء مشروع جديد" من القائمة الرئيسية
   • أدخل معلومات المشروع (الاسم، الموقع، العميل، إلخ)

2️⃣  استيراد البيانات:
   • استيراد ملف العطاء (جدول الكميات والأسعار)
   • استيراد ملف المخطط (الكميات من المخططات الهندسية)

3️⃣  مقارنة الكميات:
   • يتم حساب الفرق بين كميات العطاء والمخطط
   • عرض البنود الحرجة التي تجاوزت نسبة الفرق المسموحة

4️⃣  تحليل التكاليف:
   • حساب إجمالي التكاليف
   • عرض الانحرافات المالية
   • توليد التوصيات

5️⃣  إنشاء التقارير:
   • تقرير PDF شامل يحتوي على جميع التحليلات
   • تقرير Excel يمكن تحديثه وتعديله

📝 ملاحظات مهمة:
   • تأكد من صيغة ملفات Excel قبل الاستيراد
   • يجب أن تحتوي الملفات على العناوين باللغة العربية
   • يتم حفظ المشاريع تلقائياً في مجلد reports
        """)
        print("="*70)
