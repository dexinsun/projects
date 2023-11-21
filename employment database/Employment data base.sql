
-- 0) the name of the database on the class server in which I can find your schema
-- vinhqn1

-- 1) Create your schema

CREATE TABLE Company (
  id INT NOT NULL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  location VARCHAR(255),
  num_employees INT,
  industry VARCHAR(255),
  description TEXT
);

-- table could not be named User
CREATE TABLE UserData (
  id INT NOT NULL PRIMARY KEY,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50),
  email VARCHAR(50) NOT NULL,
  education TEXT,
  experience TEXT
);

CREATE TABLE Review (
  id INT NOT NULL PRIMARY KEY,
  description TEXT,
  rating INT NOT NULL,
  user_id INT NOT NULL,
  company_id INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES UserData(id),
  FOREIGN KEY (company_id) REFERENCES Company(id)
);

CREATE TABLE OpenPosition (
  id INT NOT NULL PRIMARY KEY,
  position VARCHAR(255) NOT NULL,
  description TEXT,
  link VARCHAR(255),
  available BOOLEAN NOT NULL,
  company_id INT NOT NULL,
  date_posted TIMESTAMP NOT NULL,
  FOREIGN KEY (company_id) REFERENCES Company(id)
);


CREATE TABLE EmployeePost (
  id INT NOT NULL PRIMARY KEY,
  position VARCHAR(255) NOT NULL,
  education TEXT,
  work_experience TEXT,
  salary FLOAT,
  date_posted TIMESTAMP NOT NULL,
  user_id INT NOT NULL,
  company_id INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES UserData(id),
  FOREIGN KEY (company_id) REFERENCES Company(id)
);


-- 2) Implement your queries

-- What are all of the companies in the biomedical industry which are located in Seattle, WA, and what is their average rating? (job seeker)
SELECT Company.name, AVG(Review.rating) AS avg_rating 
FROM Company
INNER JOIN Review ON Company.id = Review.company_id
WHERE Company.industry = 'biomedical' AND Company.location = 'Seattle, WA'
GROUP BY Company.name;

-- What is the average salary for the industry I want to apply ?（job seekers）
SELECT AVG(salary) AS avg_salary FROM job_listings WHERE industry = 'data scientists';

-- How many other companies are offering positions in the industry I want to apply for? （job seekers）
SELECT COUNT(DISTINCT company_name) AS num_companies FROM Company
INNER JOIN OpenPosition ON Company.id = OpenPosition.company_id
WHERE OpenPosition.position = 'data scientists';

-- What education qualifications (experiences) should I have for the position I want?（job seekers）
SELECT education FROM EmployeePost WHERE position = 'Data Scientist';

--  How are the average ratings of data analysts different from the tech industry and financial industry? (Jobseeker)
FROM Review r
JOIN Company c ON r.company_id = c.id
JOIN EmployeePost e ON c.id = e.company_id
WHERE position = 'Data Analysts'
AND (industry = 'tech' OR industry = 'financial')
GROUP BY position, industry


-- What’s the typical salary for applicants who have high-school level’s education in this industry? (Job seeker)
SELECT avg(salary) as typical_salary
FROM EmployeePost e
JOIN Company c ON e.company_id = c.id
WHERE education = 'High School' AND industry = 'Business Service';

-- What are the latest open positions and what company do they belong to? (job seeker) 
SELECT position, date_posted, c.name
FROM OpenPosition o
JOIN Company c ON c.id = o.company_id
WHERE o.available = TRUE
GROUP BY c.name
ORDER BY date_posted DESC
LIMIT 10;

-- What are the typical education backgrounds of employees who have posted work experience in the employee’s post? (company recruiting team or job seeker) 
SELECT education, COUNT(*) as num_employees
FROM EmployeePost
GROUP BY education
ORDER BY num_employees DESC;

-- What is the average salary in specific position for those specific industry located in New York? (job seeker)

