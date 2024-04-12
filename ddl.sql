-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: chatbot
-- ------------------------------------------------------
-- Server version	8.0.36

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
-- Table structure for table `게시판`
--

DROP TABLE IF EXISTS `게시판`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `게시판` (
  `게시물ID` varchar(255) NOT NULL,
  `대시보드key` varchar(255) DEFAULT NULL,
  `제목` varchar(255) DEFAULT NULL,
  `학생ID` varchar(255) DEFAULT NULL,
  `선생ID` varchar(255) DEFAULT NULL,
  `작성내용` varchar(255) DEFAULT NULL,
  `작성시간` datetime DEFAULT NULL,
  PRIMARY KEY (`게시물ID`),
  KEY `학생ID` (`학생ID`),
  KEY `선생ID` (`선생ID`),
  KEY `대시보드key` (`대시보드key`),
  CONSTRAINT `게시판_ibfk_1` FOREIGN KEY (`학생ID`) REFERENCES `학생` (`학생ID`),
  CONSTRAINT `게시판_ibfk_2` FOREIGN KEY (`선생ID`) REFERENCES `선생` (`선생ID`),
  CONSTRAINT `게시판_ibfk_3` FOREIGN KEY (`대시보드key`) REFERENCES `대시보드` (`대시보드key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `게시판`
--

LOCK TABLES `게시판` WRITE;
/*!40000 ALTER TABLE `게시판` DISABLE KEYS */;
INSERT INTO `게시판` VALUES ('글1','key1','test1','학생1',NULL,'게시물 내용1','2024-04-01 09:00:00'),('글2','key2','test2',NULL,'선생1','게시물 내용2','2024-04-02 10:00:00');
/*!40000 ALTER TABLE `게시판` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `대시보드`
--

DROP TABLE IF EXISTS `대시보드`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `대시보드` (
  `대시보드key` varchar(255) NOT NULL,
  `과목명` varchar(255) DEFAULT NULL,
  `학년` int DEFAULT NULL,
  `학급` int DEFAULT NULL,
  `담당선생ID` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`대시보드key`),
  KEY `담당선생ID` (`담당선생ID`),
  KEY `idx_학년` (`학년`),
  KEY `idx_학급` (`학급`),
  CONSTRAINT `대시보드_ibfk_1` FOREIGN KEY (`담당선생ID`) REFERENCES `선생` (`선생ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `대시보드`
--

LOCK TABLES `대시보드` WRITE;
/*!40000 ALTER TABLE `대시보드` DISABLE KEYS */;
INSERT INTO `대시보드` VALUES ('key1','과목1',1,1,'선생1'),('key2','과목2',1,2,'선생2');
/*!40000 ALTER TABLE `대시보드` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `댓글`
--

DROP TABLE IF EXISTS `댓글`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `댓글` (
  `댓글ID` varchar(255) NOT NULL,
  `작성자ID` varchar(255) DEFAULT NULL,
  `내용` varchar(255) DEFAULT NULL,
  `댓글시간` datetime DEFAULT NULL,
  `게시물ID` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`댓글ID`),
  KEY `게시물ID` (`게시물ID`),
  CONSTRAINT `댓글_ibfk_1` FOREIGN KEY (`게시물ID`) REFERENCES `게시판` (`게시물ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `댓글`
--

LOCK TABLES `댓글` WRITE;
/*!40000 ALTER TABLE `댓글` DISABLE KEYS */;
INSERT INTO `댓글` VALUES ('댓글1','학생1','댓글 내용1','2024-04-03 09:00:00','글1'),('댓글2','선생1','댓글 내용2','2024-04-04 10:00:00','글2');
/*!40000 ALTER TABLE `댓글` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `선생`
--

DROP TABLE IF EXISTS `선생`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `선생` (
  `선생ID` varchar(255) NOT NULL,
  `성별` varchar(255) DEFAULT NULL,
  `이름` varchar(255) DEFAULT NULL,
  `생년월일` date DEFAULT NULL,
  `이메일` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`선생ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `선생`
--

LOCK TABLES `선생` WRITE;
/*!40000 ALTER TABLE `선생` DISABLE KEYS */;
INSERT INTO `선생` VALUES ('선생1','남자','김선생','1980-01-01','teacher1@example.com'),('선생2','여자','박선생','1985-02-02','teacher2@example.com');
/*!40000 ALTER TABLE `선생` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `챗봇`
--

DROP TABLE IF EXISTS `챗봇`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `챗봇` (
  `시간` datetime NOT NULL,
  `학생ID` varchar(255) NOT NULL,
  `질문` varchar(255) DEFAULT NULL,
  `챗봇응답` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`시간`,`학생ID`),
  KEY `학생ID` (`학생ID`),
  CONSTRAINT `챗봇_ibfk_1` FOREIGN KEY (`학생ID`) REFERENCES `학생` (`학생ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `챗봇`
--

LOCK TABLES `챗봇` WRITE;
/*!40000 ALTER TABLE `챗봇` DISABLE KEYS */;
INSERT INTO `챗봇` VALUES ('2024-04-01 09:00:00','학생1','안녕하세요?','안녕하세요!');
/*!40000 ALTER TABLE `챗봇` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `첨부파일`
--

DROP TABLE IF EXISTS `첨부파일`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `첨부파일` (
  `파일ID` varchar(255) NOT NULL,
  `게시물ID` varchar(255) DEFAULT NULL,
  `파일명` varchar(255) DEFAULT NULL,
  `파일경로` varchar(255) DEFAULT NULL,
  `시간` datetime DEFAULT NULL,
  PRIMARY KEY (`파일ID`),
  KEY `게시물ID` (`게시물ID`),
  CONSTRAINT `첨부파일_ibfk_1` FOREIGN KEY (`게시물ID`) REFERENCES `게시판` (`게시물ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `첨부파일`
--

LOCK TABLES `첨부파일` WRITE;
/*!40000 ALTER TABLE `첨부파일` DISABLE KEYS */;
INSERT INTO `첨부파일` VALUES ('파일1','글1','파일1.txt','/path/to/파일1.txt','2024-04-01 09:00:00'),('파일2','글2','파일2.txt','/path/to/파일2.txt','2024-04-02 10:00:00');
/*!40000 ALTER TABLE `첨부파일` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `학생`
--

DROP TABLE IF EXISTS `학생`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `학생` (
  `학생ID` varchar(255) NOT NULL,
  `성별` varchar(255) DEFAULT NULL,
  `이름` varchar(255) DEFAULT NULL,
  `생년월일` date DEFAULT NULL,
  `휴대폰번호` varchar(255) DEFAULT NULL,
  `학년` int DEFAULT NULL,
  `학급` int DEFAULT NULL,
  PRIMARY KEY (`학생ID`),
  KEY `학년` (`학년`),
  KEY `학급` (`학급`),
  CONSTRAINT `학생_ibfk_1` FOREIGN KEY (`학년`) REFERENCES `대시보드` (`학년`),
  CONSTRAINT `학생_ibfk_2` FOREIGN KEY (`학급`) REFERENCES `대시보드` (`학급`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `학생`
--

LOCK TABLES `학생` WRITE;
/*!40000 ALTER TABLE `학생` DISABLE KEYS */;
INSERT INTO `학생` VALUES ('학생1','남자','홍길동','2000-01-01','010-1234-5678',1,1),('학생2','여자','김영희','2000-02-02','010-2345-6789',1,1),('학생3','남자','이철수','2000-03-03','010-3456-7890',1,2);
/*!40000 ALTER TABLE `학생` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-12 15:23:43
