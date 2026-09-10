"""نماذج البيانات الأساسية"""
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class WorkItem:
    """بند العمل"""
    id: str
    name: str
    category: str  # فئة البند (حفريات، خرسانة، إلخ)
    unit: str  # الوحدة (متر، متر مكعب، إلخ)
    quote_quantity: float = 0.0  # كمية العطاء
    plan_quantity: float = 0.0   # كمية المخطط
    unit_price: float = 0.0      # سعر الوحدة
    total_cost: float = field(default=0.0, init=False)
    notes: str = ""
    
    def __post_init__(self):
        self.total_cost = self.quote_quantity * self.unit_price
    
    def calculate_variance(self) -> float:
        """حساب الفرق بين كميات العطاء والمخطط"""
        return self.quote_quantity - self.plan_quantity
    
    def get_variance_percentage(self) -> float:
        """الحصول على نسبة الفرق"""
        if self.plan_quantity == 0:
            return 0
        return (self.calculate_variance() / self.plan_quantity) * 100

@dataclass
class Project:
    """المشروع"""
    id: str
    name: str
    location: str
    client_name: str
    start_date: datetime
    end_date: datetime
    budget: float = 0.0
    description: str = ""
    work_items: List[WorkItem] = field(default_factory=list)
    
    def add_work_item(self, item: WorkItem):
        """إضافة بند عمل"""
        self.work_items.append(item)
    
    def get_total_cost(self) -> float:
        """الحصول على إجمالي التكلفة"""
        return sum(item.total_cost for item in self.work_items)
    
    def get_total_quote_quantity(self) -> float:
        """الحصول على إجمالي كمية العطاء"""
        return sum(item.quote_quantity for item in self.work_items)
    
    def get_total_plan_quantity(self) -> float:
        """الحصول على إجمالي كمية المخطط"""
        return sum(item.plan_quantity for item in self.work_items)

@dataclass
class FinancialReport:
    """التقرير المالي"""
    project_id: str
    report_date: datetime
    total_quote_cost: float
    total_actual_cost: float
    variance: float = field(default=0.0, init=False)
    variance_percentage: float = field(default=0.0, init=False)
    status: str = ""  # Good, Warning, Critical
    recommendations: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        self.variance = self.total_actual_cost - self.total_quote_cost
        if self.total_quote_cost != 0:
            self.variance_percentage = (self.variance / self.total_quote_cost) * 100
        
        if self.variance_percentage <= 5:
            self.status = "Good"
        elif self.variance_percentage <= 10:
            self.status = "Warning"
        else:
            self.status = "Critical"
