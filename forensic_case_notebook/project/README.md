# 🔬 Forensic Scientist's Case Notebook
### AI Classification of Saliva & Sweat Stains

เว็บแอป Streamlit สำหรับโครงงานวิทยาศาสตร์ — ผู้ใช้ Upload รูปคราบ (หลายภาพได้)
แล้วโมเดล **EfficientNetB0** ที่ Train เองจะจำแนกว่าเป็น **Saliva** หรือ **Sweat**
พร้อมค่า **Confidence** ในธีมสมุดบันทึกนักนิติวิทยาศาสตร์ (hand-drawn / doodle)

---

## 📁 โครงสร้างโปรเจกต์

```
project/
├── app.py                    ← หน้าเว็บหลักทั้งหมด (UI, routing, 6 หน้า)
├── model/
│   └── best_model_final.keras   ← โมเดลที่เทรนไว้แล้ว (inference only)
├── utils/
│   ├── model_loader.py       ← โหลด + cache โมเดล
│   └── predictor.py          ← preprocessing + prediction (IMG_SIZE, CLASS_NAMES อยู่ที่นี่)
├── assets/
│   ├── style.css             ← ธีมสมุดบันทึก (สี/ฟอนต์/สแตมป์/โพลารอยด์)
│   └── doodles.py            ← ภาพวาดเส้น SVG (กล้องจุลทรรศน์, DNA, หยดน้ำ ฯลฯ)
├── .streamlit/
│   └── config.toml           ← ธีมสี Streamlit
├── requirements.txt
└── README.md
```

---

## 1. วิธีใส่โมเดล (Model)

ไฟล์ `best_model_final.keras` ถูกวางไว้ใน `model/` เรียบร้อยแล้ว หากต้องการ
เปลี่ยนโมเดลในอนาคต:

1. นำไฟล์ `.keras` ใหม่มาวางแทนที่ใน `model/best_model_final.keras`
   (หรือแก้ path ใน `utils/model_loader.py` ตัวแปร `MODEL_PATH`)
2. ถ้าจำนวนคลาสหรือขนาดภาพเปลี่ยน ให้แก้ในไฟล์ `utils/predictor.py`:
   ```python
   IMG_SIZE = 224
   CLASS_NAMES = ["Saliva", "Sweat"]   # ต้องเรียงลำดับตรงกับตอนเทรน (index 0, 1, ...)
   ```
3. โมเดลนี้ (จากการตรวจสอบไฟล์) มี layer `Rescaling` + `Normalization`
   ฝังอยู่ในตัว EfficientNetB0 อยู่แล้ว → แอปจึงส่งค่าพิกเซล **0–255 แบบดิบ**
   (ไม่ได้หาร 255 เอง) เข้าโมเดลโดยตรง ตาม comment ในไฟล์ `predictor.py`
   ถ้าคุณเทรนโมเดลใหม่ด้วย preprocessing แบบอื่น ให้แก้ฟังก์ชัน
   `preprocess_image()` ในไฟล์เดียวกันให้ตรงกัน

> แอปนี้ทำ **Inference เท่านั้น** — โค้ดไม่มีส่วนใดที่ train หรือแก้ไขน้ำหนักโมเดล

---

## 2. วิธีติดตั้ง (Install)

ต้องมี Python 3.10–3.12 ในเครื่อง จากนั้น:

```bash
cd project
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

---

## 3. วิธี Run Local

```bash
streamlit run app.py
```

จากนั้นเบราว์เซอร์จะเปิดที่ `http://localhost:8501` โดยอัตโนมัติ
(ถ้าไม่เปิดเอง ให้เปิดลิงก์นี้เอง)

**Flow การใช้งาน:**
`OPEN CASE FILE → COLLECT EVIDENCE → UPLOAD IMAGES → EXAMINE EVIDENCE → AI ANALYSIS → CASE FINDINGS → CASE CLOSED`

---

## 4. วิธี Deploy บน Streamlit Community Cloud

### ขั้นตอนที่ 1 — สร้าง GitHub Repository
1. สร้าง repo ใหม่บน GitHub (public หรือ private ก็ได้ เช่น `forensic-case-notebook`)
2. อัปโหลดไฟล์ทั้งหมดในโฟลเดอร์ `project/` ขึ้น repo นี้ (ทั้ง `app.py`, `model/`,
   `utils/`, `assets/`, `.streamlit/`, `requirements.txt`)

   ตัวอย่างคำสั่ง:
   ```bash
   cd project
   git init
   git add .
   git commit -m "Forensic Case Notebook - initial commit"
   git branch -M main
   git remote add origin https://github.com/<username>/forensic-case-notebook.git
   git push -u origin main
   ```

   > **หมายเหตุเรื่องขนาดไฟล์:** โมเดล `.keras` มีขนาดประมาณ 16-17 MB ซึ่ง GitHub
   > ปกติรับได้สบาย (limit คือ 100 MB ต่อไฟล์) ไม่ต้องใช้ Git LFS

