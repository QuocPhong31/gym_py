-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: manadb
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bang_diem`
--

DROP TABLE IF EXISTS `bang_diem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bang_diem` (
  `idBangDiem` int NOT NULL AUTO_INCREMENT,
  `hocSinh_id` int NOT NULL,
  `loai_diem` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `diem` float DEFAULT NULL,
  `monHoc_id` int NOT NULL,
  `giaoVien_id` int NOT NULL,
  `hocKy_id` int NOT NULL,
  PRIMARY KEY (`idBangDiem`),
  KEY `hocSinh_id` (`hocSinh_id`),
  KEY `monHoc_id` (`monHoc_id`),
  KEY `giaoVien_id` (`giaoVien_id`),
  KEY `hocKy_id` (`hocKy_id`),
  CONSTRAINT `bang_diem_ibfk_1` FOREIGN KEY (`hocSinh_id`) REFERENCES `hoc_sinh` (`idHocSinh`),
  CONSTRAINT `bang_diem_ibfk_2` FOREIGN KEY (`monHoc_id`) REFERENCES `monhoc` (`idMonHoc`),
  CONSTRAINT `bang_diem_ibfk_3` FOREIGN KEY (`giaoVien_id`) REFERENCES `giaovien` (`id`),
  CONSTRAINT `bang_diem_ibfk_4` FOREIGN KEY (`hocKy_id`) REFERENCES `hoc_ky` (`idHocKy`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bang_diem`
--

