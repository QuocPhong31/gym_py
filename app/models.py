from datetime import date
from email.policy import default

from app import db, app
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, BOOLEAN, Date, Enum, UniqueConstraint
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum as RoleEnum, unique
from flask_login import UserMixin
import hashlib
from sqlalchemy.orm import relationship, Relationship


class UserRole(RoleEnum):
    NGUOIQUANTRI = 1
    THUNGAN = 2
    LETAN = 3

# class Khoi(RoleEnum):
#     KHOI10 = 1
#     KHOI11 = 2
#     KHOI12 = 3
#
# class MonHoc(db.Model):
#     __tablename__ = 'monhoc'
#     idMonHoc = Column(Integer, primary_key=True, autoincrement=True)
#     tenMonHoc = Column(String(50), unique=True, nullable=False)
#     soCot15p = Column(Integer, nullable=False)
#     soCot1Tiet = Column(Integer, nullable=False)
#     soCotThi = Column(Integer, nullable=False)
#     giaoViens = relationship('GiaoVien',backref='monhoc', lazy=True)
#
#     def __str__(self):
#         return self.tenMonHoc
#
# class HocKy(db.Model):
#     idHocKy = Column(Integer, primary_key=True, autoincrement=True)
#     namHoc = Column(String(20), nullable=False)
#     hocKy = Column(String(20), nullable=False)
#
#     def __str__(self):
#         return f"{self.namHoc} - {self.hocKy}"
#
#     def get_HocKy(self):
#         return self.hocKy
#
#     def get_NamHoc(self):
#         return self.namHoc

class User(db.Model, UserMixin):
    __tablename__ = 'users'  # Tạo bảng User trong DB

    id = Column(Integer, primary_key=True, autoincrement=True)
    hoTen = Column(String(50), nullable=False)
    gioiTinh = Column(Boolean, nullable=False)
    ngaySinh = Column(Date, nullable=False)
    diaChi = Column(String(255), nullable=False)
    SDT = Column(String(20), unique=True, nullable=False)
    eMail = Column(String(255), unique=True, nullable=False)
    taiKhoan = Column(String(50), unique=True, nullable=False)
    matKhau = Column(String(255), nullable=False)

    def __str__(self):
        return self.hoTen

    def get_id(self):
        return str(self.id)

    def get_taiKhoan(self):
        return self.taiKhoan

    def set_password(self, password):
        self.matKhau = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.matKhau, password)


class NhanVien(User):
    __tablename__ = 'nhanvien'  # Tạo bảng NhanVien trong DB, không tạo bảng User

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)  # Khóa ngoại trỏ tới bảng users
    vaiTro = Column(Enum(UserRole))

    def get_VaiTro(self):
        return self.vaiTro


