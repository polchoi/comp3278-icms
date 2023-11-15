INSERT INTO Student
VALUES 
    ("Steve Huh", "03:59:21", "2023-10-12", "steveh@icms.edu.hk"),
    ("Paul Choi", "12:01:11", "2023-10-12", "paulc@icms.edu.hk"),
    ("Joon Moon", "08:26:48", "2023-10-12", "joonm@icms.edu.hk"),
    ("Siwoo Kim", "15:36:57", "2023-10-12", "siwook@icms.edu.hk"),
    ("Hyunwoo Kang", "19:12:10", "2023-10-12", "hyunk@icms.edu.hk");

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
    ("COMP3278", "2023-2024", "1", "13:30:00", "15:20:00", "MON", 1, 2),
    ("COMP3230", "2023-2024", "1", "10:30:00", "12:20:00", "THU", 2, 1),
    ("COMP3270", "2023-2024", "1", "15:30:00", "16:20:00", "TUE", 1, 3),
    ("FINA2382", "2023-2024", "1", "13:30:00", "14:20:00", "WED", 6, 4),
    ("KORE1001", "2023-2024", "1", "09:30:00", "10:20:00", "FRI", 4, 3),
    ("ENGG1330", "2023-2024", "1", "11:30:00", "13:20:00", "MON", 8, 5),
    ("COMP3358", "2023-2024", "1", "16:30:00", "17:20:00", "WED", 3, 1),
    ("ACCT1101", "2023-2024", "1", "14:30:00", "16:20:00", "THU", 5, 5),
    ("COMP3358", "2023-2024", "1", "09:30:00", "11:20:00", "TUE", 7, 4),
    ("COMP3351", "2023-2024", "2", "11:30:00", "12:20:00", "MON", 3, 5),
    ("COMP3278", "2022-2023", "1", "13:30:00", "15:20:00", "TUE", 1, 2),
    ("ECON2280", "2022-2023", "1", "12:30:00", "14:20:00", "MON", 6, 4),
    ("ACCT1101", "2022-2023", "2", "09:30:00", "11:20:00", "THU", 5, 5);
