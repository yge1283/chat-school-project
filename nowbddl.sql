CREATE DATABASE IF NOT EXISTS us;
USE us;

CREATE TABLE IF NOT EXISTS `게시판` (
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
  KEY `대시보드key` (`대시보드key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS`대시보드` (
  `대시보드key` varchar(255) NOT NULL,
  `과목명` varchar(255) DEFAULT NULL,
  `학년` int DEFAULT NULL,
  `학급` int DEFAULT NULL,
  `담당선생ID` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`대시보드key`),
  KEY `담당선생ID` (`담당선생ID`),
  KEY `idx_학년` (`학년`),
  KEY `idx_학급` (`학급`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `댓글` (
  `댓글ID` varchar(255) NOT NULL,
  `작성자ID` varchar(255) DEFAULT NULL,
  `내용` varchar(255) DEFAULT NULL,
  `댓글시간` datetime DEFAULT NULL,
  `게시물ID` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`댓글ID`),
  KEY `게시물ID` (`게시물ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `선생` (
  `선생ID` varchar(255) NOT NULL,
  `성별` varchar(255) DEFAULT NULL,
  `이름` varchar(255) DEFAULT NULL,
  `생년월일` date DEFAULT NULL,
  `이메일` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`선생ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `챗봇` (
  `시간` datetime NOT NULL,
  `학생ID` varchar(255) NOT NULL,
  `질문` varchar(255) DEFAULT NULL,
  `챗봇응답` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`시간`,`학생ID`),
  KEY `학생ID` (`학생ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `첨부파일` (
  `파일ID` varchar(255) NOT NULL,
  `게시물ID` varchar(255) DEFAULT NULL,
  `파일명` varchar(255) DEFAULT NULL,
  `파일경로` varchar(255) DEFAULT NULL,
  `시간` datetime DEFAULT NULL,
  PRIMARY KEY (`파일ID`),
  KEY `게시물ID` (`게시물ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

ALTER TABLE `게시판`
ADD CONSTRAINT `게시판_ibfk_1` FOREIGN KEY (`학생ID`) REFERENCES `학생` (`학생ID`)
IF NOT EXISTS,
ADD CONSTRAINT `게시판_ibfk_2` FOREIGN KEY (`선생ID`) REFERENCES `선생` (`선생ID`)
IF NOT EXISTS,
ADD CONSTRAINT `게시판_ibfk_3` FOREIGN KEY (`대시보드key`) REFERENCES `대시보드` (`대시보드key`)
IF NOT EXISTS;

ALTER TABLE `댓글`
ADD CONSTRAINT `댓글_ibfk_1` FOREIGN KEY (`게시물ID`) REFERENCES `게시판` (`게시물ID`)
IF NOT EXISTS;

ALTER TABLE `대시보드`
ADD CONSTRAINT `대시보드_ibfk_1` FOREIGN KEY (`담당선생ID`) REFERENCES `선생` (`선생ID`)
IF NOT EXISTS;

ALTER TABLE `챗봇`
ADD CONSTRAINT `챗봇_ibfk_1` FOREIGN KEY (`학생ID`) REFERENCES `학생` (`학생ID`)
IF NOT EXISTS;

ALTER TABLE `첨부파일`
ADD CONSTRAINT `첨부파일_ibfk_1` FOREIGN KEY (`게시물ID`) REFERENCES `게시판` (`게시물ID`)
IF NOT EXISTS;

ALTER TABLE `학생`
ADD CONSTRAINT `학생_ibfk_1` FOREIGN KEY (`학년`) REFERENCES `대시보드` (`학년`)
IF NOT EXISTS,
ADD CONSTRAINT `학생_ibfk_2` FOREIGN KEY (`학급`) REFERENCES `대시보드` (`학급`)
IF NOT EXISTS;

INSERT INTO 선생 (선생ID, 성별, 이름, 생년월일, 이메일)
VALUES ('teacher1', '남성', '홍길동', '1980-01-01', 'teacher1@example.com'),
       ('teacher2', '여성', '김영희', '1985-03-15', 'teacher2@example.com'),
       ('teacher3', '남성', '이철수', '1990-05-20', 'teacher3@example.com');

-- 대시보드 테이블에 데이터 삽입
INSERT INTO 대시보드 (대시보드key, 과목명, 학년, 학급, 담당선생ID)
VALUES ('dashboard1', '수학', 1, 1, 'teacher1'),
       ('dashboard2', '영어', 1, 2, 'teacher2'),
       ('dashboard3', '국어', 2, 1, 'teacher3');

-- 학생 테이블에 데이터 삽입
INSERT INTO 학생 (학생ID, 성별, 이름, 생년월일, 휴대폰번호, 학년, 학급)
VALUES ('student1', '여성', '김영희', '2005-03-15', '010-1234-5678', 1, 1),
       ('student2', '남성', '박철수', '2006-06-20', '010-2345-6789', 1, 2),
       ('student3', '여성', '이영자', '2007-09-25', '010-3456-7890', 2, 1);

-- 게시판 테이블에 데이터 삽입
INSERT INTO 게시판 (게시물ID, 대시보드key, 제목, 학생ID, 선생ID, 작성내용, 작성시간)
VALUES ('post1', 'dashboard1', '질문 게시물1', 'student1', 'teacher1', '질문 내용입니다.', NOW()),
       ('post2', 'dashboard2', '질문 게시물2', 'student2', 'teacher2', '질문 내용입니다.', NOW()),
       ('post3', 'dashboard3', '질문 게시물3', 'student3', 'teacher3', '질문 내용입니다.', NOW());

-- 댓글 테이블에 데이터 삽입
INSERT INTO 댓글 (댓글ID, 작성자ID, 내용, 댓글시간, 게시물ID)
VALUES ('comment1', 'student1', '답변 내용입니다.', NOW(), 'post1'),
       ('comment2', 'student2', '답변 내용입니다.', NOW(), 'post2'),
       ('comment3', 'student3', '답변 내용입니다.', NOW(), 'post3');

-- 챗봇 테이블에 데이터 삽입
INSERT INTO 챗봇 (시간, 학생ID, 질문, 챗봇응답)
VALUES (NOW(), 'student1', '질문 내용입니다.', '챗봇 응답 내용입니다.'),
       (NOW(), 'student2', '질문 내용입니다.', '챗봇 응답 내용입니다.'),
       (NOW(), 'student3', '질문 내용입니다.', '챗봇 응답 내용입니다.');

-- 첨부파일 테이블에 데이터 삽입
INSERT INTO 첨부파일 (파일ID, 게시물ID, 파일명, 파일경로, 시간)
VALUES ('file1', 'post1', '첨부파일1', '/path/to/file1', NOW()),
       ('file2', 'post2', '첨부파일2', '/path/to/file2', NOW()),
       ('file3', 'post3', '첨부파일3', '/path/to/file3', NOW());
