from random import choice

from flask import render_template, request, redirect, session, flash, url_for
from sqlalchemy import and_, Null
from app import app, db, dao, login
from datetime import date, datetime

# from app.dao import get_class_by_id
from app.models import UserRole
from flask_login import login_user, logout_user, current_user, login_required

app.secret_key = 'secret_key'  # Khóa bảo mật cho session

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login_process():
    thong_bao = None
    flag = False
    if request.method.__eq__('POST'):
        taiKhoan = request.form.get('taiKhoan')
        matKhau = request.form['matKhau']
        nv = dao.auth_nhan_vien(taikhoan=taiKhoan, matkhau=matKhau)
        if nv:
            flag=True
            if nv.get_VaiTro() == UserRole.THUNGAN:
                login_user(nv)
                return redirect(f'/nhan-vien/{taiKhoan}')
            elif nv.get_VaiTro() == UserRole.NGUOIQUANTRI:
                login_user(nv)
                return redirect('/admin')
        if not flag:
            gv = dao.auth_giao_vien(taikhoan=taiKhoan, matkhau=matKhau)
            if gv:
                login_user(gv)
                return redirect(f'/giao-vien/{taiKhoan}')
        thong_bao = "Sai tài khoản/ mật khẩu"
    return render_template('login.html', err_msg=thong_bao)

@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)

@app.route('/nhan-vien/<taikhoan>')
def thong_tin_nhan_vien(taikhoan):
    return render_template('nhan_vien.html',taikhoan=taikhoan)

@app.route('/giao-vien/<taikhoan>')
def thong_tin_giao_vien(taikhoan):
    gv = dao.get_gv_by_id(current_user.id)
    return render_template('giao_vien.html', taikhoan=taikhoan, giaovien=gv)

@app.route('/logout', methods=['get', 'post'])
def logout_process():
    logout_user()
    return redirect('/login')

@app.route('/nhan-vien/<taikhoan>/nhap-ho-so', methods=['POST'])
def kiem_tra_tuoi(taikhoan):
    session['taikhoan'] = taikhoan
    quy_dinh = dao.get_quy_dinh()
    min_age = quy_dinh.min_age
    max_age = quy_dinh.max_age
    ngay_sinh = request.form.get('ngaySinh')
    if ngay_sinh:
        ngay_sinh = datetime.strptime(ngay_sinh, "%Y-%m-%d").date()
        hom_nay = date.today()
        tuoi = hom_nay.year - ngay_sinh.year
        if min_age <= tuoi <= max_age:
            flash("Tuổi hợp lệ. Hãy nhập thông tin chi tiết.", "success")
            return render_template('nhap_thong_tin_hoc_sinh.html', ngay_sinh=ngay_sinh, taikhoan=taikhoan)
        else:
            flash(f"Tuổi không phù hợp: {tuoi} tuổi!!!", "warning")
            return redirect(f'/nhan-vien/{taikhoan}')
    return "Không nhận được thông tin ngày sinh!"

