CREATE SCHEMA HR_VATAR;
USE HR_VATAR;

CREATE TABLE CandidateAccounts (
    CandidateID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100),
    Password VARCHAR(100)
);
CREATE TABLE CompanyAccounts (
    CompanyID INT AUTO_INCREMENT PRIMARY KEY,
    HRName VARCHAR(50),
    CompanyName VARCHAR(100),
    Email VARCHAR(100),
    Password VARCHAR(100)
);