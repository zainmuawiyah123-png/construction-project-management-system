# أمثلة الاستخدام
# Usage Examples

## مثال 1: إنشاء مشروع جديد برمجياً

```python
from datetime import datetime
from src.core.project_manager import ProjectManager
from src.core.models import WorkItem

# إنشاء مدير المشاريع
pm = ProjectManager()

# إنشاء مشروع جديد
project = pm.create_project(
    name="مشروع البناء الجديد",
    location="الرياض - حي الروضة",
    client_name="شركة العمار للتطوير",
    start_date=datetime(2026, 1, 1),
    end_date=datetime(2026, 12, 31),
    budget=5000000,
    description="مشروع بناء عمارة سكنية 10 طوابق"
)

print(f"تم إنشاء المشروع: {project.name}")
print(f"معرف المشروع: {project.id}")
```

## مثال 2: إضافة بنود عمل يدوياً

```python
from src.core.models import WorkItem

# إنشاء بنود العمل
item1 = WorkItem(
    id="ITEM_001",
    name="تسوية الموقع",
    category="01",
    unit="متر مربع",
    quote_quantity=1000,
    unit_price=50,
    notes="أعمال تسوية أولية للموقع"
)

item2 = WorkItem(
    id="ITEM_002",
    name="حفريات الأساسات",
    category="02",
    unit="متر مكعب",
    quote_quantity=500,
    unit_price=100,
    notes="حفر على عمق 2 متر"
)

# إضافة البنود للمشروع
pm.add_work_item_to_project(project.id, item1)
pm.add_work_item_to_project(project.id, item2)

print(f"تم إضافة {len(project.work_items)} بند عمل")
```

## مثال 3: استيراد البيانات من ملفات Excel

```python
# استيراد بنود العطاء
pm.import_quote_items(
    project.id,
    "data/quote.xlsx"
)
print("تم استيراد بنود العطاء")

# استيراد كميات المخطط
pm.import_plan_items(
    project.id,
    "data/plan.xlsx"
)
print("تم استيراد كميات المخطط")
```

## مثال 4: مقارنة الكميات

```python
from src.core.quantity_manager import QuantityManager

# إنشاء مدير الكميات
qty_manager = QuantityManager(project)

# الحصول على المقارنة الكاملة
comparison = qty_manager.compare_quantities()
print("\nمقارنة الكميات:")
print(comparison)

# الحصول على الإجمالي
totals = qty_manager.get_total_quantities()
print(f"\nإجمالي كمية العطاء: {totals['إجمالي_كمية_العطاء']}")
print(f"إجمالي كمية المخطط: {totals['إجمالي_كمية_المخطط']}")
print(f"الفرق: {totals['إجمالي_الفرق']}")
print(f"نسبة الفرق: {totals['نسبة_الفرق_%']}%")

# البنود الحرجة
critical_items = qty_manager.get_critical_items(threshold=10)
print(f"\nعدد البنود الحرجة: {len(critical_items)}")
for item in critical_items:
    print(f"  - {item['البند']}: {item['نسبة_الفرق_%']}%")
```

## مثال 5: تحليل التكاليف

```python
from src.core.financial_manager import FinancialManager

# إنشاء مدير التقارير المالية
fm = FinancialManager(project)

# حساب التكاليف
costs = fm.calculate_costs()
print("\nتحليل التكاليف:")
print(f"إجمالي تكلفة العطاء: {costs['إجمالي_تكلفة_العطاء']:,.2f}")
print(f"إجمالي التكلفة الفعلية: {costs['إجمالي_التكلفة_الفعلية']:,.2f}")
print(f"الانحراف: {costs['الانحراف']:,.2f}")
print(f"نسبة الانحراف: {costs['نسبة_الانحراف_%']}%")

# التكاليف حسب الفئة
costs_by_category = fm.get_cost_by_category()
print("\nالتكاليف حسب الفئة:")
print(costs_by_category)

# التقرير المالي الشامل
report = fm.generate_financial_report()
print(f"\nحالة المشروع: {report.status}")
print("\nالتوصيات:")
for recommendation in report.recommendations:
    print(f"  {recommendation}")
```

## مثال 6: إنشاء التقارير

```python
from src.reports.report_generator import ReportGenerator

# إنشاء مولد التقارير
report_gen = ReportGenerator(project)

# إنشاء تقرير PDF
pdf_path = report_gen.generate_pdf_report()
print(f"تم إنشاء تقرير PDF: {pdf_path}")

# إنشاء تقرير Excel
excel_path = report_gen.generate_excel_report()
print(f"تم إنشاء تقرير Excel: {excel_path}")

# ملخص تنفيذي
summary = report_gen.generate_executive_summary()
print("\nالملخص التنفيذي:")
print(f"اسم المشروع: {summary['project_name']}")
print(f"الحالة: {summary['status']}")
print(f"عدد البنود الحرجة: {summary['critical_items_count']}")
```

## مثال 7: حفظ المشروع

```python
# حفظ المشروع إلى ملف Excel
pm.save_project_to_excel(project.id)
print(f"تم حفظ المشروع في: reports/project_{project.id}.xlsx")
```

## مثال 8: استرجاع المشاريع

```python
# الحصول على مشروع محدد
project = pm.get_project("PRJ_20260910085741")
if project:
    print(f"المشروع: {project.name}")
    print(f"عدد البنود: {len(project.work_items)}")

# الحصول على جميع المشاريع
all_projects = pm.get_all_projects()
print(f"\nعدد المشاريع المسجلة: {len(all_projects)}")
for proj_id, proj in all_projects.items():
    print(f"  - {proj.name} ({proj_id})")
```

## مثال 9: حلقة العمل الكاملة

```python
# إنشاء مشروع كامل من الصفر

# 1. إنشاء المشروع
pm = ProjectManager()
project = pm.create_project(
    name="مشروع سكني",
    location="جدة",
    client_name="عميل",
    start_date=datetime(2026, 1, 1),
    end_date=datetime(2026, 12, 31)
)

# 2. استيراد البيانات
pm.import_quote_items(project.id, "quote.xlsx")
pm.import_plan_items(project.id, "plan.xlsx")

# 3. تحليل الكميات
qty_manager = QuantityManager(project)
qty_comparison = qty_manager.compare_quantities()

# 4. تحليل التكاليف
fm = FinancialManager(project)
fin_analysis = fm.get_cost_by_category()

# 5. إنشاء التقارير
report_gen = ReportGenerator(project)
report_gen.generate_pdf_report()
report_gen.generate_excel_report()

print("✅ تم إكمال دورة العمل بنجاح")
```

## مثال 10: التعامل مع الأخطاء

```python
try:
    # محاولة استيراد ملف
    pm.import_quote_items(project.id, "nonexistent.xlsx")
except FileNotFoundError:
    print("❌ الملف غير موجود")
except Exception as e:
    print(f"❌ خطأ: {str(e)}")

try:
    # محاولة الحصول على مشروع
    project = pm.get_project("INVALID_ID")
    if not project:
        print("❌ المشروع غير موجود")
except Exception as e:
    print(f"❌ خطأ: {str(e)}")
```

---

هذه أمثلة عملية تغطي جميع وظائف البرنامج الأساسية!
