from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
# อนุญาต CORS เพื่อให้หน้าเว็บ (Port ต่างๆ) สามารถส่งข้อมูลมาที่ Python ได้
CORS(app)

# ตั้งค่าโฟลเดอร์เก็บไฟล์
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return jsonify({"status": "online", "message": "Assignment Hub Backend is running"})

@app.route('/upload', methods=['POST'])
def upload():
    # 1. เช็คว่ามีไฟล์ส่งมาใน Request หรือไม่
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']

    # 2. เช็คว่าชื่อไฟล์ว่างหรือไม่ (กรณีไม่ได้เลือกไฟล์)
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        # 3. ทำให้ชื่อไฟล์ปลอดภัย (ลบอักขระพิเศษที่อาจเป็นอันตราย)
        filename = secure_filename(file.filename)
        
        # 4. บันทึกไฟล์
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        return jsonify({
            "message": "Upload successful!",
            "filename": filename,
            "path": file_path
        }), 200

if __name__ == '__main__':
    # รันเซิร์ฟเวอร์
    app.run(debug=True, port=5000)