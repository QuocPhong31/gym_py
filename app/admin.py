import hashlib

from flask_admin import Admin
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, validators, ValidationError

from app import app, db
from flask_admin.contrib.sqla import ModelView
from app.models import NhanVien

admin = Admin(app=app, name='Người Quản Trị', template_mode='bootstrap4')

# def validate_min_age(form, field):
#     if form.max_age.data and field.data > form.max_age.data:
#         raise ValidationError('Tuổi tối thiểu không được lớn hơn tuổi tối đa.')
#
# class QuiDinhForm(FlaskForm):
#     min_age = IntegerField('Tuổi tối thiểu', validators=[validators.NumberRange(min=1), validate_min_age])
#     max_age = IntegerField('Tuổi tối đa', validators=[validators.NumberRange(min=1)])
#     si_so = IntegerField('Sĩ số', validators=[validators.NumberRange(min=1)])
#     so_cot_15p = IntegerField('Số cột 15p', validators=[validators.NumberRange(min=1)])
#     so_cot_1tiet = IntegerField('Số cột 1 tiết', validators=[validators.NumberRange(min=1)])
#     so_cot_thi = IntegerField('Số cột thi', validators=[validators.NumberRange(min=1)])
#
# class QuiDinhView(ModelView):
#     form_columns = ['min_age', 'max_age', 'si_so', 'so_cot_15p', 'so_cot_1tiet', 'so_cot_thi']
#     column_list = ['min_age', 'max_age', 'si_so', 'so_cot_15p', 'so_cot_1tiet', 'so_cot_thi']
#     column_labels = {
#         'min_age': 'Tuổi tối thiểu',
#         'max_age': 'Tuổi tối đa',
#         'si_so': 'Sĩ số',
#         'so_cot_15p': 'Số cột 15p',
#         'so_cot_1tiet': 'Số cột 1 tiết',
#         'so_cot_thi': 'Số cột thi'
#     }
#     can_create = False
#     can_delete = False
#     form=QuiDinhForm
#
# class PhongHocForm(FlaskForm):
#     tenPhong = IntegerField('Số phòng', validators=[validators.NumberRange(min=1)])
#
# class PhongHocView(ModelView):
#     column_list = ['tenPhong']
#     column_labels = {'tenPhong':'Số phòng'}
#     form = PhongHocForm
#     column_searchable_list = ['tenPhong']
#
# class MonHocForm(FlaskForm):
#     tenMonHoc = StringField('Môn')
#     soCot15p = IntegerField('Số cột 15p')
#     soCot1Tiet = IntegerField('Số cột 1 tiết')
#     soCotThi = IntegerField('Số cột thi')
#
#     def __init__(self, *args, **kwargs):
#         super(MonHocForm, self).__init__(*args, **kwargs)
#         quy_dinh = QuyDinh.query.first()
#         if quy_dinh: #Kiểm tra quy định có tồn tại hay không
#             self.soCot15p.validators = [validators.NumberRange(min=1, max=quy_dinh.so_cot_15p)]
#             self.soCot1Tiet.validators = [validators.NumberRange(min=1, max=quy_dinh.so_cot_1tiet)]
#             self.soCotThi.validators = [validators.NumberRange(min=1, max=quy_dinh.so_cot_thi)]
#
# class MonHocView(ModelView):
#     column_list = ['tenMonHoc','soCot15p','soCot1Tiet','soCotThi']
#     column_labels = {
#         'tenMonHoc':'Môn',
#         'soCot15p':'Số cột 15p',
#         'soCot1Tiet':'Số cột 1 tiết',
#         'soCotThi':'Số cột thi'
#     }
#     form = MonHocForm
#     column_searchable_list = ['tenMonHoc']

class NhanVienView(ModelView):
    column_labels = {
        'hoTen': 'Họ tên',
        'gioiTinh': 'Giới tính',
        'ngaySinh': 'Ngày sinh',
        'diaChi': 'Địa chỉ',
        'SDT': 'Số điện thoại',
        'eMail': 'Email',
        'taiKhoan': 'Tài khoản',
        'matKhau': 'Mật khẩu',
        'vaiTro': 'Vai trò'
    }
    column_searchable_list = ['hoTen']
    column_filters = ['vaiTro','gioiTinh']

    def on_model_change(self, form, model, is_created):
        if form.matKhau.data:
            model.matKhau = hashlib.md5(form.matKhau.data.encode('utf-8')).hexdigest()
        super(NhanVienView, self).on_model_change(form, model, is_created)

