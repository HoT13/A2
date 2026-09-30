Game Company Borrow System (A2 Project)
ระบบจัดการยืม-คืนอุปกรณ์เกมและสื่อบันเทิงส่วนกลางสำหรับบริษัทพัฒนาเกม พัฒนาด้วยภาษา Python 
โดยประยุกต์ใช้แนวคิดการเขียนโปรแกรมเชิงวัตถุ (Object-Oriented Programming - OOP) และโครงสร้างข้อมูล (Data Structures) 
เพื่อควบคุมสต็อกอุปกรณ์และประวัติการยืม-คืนของพนักงานได้อย่างถูกต้อง แม่นยำ📌 System Architecture & Featuresระบบประกอบด้วย 2 คลาสหลัก ดังนี้:
1. Class GamingDeviceคลาสสำหรับจัดเก็บข้อมูลของอุปกรณ์แต่ละชิ้นAttributes: device_id, name, category, stockSpecial Method __str__(): จัดรูปแบบการแสดงผลข้อมูลอุปกรณ์ให้เป็นระเบียบ อ่านง่ายเมื่อเรียกใช้งานผ่าน print()
2. Class GameCompanyBorrowSystemคลาสหลักสำหรับบริหารจัดการคลังและการยืม-คืนInventory Tracking (self.inventory): ใช้ Dictionary เก็บ Object ของอุปกรณ์โดยมี device_id เป็น Key
ช่วยให้การค้นหาและเข้าถึงข้อมูลมีประสิทธิภาพสูง ($O(1)$)Borrow Records (self.borrow_records): ใช้ Nested Dictionary ในรูปแบบ { emp_name: { device_id: quantity } }
เพื่อบันทึกประวัติการยืมของพนักงานแต่ละคนแยกตามรายชิ้นMain Methods:display_inventory(): แสดงรายการอุปกรณ์และจำนวนสต็อกคงเหลือทั้งหมดborrow_device(emp_name, device_id, qty):
ตรวจสอบเงื่อนไข ตัดสต็อก และบันทึกประวัติการยืมreturn_device(emp_name, device_id, qty): ตรวจสอบประวัติ คืนสต็อกเข้าคลัง และอัปเดต/ลบประวัติการยืม


🛡️ Error Handling & Data Validationระบบได้รับการออกแบบให้มีกลไกป้องกันข้อผิดพลาด (Defensive Programming) 
เพื่อป้องกันโปรแกรมหยุดทำงาน (Crash) ดังนี้:ประเภท Errorสาเหตุที่อาจเกิดขึ้นกลไกการจัดการและการแก้ไข (Validation Solution)Invalid Key Errorกรอก device_id ที่ไม่มีอยู่จริงในระบบตรวจสอบด้วยเงื่อนไข 
if device_id not in self.inventory ก่อนเข้าถึงข้อมูลInvalid Quantity Errorระบุจำนวนยืมเป็น 0, ติดลบ หรือยืมเกินจำนวนสต็อกที่มีตรวจสอบ if qty <= 0 และ if device.stock < qty 
ก่อนทำการตัดสต็อกUnmatched Record Errorพยายามคืนอุปกรณ์ที่ตนเองไม่ได้ยืม หรือคืนเกินจำนวนที่ยืมไปตรวจสอบใน borrow_records ระดับพนักงานและรหัสอุปกรณ์ก่อนคืนสต็อก🚀 How to Run & Sample Usage
