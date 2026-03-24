# 📚 Assignment Submission System

ยินดีต้อนรับสู่โปรเจคระบบส่งงาน! โปรเจคนี้ใช้สถาปัตยกรรมแบบ Containerized เพื่อให้ทุกคนในทีมสามารถรันโค้ดและฐานข้อมูล (MSSQL) บนเครื่องตัวเองได้เหมือนกัน 100% โดยไม่ต้องติดตั้งโปรแกรมยุ่งยาก

## 🛠️ สิ่งที่ต้องมีในเครื่อง (Prerequisites)
ก่อนเริ่มทำงาน กรุณาตรวจสอบให้แน่ใจว่าเครื่องของคุณติดตั้งโปรแกรมเหล่านี้แล้ว:
1. **Git** - สำหรับจัดการ Source Code
2. **Docker Desktop** - สำหรับรันจำลอง Server และ Database (เปิดโปรแกรมทิ้งไว้ด้วยนะ)
3. **VS Code** (หรือ IDE ที่คุณถนัด)
4. (Option) **SQL Server Management studio** - สำหรับเปิดดูข้อมูลใน Database

---

## 🚀 วิธีการติดตั้งและรันโปรเจค (Getting Started)

### Step 1: Clone โปรเจคลงเครื่อง
เปิด Terminal (หรือ Git Bash) แล้วรันคำสั่ง:
```bash
git clone <ใส่-URL-ของ-GitHub-Repo-ตรงนี้>
cd <ชื่อโฟลเดอร์โปรเจค>
```

### Step 2: รันระบบทั้งหมดด้วยคำสั่งเดียว!
เพื่อให้ง่ายที่สุด จึง seting Infra ทุกอย่างไว้ให้แล้ว คุณแค่รันคำสั่งนี้:
```bash
Bash

docker-compose up -d --build
```
รอประมาณ 1-2 นาที... สิ่งที่คำสั่งนี้ทำให้คุณคือ:

🐘 ดาวน์โหลดและเปิดใช้งาน MSSQL Database

🛠️ สร้าง Database ชื่อ assignment_system ให้อัตโนมัติ (ผ่าน db-init)

🐍 ติดตั้ง Library ทั้งหมดและรัน Python Flask Backend

### Step 3: ตรวจสอบว่าระบบทำงานปกติไหม
เปิด Web Browser แล้วเข้าไปที่:
👉 http://localhost:5000/api/health

ถ้าหน้าเว็บแสดงผลเป็นข้อความ JSON ว่า "status": "success" แสดงว่า Backend และ Database ของคุณพร้อมลุยแล้ว! 🎉

## 🗄️ ข้อมูลสำหรับเชื่อมต่อ Database (สำหรับทีม Backend & Design)
หากคุณต้องการเปิดดูตารางข้อมูล ให้ใช้โปรแกรม SQL Server Management studio เชื่อมต่อด้วยข้อมูลนี้:

- Host: localhost

- Port: 1433

- Database: assignment_system

- Username: sa

- Password: SuperStrongPass123!

(ข้อควรระวัง: อย่าลืมติ๊กตั้งค่า Trust Server Certificate เป็น True ในโปรแกรมด้วย)

## 🛑 วิธีปิดการทำงาน
เมื่อทำงานเสร็จแล้ว หรือต้องการปิดระบบเพื่อประหยัด RAM เครื่อง ให้รันคำสั่ง:
```bash
Bash

docker-compose down
```
(ไม่ต้องห่วง ข้อมูลใน Database จะไม่หายไปไหน เพราะเราผูก Volume เก็บไว้ในเครื่องแล้ว)

## 💡 คำแนะนำเพิ่มเติม (Troubleshooting)
ถ้ามีการอัปเดต Library อัปเดตใหม่ใน Backend:
อย่าลืมรัน docker-compose up -d --build เพื่อให้ระบบสร้าง Container ใหม่รับรู้ Library ใหม่ด้วย