# class GiaoVien(User):
#     __tablename__ = 'giaovien'  # Tạo bảng GiaoVien trong DB, không tạo bảng User
#
#     id = Column(Integer, ForeignKey('users.id'), primary_key=True)  # Khóa ngoại trỏ tới bảng users
#     idMonHoc = Column(Integer, ForeignKey('monhoc.idMonHoc'), nullable=True)
#
#     monHoc = relationship('MonHoc', backref='giaovien')
#
# class GiaoVienDayHoc(db.Model):
#     __tablename__ = 'giao_vien_day_hoc'
#     idGiaoVienDayHoc = Column(Integer, primary_key=True,autoincrement=True)
#     idGiaoVien = Column(Integer, ForeignKey('giaovien.id'),nullable=True)
#     idHocKy = Column(Integer, ForeignKey(HocKy.idHocKy),nullable=True)
#     idDsLop = Column(Integer, ForeignKey('danh_sach_lop.maDsLop', ondelete="CASCADE"), nullable=True)
#
#     # Quan hệ với DanhSachLop
#     hoc_ky = relationship('HocKy', backref='giaoVienDayHoc')
#     giaoVien = relationship(GiaoVien, backref="dayLop")
#     lopDay = relationship('DanhSachLop', backref='giaoVienPhuTrach')
#
#
# class HocSinh(db.Model):
#     idHocSinh = Column(Integer, primary_key=True, autoincrement=True)
#     hoTen = Column(String(50), nullable=False)
#     gioiTinh = Column(Boolean, nullable=False)
#     ngaySinh = Column(Date, nullable=False)
#     khoi = Column(String(50), nullable=False)
#     diaChi = Column(String(255), nullable=False)
#     SDT = Column(String(20), nullable=False)
#     eMail = Column(String(255), unique=True, nullable=False)
#     maDsLop = Column(Integer, ForeignKey('danh_sach_lop.maDsLop'), nullable=True)
#
#     hocSinhLop = relationship('DanhSachLop', backref='danhSachHocSinh')
#     bang_diem = relationship('BangDiem', backref='hoc_sinh', lazy=True)  # Thêm quan hệ này
#
# class BangDiem(db.Model):
#     __tablename__ = 'bang_diem'
#
#     idBangDiem = Column(Integer, primary_key=True)
#     hocSinh_id = Column(Integer, ForeignKey('hoc_sinh.idHocSinh'), nullable=False)
#     loai_diem = Column(String(20))  # Ví dụ: "15p", "1_tiet", "thi"
#     diem = Column(Float)
#     monHoc_id = Column(Integer, ForeignKey('monhoc.idMonHoc'), nullable=False)  # Môn học
#     giaoVien_id = Column(Integer, ForeignKey('giaovien.id'), nullable=False)  # Giáo viên
#     hocKy_id = Column(Integer, ForeignKey('hoc_ky.idHocKy'), nullable=False)  # Học kỳ
#
#     mon_hoc = relationship('MonHoc', backref='bang_diem')
#     giao_vien = relationship('GiaoVien', backref='bang_diem')
#     hoc_ky = relationship('HocKy', backref='bang_diem')
#
# class BangDiemTB(db.Model):
#     __tablename__ = 'bang_diem_tb'
#
#     idBangDiemTB = Column(Integer, primary_key=True, autoincrement=True)
#     hocSinh_id = Column(Integer, ForeignKey('hoc_sinh.idHocSinh'), nullable=False)
#     hocKy_id = Column(Integer, ForeignKey('hoc_ky.idHocKy'), nullable=False)
#     diem_trung_binh = Column(Float, nullable=False)
#
#     hoc_sinh = relationship('HocSinh', backref='bang_diem_tb')
#     hoc_ky = relationship('HocKy', backref='bang_diem_tb')
#
#     def __str__(self):
#         return f"HS: {self.hocSinh_id}, HK: {self.hocKy_id}, TB: {self.diem_trung_binh}"
#
#
# class PhongHoc(db.Model):
#     idPhongHoc = Column(Integer, primary_key=True, autoincrement=True)
#     tenPhong = Column(String(50), unique=True, nullable=False)  # VD: "Phòng 101", "Phòng 202"
#
#     def __str__(self):
#         return self.tenPhong
#
#
# class DanhSachLop(db.Model):
#     maDsLop = Column(Integer, primary_key=True, autoincrement=True)
#     idPhongHoc = Column(Integer, ForeignKey(PhongHoc.idPhongHoc),unique=True, nullable=True)
#     tenLop = Column(String(50),nullable=True)
#     khoi = Column(String(50), nullable=False)
#     giaoVienChuNhiem_id = Column(Integer, ForeignKey(GiaoVien.id), nullable=True)
#     siSoHienTai = Column(Integer, nullable=False)
#     siSo = Column(Integer, nullable=False)
#     hocKy_id = Column(Integer, ForeignKey(HocKy.idHocKy), nullable=False)
#     active = Column(Boolean, default=True)
#
#     giaoVienChuNhiem = relationship(GiaoVien, backref='lop')
#     hocKy = relationship(HocKy, backref='lop')
#     hocSinhs = relationship(HocSinh, backref='danhSachLop', lazy=True)
#     phongHoc = relationship(PhongHoc, backref='danhSachLops')
#
#     # Thêm quan hệ với GiaoVienChuNhiem
#     giaoVienDayHocs = relationship(
#         'GiaoVienDayHoc',
#         backref='lop',
#         cascade="all, delete",
#         lazy=True
#     )
#
#     def __str__(self):
#         return f"{self.tenLop}"
#
# class QuyDinh(db.Model):
#     idQuyDinh = Column(Integer, primary_key=True, autoincrement=True)
#     min_age = Column(Integer)
#     max_age = Column(Integer)
#     si_so = Column(Integer)
#     so_cot_15p = Column(Integer)
#     so_cot_1tiet = Column(Integer)
#     so_cot_thi=Column(Integer)

if __name__== '__main__':
    with app.app_context():
        db.create_all()

        u = NhanVien(hoTen="Nguyễn Đăng Khôi", gioiTinh=True, ngaySinh=date(2004, 2, 21),
                     diaChi="Thành phố Hồ Chí Minh",SDT="0762464676",eMail="khoi123@gmail.com",
                     taiKhoan='admin', matKhau=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                     vaiTro=UserRole.NGUOIQUANTRI)
        db.session.add(u)
        # db.session.commit()


        # Tạo nhân viên
        nv = NhanVien(
            hoTen="Trần Quốc Phong",
            gioiTinh=True,
            ngaySinh=date(2004, 11, 24),
            diaChi="Thành phố Hồ Chí Minh",
            SDT="0799773010",
            eMail="toquocphong123@gmail.com",
            vaiTro=UserRole.THUNGAN,
            taiKhoan="quocphong",
            matKhau=str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        )
        db.session.add(nv)
        db.session.commit()
