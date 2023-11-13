-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Feb 17, 2020 at 09:41 PM
-- Server version: 5.7.28-0ubuntu0.18.04.4
-- PHP Version: 7.2.24-0ubuntu0.18.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `facerecognition`
--

-- --------------------------------------------------------

--
-- Table structure for table `Student`
--
DROP TABLE IF EXISTS Student;

-- Create TABLE 'Student'
CREATE TABLE Student (
  `student_id` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `login_time` time NOT NULL,
  `login_date` date NOT NULL,
  PRIMARY KEY (student_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES Student WRITE;
/*!40000 ALTER TABLE `Student` DISABLE KEYS */;
INSERT INTO Student VALUES (1, "JACK", NOW(), '2021-01-20');
/*!40000 ALTER TABLE `Student` ENABLE KEYS */;
UNLOCK TABLES;

CREATE TABLE Teacher (
  `teacher_id` int NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (teacher_id)
);

-- Create TABLE 'Classroom'
CREATE TABLE Classroom (
  `classroom_id` int NOT NULL,
  `classroom_address` varchar(250) NOT NULL,
  PRIMARY KEY (classroom_id)
);

-- Create TABLE 'Course'
CREATE TABLE Course (
  'course_code' varchar(8) NOT NULL,
  `name` varchar(250) NOT NULL,
  `lecture_day` varchar(3) NOT NULL,
  `start_time` time NOT NULL,
  `classroom_id` int NOT NULL,
  `teacher_id` int NOT NULL,
  PRIMARY KEY (course_code),
  FOREIGN KEY (classroom_id) REFERENCES Classroom(classroom_id),
  FOREIGN KEY (teacher_id) REFERENCES Teacher(teacher_id)
);

CREATE TABLE TeacherMessage (
  `message_id` int NOT NULL,
  `course_code` int NOT NULL,
  `message` varchar(250) NOT NULL,
  `date_sent` date NOT NULL,
  `time_sent` time NOT NULL,
  PRIMARY KEY (message_id, course_code),
  FOREIGN KEY (course_code) REFERENCES ㄴCourse(course_code)
);

CREATE TABLE Enrollment (
  `student_id` int NOT NULL,
  `course_id` int NOT NULL,
  PRIMARY KEY (student_id, course_id),
  FOREIGN KEY (student_id) REFERENCES Student(student_id),
  FOREIGN KEY (course_id) REFERENCES Course(course_id)
);

CREATE TABLE Lecture (
  `lecture_id` int NOT NULL,
  `course_id` int NOT NULL,
  `lecture_date` date NOT NULL,
  PRIMARY KEY (lecture_id),
  FOREIGN KEY (course_id) REFERENCES Course(course_id)
);

CREATE TABLE LectureFile (
  `material_id` int NOT NULL,
  `lecture_id` int NOT NULL,
  `file_name` varchar(250) NOT NULL,
  `file_type` varchar(250) NOT NULL,
  `file_size` int NOT NULL,
  PRIMARY KEY (material_id, lecture_id),
  FOREIGN KEY (lecture_id) REFERENCES Lecture(lecture_id)
);

CREATE TABLE LectureZoomLink (
  `lecture_id` int NOT NULL,
  `zoom_link` varchar(250) NOT NULL,
  PRIMARY KEY (zoom_link)
);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
