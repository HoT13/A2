import json
import os
from typing import Dict, List, Optional, Tuple


class GamingDevice:
    """คลาสสำหรับจัดเก็บข้อมูลอุปกรณ์เกมแต่ละชิ้น (OOP & Encapsulation)"""
    
    def __init__(self, device_id: str, name: str, category: str, stock: int, location: Tuple[int, int] = (0, 0)):
        self.device_id: str = device_id
        self.name: str = name
        self.category: str = category
        self._stock: int = 0
        self.stock = stock  # เรียกใช้งานผ่าน Property Setter เพื่อป้องกันค่าติดลบ
        self.location: Tuple[int, int] = location  # พิกัดตู้เก็บของ (2D Array Index)

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, value: int) -> None:
        if value < 0:
            raise ValueError("❌ Error: จำนวนสต็อกต้องไม่ติดลบ")
        self._stock = value

    def to_dict(self) -> dict:
        """แปลง Object เป็น Dictionary สำหรับบันทึกลงไฟล์ JSON (File I/O)"""
        return {
            "device_id": self.device_id,
            "name": self.name,
            "category": self.category,
            "stock": self.stock,
            "location": list(self.location)
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'GamingDevice':
        """สร้าง Object กลับมาจากข้อมูลในไฟล์ JSON"""
        return cls(
            data["device_id"],
            data["name"],
            data["category"],
            data["stock"],
            tuple(data.get("location", (0, 0)))
        )

    def __str__(self) -> str:
        row, col = self.location
        return (f"[{self.device_id}] {self.name:<24} | "
                f"หมวดหมู่: {self.category:<12} | "
                f"คงเหลือ: {self.stock:>2} ชิ้น | "
                f"พิกัดชั้นวาง [R{row}:C{col}]")


class GameCompanyBorrowSystem:
    """คลาสควบคุมระบบจัดการคลังและประวัติการยืม-คืน (OOP & Data Structures)"""
    
    def __init__(self, storage_rows: int = 3, storage_cols: int = 4, filepath: str = "inventory_data.json"):
        self.filepath: str = filepath
        
        # การประยุกต์ใช้ 2D Array สำหรับจำลองผังตู้เก็บอุปกรณ์ในคลัง (3x4 Grid)
        self.storage_grid: List[List[Optional[str]]] = [
            [None for _ in range(storage_cols)] for _ in range(storage_rows)
        ]
        
        self.inventory: Dict[str, GamingDevice] = {}
        self.borrow_records: Dict[str, Dict[str, int]] = {}
        
        # โหลดข้อมูลจากไฟล์ JSON หากไม่มีจะใช้ค่าเริ่มต้น
        if not self.load_data():
            self._init_default_inventory()

    def _init_default_inventory(self) -> None:
        defaults = [
            GamingDevice("G01", "PlayStation 5 DevKit", "Console", 3, (0, 0)),
            GamingDevice("G02", "Meta Quest 3 VR Headset", "VR Gear", 5, (0, 1)),
            GamingDevice("G03", "Elgato 4K60 Capture Card", "Streaming", 4, (1, 0)),
            GamingDevice("G04", "Steam Deck OLED 1TB", "Handheld", 2, (1, 1))
        ]
        for dev in defaults:
            self.inventory[dev.device_id] = dev
            r, c = dev.location
            self.storage_grid[r][c] = dev.device_id

    def display_inventory(self) -> None:
        """แสดงรายการอุปกรณ์ทั้งหมดในคลัง"""
        print("\n" + "=" * 82)
        print(" 🎮 รายการอุปกรณ์เกมและสื่อบันเทิงส่วนกลาง (Company Inventory)")
        print("=" * 82)
        for device in self.inventory.values():
            print(device)
        print("=" * 82)

    def display_storage_grid(self) -> None:
        """แสดงแผนผังตำแหน่ง 2D Grid ของตู้เก็บอุปกรณ์"""
        print("\n" + "─" * 55)
        print(" 📦 แผนผังตำแหน่งชั้นวางอุปกรณ์ในคลัง (2D Storage Grid)")
        print("─" * 55)
        for r_idx, row in enumerate(self.storage_grid):
            row_str = f"Row {r_idx} | "
            for col_item in row:
                slot = f"[{col_item}]" if col_item else "[  EMPTY  ]"
                row_str += f"{slot:<11} "
            print(row_str)
        print("─" * 55)

    def borrow_device(self, emp_name: str, device_id: str, qty: int) -> str:
        """ฟังก์ชันยืมอุปกรณ์ ตรวจสอบเงื่อนไข ตัดสต็อก และบันทึกประวัติ"""
        if device_id not in self.inventory:
            return "❌ Error: ไม่พบรหัสอุปกรณ์นี้ในคลัง"
        
        device = self.inventory[device_id]
        if qty <= 0:
            return "❌ Error: จำนวนที่ยืมต้องมากกว่า 0"
        if device.stock < qty:
            return f"❌ Error: อุปกรณ์ไม่พอ (ในคลังเหลือเพียง {device.stock} ชิ้น)"

        # ตัดสต็อก
        device.stock -= qty
        
        # บันทึกประวัติพนักงาน (Nested Dictionary)
        if emp_name not in self.borrow_records:
            self.borrow_records[emp_name] = {}
        
        current_borrowed = self.borrow_records[emp_name].get(device_id, 0)
        self.borrow_records[emp_name][device_id] = current_borrowed + qty
        
        self.save_data()  # บันทึกลงไฟล์อัตโนมัติ
        return f"✅ บันทึกสำเร็จ: คุณ '{emp_name}' ยืม {device.name} จำนวน {qty} ชิ้น"

    def return_device(self, emp_name: str, device_id: str, qty: int) -> str:
        """ฟังก์ชันคืนอุปกรณ์ ตรวจสอบประวัติ คืนสต็อก และอัปเดตข้อมูล"""
        if emp_name not in self.borrow_records or device_id not in self.borrow_records[emp_name]:
            return f"❌ Error: ไม่พบประวัติการยืมอุปกรณ์รหัส [{device_id}] ของคุณ '{emp_name}'"
        
        borrowed_qty = self.borrow_records[emp_name][device_id]
        if qty <= 0 or qty > borrowed_qty:
            return f"❌ Error: จำนวนที่คืนไม่ถูกต้อง (ท่านเคยยืมไป {borrowed_qty} ชิ้น)"

        # คืนสต็อกและอัปเดตประวัติ
        self.borrow_records[emp_name][device_id] -= qty
        if self.borrow_records[emp_name][device_id] == 0:
            del self.borrow_records[emp_name][device_id]
            if not self.borrow_records[emp_name]:
                del self.borrow_records[emp_name]
        
        self.inventory[device_id].stock += qty
        self.save_data()  # บันทึกลงไฟล์อัตโนมัติ
        return f"✅ บันทึกสำเร็จ: คุณ '{emp_name}' คืน {self.inventory[device_id].name} จำนวน {qty} ชิ้นเรียบร้อย"

    def display_employee_records(self, emp_name: str) -> None:
        """แสดงรายการอุปกรณ์ที่พนักงานกำลังยืมอยู่"""
        print(f"\n📋 รายการอุปกรณ์ที่กำลังยืมอยู่ของ: คุณ '{emp_name}'")
        if emp_name not in self.borrow_records or not self.borrow_records[emp_name]:
            print("   (ไม่มีรายการยืมค้างในระบบ)")
            return
        
        for dev_id, qty in self.borrow_records[emp_name].items():
            dev_name = self.inventory[dev_id].name if dev_id in self.inventory else "Unknown"
            print(f"   • [{dev_id}] {dev_name:<25} จำนวน {qty} ชิ้น")

    def save_data(self) -> None:
        """บันทึกข้อมูลทั้งหมดลงไฟล์ JSON (File I/O Module)"""
        data = {
            "inventory": {k: v.to_dict() for k, v in self.inventory.items()},
            "borrow_records": self.borrow_records
        }
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"⚠️ บันทึกไฟล์ไม่สำเร็จ: {e}")

    def load_data(self) -> bool:
        """โหลดข้อมูลทั้งหมดจากไฟล์ JSON (File I/O Module)"""
        if not os.path.exists(self.filepath):
            return False
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.inventory = {
                    k: GamingDevice.from_dict(v) 
                    for k, v in data.get("inventory", {}).items()
                }
                self.borrow_records = data.get("borrow_records", {})
                
                for dev in self.inventory.values():
                    r, c = dev.location
                    if r < len(self.storage_grid) and c < len(self.storage_grid[0]):
                        self.storage_grid[r][c] = dev.device_id
                return True
        except (json.JSONDecodeError, KeyError, IOError):
            return False


# --- ส่วนทดสอบการทำงานของโปรแกรม ---
if __name__ == "__main__":
    system = GameCompanyBorrowSystem()
    
    # 1.แสดงรายการคลังและผัง 2D Grid
    system.display_inventory()
    system.display_storage_grid()
    
    # 2.ทดสอบยืมปกติ
    print(system.borrow_device("สมชาย (Dev)", "G01", 1))
    print(system.borrow_device("สมหญิง (QA)", "G02", 2))
    
    # 3.ตรวจสอบประวัติการยืมรายบุคคล
    system.display_employee_records("สมชาย (Dev)")
    
    # 4.ทดสอบยืมเกินสต็อก (ระบบดัก Error ป้องกันพัง)
    print(system.borrow_device("กิตติ (Tester)", "G04", 5))
    
    # 5.ทดสอบคืนอุปกรณ์
    print(system.return_device("สมชาย (Dev)", "G01", 1))
    
    # 6.แสดงคลังหลังอัปเดต
    system.display_inventory()