LOCK TABLES `bang_diem` WRITE;
/*!40000 ALTER TABLE `bang_diem` DISABLE KEYS */;
/*!40000 ALTER TABLE `bang_diem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bang_diem_tb`
--

DROP TABLE IF EXISTS `bang_diem_tb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bang_diem_tb` (
  `idBangDiemTB` int NOT NULL AUTO_INCREMENT,
  `hocSinh_id` int NOT NULL,
  `hocKy_id` int NOT NULL,
  `diem_trung_binh` float NOT NULL,
  PRIMARY KEY (`idBangDiemTB`),
  KEY `hocSinh_id` (`hocSinh_id`),
  KEY `hocKy_id` (`hocKy_id`),
  CONSTRAINT `bang_diem_tb_ibfk_1` FOREIGN KEY (`hocSinh_id`) REFERENCES `hoc_sinh` (`idHocSinh`),
  CONSTRAINT `bang_diem_tb_ibfk_2` FOREIGN KEY (`hocKy_id`) REFERENCES `hoc_ky` (`idHocKy`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bang_diem_tb`
--

LOCK TABLES `bang_diem_tb` WRITE;
/*!40000 ALTER TABLE `bang_diem_tb` DISABLE KEYS */;
/*!40000 ALTER TABLE `bang_diem_tb` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `danh_sach_lop`
--

DROP TABLE IF EXISTS `danh_sach_lop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `danh_sach_lop` (
  `maDsLop` int NOT NULL AUTO_INCREMENT,
  `idPhongHoc` int DEFAULT NULL,
  `tenLop` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `khoi` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `giaoVienChuNhiem_id` int DEFAULT NULL,
  `siSoHienTai` int NOT NULL,
  `siSo` int NOT NULL,
  `hocKy_id` int NOT NULL,
  `active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`maDsLop`),
  UNIQUE KEY `idPhongHoc` (`idPhongHoc`),
  KEY `giaoVienChuNhiem_id` (`giaoVienChuNhiem_id`),
  KEY `hocKy_id` (`hocKy_id`),
  CONSTRAINT `danh_sach_lop_ibfk_1` FOREIGN KEY (`idPhongHoc`) REFERENCES `phong_hoc` (`idPhongHoc`),
  CONSTRAINT `danh_sach_lop_ibfk_2` FOREIGN KEY (`giaoVienChuNhiem_id`) REFERENCES `giaovien` (`id`),
  CONSTRAINT `danh_sach_lop_ibfk_3` FOREIGN KEY (`hocKy_id`) REFERENCES `hoc_ky` (`idHocKy`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `danh_sach_lop`
--

LOCK TABLES `danh_sach_lop` WRITE;
/*!40000 ALTER TABLE `danh_sach_lop` DISABLE KEYS */;
/*!40000 ALTER TABLE `danh_sach_lop` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `giao_vien_day_hoc`
--

DROP TABLE IF EXISTS `giao_vien_day_hoc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `giao_vien_day_hoc` (
  `idGiaoVienDayHoc` int NOT NULL AUTO_INCREMENT,
  `idGiaoVien` int DEFAULT NULL,
  `idHocKy` int DEFAULT NULL,
  `idDsLop` int DEFAULT NULL,
  PRIMARY KEY (`idGiaoVienDayHoc`),
  KEY `idGiaoVien` (`idGiaoVien`),
  KEY `idHocKy` (`idHocKy`),
  KEY `idDsLop` (`idDsLop`),
  CONSTRAINT `giao_vien_day_hoc_ibfk_1` FOREIGN KEY (`idGiaoVien`) REFERENCES `giaovien` (`id`),
  CONSTRAINT `giao_vien_day_hoc_ibfk_2` FOREIGN KEY (`idHocKy`) REFERENCES `hoc_ky` (`idHocKy`),
  CONSTRAINT `giao_vien_day_hoc_ibfk_3` FOREIGN KEY (`idDsLop`) REFERENCES `danh_sach_lop` (`maDsLop`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `giao_vien_day_hoc`
--

LOCK TABLES `giao_vien_day_hoc` WRITE;
/*!40000 ALTER TABLE `giao_vien_day_hoc` DISABLE KEYS */;
/*!40000 ALTER TABLE `giao_vien_day_hoc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `giaovien`
--

DROP TABLE IF EXISTS `giaovien`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `giaovien` (
  `id` int NOT NULL,
  `idMonHoc` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idMonHoc` (`idMonHoc`),
  CONSTRAINT `giaovien_ibfk_1` FOREIGN KEY (`id`) REFERENCES `users` (`id`),
  CONSTRAINT `giaovien_ibfk_2` FOREIGN KEY (`idMonHoc`) REFERENCES `monhoc` (`idMonHoc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `giaovien`
--

LOCK TABLES `giaovien` WRITE;
/*!40000 ALTER TABLE `giaovien` DISABLE KEYS */;
INSERT INTO `giaovien` VALUES (6,1),(4,2),(5,2),(3,3);
/*!40000 ALTER TABLE `giaovien` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hoc_ky`
--

DROP TABLE IF EXISTS `hoc_ky`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hoc_ky` (
  `idHocKy` int NOT NULL AUTO_INCREMENT,
  `namHoc` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `hocKy` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`idHocKy`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hoc_ky`
--

LOCK TABLES `hoc_ky` WRITE;
/*!40000 ALTER TABLE `hoc_ky` DISABLE KEYS */;
INSERT INTO `hoc_ky` VALUES (1,'2023-2024','1'),(2,'2023-2024','2');
/*!40000 ALTER TABLE `hoc_ky` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hoc_sinh`
--

DROP TABLE IF EXISTS `hoc_sinh`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hoc_sinh` (
  `idHocSinh` int NOT NULL AUTO_INCREMENT,
  `hoTen` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `gioiTinh` tinyint(1) NOT NULL,
  `ngaySinh` date NOT NULL,
  `khoi` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `diaChi` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `SDT` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `eMail` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `maDsLop` int DEFAULT NULL,
  PRIMARY KEY (`idHocSinh`),
  UNIQUE KEY `eMail` (`eMail`),
  KEY `maDsLop` (`maDsLop`),
  CONSTRAINT `hoc_sinh_ibfk_1` FOREIGN KEY (`maDsLop`) REFERENCES `danh_sach_lop` (`maDsLop`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hoc_sinh`
--

LOCK TABLES `hoc_sinh` WRITE;
/*!40000 ALTER TABLE `hoc_sinh` DISABLE KEYS */;
INSERT INTO `hoc_sinh` VALUES (1,'Trần Huỳnh Sang',1,'2009-02-02','Khối 10','Cà Mau','0987654321','hsang1@gmail.com',NULL),(2,'Nguyễn Đăng Khôi',1,'2008-04-01','Khối 10','Thành phố Hồ Chí Minh','0987425414','dangkhoi@gmail.com',NULL),(3,'Trần Hạ Vi',0,'2007-05-02','Khối 12','Thành phố Hồ Chí Minh','0762590922','vivi@gmail.com',NULL);
/*!40000 ALTER TABLE `hoc_sinh` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `monhoc`
--

DROP TABLE IF EXISTS `monhoc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `monhoc` (
  `idMonHoc` int NOT NULL AUTO_INCREMENT,
  `tenMonHoc` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `soCot15p` int NOT NULL,
  `soCot1Tiet` int NOT NULL,
  `soCotThi` int NOT NULL,
  PRIMARY KEY (`idMonHoc`),
  UNIQUE KEY `tenMonHoc` (`tenMonHoc`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `monhoc`
--

LOCK TABLES `monhoc` WRITE;
/*!40000 ALTER TABLE `monhoc` DISABLE KEYS */;
INSERT INTO `monhoc` VALUES (1,'Văn',5,3,1),(2,'Toán',5,3,1),(3,'Anh',3,2,1);
/*!40000 ALTER TABLE `monhoc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nhanvien`
--

DROP TABLE IF EXISTS `nhanvien`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nhanvien` (
  `id` int NOT NULL,
  `vaiTro` enum('NGUOIQUANTRI','NHANVIEN') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `nhanvien_ibfk_1` FOREIGN KEY (`id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nhanvien`
--

LOCK TABLES `nhanvien` WRITE;
/*!40000 ALTER TABLE `nhanvien` DISABLE KEYS */;
INSERT INTO `nhanvien` VALUES (1,'NGUOIQUANTRI'),(2,'NHANVIEN');
/*!40000 ALTER TABLE `nhanvien` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `phong_hoc`
--

DROP TABLE IF EXISTS `phong_hoc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `phong_hoc` (
  `idPhongHoc` int NOT NULL AUTO_INCREMENT,
  `tenPhong` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`idPhongHoc`),
  UNIQUE KEY `tenPhong` (`tenPhong`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `phong_hoc`
--

LOCK TABLES `phong_hoc` WRITE;
/*!40000 ALTER TABLE `phong_hoc` DISABLE KEYS */;
INSERT INTO `phong_hoc` VALUES (1,'11'),(2,'12'),(3,'13'),(4,'14'),(5,'15'),(6,'16'),(7,'17'),(8,'18'),(9,'19'),(10,'20'),(11,'21'),(12,'22'),(13,'23'),(14,'24'),(15,'25');
/*!40000 ALTER TABLE `phong_hoc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quy_dinh`
--

DROP TABLE IF EXISTS `quy_dinh`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quy_dinh` (
  `idQuyDinh` int NOT NULL AUTO_INCREMENT,
  `min_age` int DEFAULT NULL,
  `max_age` int DEFAULT NULL,
  `si_so` int DEFAULT NULL,
  `so_cot_15p` int DEFAULT NULL,
  `so_cot_1tiet` int DEFAULT NULL,
  `so_cot_thi` int DEFAULT NULL,
  PRIMARY KEY (`idQuyDinh`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quy_dinh`
--

LOCK TABLES `quy_dinh` WRITE;
/*!40000 ALTER TABLE `quy_dinh` DISABLE KEYS */;
INSERT INTO `quy_dinh` VALUES (1,15,20,40,5,3,1);
/*!40000 ALTER TABLE `quy_dinh` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `hoTen` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `gioiTinh` tinyint(1) NOT NULL,
  `ngaySinh` date NOT NULL,
  `diaChi` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `SDT` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `eMail` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `taiKhoan` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `matKhau` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `SDT` (`SDT`),
  UNIQUE KEY `eMail` (`eMail`),
  UNIQUE KEY `taiKhoan` (`taiKhoan`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Tô Quốc Bình',1,'2004-02-21','Thành phố Hồ Chí Minh','0762590966','toquocbinh2102@gmail.com','admin','e10adc3949ba59abbe56e057f20f883e'),(2,'Trần Quốc Phong',1,'2004-10-30','Thành phố Hồ Chí Minh','0799773010','toquocphong2102@gmail.com','quocphong','e10adc3949ba59abbe56e057f20f883e'),(3,'Lý Vi Quyền',0,'1988-04-19','Thành phố Hồ Chí Minh','0283574403','viquyen@gmail.com','viquyen','e10adc3949ba59abbe56e057f20f883e'),(4,'Phan Trần Minh Khuê',1,'1979-05-22','Thành phố Hồ Chí Minh','0283574401','minhkhue@gmail.com','minhkhue','e10adc3949ba59abbe56e057f20f883e'),(5,'Nguyễn Thị Mai Trang',0,'1980-06-10','Thành phố Hồ Chí Minh','0762595418','maitrang@gmail.com','maitrang','e10adc3949ba59abbe56e057f20f883e'),(6,'Tô Oai Hùng',1,'1977-09-21','Thành phố Hồ Chí Minh','0762578418','oaihung@gmail.com','oaihung','e10adc3949ba59abbe56e057f20f883e');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-27 23:04:12
