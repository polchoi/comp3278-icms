INSERT INTO Student
VALUES 
    (1, "Steve Huh", "03:59:21", "2023-10-12", "steveh@icms.edu.hk"),
    (2, "Paul Choi", "12:01:11", "2023-10-12", "paulc@icms.edu.hk"),
    (3, "Joon Moon", "08:26:48", "2023-10-12", "joonm@icms.edu.hk"),
    (4, "Siwoo Kim", "15:36:57", "2023-10-12", "siwook@icms.edu.hk"),
    (5, "Hyunwoo Kang", "19:12:10", "2023-10-12", "hyunk@icms.edu.hk");

INSERT INTO Classroom
VALUES
    (1, "Knowles Building KB223"),
    (2, "Meng Wah Complex MWT1"),
    (3, "T. T. Tsui Building TT404"),
    (4, "Main Building MB201"),
    (5, "Centennial Campus Grand Hall");

INSERT INTO Teacher
VALUES
    (1, "Linda Isabela"),
    (2, "Thomas Phelix"),
    (3, "Henry Casimiro"),
    (4, "Calvin Choi"),
    (5, "Karl Hamil"),
    (6, "Thomas Heo"),
    (7, "James Wu"),
    (8, "Albert Scott");

INSERT INTO Course
VALUES
    ("COMP3278", "Introduction to database management systems"),
    ("ECON2280", "Introductory Econometrics"),
    ("KORE1001", "Korean I"),
    ("FINA2382", "International Finance Management"),
    ("ENGG1330", "Computer Programming I"),
    ("COMP3230", "Principles of Operating Systems"),
    ("COMP3358", "Distributed and Parallel Computing"),
    ("COMP3270", "Artificial Intelligence"),
    ("COMP3351", "Advanced Algorithm Analysis"),
    ("ACCT1101", "Introduction to Financial Accounting");

INSERT INTO CourseOffered
VALUES
    (1, "COMP3278", "2022-2023", "1", "13:30:00", "15:20:00", "TUE", 1, 2),
    (2, "ECON2280", "2022-2023", "1", "12:30:00", "14:20:00", "MON", 6, 4),
    (3, "ACCT1101", "2022-2023", "2", "09:30:00", "11:20:00", "THU", 5, 5),
    (4, "COMP3278", "2023-2024", "1", "13:30:00", "15:20:00", "MON", 1, 2),
    (5, "COMP3230", "2023-2024", "1", "10:30:00", "12:20:00", "THU", 2, 1),
    (6, "COMP3270", "2023-2024", "1", "15:30:00", "16:20:00", "TUE", 1, 3),
    (7, "FINA2382", "2023-2024", "1", "13:30:00", "14:20:00", "WED", 6, 4),
    (8, "KORE1001", "2023-2024", "1", "09:30:00", "10:20:00", "FRI", 4, 3),
    (9, "ENGG1330", "2023-2024", "1", "11:30:00", "13:20:00", "MON", 8, 5),
    (10, "COMP3358", "2023-2024", "1", "16:30:00", "17:20:00", "WED", 3, 1),
    (11, "ACCT1101", "2023-2024", "1", "14:30:00", "16:20:00", "THU", 5, 5),
    (12, "COMP3358", "2023-2024", "1", "09:30:00", "11:20:00", "TUE", 7, 4),
    (13, "COMP3351", "2023-2024", "2", "11:30:00", "12:20:00", "MON", 3, 5),
    (14, "ECON2280", "2023-2024", "2", "13:30:00", "15:20:00", "WED", 6, 2);

INSERT INTO Enrolls
VALUES
    (1, 4),
    (2, 5),
    (3, 6),
    (4, 7),
    (5, 8);

INSERT INTO Lecture
VALUES
    (4, 1, "2023-09-05", "www.zoom.com/comp3278-1"),
    (5, 2, "2023-09-08", "www.zoom.com/comp3230-1"),
    (6, 3, "2023-09-13", "www.zoom.com/comp3270-1"),
    (7, 4, "2023-09-14", "www.zoom.com/fina2382-1"),
    (8, 5, "2023-09-16", "www.zoom.com/kore1001-1");

INSERT INTO LectureTeacherMessage
VALUES
    (4, 1, 1, "Welcome to COMP 3278!"),
    (5, 2, 1, "Welcome to COMP 3230!"),
    (6, 3, 1, "Welcome to COMP 3270!"),
    (7, 4, 1, "Welcome to FINA 2382!"),
    (8, 5, 1, "Welcome to KORE 1001!");

INSERT INTO Material
VALUES
    (4, "COMP3278-Lecture Notes-1", "www.icms.com/comp3278/lecture-notes-1"),
    (5, "COMP3230-Lecture Notes-1", "www.icms.com/comp3230/lecture-notes-1"),
    (6, "COMP3270-Lecture Notes-1", "www.icms.com/comp3270/lecture-notes-1"),
    (7, "FINA2382-Lecture Notes-1", "www.icms.com/fina2382/lecture-notes-1"),
    (8, "KORE1001-Lecture Notes-1", "www.icms.com/kore1001/lecture-notes-1"),
    (4, "COMP3278-Tutorial Notes-1", "www.icms.com/comp3278/tutorial-notes-1"),
    (5, "COMP3230-Tutorial Notes-1", "www.icms.com/comp3230/tutorial-notes-1"),
    (6, "COMP3270-Tutorial Notes-1", "www.icms.com/comp3270/tutorial-notes-1"),
    (7, "FINA2382-Tutorial Notes-1", "www.icms.com/fina2382/tutorial-notes-1"),
    (8, "KORE1001-Tutorial Notes-1", "www.icms.com/kore1001/tutorial-notes-1");