# class GiaoVienView(ModelView):
#     column_list = ['hoTen', 'gioiTinh', 'ngaySinh', 'diaChi', 'SDT', 'eMail', 'monHoc', 'taiKhoan', 'matKhau']
#     form_columns = ['hoTen', 'gioiTinh', 'ngaySinh', 'diaChi', 'SDT', 'eMail', 'taiKhoan', 'matKhau', 'monHoc']
#     column_labels = {
#         'hoTen': 'Họ tên',
#         'gioiTinh': 'Giới tính',
#         'ngaySinh': 'Ngày sinh',
#         'diaChi': 'Địa chỉ',
#         'SDT': 'Số điện thoại',
#         'eMail': 'Email',
#         'monHoc': 'Môn',
#         'taiKhoan': 'Tài khoản ',
#         'matKhau': 'Mật khẩu',
#         'monHoc.tenMonHoc':'Môn học'
#     }
#     column_searchable_list = ['hoTen']
#     column_filters = ['monHoc.tenMonHoc','gioiTinh']
#
#     def on_model_change(self, form, model, is_created):
#         if form.matKhau.data:
#             model.matKhau = hashlib.md5(form.matKhau.data.encode('utf-8')).hexdigest()
#         super(GiaoVienView, self).on_model_change(form, model, is_created)
#
# class GiaoVienDayHocView(ModelView):
#     column_list = ['hoc_ky.namHoc', 'giaoVien', 'giaoVien.monHoc', 'lopDay']
#     column_labels = {
#         'hoc_ky.namHoc': 'Năm học',
#         'giaoVien': 'Giáo Viên',
#         'lopDay': 'Lớp',
#         'giaoVien.monHoc': 'Môn Học',
#         'lopDay.tenLop':'Lớp',
#         'giaoVien.monHoc.tenMonHoc':'Môn',
#         'giaoVien.hoTen':'Họ Tên'
#     }
#     can_create = False
#     can_edit = False
#     column_searchable_list = ['giaoVien.hoTen']
#     column_filters = ['hoc_ky.namHoc', 'lopDay.tenLop','giaoVien.monHoc.tenMonHoc']
#
#     def get_query(self):
#         # Thực hiện sắp xếp năm học giảm dần
#         return (
#             self.session.query(self.model)
#             .join(HocKy, HocKy.idHocKy == self.model.idHocKy)  # JOIN với bảng HocKy
#             .order_by(HocKy.namHoc.desc())  # Sắp xếp theo năm học giảm dần
#         )
#
# class HocSinhView(ModelView):
#     form_columns = ['hocSinhLop', 'hoTen', 'gioiTinh','ngaySinh', 'khoi','diaChi','SDT','eMail']
#     column_list = ['hoTen', 'gioiTinh', 'ngaySinh', 'khoi','diaChi','SDT','eMail','hocSinhLop']
#     column_labels = {
#         'hoTen': 'Họ tên',
#         'gioiTinh': 'Giới tính',
#         'ngaySinh': 'Ngày sinh',
#         'khoi':'Khối',
#         'diaChi':'Địa chỉ',
#         'SDT':'Số điện thoại',
#         'hocSinhLop':'Học lớp',
#         'hocSinhLop.tenLop':'Lớp'
#     }
#     can_create = False
#     column_searchable_list = ['hoTen']
#     column_filters = ['khoi', 'hocSinhLop.tenLop', 'gioiTinh']
#
#     def get_query(self):
#         return self.session.query(self.model).order_by(self.model.khoi.desc())
#
# class DanhSachLopView(ModelView):
#     form_columns = ['tenLop', 'hocKy', 'giaoVienChuNhiem', 'phongHoc', 'siSo', 'active']
#     column_list = ['tenLop', 'hocKy.namHoc', 'giaoVienChuNhiem', 'phongHoc', 'siSoHienTai', 'siSo', 'active']
#     column_labels = {
#         'tenLop':'Lớp',
#         'hocKy.namHoc': 'Năm học',
#         'giaoVienChuNhiem':'Giáo viên chủ nhiệm',
#         'phongHoc':'Phòng',
#         'siSoHienTai':"Sĩ số lớp",
#         'siSo':'Sĩ số tối đa',
#         'active':'Trạng thái',
#         'giaoVienChuNhiem.hoTen':'Giáo Viên Chủ Nhiệm'
#     }
#     can_create = False
#     column_searchable_list = ['giaoVienChuNhiem.hoTen']
#     column_filters = ['tenLop', 'hocKy.namHoc']
#
#     def edit_form(self, obj=None):
#         form = super(DanhSachLopView, self).edit_form(obj)
#         hoc_ky_moi = HocKy.query.order_by(HocKy.namHoc.desc()).limit(2).all()
#
#         if hoc_ky_moi:
#             hk_ids = [hk.idHocKy for hk in hoc_ky_moi]
#             # Lọc các học kỳ trong form chỉ giữ lại 2 học kỳ mới nhất.
#             form.hocKy.query_factory = lambda: HocKy.query.filter(HocKy.idHocKy.in_(hk_ids))
#         return form
#
#     def get_query(self):
#         return self.session.query(self.model).order_by(self.model.active.desc(), self.model.tenLop)
#
# admin.add_view(QuiDinhView(QuyDinh, db.session))
# admin.add_view(PhongHocView(PhongHoc, db.session))
# admin.add_view(MonHocView(MonHoc, db.session))
admin.add_view(NhanVienView(NhanVien, db.session))
# admin.add_view(GiaoVienView(GiaoVien, db.session))
# admin.add_view(GiaoVienDayHocView(GiaoVienDayHoc, db.session))
# admin.add_view(HocSinhView(HocSinh, db.session))
# admin.add_view(DanhSachLopView(DanhSachLop, db.session))

