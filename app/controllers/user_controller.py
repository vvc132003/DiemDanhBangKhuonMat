# /app/controllers/user_controller.py

from flask import Blueprint, render_template
from app.model.user import Users, AttendanceRecords, db
from flask import Flask, render_template, request, jsonify
import cv2
import os
import face_recognition
import pyttsx3
import numpy as np
from datetime import datetime, date, time

user_bp = Blueprint('user', __name__)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


@user_bp.route('/')
def uploadanh():
    return render_template("uploadanh.html")


def doc_van_ban(van_ban):
    # Khởi tạo đối tượng engine
    engine = pyttsx3.init()

    # Sử dụng hàm say để đọc văn bản
    engine.say(van_ban)

    # Chạy và đợi đến khi kết thúc đọc văn bản
    engine.runAndWait()


@user_bp.route('/upload', methods=['POST'])
def upload():
    try:
        # Nhận file ảnh từ yêu cầu POST
        file = request.files['image']
        # Đường dẫn ảnh
        img_folder = "images/"
        # Lưu file ảnh vào thư mục images
        file_path = os.path.join(img_folder, file.filename)
        file.save(file_path)
        # Đọc ảnh từ đường dẫn
        img = cv2.imread(file_path)
        # Chuyển đổi ảnh sang đen trắng (grayscale) để tăng hiệu suất
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Áp dụng bộ lọc Haar để nhận diện khuôn mặt
        faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5)
        if len(faces) == 0:
            van_ban_can_doc = "Không phát hiện khuôn mặt nào"
            # Gọi hàm để đọc văn bản
            return jsonify(doc_van_ban(van_ban_can_doc))
        # Vẽ hình chữ nhật xung quanh các khuôn mặt nhận diện được
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        img_nhandien = "imagehuanluyen/"
        # Tạo tên file mới để tránh trùng lặp
        new_filename = file.filename
        # Lưu ảnh đã nhận diện khuôn mặt với tên mới
        output_path = os.path.join(img_nhandien, new_filename)
        cv2.imwrite(output_path, img)
        # Lấy thông tin từ file ảnh và lưu vào CSDL
        full_name = request.form.get('fullName')
        # Lưu thông tin vào CSDL
        new_user = Users(userName=full_name, image=output_path)
        db.session.add(new_user)
        db.session.commit()
        # Trả về đường dẫn ảnh đã nhận diện khuôn mặt dưới dạng JSON
        return jsonify({'message': 'Face detection successful.', 'image_path': output_path})

    except Exception as e:
        # Trả về thông điệp lỗi dưới dạng JSON nếu có lỗi xảy ra
        return jsonify({'message': f'Error: {str(e)}'})


@user_bp.route('/camera')
def camera():
    return render_template("camera.html")


@user_bp.route('/attendance_page')
def attendance_page():
    # Query the database using the ORM
    attendance_records = AttendanceRecords.query.all()

    # Convert the results to a list of dictionaries
    attendance_data = [
        {'id': record.id, 'name': record.user_id, 'time': record.checkInTime}
        for record in attendance_records
    ]
    return jsonify(attendance_data)


@user_bp.route('/attendance', methods=['POST'])
def attendance():
    try:
        # Nhận file ảnh từ yêu cầu POST
        file = request.files['image']
        # Nhận diện khuôn mặt trong ảnh
        unknown_image = face_recognition.load_image_file(file)
        unknown_face_encoding = face_recognition.face_encodings(unknown_image)
        if not unknown_face_encoding:
            # Nếu không tìm thấy khuôn mặt
            return jsonify({'message': 'Không phát hiện khuôn mặt.'})
        # orm user , lấy dữ liệu
        registered_users = Users.query.all()
        # So sánh với danh sách người dùng đã đăng ký
        for user in registered_users:
            user_id = user.id
            user_name = user.userName
            anhdaidien_value = user.image
            # Tải ảnh đại diện và lấy mã hóa khuôn mặt từ ảnh
            known_image = face_recognition.load_image_file(anhdaidien_value)
            known_face_encoding = face_recognition.face_encodings(known_image)
            if not known_face_encoding:
                # Nếu không tìm thấy khuôn mặt trong ảnh của người dùng đã đăng ký
                return jsonify({'message': 'Không tinmf thấy khuôn mặt.'})
            # Lấy ngày hôm nay
            today = date.today()
            # So sánh các khuôn mặt
            results = face_recognition.compare_faces(known_face_encoding, unknown_face_encoding[0])
            if any(results):
                # Nếu có ít nhất một sự khớp, ghi lại sự kiện điểm danh
                print(f"ID: {user_id}, Họ và tên: {user_name}, Đường dẫn ảnh: {anhdaidien_value}")
                # Kiểm tra xem người dùng đã điểm danh hôm nay chưa
                attendance_record = AttendanceRecords.query.filter(
                    AttendanceRecords.user_id == user_id,
                    AttendanceRecords.checkInTime >= today
                ).first()
                if attendance_record:
                    # Kiểm tra xem đã check-out chưa
                    if attendance_record.check_in_out_type == 'check_out':
                        return jsonify({'message': 'Người dùng đã điểm danh check-out hôm nay.'})
                    else:
                        # 17:00 check_out
                        now = datetime.now().time()
                        checkout_time = time(17, 0)  # 17:00
                        if now > checkout_time:
                            # Nếu chưa check-out, thực hiện check-out
                            attendance_record.check_in_out_type = 'check_out'
                            attendance_record.checkInTime = datetime.now()
                            # Lưu thông tin điểm danh vào CSDL sử dụng ORM
                            db.session.commit()
                            return jsonify({'message': 'Check-out thành công.', 'attendance_record': {
                                'user_id': attendance_record.user_id,
                                'checkInTime': attendance_record.checkInTime,
                                'check_in_out_type': attendance_record.check_in_out_type
                            }})
                        else:
                            return jsonify({'message': 'Chưa đến giờ check-out.'})
                else:
                    # Nếu chưa điểm danh, thực hiện điểm danh check-in
                    new_attendance_checkin = AttendanceRecords(user_id=user_id, checkInTime=datetime.now(),
                                                               check_in_out_type='check_in')
                    # Lưu thông tin điểm danh vào CSDL sử dụng ORM
                    db.session.add(new_attendance_checkin)
                    db.session.commit()
                    return jsonify({'message': 'Check-in thành công.', 'attendance_record': {
                        'user_id': new_attendance_checkin.user_id,
                        'checkInTime': new_attendance_checkin.checkInTime,
                        'check_in_out_type': new_attendance_checkin.check_in_out_type
                    }})

        # Nếu không có sự khớp với người dùng nào
        return jsonify({'message': 'Không có ảnh nào .'})
    except Exception as e:
        # Trả về thông điệp lỗi dưới dạng JSON nếu có lỗi xảy ra
        return jsonify({'message': f'Error: {str(e)}'})
