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