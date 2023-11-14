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
  `email` varchar(50) NOT NULL,
  PRIMARY KEY (student_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES Student WRITE;
/*!40000 ALTER TABLE `Student` DISABLE KEYS */;
INSERT INTO Student VALUES (1, "JACK", NOW(), '2021-01-20');
/*!40000 ALTER TABLE `Student` ENABLE KEYS */;
UNLOCK TABLES;

-- Create TABLE 'Classroom'
CREATE TABLE Classroom (
  `classroom_id` int NOT NULL,
  `classroom_address` varchar(250) NOT NULL,
  PRIMARY KEY (classroom_id)
);

-- Create TABLE 'Teacher'
CREATE TABLE Teacher (
  `teacher_id` int NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (teacher_id)
);

-- Create TABLE 'Course'
CREATE TABLE Course (
  `course_code` varchar(8) NOT NULL,
  `name` varchar(250) NOT NULL,
  PRIMARY KEY (course_code)
);

-- Create TABLE 'CourseOffered'
CREATE TABLE CourseOffered (
  `course_id` int NOT NULL,
  `course_code` varchar(8) NOT NULL,
  `ac_year` int NOT NULL,
  `semester` int NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `lecture_day` varchar(3) NOT NULL,
  `teacher_id` int NOT NULL,
  `classroom_id` int NOT NULL,
  PRIMARY KEY (course_id),
  FOREIGN KEY (course_code) REFERENCES Course(course_code),
  FOREIGN KEY (classroom_id) REFERENCES Classroom(classroom_id),
  FOREIGN KEY (teacher_id) REFERENCES Teacher(teacher_id)
);

-- Create TABLE 'Enrolls'
CREATE TABLE Enrolls (
  `student_id` int NOT NULL,
  `course_id` int NOT NULL,
  PRIMARY KEY (student_id, course_id),
  FOREIGN KEY (student_id) REFERENCES Student(student_id),
  FOREIGN KEY (course_id) REFERENCES CourseOffered(course_id)
);

-- Create TABLE 'Lecture'
CREATE TABLE Lecture (
  `course_id` int NOT NULL,
  `lecture_id` int NOT NULL,
  `lecture_date` date NOT NULL,
  `zoom_link` varchar(250) NOT NULL,
  PRIMARY KEY (course_id, lecture_id),
  FOREIGN KEY (course_id) REFERENCES CourseOffered(course_id)
);

-- Create TABLE 'LectureTeacherMessage'
CREATE TABLE LectureTeacherMessage (
  `course_id` int NOT NULL,
  `lecture_id` int NOT NULL,
  `message_id` int NOT NULL,
  `message` varchar(250) NOT NULL,
  PRIMARY KEY (course_id, lecture_id, message_id),
  FOREIGN KEY (course_id) REFERENCES Course(course_id),
  FOREIGN KEY (lecture_id) REFERENCES Lecture(lecture_id)
);

-- Create TABLE 'Material'
CREATE TABLE Material (
  `course_id` int NOT NULL,
  `material_name` varchar(250) NOT NULL,
  `material_link` varchar(250) NOT NULL,
  PRIMARY KEY (course_id),
  FOREIGN KEY (course_id) REFERENCES CourseOffered(course_id)
);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
