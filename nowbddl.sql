drop database chatbot;

CREATE DATABASE IF NOT EXISTS chatbot;
USE chatbot;
CREATE TABLE `학생` (
  `학생ID` INT NOT NULL AUTO_INCREMENT,
  `성별` varchar(255) DEFAULT NULL,
  `이름` varchar(255) DEFAULT NULL,
  `생년월일` date DEFAULT NULL,
  `휴대폰번호` varchar(255) DEFAULT NULL,
  `학년` int DEFAULT NULL,
  `학급` int DEFAULT NULL,
  PRIMARY KEY (`학생ID`),
  KEY `학년` (`학년`),
  KEY `학급` (`학급`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE IF NOT EXISTS `게시판` (
  `게시물ID` INT NOT NULL AUTO_INCREMENT,
  `대시보드key` int DEFAULT NULL,
  `제목` varchar(255) DEFAULT NULL,
  `학생ID` int DEFAULT NULL,
  `선생ID` int DEFAULT NULL,
  `작성내용` varchar(255) DEFAULT NULL,
  `작성시간` datetime DEFAULT NULL,
  PRIMARY KEY (`게시물ID`),
  KEY `학생ID` (`학생ID`),
  KEY `선생ID` (`선생ID`),
  KEY `대시보드key` (`대시보드key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS`대시보드` (
  `대시보드key` INT NOT NULL AUTO_INCREMENT,
  `과목명` varchar(255) DEFAULT NULL,
  `학년` int DEFAULT NULL,
  `학급` int DEFAULT NULL,
  `담당선생ID` int DEFAULT NULL,
  PRIMARY KEY (`대시보드key`),
  KEY `담당선생ID` (`담당선생ID`),
  KEY `idx_학년` (`학년`),
  KEY `idx_학급` (`학급`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `댓글` (
  `댓글ID` INT NOT NULL AUTO_INCREMENT,
  `작성자ID` int DEFAULT NULL,
  `내용` varchar(255) DEFAULT NULL,
  `댓글시간` datetime DEFAULT NULL,
  `게시물ID` int DEFAULT NULL,
  PRIMARY KEY (`댓글ID`),
  KEY `게시물ID` (`게시물ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `선생` (
  `선생ID` INT NOT NULL AUTO_INCREMENT,
  `성별` varchar(255) DEFAULT NULL,
  `이름` varchar(255) DEFAULT NULL,
  `생년월일` date DEFAULT NULL,
  `이메일` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`선생ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `챗봇` (
  `시간` datetime NOT NULL,
  `학생ID` int NOT NULL,
  `질문` varchar(255) DEFAULT NULL,
  `챗봇응답` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`시간`,`학생ID`),
  KEY `학생ID` (`학생ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `첨부파일` (
  `파일ID` INT NOT NULL AUTO_INCREMENT,
  `게시물ID` int DEFAULT NULL,
  `파일명` varchar(255) DEFAULT NULL,
  `파일경로` varchar(255) DEFAULT NULL,
  `시간` datetime DEFAULT NULL,
  PRIMARY KEY (`파일ID`),
  KEY `게시물ID` (`게시물ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `문제` (
  `문제번호` int NOT NULL AUTO_INCREMENT,
  `대시보드` int NOT NULL,
  `유형` varchar(255) NOT NULL,
  `문제질문` varchar(255) NOT NULL,
  `문제내용` text,
  `보기1` varchar(255) DEFAULT NULL,
  `보기2` varchar(255) DEFAULT NULL,
  `보기3` varchar(255) DEFAULT NULL,
  `보기4` varchar(255) DEFAULT NULL,
  `보기5` varchar(255) DEFAULT NULL,
  `정답` varchar(50) DEFAULT NULL,
  `문항UID` varchar(50) DEFAULT NULL,
  `빈칸개수` int DEFAULT NULL,
  `빈칸1의정답` varchar(50) DEFAULT NULL,
  `빈칸2의정답` varchar(50) DEFAULT NULL,
  `빈칸3의정답` varchar(50) DEFAULT NULL,
  `빈칸4의정답` varchar(50) DEFAULT NULL,
  `빈칸5의정답` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`문제번호`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

create table `시간표`(
	`대시보드key` int NOT NULL,
	`요일` varchar(50) NOT NULL,
    `시간` int NOT NULL,
    PRIMARY KEY (`대시보드key`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

create table `메모장`(
	`작성자id` int NOT NULL,
    `내용` varchar(50) DEFAULT NULL,
    PRIMARY KEY (`작성자id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

create table `학습 진도 현황`(
	`학생id` int NOT NULL,
    `내용` varchar(50) DEFAULT NULL,
    PRIMARY KEY (`학생id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

ALTER TABLE `게시판`
ADD CONSTRAINT `게시판_ibfk_1` FOREIGN KEY (`학생ID`) REFERENCES `학생` (`학생ID`) ON DELETE CASCADE,
ADD CONSTRAINT `게시판_ibfk_2` FOREIGN KEY (`선생ID`) REFERENCES `선생` (`선생ID`) ON DELETE CASCADE,
ADD CONSTRAINT `게시판_ibfk_3` FOREIGN KEY (`대시보드key`) REFERENCES `대시보드` (`대시보드key`);

ALTER TABLE `댓글`
ADD CONSTRAINT `댓글_ibfk_1` FOREIGN KEY (`게시물ID`) REFERENCES `게시판` (`게시물ID`) ON DELETE CASCADE;

ALTER TABLE `대시보드`
ADD CONSTRAINT `대시보드_ibfk_1` FOREIGN KEY (`담당선생ID`) REFERENCES `선생` (`선생ID`);

ALTER TABLE `챗봇`
ADD CONSTRAINT `챗봇_ibfk_1` FOREIGN KEY (`학생ID`) REFERENCES `학생` (`학생ID`) ON DELETE CASCADE;

ALTER TABLE `첨부파일`
ADD CONSTRAINT `첨부파일_ibfk_1` FOREIGN KEY (`게시물ID`) REFERENCES `게시판` (`게시물ID`) ON DELETE CASCADE;
ALTER TABLE `대시보드`
ADD INDEX `idx_학년_학급` (`학년`, `학급`);

ALTER TABLE `학생`
ADD CONSTRAINT `학생_ibfk_1` FOREIGN KEY (`학년`, `학급`) REFERENCES `대시보드` (`학년`, `학급`);

INSERT INTO 선생 (성별, 이름, 생년월일, 이메일) VALUES
('남', '이순신', '1980-01-01', '이순신@example.com'),
('여', '유관순', '1985-02-15', '유관순@example.com'),
('남', '김유신', '1990-05-20', '김유신@example.com');
INSERT INTO 대시보드 (과목명, 학년, 학급, 담당선생ID) VALUES
('수학', 1, 1, 1),
('국어', 2, 3, 2),
('영어', 3, 2, 3);
INSERT INTO 학생 (성별, 이름, 생년월일, 휴대폰번호, 학년, 학급) VALUES
('남', '홍길동', '2000-03-10', '010-1234-5678', 1, 1),
('여', '김철수', '2001-06-20', '010-5678-1234', 2, 3),
('남', '이영희', '2002-09-15', '010-9876-5432', 3, 2);
INSERT INTO 게시판 (대시보드key, 제목, 학생ID, 선생ID, 작성내용, 작성시간) VALUES
(1, '공지사항', 1, NULL, '오늘은 수업 중요한 내용을 다룹니다.', NOW()),
(2, '시험 일정 안내', NULL, 2, '다음주 수요일에 시험이 있습니다.', NOW()),
(3, '졸업식 안내', 3, NULL, '내일 졸업식이 있습니다. 참석 바랍니다.', NOW());

INSERT INTO 댓글 (작성자ID, 내용, 댓글시간, 게시물ID) VALUES
(1, '시험은 어떤 내용으로 나올까요?', NOW(), 1),
(2, '시험 장소는 어디인가요?', NOW(), 2),
(3, '졸업식 준비 잘 되었나요?', NOW(), 3);
INSERT INTO 챗봇 (시간, 학생ID, 질문, 챗봇응답) VALUES
(NOW(), 1, '수업 시간이 변경되었나요?', '네, 시간이 변경되었습니다.'),
(NOW(), 2, '다음 시험 범위가 무엇인가요?', '시험 범위는 교과서 1장부터 5장까지 입니다.'),
(NOW(), 3, '졸업식 복장은 어떻게 하나요?', '정장 착용 바랍니다.');
INSERT INTO 첨부파일 (게시물ID, 파일명, 파일경로, 시간) VALUES
(1, '자료.pdf', '/files/자료.pdf', NOW()),
(2, '시험 일정.xlsx', '/files/시험일정.xlsx', NOW()),
(3, '졸업식 안내문.docx', '/files/졸업식안내문.docx', NOW());