### ขั้นตอนที่ 2 — Deploy บน Streamlit Cloud
1. ไปที่ [share.streamlit.io](https://share.streamlit.io) แล้ว Sign in ด้วย GitHub
2. กด **"New app"**
3. เลือก Repository, Branch (`main`), และ Main file path เป็น `app.py`
4. กด **"Deploy!"** แล้วรอ 2-5 นาที (รอบแรกจะช้าหน่อยเพราะต้องติดตั้ง TensorFlow)

### ขั้นตอนที่ 3 — ตรวจสอบ
- เปิด URL ที่ได้ (รูปแบบ `https://<app-name>-<random>.streamlit.app`)
- ลอง Upload รูปทดสอบ 1-2 ภาพ เพื่อยืนยันว่าโมเดลโหลดและทำนายได้

> **Tip:** ถ้า Deploy แล้วเจอปัญหาเรื่อง memory/build time เกิน (free tier มี
> RAM จำกัด ~1GB) ให้ลองแปลงโมเดลเป็น `.tflite` เพื่อลดขนาด runtime หรือ
> ปิดฟีเจอร์ data augmentation layers ที่ไม่จำเป็นตอน inference ก็ได้

---

## 5. วิธีสร้าง URL สำหรับเปิดบน iPad / มือถือ

URL ที่ได้จาก Streamlit Cloud (เช่น `https://forensic-case-notebook.streamlit.app`)
**ใช้ได้ทันทีบนทุกอุปกรณ์** (คอมพิวเตอร์ / iPad / มือถือ) เพราะเป็นเว็บแอปที่รองรับ
Responsive Design อยู่แล้ว เพียงเปิด Safari / Chrome บน iPad หรือมือถือแล้ววาง
URL นี้ลงไปได้เลย ไม่ต้องติดตั้งอะไรเพิ่ม

**เคล็ดลับสำหรับวันนำเสนอ:** เพิ่มเว็บนี้ลงหน้าจอ Home ของ iPad ได้โดย
กดปุ่ม Share → "Add to Home Screen" เพื่อให้เปิดได้เหมือนแอปจริง

---

## 6. วิธีสร้าง QR Code สำหรับ URL

วิธีที่ง่ายที่สุด (ไม่ต้องติดตั้งอะไร):

1. เปิดเว็บ [qr-code-generator.com](https://www.qr-code-generator.com) หรือ
   [qrcode-monkey.com](https://www.qrcode-monkey.com)
2. วาง URL ของแอป (จาก Streamlit Cloud) ลงในช่อง
3. ปรับแต่งสี/ดีไซน์ให้เข้าธีม cream/blue/mint ของโปรเจกต์ได้ตามใจ (ใส่โลโก้
   กล้องจุลทรรศน์หรือ DNA ตรงกลาง QR เพื่อความสวยงาม)
4. ดาวน์โหลดเป็นไฟล์ PNG/SVG แล้วนำไปพิมพ์ติดบอร์ดโครงงานได้เลย

หรือถ้าต้องการสร้างด้วยโค้ด Python (ทำครั้งเดียวตอนเตรียมงาน ไม่ต้องอยู่ในแอป):

```bash
pip install qrcode[pil]
python -c "
import qrcode
img = qrcode.make('https://<your-app-url>.streamlit.app')
img.save('case_notebook_qr.png')
"
```

---

## 🎨 เกี่ยวกับดีไซน์

ธีม **"Forensic Scientist's Case Notebook"** ออกแบบให้ผู้ใช้รู้สึกเหมือนเปิด
แฟ้มคดีจริง มีองค์ประกอบ: กระดาษสีครีม เส้นบรรทัดสมุด เทปกาว คลิปหนีบกระดาษ
รูปแบบโพลารอยด์สำหรับรูปหลักฐาน และตราประทับ "CASE ANALYZED" / "CLASSIFIED" /
"CASE CLOSED" ทั้งหมดสร้างด้วย CSS + SVG ล้วน ๆ ไม่ต้องพึ่งไฟล์รูปภาพภายนอก
จึง deploy ได้เบาและเร็ว

## ⚠️ ข้อควรทราบ

- โมเดลนี้ทำ **Inference เท่านั้น** ไม่มีการ train หรือ fine-tune ใด ๆ ในแอปนี้
- ผลการจำแนกจาก AI เป็นเพียงการสาธิตสำหรับโครงงานวิทยาศาสตร์ ไม่ใช่การวิเคราะห์
  ทางนิติวิทยาศาสตร์ที่ใช้งานได้จริงในทางกฎหมาย
