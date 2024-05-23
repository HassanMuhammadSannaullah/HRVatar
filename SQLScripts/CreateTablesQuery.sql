-- CREATE SCHEMA HR_VATAR;
USE HR_VATAR;

-- CREATE TABLE CandidateAccounts (
--     CandidateID INT AUTO_INCREMENT PRIMARY KEY,
--     FirstName VARCHAR(50),
--     LastName VARCHAR(50),
--     Email VARCHAR(100),
--     Password VARCHAR(100),
--     profileimage BLOB -- Assuming you want to store images as binary data
-- );
-- CREATE TABLE CompanyAccounts (
--     CompanyID INT AUTO_INCREMENT PRIMARY KEY,
--     HRName VARCHAR(50),
--     CompanyName VARCHAR(100),
--     Email VARCHAR(100),
--     Password VARCHAR(100),
-- 	profileimage BLOB
-- );

-- ALTER TABLE CandidateAccounts
-- MODIFY COLUMN profileimage LONGBLOB;

-- ALTER TABLE CompanyAccounts
-- MODIFY COLUMN profileimage LONGBLOB;


-- CREATE TABLE jobs (
--     CompanyID INT,
--     JobPosition VARCHAR(255),
--     Description TEXT,
--     CandidateRequirement TEXT,
--     PostedOnLinkedIn ENUM('yes', 'no'),
--     StillHiring ENUM('yes', 'no')
-- );

ALTER TABLE jobs
ADD COLUMN jobid INT AUTO_INCREMENT PRIMARY KEY FIRST;