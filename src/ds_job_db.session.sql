-- @block

CREATE TABLE job_post_links (
    id INT PRIMARY KEY,
    job_url VARCHAR (255)
);

CREATE TABLE job_postings (
    id INT PRIMARY KEY,
    job_post_link_id INT,
    job_title VARCHAR (255),
    company_name VARCHAR (255),
    country VARCHAR (50),
    location VARCHAR (100),
    min_salary INT,
    max_salary INT,
    job_description TEXT
);

-- @block

ALTER TABLE job_post_links ADD COLUMN country VARCHAR (50);

-- @block
SHOW VARIABLES LIKE 'local_infile';

-- @block
ALTER TABLE job_post_links MODIFY ID INT NOT NULL AUTO_INCREMENT;

-- @block
SELECT * FROM job_post_links;

-- @block
-- Identify duplicate job URLs in the job_post_links table
SELECT job_url, COUNT(*) from job_post_links
GROUP BY job_url
HAVING COUNT(job_url) > 1;

-- @block
ALTER TABLE job_postings MODIFY id INT NOT NULL AUTO_INCREMENT;

-- @block
ALTER TABLE job_postings
DROP COLUMN country;

-- @block
ALTER TABLE job_postings ADD COLUMN post_date VARCHAR(30);

-- @block
SELECT * FROM job_postings;