# @app.route('/nhan-vien/<taikhoan>/luu-hoc-sinh', methods=['POST'])
# def luu_hoc_sinh(taikhoan):
#     try:
#         taikhoan = session.get('taikhoan')
#         so_dien_thoai = request.form.get('soDienThoai')
#         ngay_sinh = request.form.get('ngaySinh')
#         if len(so_dien_thoai) != 10 or not so_dien_thoai.isdigit():
#             flash("Số điện thoại không hợp lệ. Vui lòng nhập đúng 10 số.", "error")
#             return render_template('nhap_thong_tin_hoc_sinh.html', ngay_sinh=ngay_sinh, taikhoan=taikhoan)
#         ho_ten = request.form.get('hoTen')
#         gioi_tinh = request.form.get('gioiTinh')  # Nam = 1, Nữ = 0
#         khoi = request.form.get('khoi')
#         dia_chi = request.form.get('diaChi')
#         email = request.form.get('email')
#         # Tạo đối tượng học sinh
#         hoc_sinh = HocSinh(
#             hoTen=ho_ten,
#             gioiTinh=(gioi_tinh == '1'),
#             ngaySinh=datetime.strptime(ngay_sinh, "%Y-%m-%d").date(),
#             khoi=khoi,
#             diaChi=dia_chi,
#             SDT=so_dien_thoai,
#             eMail=email,
#             maDsLop=None
#         )
#         db.session.add(hoc_sinh)
#         db.session.commit()
#         flash("Học sinh đã được lưu thành công!", "success")
#         return redirect(f"/nhan-vien/{taikhoan}")
#     except Exception as e:
#         db.session.rollback()
#         flash(f"Email đã tồn tại. Vui lòng nhập lại!", "error")
#         return render_template('nhap_thong_tin_hoc_sinh.html', ngay_sinh=ngay_sinh, taikhoan=taikhoan)
#
# @app.route('/nhan-vien/<taikhoan>/danh-sach-lop')
# def show_ds_lop(taikhoan):
#     dsLop = DanhSachLop.query.filter(DanhSachLop.active == True)
#     return render_template('danh_sach_lop.html', danh_sach_lop=dsLop, taikhoan=taikhoan)
#
# @app.route('/tao-danh-sach-lop')
# def create_auto_classes():
#     try:
#         quy_dinh = dao.get_quy_dinh()
#         hoc_ky = HocKy.query.filter(HocKy.hocKy == "1").order_by(HocKy.idHocKy.desc()).first()
#         students = HocSinh.query.filter(HocSinh.maDsLop == None, HocSinh.khoi!="").all()
#         if not students:
#             flash("Không có học sinh nào để tạo lớp!", "error")
#             return redirect('/admin')
#         grade_groups = {
#             "10": [],
#             "11": [],
#             "12": []
#         }
#         for student in students:
#             if student.khoi == "Khối 10":
#                 grade_groups["10"].append(student)
#             elif student.khoi == "Khối 11":
#                 grade_groups["11"].append(student)
#             elif student.khoi == "Khối 12":
#                 grade_groups["12"].append(student)
#         ds_giao_vien = dao.get_ds_gv()
#         giao_vien_by_mon = {mon.idMonHoc: [] for mon in MonHoc.query.all()}
#         for gv in ds_giao_vien:
#             giao_vien_by_mon[gv.idMonHoc].append(gv)
#
#         for khoi, group_students in grade_groups.items():
#             siSo = quy_dinh.si_so
#             for i in range(0, len(group_students), siSo):
#                 class_students = group_students[i:i + siSo]
#                 gv_chu_nhiem = choice(ds_giao_vien)
#                 lop_moi = DanhSachLop(
#                     tenLop=f"{khoi}A{i + 1}",
#                     khoi = f"Khối {khoi}",
#                     giaoVienChuNhiem_id=gv_chu_nhiem.id,
#                     siSoHienTai=len(class_students),
#                     siSo=siSo,
#                     hocKy_id=hoc_ky.idHocKy
#                 )
#                 db.session.add(lop_moi)
#                 db.session.commit()
#
#                 giao_vien_day_hoc = GiaoVienDayHoc(
#                     idGiaoVien=gv_chu_nhiem.id,
#                     idDsLop=lop_moi.maDsLop,
#                     idHocKy=hoc_ky.idHocKy
#                 )
#                 db.session.add(giao_vien_day_hoc)
#
#                 mon_con_lai = [mon for mon in MonHoc.query.all() if mon.idMonHoc != gv_chu_nhiem.idMonHoc]
#                 # Gán giáo viên cho các môn học còn thiếu
#                 for mon in mon_con_lai:
#                     ds_gv_theo_mon = giao_vien_by_mon[mon.idMonHoc]
#                     if ds_gv_theo_mon:
#                         gv = choice(ds_gv_theo_mon)
#                         lop_moi.giaoVienDayHocs.append(GiaoVienDayHoc(
#                             idGiaoVien=gv.id,
#                             idDsLop=lop_moi.maDsLop,
#                             idHocKy = hoc_ky.idHocKy
#                         ))
#                 ds_giao_vien.remove(gv_chu_nhiem)
#                 for student in class_students:
#                     student.maDsLop = lop_moi.maDsLop
#                     db.session.add(student)
#         db.session.commit()
#         flash("Danh sách lớp đã được tạo thành công!", "success")
#     except Exception as e:
#         db.session.rollback()
#         flash(f"Lỗi khi tạo danh sách lớp: {str(e)}", "error")
#     return redirect('/admin')
#
# @app.route('/nhan-vien/<taikhoan>/danh-sach-lop/sua/<int:id>', methods=['GET', 'POST'])
# def sua_ds_lop(id,taikhoan):
#     session['taikhoan'] = taikhoan
#     lop = dao.get_class_by_id(id)
#     list_hs = dao.get_ds_hs_by_ma_lop(lop.maDsLop)
#     # Lấy danh sách phòng học chưa được chọn
#     list_phong = dao.get_ds_phong()
#     list_phong_da_chon = {p.idPhongHoc for p in DanhSachLop.query.filter(DanhSachLop.idPhongHoc != None)}
#     list_phong = [phong for phong in list_phong if
#                   phong.idPhongHoc not in list_phong_da_chon or phong.idPhongHoc == lop.idPhongHoc]
#     if request.method == 'POST':
#         try:
#             lop.tenLop = request.form.get("tenLop")
#             lop.idPhongHoc = int(request.form.get("phongHoc"))
#             db.session.commit()
#             flash("Cập nhật thông tin lớp thành công", "success")
#             return redirect(f'/nhan-vien/{taikhoan}/danh-sach-lop')
#         except Exception as e:
#             db.session.rollback()
#             flash(f"Lỗi khi lưu dữ liệu: {str(e)}", "danger")
#             return redirect(request.url)
#     return render_template('sua_lop.html', lop=lop, danh_sach_phong=list_phong, danh_sach_hoc_sinh=list_hs,taikhoan=taikhoan)
#
# @app.route('/them-hoc-sinh/<int:id>', methods=['GET', 'POST'])
# def them_hoc_sinh(id):
#     taikhoan = session.get('taikhoan')
#     lop = dao.get_class_by_id(id)
#     if lop.siSoHienTai == lop.siSo:
#         flash("Sĩ số hiện tại đã bằng sĩ số lớp!", "danger")
#         return redirect(f'/nhan-vien/{taikhoan}/danh-sach-lop/sua/{lop.maDsLop}')
#     ds_hs_chua_lop = HocSinh.query.filter(HocSinh.maDsLop==None , HocSinh.khoi==lop.khoi)
#     if request.method == 'POST':
#         try:
#             list_hs_ids = request.form.getlist("hocSinh")
#             if not list_hs_ids:
#                 flash("Vui lòng chọn ít nhất một học sinh!", "danger")
#                 return redirect(request.url)
#
#             si_so_hien_tai = HocSinh.query.filter(HocSinh.maDsLop == id).count()
#             so_hoc_sinh_them = len(list_hs_ids)
#             si_so_moi = si_so_hien_tai + so_hoc_sinh_them
#
#             if si_so_moi > lop.siSo:
#                 flash("Không thể thêm vì vượt quá sĩ số lớp!", "danger")
#                 return redirect(request.url)
#             else:
#                 lop.siSoHienTai = si_so_moi
#
#             for hoc_sinh_id in list_hs_ids:
#                 hoc_sinh = dao.get_hs_by_id(hoc_sinh_id)
#                 hoc_sinh.maDsLop = id
#                 db.session.add(hoc_sinh)
#             db.session.commit()
#             flash(f"Đã thêm {so_hoc_sinh_them} học sinh vào lớp!", "success")
#             return redirect(f'/nhan-vien/{taikhoan}/danh-sach-lop/sua/{id}')
#         except Exception as e:
#             db.session.rollback()
#             flash(f"Lỗi khi thêm học sinh: {str(e)}", "danger")
#             return redirect(request.url)
#     return render_template('them_hoc_sinh.html', danh_sach_hoc_sinh=ds_hs_chua_lop, lop=lop, taikhoan=taikhoan)
#
# @app.route('/xoa-hoc-sinh', methods=['POST'])
# def xoa_hoc_sinh():
#     taikhoan = session.get('taikhoan')
#     id_hoc_sinh = request.form.get('idHocSinh')
#     if id_hoc_sinh:
#         hoc_sinh = dao.get_hs_by_id(id_hoc_sinh)
#         if hoc_sinh:
#             lop = dao.get_class_by_id(hoc_sinh.maDsLop)
#             lop.siSoHienTai -= 1
#             hoc_sinh.maDsLop = None
#             db.session.commit()
#             flash('Đã xóa học sinh khỏi danh sách lớp thành công!', 'success')
#             return redirect(f'/nhan-vien/{taikhoan}/danh-sach-lop/sua/{lop.maDsLop}')  # Chuyển hướng về danh sách lớp
#     flash('Không nhận được ID học sinh để xóa!', 'danger')
#     return redirect(url_for('show_ds_lop'))
#
# @app.route('/giao-vien/<taikhoan>/danh-sach-lop-day')
# def danh_sach_lop_day(taikhoan):
#     nam_hoc_moi_nhat = db.session.query(HocKy.namHoc).order_by(HocKy.namHoc.desc()).first()
#     # Lấy danh sách lớp mà giáo viên đang dạy trong năm học mới nhất
#     danh_sach_lop_ids = db.session.query(GiaoVienDayHoc.idDsLop).filter(
#         GiaoVienDayHoc.idGiaoVien == current_user.id,
#         GiaoVienDayHoc.idHocKy.in_(
#             db.session.query(HocKy.idHocKy).filter(HocKy.namHoc == nam_hoc_moi_nhat.namHoc)
#         )
#     ).distinct()
#     danh_sach_lop = DanhSachLop.query.filter(DanhSachLop.maDsLop.in_(danh_sach_lop_ids)).all()
#     return render_template('danh_sach_lop_gv.html', danh_sach_lop=danh_sach_lop, taikhoan=taikhoan)
#
# @app.route('/giao-vien/<taikhoan>/danh-sach-lop-day/<int:lop_id>/nhap-diem', methods=['GET', 'POST'])
# def nhap_diem(lop_id, taikhoan):
#     lop = DanhSachLop.query.get(lop_id)
#     danh_sach_hoc_sinh = dao.get_ds_hs_by_ma_lop(lop_id)
#     gv = dao.get_gv_by_id(current_user.id)
#     giao_vien_id = gv.id
#     mon_hoc = dao.get_mon_by_id(gv.idMonHoc)
#     hoc_ky = dao.get_hk_by_id(lop.hocKy_id)
#     so_cot_15p = mon_hoc.soCot15p
#     so_cot_1_tiet = mon_hoc.soCot1Tiet
#
#     # Lấy dữ liệu điểm từ cơ sở dữ liệu
#     for hoc_sinh in danh_sach_hoc_sinh:
#         hoc_sinh.diem_15p = [
#             diem.diem for diem in BangDiem.query.filter_by(
#                 hocSinh_id=hoc_sinh.idHocSinh,
#                 monHoc_id=mon_hoc.idMonHoc,
#                 hocKy_id=hoc_ky.idHocKy
#             ).filter(BangDiem.loai_diem.like("15p%"))
#         ]
#         hoc_sinh.diem_1_tiet = [
#             diem.diem for diem in BangDiem.query.filter_by(
#                 hocSinh_id=hoc_sinh.idHocSinh,
#                 monHoc_id=mon_hoc.idMonHoc,
#                 hocKy_id=hoc_ky.idHocKy
#             ).filter(BangDiem.loai_diem.like("1_tiet%")).order_by(BangDiem.loai_diem)
#         ]
#         diem_thi = BangDiem.query.filter_by(
#             hocSinh_id=hoc_sinh.idHocSinh,
#             monHoc_id=mon_hoc.idMonHoc,
#             hocKy_id=hoc_ky.idHocKy,
#             loai_diem='thi'
#         ).first()
#         hoc_sinh.diem_thi = diem_thi.diem if diem_thi else None
#     if request.method == 'POST':
#         try:
#             for i, hoc_sinh in enumerate(danh_sach_hoc_sinh):
#                 # Lưu điểm 15 phút
#                 for j in range(so_cot_15p):
#                     diem_key = f'diem_15p_{j}[]'
#                     diem_15p = request.form.getlist(diem_key)[i]
#                     if diem_15p:
#                         bang_diem_15p = BangDiem.query.filter_by(
#                             hocSinh_id=hoc_sinh.idHocSinh,
#                             loai_diem=f'15p_{j + 1}',
#                             monHoc_id=mon_hoc.idMonHoc,
#                             hocKy_id=hoc_ky.idHocKy
#                         ).first()
#                         if not bang_diem_15p:
#                             bang_diem_15p = BangDiem(
#                                 hocSinh_id=hoc_sinh.idHocSinh,
#                                 loai_diem=f'15p_{j + 1}',
#                                 diem=float(diem_15p),
#                                 monHoc_id=mon_hoc.idMonHoc,
#                                 giaoVien_id=giao_vien_id,
#                                 hocKy_id=hoc_ky.idHocKy
#                             )
#                             db.session.add(bang_diem_15p)
#                         else:
#                             bang_diem_15p.diem = float(diem_15p)
#                 # Lưu điểm 1 tiết
#                 for j in range(so_cot_1_tiet):
#                     diem_key = f'diem_1_tiet_{j}[]'
#                     diem_1_tiet = request.form.getlist(diem_key)[i]
#                     if diem_1_tiet:
#                         bang_diem_1_tiet = BangDiem.query.filter_by(
#                             hocSinh_id=hoc_sinh.idHocSinh,
#                             loai_diem=f'1_tiet_{j + 1}',
#                             monHoc_id=mon_hoc.idMonHoc,
#                             hocKy_id=hoc_ky.idHocKy
#                         ).first()
#                         if not bang_diem_1_tiet:
#                             bang_diem_1_tiet = BangDiem(
#                                 hocSinh_id=hoc_sinh.idHocSinh,
#                                 loai_diem=f'1_tiet_{j + 1}',
#                                 diem=float(diem_1_tiet),
#                                 monHoc_id=mon_hoc.idMonHoc,
#                                 giaoVien_id=giao_vien_id,
#                                 hocKy_id=hoc_ky.idHocKy
#                             )
#                             db.session.add(bang_diem_1_tiet)
#                         else:
#                             bang_diem_1_tiet.diem = float(diem_1_tiet)
#                 # Lưu điểm thi
#                 diem_thi = request.form.getlist('diem_thi[]')[i]
#                 if diem_thi:
#                     bang_diem_thi = BangDiem.query.filter_by(
#                         hocSinh_id=hoc_sinh.idHocSinh,
#                         loai_diem='thi',
#                         monHoc_id=mon_hoc.idMonHoc,
#                         hocKy_id=hoc_ky.idHocKy
#                     ).first()
#                     if not bang_diem_thi:
#                         bang_diem_thi = BangDiem(
#                             hocSinh_id=hoc_sinh.idHocSinh,
#                             loai_diem='thi',
#                             diem=float(diem_thi),
#                             monHoc_id=mon_hoc.idMonHoc,
#                             giaoVien_id=giao_vien_id,
#                             hocKy_id=hoc_ky.idHocKy
#                         )
#                         db.session.add(bang_diem_thi)
#                     else:
#                         bang_diem_thi.diem = float(diem_thi)
#             db.session.commit()
#             flash("Điểm đã được lưu thành công!", "success")
#             return redirect(f'/giao-vien/{taikhoan}/danh-sach-lop-day/{lop_id}')
#         except Exception as e:
#             db.session.rollback()
#             flash(f"Lỗi khi lưu điểm: {str(e)}", "danger")
#     return render_template('nhap_diem.html',lop=lop,danh_sach_hoc_sinh=danh_sach_hoc_sinh,hoc_ky=hoc_ky,
#         mon_hoc=mon_hoc,so_cot_15p=so_cot_15p,so_cot_1_tiet=so_cot_1_tiet,taikhoan=taikhoan)
#
# @app.route('/giao-vien/<taikhoan>/danh-sach-lop-day/<int:lop_id>')
# def xem_lop(lop_id, taikhoan):
#     lop = DanhSachLop.query.get(lop_id)
#     danh_sach_hoc_sinh = HocSinh.query.filter(HocSinh.maDsLop == lop_id).all()
#     hoc_ky = HocKy.query.get(lop.hocKy_id)
#     giaoVien = GiaoVien.query.get(current_user.id)
#     mon_hoc_id = giaoVien.idMonHoc
#
#     for hoc_sinh in danh_sach_hoc_sinh:
#         # Lấy điểm cột 15 phút
#         diem_15p = [
#             diem.diem for diem in BangDiem.query.filter_by(
#                 hocSinh_id=hoc_sinh.idHocSinh,
#                 monHoc_id=mon_hoc_id,
#                 hocKy_id=hoc_ky.idHocKy
#             ).filter(BangDiem.loai_diem.like("15p%"))]
#         # Lấy điểm cột 1 tiết
#         diem_1_tiet = [
#             diem.diem for diem in BangDiem.query.filter_by(
#                 hocSinh_id=hoc_sinh.idHocSinh,
#                 monHoc_id=mon_hoc_id,
#                 hocKy_id=hoc_ky.idHocKy
#             ).filter(BangDiem.loai_diem.like("1_tiet%"))]
#         # Lấy điểm thi
#         diem_thi = BangDiem.query.filter_by(
#             hocSinh_id=hoc_sinh.idHocSinh,
#             monHoc_id=mon_hoc_id,
#             hocKy_id=hoc_ky.idHocKy,
#             loai_diem='thi'
#         ).first()
#         # Tính trung bình 15 phút và 1 tiết
#         hoc_sinh.tb_15p = round(sum(diem_15p) / len(diem_15p), 2) if len(diem_15p) > 0 else ""
#         hoc_sinh.tb_1_tiet = round(sum(diem_1_tiet) / len(diem_1_tiet), 2) if len(diem_1_tiet) > 0 else ""
#         hoc_sinh.diem_thi = diem_thi.diem if diem_thi is not None else ""
#
#         if diem_15p is not None and diem_1_tiet is not None and diem_thi is not None:
#             hoc_sinh.diem_trung_binh = round(
#                 ((hoc_sinh.tb_15p) + (hoc_sinh.tb_1_tiet * 2) + (hoc_sinh.diem_thi * 3)) / 6, 2)
#         else:
#             hoc_sinh.diem_trung_binh = None
#     return render_template('danh_sach_hs.html',lop=lop,danh_sach_hoc_sinh=danh_sach_hoc_sinh,hoc_ky=hoc_ky,taikhoan=taikhoan)
#
# @app.route('/chuyen-diem-hoc-ky', methods=['POST'])
# def chuyen_diem_hoc_ky():
#     hoc_ky_hien_tai = HocKy.query.order_by(HocKy.idHocKy.desc()).first()
#     hoc_ky_tiep_theo = HocKy.query.filter(HocKy.namHoc == hoc_ky_hien_tai.namHoc, HocKy.hocKy != hoc_ky_hien_tai.hocKy).first()
#     bang_diem_cu = BangDiem.query.filter_by(hocKy_id=hoc_ky_hien_tai.idHocKy).all()
#
#     for diem in bang_diem_cu:
#         bang_diem_moi = BangDiem(
#             hocSinh_id=diem.hocSinh_id,
#             loai_diem=diem.loai_diem,
#             monHoc_id=diem.monHoc_id,
#             giaoVien_id=diem.giaoVien_id,
#             hocKy_id=hoc_ky_tiep_theo.idHocKy
#         )
#         db.session.add(bang_diem_moi)
#     db.session.commit()
#     flash('Đã chuyển điểm sang học kỳ tiếp theo!', 'success')
#     return redirect('/admin')
#
# @app.route('/giao-vien/<taikhoan>/lop-chu-nhiem')
# def danh_sach_lop_chu_nhiem(taikhoan):
#     session['taikhoan'] = taikhoan
#     lop_chu_nhiem = DanhSachLop.query.filter_by(giaoVienChuNhiem_id=current_user.id,active=True).first()
#     if lop_chu_nhiem:
#         danh_sach_hoc_sinh = dao.get_ds_hs_by_ma_lop(lop_chu_nhiem.maDsLop)
#         danh_sach_mon_hoc = dao.get_ds_mon()
#         nam_hoc_moi_nhat = db.session.query(HocKy.namHoc).order_by(HocKy.namHoc.desc()).first()
#         danh_sach_hoc_ky = HocKy.query.filter_by(namHoc=nam_hoc_moi_nhat.namHoc).order_by(HocKy.hocKy).all()
#
#         # Lấy học kỳ được chọn hoặc mặc định là học kỳ hiện tại của lớp
#         hoc_ky_id = request.args.get('hocKy', lop_chu_nhiem.hocKy_id, type=int)
#         hoc_ky = dao.get_hk_by_id(hoc_ky_id)
#
#         # Lấy bảng điểm theo môn và loại điểm
#         bang_diem = {}
#         for hs in danh_sach_hoc_sinh:
#             bang_diem[hs.idHocSinh] = {
#                 "15p": {mon.tenMonHoc: None for mon in danh_sach_mon_hoc},
#                 "1_tiet": {mon.tenMonHoc: None for mon in danh_sach_mon_hoc},
#                 "thi": {mon.tenMonHoc: None for mon in danh_sach_mon_hoc},
#                 "tb_mon": {mon.tenMonHoc: None for mon in danh_sach_mon_hoc}  # Thêm điểm trung bình môn
#             }
#             diem_cua_hoc_sinh = BangDiem.query.filter_by(hocSinh_id=hs.idHocSinh, hocKy_id=hoc_ky_id).all()
#             for mon in danh_sach_mon_hoc:
#                 ten_mon = mon.tenMonHoc
#                 diem_hs_mon = {diem for diem in diem_cua_hoc_sinh if diem.monHoc_id.__eq__(mon.idMonHoc)}
#                 ds_15p=[]
#                 ds_1_tiet=[]
#                 thi=[]
#                 for diem in diem_hs_mon:
#                     if diem.loai_diem.startswith("15p"):
#                         ds_15p.append(diem.diem)
#                     elif diem.loai_diem.startswith("1_tiet"):
#                         ds_1_tiet.append(diem.diem)
#                     else:
#                         thi.append(diem.diem)
#                 tb_15p = round(sum(ds_15p)/len(ds_15p),2) if len(ds_15p)>0 else None
#                 tb_1Tiet = round(sum(ds_1_tiet)/len(ds_1_tiet),2) if len(ds_1_tiet)>0 else None
#                 dThi = round(sum(thi)/len(thi),2) if len(thi)>0 else None
#                 bang_diem[hs.idHocSinh]["15p"][ten_mon] = tb_15p
#                 bang_diem[hs.idHocSinh]["1_tiet"][ten_mon] = tb_1Tiet
#                 bang_diem[hs.idHocSinh]["thi"][ten_mon] = dThi
#                 if (bang_diem[hs.idHocSinh]["15p"][ten_mon] is not None and bang_diem[hs.idHocSinh]["1_tiet"][ten_mon] is not None
#                     and bang_diem[hs.idHocSinh]["thi"][ten_mon] is not None):
#                     tb_mon = (
#                         bang_diem[hs.idHocSinh]["15p"][ten_mon]
#                         + bang_diem[hs.idHocSinh]["1_tiet"][ten_mon] * 2
#                         + bang_diem[hs.idHocSinh]["thi"][ten_mon] * 3
#                     ) / 6
#                     bang_diem[hs.idHocSinh]["tb_mon"][ten_mon] = round(tb_mon, 2)
#             # Kiểm tra điều kiện nhập đủ điểm Toán, Văn, Anh trước khi tính điểm trung bình toàn bộ môn
#             mon_can_thiet = ["Toán", "Văn", "Anh"]
#             if all(
#                 bang_diem[hs.idHocSinh]["tb_mon"].get(mon) is not None
#                 for mon in mon_can_thiet):
#                 diem_tb_cac_mon = [
#                     bang_diem[hs.idHocSinh]["tb_mon"][mon.tenMonHoc]
#                     for mon in danh_sach_mon_hoc
#                     if bang_diem[hs.idHocSinh]["tb_mon"][mon.tenMonHoc] is not None
#                 ]
#                 hs.diem_trung_binh = round(sum(diem_tb_cac_mon) / len(diem_tb_cac_mon), 2) if diem_tb_cac_mon else None
#                 # Xếp loại
#                 diem_toan = bang_diem[hs.idHocSinh]["tb_mon"].get("Toán", 0)
#                 diem_van = bang_diem[hs.idHocSinh]["tb_mon"].get("Văn", 0)
#                 if (diem_toan >= 8.0 or diem_van >= 8.0) and all(d >= 6.5 for d in diem_tb_cac_mon):
#                     hs.xep_loai = "Giỏi"
#                 elif (diem_toan >= 6.5 or diem_van >= 6.5) and all(d >= 5.0 for d in diem_tb_cac_mon):
#                     hs.xep_loai = "Khá"
#                 elif (diem_toan >= 3.5 or diem_van >= 3.5) and all(d >= 2.0 for d in diem_tb_cac_mon):
#                     hs.xep_loai = "Yếu"
#                 else:
#                     hs.xep_loai = "Kém"
#             else:
#                 # Nếu chưa nhập đủ điểm thì để trống
#                 hs.diem_trung_binh = None
#                 hs.xep_loai = None
#         return render_template('danh_sach_lop_chu_nhiem.html',lop=lop_chu_nhiem,danh_sach_hoc_sinh=danh_sach_hoc_sinh,
#             danh_sach_mon_hoc=danh_sach_mon_hoc,bang_diem=bang_diem,hoc_ky=hoc_ky,danh_sach_hoc_ky=danh_sach_hoc_ky,taikhoan=taikhoan)
#     else:
#         flash("Hiện tại bạn không có chủ nhệm lớp nào!", "warning")
#         return redirect(f'/giao-vien/{taikhoan}')
#
# @app.route('/giao-vien/<taikhoan>/lop-chu-nhiem/bang-diem-tong-ket', methods=['GET'])
# def bang_diem_tong_ket(taikhoan):
#     gv = GiaoVien.query.get(current_user.id)
#     lop_chu_nhiem = DanhSachLop.query.filter_by(giaoVienChuNhiem_id=gv.id, active=True).first()
#     danh_sach_hoc_sinh = HocSinh.query.filter_by(maDsLop=lop_chu_nhiem.maDsLop).all()
#     bang_diem_tong_ket = []
#
#     for hs in danh_sach_hoc_sinh:
#         hoc_ky_moi_nhat = HocKy.query.order_by(HocKy.idHocKy.desc()).first()
#         hk_id = hoc_ky_moi_nhat.idHocKy
#         diem_tb_hk1 = BangDiemTB.query.filter_by(hocSinh_id=hs.idHocSinh, hocKy_id=hk_id-1).first()
#         diem_tb_hk2 = BangDiemTB.query.filter_by(hocSinh_id=hs.idHocSinh, hocKy_id=hk_id).first()
#
#         bang_diem_tong_ket.append({
#             'ho_ten': hs.hoTen,
#             'lop': lop_chu_nhiem.tenLop if lop_chu_nhiem else "",
#             'diem_tb_hk1': diem_tb_hk1.diem_trung_binh if diem_tb_hk1 else "",
#             'diem_tb_hk2': diem_tb_hk2.diem_trung_binh if diem_tb_hk2 else "",
#         })
#     return render_template('bang_diem_tong_ket.html',bang_diem_tong_ket=bang_diem_tong_ket,lop=lop_chu_nhiem,
#         enumerate=enumerate,taikhoan=taikhoan)
#
# @app.route('/xac-nhan-bang-diem', methods=['POST'])
# def xac_nhan_bang_diem():
#     taikhoan = session.get('taikhoan')
#     ma_ds_lop = request.form.get('maDsLop')
#     lop = dao.get_class_by_id(ma_ds_lop)
#     danh_sach_hoc_sinh = dao.get_ds_hs_by_ma_lop(ma_ds_lop)
#     hoc_ky_id = lop.hocKy_id
#
#     for hs in danh_sach_hoc_sinh:
#         diem_tb = dao.tinh_diem_trung_binh(hs.idHocSinh, hoc_ky_id)
#         if diem_tb is not None:
#             bang_diem_tb = BangDiemTB.query.filter_by(hocSinh_id=hs.idHocSinh, hocKy_id=hoc_ky_id).first()
#             if not bang_diem_tb:
#                 bang_diem_tb = BangDiemTB(
#                     hocSinh_id=hs.idHocSinh,
#                     hocKy_id=hoc_ky_id,
#                     diem_trung_binh=diem_tb
#                 )
#                 db.session.add(bang_diem_tb)
#             else:
#                 bang_diem_tb.diem_trung_binh = diem_tb
#     db.session.commit()
#     flash("Bảng điểm đã được xác nhận và lưu thành công!", "success")
#     return redirect(f'/giao-vien/{taikhoan}/lop-chu-nhiem')
#
# @app.route('/thong-ke-bao-cao', methods=['GET', 'POST'])
# def thong_ke_bao_cao():
#     try:
#         nam_hoc_moi_nhat = db.session.query(HocKy.namHoc).order_by(HocKy.namHoc.desc()).first()
#         danh_sach_hoc_ky = HocKy.query.filter_by(namHoc=nam_hoc_moi_nhat.namHoc).order_by(HocKy.hocKy).all()
#         if request.method == 'POST':
#             khoi_lop = request.form.get('khoiLop')
#             mon_hoc_id = request.form.get('monHoc')
#             hoc_ky_id = request.form.get('hocKy')
#             danh_sach_khoi_lop = DanhSachLop.query.filter_by(khoi=khoi_lop, active = True)
#             data = []
#
#             for lop in danh_sach_khoi_lop:
#                 ds_hoc_sinh = lop.hocSinhs
#                 si_so = len(ds_hoc_sinh)
#                 so_luong_dat = 0
#                 for hs in ds_hoc_sinh:
#                     diem_tb_mon = dao.tinh_diem_tb_mon(hs.idHocSinh,hoc_ky_id,mon_hoc_id)
#                     if diem_tb_mon is not None and diem_tb_mon>=5:
#                         so_luong_dat+=1
#                 ty_le = round((so_luong_dat / si_so) * 100, 2) if si_so > 0 else 0
#                 # Thêm dữ liệu vào mảng data
#                 data.append({
#                     "lop": lop.tenLop,
#                     "si_so": si_so,
#                     "so_luong_dat": so_luong_dat,
#                     "ty_le": ty_le
#                 })
#             return render_template('thong_ke_bao_cao.html',data=data,danh_sach_mon_hoc=dao.get_ds_mon(),
#                     danh_sach_hoc_ky=danh_sach_hoc_ky,enumerate=enumerate)
#         return render_template('thong_ke_bao_cao.html',danh_sach_mon_hoc=dao.get_ds_mon(),danh_sach_hoc_ky=danh_sach_hoc_ky)
#     except Exception as e:
#         flash(f"Đã xảy ra lỗi: {str(e)}", "danger")
#         return redirect('/admin')
#
# @app.route('/ket-thuc-nam-hoc', methods=['POST'])
# def ket_thuc_nam_hoc():
#     try:
#         ds_lop = DanhSachLop.query.filter_by(active=True).all()
#         if not ds_lop:
#             flash(f"Chưa bắt đầu năm học mới!", "danger")
#             return redirect('/admin')
#         hoc_ky = HocKy.query.order_by(HocKy.idHocKy.desc()).first()
#         idHocKy = hoc_ky.idHocKy
#         for lop in ds_lop:
#             ds_hoc_sinh = lop.hocSinhs
#             for hs in ds_hoc_sinh:
#                 flag = True
#                 hs.maDsLop=None
#                 ds_mon = dao.get_ds_mon()
#                 for mon in ds_mon:
#                     dtb_mon1 = dao.tinh_diem_tb_mon(hs.idHocSinh,idHocKy-1,mon.idMonHoc)
#                     dtb_mon2 = dao.tinh_diem_tb_mon(hs.idHocSinh,idHocKy,mon.idMonHoc)
#                     dtb_mon = (dtb_mon1+dtb_mon2)/2
#                     if dtb_mon < 3.5:
#                         flag = False
#                         break
#                 if flag:
#                     dtb_ky1 = BangDiemTB.query.filter_by(hocSinh_id=hs.idHocSinh, hocKy_id=idHocKy-1).first()
#                     dtb_ky2 = BangDiemTB.query.filter_by(hocSinh_id=hs.idHocSinh, hocKy_id=idHocKy).first()
#                     print(dtb_ky1)
#                     print(dtb_ky2)
#                     dtb_nam = (dtb_ky1.diem_trung_binh+dtb_ky2.diem_trung_binh)/2
#                     print(dtb_nam)
#                     if dtb_nam>=5:
#                         #Môn Văn
#                         mon_van = MonHoc.query.filter_by(tenMonHoc="Văn").first()
#                         dtb_van1 = dao.tinh_diem_tb_mon(hs.idHocSinh, idHocKy - 1, mon_van.idMonHoc)
#                         dtb_van2 = dao.tinh_diem_tb_mon(hs.idHocSinh, idHocKy, mon_van.idMonHoc)
#                         dtb_van = round((dtb_van1 + dtb_van2)/2,2)
#                         #Môn Toán
#                         mon_toan = MonHoc.query.filter_by(tenMonHoc="Toán").first()
#                         dtb_toan1 = dao.tinh_diem_tb_mon(hs.idHocSinh, idHocKy - 1, mon_toan.idMonHoc)
#                         dtb_toan2 = dao.tinh_diem_tb_mon(hs.idHocSinh, idHocKy, mon_toan.idMonHoc)
#                         dtb_toan = round((dtb_toan1 + dtb_toan2) / 2,2)
#                         #Môn Anh
#                         mon_anh = MonHoc.query.filter_by(tenMonHoc="Anh").first()
#                         dtb_anh1 = dao.tinh_diem_tb_mon(hs.idHocSinh, idHocKy - 1, mon_anh.idMonHoc)
#                         dtb_anh2 = dao.tinh_diem_tb_mon(hs.idHocSinh, idHocKy, mon_anh.idMonHoc)
#                         dtb_anh = round((dtb_anh1 + dtb_anh2) / 2,2)
#                         if dtb_van>=5 or dtb_toan>=5 or dtb_anh>=5:
#                             if hs.khoi.__eq__("Khối 10"):
#                                 hs.khoi = "Khối 11"
#                             elif hs.khoi.__eq__("Khối 11"):
#                                 hs.khoi = "Khối 12"
#                             elif hs.khoi.__eq__("Khối 12"):
#                                 hs.khoi = ""
#             lop.idPhongHoc = None
#             lop.active = False
#         nam_hoc_hien_tai = hoc_ky.namHoc
#         nam_hoc_bat_dau, nam_hoc_ket_thuc = map(int, nam_hoc_hien_tai.split('-'))
#         nam_hoc_moi = f"{nam_hoc_bat_dau + 1}-{nam_hoc_ket_thuc + 1}"
#
#         hoc_ky_1 = HocKy(
#             namHoc=nam_hoc_moi,
#             hocKy="1"
#         )
#         db.session.add(hoc_ky_1)
#         hoc_ky_2 = HocKy(
#             namHoc=nam_hoc_moi,
#             hocKy="2"
#         )
#         db.session.add(hoc_ky_2)
#         db.session.commit()
#         flash("Đã kết thúc năm học thành công! Các lớp và khối đã được cập nhật.", "success")
#     except Exception as e:
#         db.session.rollback()
#         flash(f"Lỗi khi kết thúc năm học: Các lớp chưa xác nhận bảng điểm", "danger")
#     return redirect('/admin')

if __name__ == '__main__':
    from app import admin
    app.run(debug=True)
