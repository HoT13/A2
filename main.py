class GamingDevice:
    def __init__(self, device_id, name, category, stock):
        self.device_id = device_id
        self.name = name
        self.category = category
        self.stock = stock

    def __str__(self):
        return f"[{self.device_id}] {self.name:<25} | หมวดหมู่: {self.category:<15} | คงเหลือ: {self.stock} ชิ้น"

class GameCompanyBorrowSystem:
    def __init__(self):
        # คลังอุปกรณ์สื่อบันเทิงและเกม
        self.inventory = {
            "G01": GamingDevice("G01", "PlayStation 5 DevKit", "Console", 3),
            "G02": GamingDevice("G02", "Meta Quest 3 VR Headset", "VR Gear", 5),
            "G03": GamingDevice("G03", "Elgato 4K60 Capture Card", "Streaming", 4),
            "G04": GamingDevice("G04", "Steam Deck OLED 1TB", "Handheld", 2)
        }
        # บันทึกการยืม {emp_name: {device_id: quantity}}
        self.borrow_records = {}

    def display_inventory(self):
        print("\n" + "="*65)
        print(" 🎮 รายการอุปกรณ์เกมและสื่อบันเทิงส่วนกลาง ")
        print("="*65)
        for device in self.inventory.values():
            print(device)
        print("="*65)

    def borrow_device(self, emp_name, device_id, qty):
        if device_id not in self.inventory:
            return "❌ Error: ไม่พบรหัสอุปกรณ์นี้ในคลัง"
        
        device = self.inventory[device_id]
        if qty <= 0:
            return "❌ Error: จำนวนที่ยืมต้องมากกว่า 0"
        if device.stock < qty:
            return f"❌ Error: อุปกรณ์ไม่พอ (ในคลังเหลือเพียง {device.stock} ชิ้น)"

        # ตัดสต๊อก
        device.stock -= qty
        
        # บันทึกประวัติพนักงาน
        if emp_name not in self.borrow_records:
            self.borrow_records[emp_name] = {}
        
        current_borrowed = self.borrow_records[emp_name].get(device_id, 0)
        self.borrow_records[emp_name][device_id] = current_borrowed + qty
        
        return f"✅ บันทึกสำเร็จ: คุณ '{emp_name}' ยืม {device.name} จำนวน {qty} ชิ้น"

    def return_device(self, emp_name, device_id, qty):
        # ตรวจสอบประวัติการยืม
        if emp_name not in self.borrow_records or device_id not in self.borrow_records[emp_name]:
            return f"❌ Error: ไม่พบประวัติการยืมอุปกรณ์รหัส [{device_id}] ของคุณ '{emp_name}'"
        
        borrowed_qty = self.borrow_records[emp_name][device_id]
        if qty <= 0 or qty > borrowed_qty:
            return f"❌ Error: จำนวนที่คืนไม่ถูกต้อง (ท่านเคยยืมไป {borrowed_qty} ชิ้น)"

        # คืนสต๊อกและอัปเดตประวัติ
        self.borrow_records[emp_name][device_id] -= qty
        if self.borrow_records[emp_name][device_id] == 0:
            del self.borrow_records[emp_name][device_id]
        
        self.inventory[device_id].stock += qty
        return f"✅ บันทึกสำเร็จ: คุณ '{emp_name}' คืน {self.inventory[device_id].name} จำนวน {qty} ชิ้นเรียบร้อย"

# --- ทดสอบการทำงานของระบบ ---
if __name__ == "__main__":
    system = GameCompanyBorrowSystem()
    
    system.display_inventory()
    
    # ทดสอบยืมปกติ
    print(system.borrow_device("สมชาย (Dev)", "G01", 1))
    print(system.borrow_device("สมหญิง (QA)", "G02", 2))
    
    # ทดสอบยืมเกินสต๊อก (จะแสดง Error)
    print(system.borrow_device("กิตติ (Tester)", "G04", 5))
    
    system.display_inventory()
    
    # ทดสอบคืนอุปกรณ์
    print(system.return_device("สมชาย (Dev)", "G01", 1))
    
    # ทดสอบเนียนคืนของที่ไม่ได้ยืม (จะแสดง Error)
    print(system.return_device("สมชาย (Dev)", "G03", 1))
    
    system.display_inventory()