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

CREATE TABLE `선생` (
  `선생ID` varchar(255) NOT NULL,
  `성별` varchar(255) DEFAULT NULL,
  `이름` varchar(255) DEFAULT NULL,
  `생년월일` date DEFAULT NULL,
  `이메일` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`선생ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `챗봇` (
  `시간` datetime NOT NULL,
  `학생ID` varchar(255) NOT NULL,
  `질문` varchar(255) DEFAULT NULL,
  `챗봇응답` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`시간`,`학생ID`),
  KEY `학생ID` (`학생ID`),
  CONSTRAINT `챗봇_ibfk_1` FOREIGN KEY (`학생ID`) REFERENCES `학생` (`학생ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