SELECT avg(salary) as typical_salary
FROM EmployeePost e
JOIN Company c ON e.company_id = c.id
WHERE e.position = 'internship' AND
 	  c.location = 'New York' AND
	  c.industry = 'Business Service';
	  
-- How much work experience usually have for a UX researcher in Company X? (Job seeker/ HR)
SELECT work_experience
FROM EmployeePost
WHERE position = 'UX Researcher'
  AND company_id = (SELECT id FROM Company WHERE name = 'Company X');

-- 3) Select one demo query for each member of your team.  Insert enough data to show that your demo queries work.  

-- Insert statements
INSERT INTO UserData VALUES (1, 'John', 'Doe', 'johndoe@example.com', 'Bachelor of Science in Computer Science', '5 years of experience in software development');
INSERT INTO UserData VALUES (2, 'Jane', 'Smith', 'janesmith@example.com', 'Bachelor of Science in Informatics', '8 years of experience in tech marketing and sales');
INSERT INTO UserData VALUES (3, 'Bob', 'Johnson', 'bobjohnson@example.com', 'Bachelor of Science in Math', '2 years of experience in data science');

INSERT INTO Company VALUES (1, 'Microsoft', 'Redmond, WA', 100000, 'technology', NULL);
INSERT INTO Company VALUES (2, 'Amazon', 'Seattle, WA', 900800, 'retail', NULL);
INSERT INTO Company VALUES (3, 'Biotech Co.', 'Seattle, WA', 2000, 'biomedical', NULL);

INSERT INTO EmployeePost VALUES (1, 'Data Scientist', 'Bachelor of Science in Computer Science', NULL, 110000, '2022-08-15 09:30:00', 1, 1);
INSERT INTO EmployeePost VALUES (2, 'Senior Data Scientist', 'Bachelor of Science in Informatics', NULL, 140000, '2023-04-18 15:45:00', 2, 1);
INSERT INTO EmployeePost VALUES (3, 'Data Scientist', 'Bachelor of Science in Math', NULL, 120000, '2022-11-25 13:20:00', 3, 2);

INSERT INTO OpenPosition VALUES (4, 'Marketing Manager', 'Develop and execute marketing campaigns for Amazon Web Services', NULL, TRUE, 2, '2022-02-28');
INSERT INTO OpenPosition VALUES (5, 'Software Development Engineer', 'Build and scale distributed systems for Amazon Retail', NULL, FALSE, 2, '2022-03-03');
INSERT INTO OpenPosition VALUES (9, 'Quality Control Specialist', 'Perform quality control tests on drug products and raw materials', NULL, FALSE, 3, '2022-03-06');

INSERT INTO Review VALUES (1, 'I had a great experience working at Biotech Co. The team is highly skilled and passionate about their work. The management is also very supportive and provides ample opportunities for professional growth.', 4, 1, 3);
INSERT INTO Review VALUES (2, 'I really enjoyed my time at Biotech Co. The work culture is collaborative and positive. Everyone is committed to achieving our mission of improving healthcare outcomes. I highly recommend this company to anyone looking to make a difference in the biotech industry.', 5, 2, 3);

-- What are all of the companies in the biomedical industry which are located in Seattle, WA, and what is their average rating? (job seeker)
SELECT Company.name, AVG(Review.rating) AS avg_rating 
FROM Company
INNER JOIN Review ON Company.id = Review.company_id
WHERE Company.industry = 'biomedical' AND Company.location = 'Seattle, WA'
GROUP BY Company.name;

-- Q2: What is the average salary for the position I want to apply ?（job seekers）
SELECT AVG(salary) AS avg_salary FROM EmployeePost WHERE position = 'Data Scientist';

-- Q4: What education qualifications (experiences) should I have for the position I want?（job seekers）
SELECT education FROM EmployeePost WHERE position = 'Data Scientist';

--  Q7:What are the latest open positions and what company do they belong to? (job seeker) 
SELECT position, date_posted, c.name
FROM OpenPosition o
JOIN Company c ON c.id = o.company_id
WHERE o.available = TRUE
ORDER BY date_posted DESC
LIMIT 10;


