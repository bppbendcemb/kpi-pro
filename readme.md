my-kpi-project/
├── docker-compose.yml           # ศูนย์รวมการควบคุมทุก Container
├── .env                         # เก็บ Password และ Config ทั้งหมด
├── app/                         # ส่วนของโปรแกรม Python (Flask)
│   ├── Dockerfile               # สูตรสร้าง Image ของ Python
│   ├── requirements.txt         # รายชื่อ Library ที่ต้องใช้
│   ├── main.py                  # ไฟล์หลักสำหรับรัน Server
│   ├── config/                  # ส่วนเชื่อมต่อฐานข้อมูล
│   │   ├── __init__.py
│   │   ├── pg_config.py         # เชื่อมต่อ Postgres (ปลายทาง)
│   │   └── mssql_config.py      # เชื่อมต่อ SQL Server (ต้นทาง)
│   ├── routes/                  # ส่วนควบคุมเส้นทาง (URL)
│   │   ├── __init__.py
│   │   └── data_routes.py
│   ├── services/                # ส่วนคำนวณและย้ายข้อมูล (Logic)
│   │   ├── __init__.py
│   │   └── sync_service.py
│   ├── models/                  # ส่วนนิยามโครงสร้างตารางข้อมูล
│   │   └── kpi_model.py
│   ├── templates/               # ส่วนหน้าตาโปรแกรม (HTML)
│   │   ├── base.html            # โครงสร้างหลัก (Navbar, Footer)
│   │   ├── index.html           # หน้าแรก/หน้า Sync ข้อมูล
│   │   └── dashboard.html       # หน้าแสดงตารางข้อมูล
│   └── static/                  # ส่วนไฟล์เสริม (CSS, JS, Images)
│       ├── css/
│       └── js/
└── data/                        # โฟลเดอร์สำหรับสำรองข้อมูล (Optional)




1. ตรวจสอบการเชื่อมต่อ SSH
เนื่องจากคุณใช้โปรโตคอล SSH ต้องมั่นใจว่าเครื่อง Linux ของคุณได้เพิ่ม SSH Key ลงใน GitHub แล้ว

Bash
ssh -T git@github.com
ถ้าขึ้นว่า Hi [Username]! You've successfully authenticated แสดงว่าใช้งานได้เลยครับ

2. ขั้นตอนการ Push งานขึ้น GitHub (ครั้งแรก)
หากโฟลเดอร์ในเครื่องยังไม่ได้เชื่อมกับ Repository นี้ให้ทำตามลำดับนี้:

Initialize Git:

Bash
git init
เพิ่มไฟล์ทั้งหมด:

Bash
git add .
Commit งาน:

Bash
git commit -m "Initial commit: Flask with Docker and PostgreSQL"
เชื่อมต่อกับ Remote:

Bash
git remote add origin git@github.com:bppbendcemb/kpi-pro.git
ตรวจสอบชื่อ Branch: (GitHub ปัจจุบันมักใช้ main)

Bash
git branch -M main
Push ขึ้น GitHub:

Bash
git push -u origin main
3. ขั้นตอนการ Update งาน (กรณีเคยเชื่อมต่อไว้แล้ว)
หากคุณมีการแก้ไขโค้ดเพิ่มเติมในภายหลัง ให้รัน 3 คำสั่งสั้นๆ นี้ครับ:

Bash
git add .
git commit -m "ระบุข้อความการแก้ไข เช่น update docker-compose"
git push origin main
4. การจัดการไฟล์ที่ไม่ต้องการ (สำคัญมาก)
สำหรับการทำโปรเจกต์ Python/Docker คุณ ไม่ควร นำไฟล์บางอย่างขึ้น GitHub เช่น Password หรือไฟล์ขยะของ Python ให้สร้างไฟล์ชื่อ .gitignore ไว้ในโฟลเดอร์หลัก:

Plaintext
# .gitignore
__pycache__/
*.pyc
.env
venv/
instance/
postgres_data/