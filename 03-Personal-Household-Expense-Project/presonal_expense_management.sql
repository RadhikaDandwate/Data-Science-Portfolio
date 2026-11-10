SELECT current_database();

-- Expense Categories Table
CREATE TABLE expense_categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL UNIQUE
);

-- Expense Subcategories
CREATE TABLE expense_subcategories (
    subcategory_id SERIAL PRIMARY KEY,
    category_id INT NOT NULL,
    subcategory_name VARCHAR(100) NOT NULL UNIQUE,
    FOREIGN KEY (category_id)
        REFERENCES expense_categories(category_id)
);

-- Family Memebers
CREATE TABLE family_members (
    member_id SERIAL PRIMARY KEY,
    member_name VARCHAR(50) NOT NULL UNIQUE
);

-- Payment Methods
CREATE TABLE payment_methods (
    payment_method_id SERIAL PRIMARY KEY,
    payment_method_name VARCHAR(50) NOT NULL UNIQUE
);

-- Vendors
CREATE TABLE vendors (
    vendor_id SERIAL PRIMARY KEY,
    vendor_name VARCHAR(100) NOT NULL UNIQUE
);

--Expenses
CREATE TABLE expenses (
    expense_id SERIAL PRIMARY KEY,
    expense_date DATE NOT NULL,
    subcategory_id INT NOT NULL,
    member_id INT NOT NULL,
    vendor_id INT NOT NULL,
    payment_method_id INT NOT NULL,
    amount NUMERIC(12,2) NOT NULL CHECK (amount > 0),
    description TEXT,
    recurring BOOLEAN NOT NULL DEFAULT FALSE,
    paid_status VARCHAR(20) NOT NULL DEFAULT 'Paid'
        CHECK (paid_status IN ('Paid', 'Pending')),

    FOREIGN KEY (subcategory_id)
        REFERENCES expense_subcategories(subcategory_id),

    FOREIGN KEY (member_id)
        REFERENCES family_members(member_id),

    FOREIGN KEY (vendor_id)
        REFERENCES vendors(vendor_id),

    FOREIGN KEY (payment_method_id)
        REFERENCES payment_methods(payment_method_id)
);

-- Quarterly budget
CREATE TABLE quarterly_budget (
    budget_id SERIAL PRIMARY KEY,
    category_id INT NOT NULL,
    budget_quarter VARCHAR(20) NOT NULL,
    previous_expense NUMERIC(12,2) NOT NULL CHECK (previous_expense >= 0),
    monthly_average NUMERIC(12,2) NOT NULL CHECK (monthly_average >= 0),
    proposed_budget NUMERIC(12,2) NOT NULL CHECK (proposed_budget >= 0),
    reason TEXT,

    FOREIGN KEY (category_id)
        REFERENCES expense_categories(category_id)
);

--Verify
SELECT * from Quarterly_budget;

---Inserting data into Tables

--Categories
INSERT INTO expense_categories (category_name) VALUES
('Household'),
('Food'),
('Farm & Animals'),
('Medical'),
('Housing'),
('Education'),
('Utilities');

-- Subcategories
INSERT INTO expense_subcategories (category_id, subcategory_name) VALUES
(1, 'Newspaper'),
(2, 'Grocery'),
(2, 'Kirana'),
(2, 'Milk'),
(3, 'Animal Food'),
(4, 'Medicines & Checkup'),
(4, 'Hospital Checkup'),
(4, 'Health Insurance'),
(5, 'Home Loan'),
(6, 'College Fees'),
(6, 'Hostel Fees'),
(6, 'Mess'),
(7, 'Phone Balance');

-- Family MEmebers
INSERT INTO family_members (member_name) VALUES
('Father'),
('Mother'),
('Grandfather'),
('Student');

-- Payment Methods
INSERT INTO payment_methods (payment_method_name) VALUES
('Cash'),
('UPI'),
('Bank Transfer');

-- Vendors
INSERT INTO vendors (vendor_name) VALUES
('Local Newspaper Vendor'),
('Local Bajar'),
('Local Milkman'),
('Kirana Store'),
('Local Store'),
('Medical Store/Clinic'),
('Hospital'),
('Mobile Recharge'),
('Home Loan Provider'),
('College'),
('College Hostel'),
('College Mess'),
('Health Insurance Provider');

--verify
SELECT * FROM expense_categories;
SELECT * FROM expense_subcategories;
SELECT * FROM family_members;
SELECT * FROM payment_methods;
SELECT * FROM vendors;

-- Temporary Table
CREATE TABLE expense_data (
    expense_id INT,
    expense_date DATE,
    category VARCHAR(50),
    subcategory VARCHAR(100),
    amount NUMERIC(12,2),
    family_member VARCHAR(50),
    vendor VARCHAR(100),
    payment_method VARCHAR(50),
    description TEXT,
    recurring BOOLEAN,
    paid_status VARCHAR(20)
        CHECK (paid_status IN ('Paid', 'Pending'))
);

-- To check the records of imported data
SELECT COUNT(*) AS total_records
FROM expense_data;

SELECT COUNT(*) FROM expense_data;


---transfer all 129 records from expense_data into the normalized expenses table.
INSERT INTO expenses (
    expense_id,
    expense_date,
    subcategory_id,
    member_id,
    vendor_id,
    payment_method_id,
    amount,
    description,
    recurring,
    paid_status
)
SELECT
    e.expense_id,
    e.expense_date,
    s.subcategory_id,
    m.member_id,
    v.vendor_id,
    p.payment_method_id,
    e.amount,
    e.description,
    e.recurring,
    e.paid_status
FROM expense_data e
JOIN expense_subcategories s
    ON LOWER(e.subcategory) = LOWER(s.subcategory_name)
JOIN family_members m
    ON LOWER(e.family_member) = LOWER(m.member_name)
JOIN vendors v
    ON LOWER(e.vendor) = LOWER(v.vendor_name)
JOIN payment_methods p
    ON LOWER(e.payment_method) = LOWER(p.payment_method_name);


-- Data Validation

--total records
SELECT COUNT(*) AS total_expenses
FROM expenses;


--Check for NULL values
SELECT COUNT(*) AS null_records
FROM expenses
WHERE expense_date IS NULL
   OR amount IS NULL
   OR subcategory_id IS NULL
   OR member_id IS NULL
   OR vendor_id IS NULL
   OR payment_method_id IS NULL;

-- check valid amounts
SELECT *
FROM expenses
WHERE amount <= 0;

--check duplicate expense ids
SELECT expense_id, COUNT(*)
FROM expenses
GROUP BY expense_id
HAVING COUNT(*) > 1;

-- check date range
SELECT MIN(expense_date) AS start_date,
       MAX(expense_date) AS end_date
FROM expenses;

-- Basic SQL Analaysis

--view expenses
SELECT *
FROM expenses;

--find expenses above 5000
SELECT *
FROM expenses
WHERE amount > 5000;

--find paid expenses above 5000
SELECT *
FROM expenses
WHERE amount > 5000
AND paid_status = 'Paid';

--find cash or UPI payments
SELECT *
FROM expenses
WHERE payment_method_id = 1
OR payment_method_id = 2;

--Unique payment methods used
SELECT DISTINCT payment_method_id
FROM expenses;

--Aggregate functions
SELECT
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_expense,
    AVG(amount) AS average_expense,
    MIN(amount) AS minimum_expense,
    MAX(amount) AS maximum_expense
FROM expenses;


--JOINS
-- To show complete expense details
SELECT
    e.expense_id,
    e.expense_date,
    c.category_name,
    s.subcategory_name,
    e.amount,
    m.member_name,
    v.vendor_name,
    p.payment_method_name
FROM expenses e
JOIN expense_subcategories s
    ON e.subcategory_id = s.subcategory_id
JOIN expense_categories c
    ON s.category_id = c.category_id
JOIN family_members m
    ON e.member_id = m.member_id
JOIN vendors v
    ON e.vendor_id = v.vendor_id
JOIN payment_methods p
    ON e.payment_method_id = p.payment_method_id;

-- Category wise expenditure
SELECT
    c.category_name,
    SUM(e.amount) AS total_expense
FROM expenses e
JOIN expense_subcategories s
    ON e.subcategory_id = s.subcategory_id
JOIN expense_categories c
    ON s.category_id = c.category_id
GROUP BY c.category_name
ORDER BY total_expense DESC;

-- Family member wise expenditure
SELECT
    m.member_name,
    SUM(e.amount) AS total_expense
FROM expenses e
JOIN family_members m
    ON e.member_id = m.member_id
GROUP BY m.member_name
ORDER BY total_expense DESC;

-- payment method wise expenditure
SELECT
    p.payment_method_name,
    SUM(e.amount) AS total_expense
FROM expenses e
JOIN payment_methods p
    ON e.payment_method_id = p.payment_method_id
GROUP BY p.payment_method_name
ORDER BY total_expense DESC;

-- CASE Classification
-- classify expenses by amount
SELECT
    expense_id,
    amount,
    CASE
        WHEN amount < 500 THEN 'Small'
        WHEN amount <= 2000 THEN 'Medium'
        WHEN amount <= 5000 THEN 'High'
        ELSE 'Very High'
    END AS expense_level
FROM expenses;

--count each expense level
SELECT
    CASE
        WHEN amount < 500 THEN 'Small'
        WHEN amount <= 2000 THEN 'Medium'
        WHEN amount <= 5000 THEN 'High'
        ELSE 'Very High'
    END AS expense_level,
    COUNT(*) AS transactions
FROM expenses
GROUP BY expense_level
ORDER BY transactions DESC;

-- Essential vs discretionary
SELECT
    c.category_name,
    CASE
        WHEN c.category_name IN
        ('Food', 'Household', 'Medical', 'Housing',
         'Education', 'Utilities', 'Farm & Animals')
        THEN 'Essential'
        ELSE 'Discretionary'
    END AS expense_type
FROM expense_categories c;

-- UNION and UNION ALL

--expenses below ₹500 and expenses above ₹5,000:
SELECT expense_id, amount
FROM expenses
WHERE amount < 500

UNION

SELECT expense_id, amount
FROM expenses
WHERE amount > 5000;

-- UNION ALL
SELECT expense_id, amount
FROM expenses
WHERE amount < 500

UNION ALL

SELECT expense_id, amount
FROM expenses
WHERE amount > 5000;

-- Date Manipulation

--Month wise Expense
SELECT
    EXTRACT(MONTH FROM expense_date) AS month,
    COUNT(*) AS transactions,
    SUM(amount) AS total_expense
FROM expenses
GROUP BY EXTRACT(MONTH FROM expense_date)
ORDER BY month;

--Month Name and Total Expense
SELECT
    TO_CHAR(expense_date, 'Month') AS month,
    SUM(amount) AS total_expense
FROM expenses
GROUP BY TO_CHAR(expense_date, 'Month'),
         EXTRACT(MONTH FROM expense_date)
ORDER BY EXTRACT(MONTH FROM expense_date);

-- Highest Spending Month
SELECT
    TO_CHAR(expense_date, 'Month') AS month,
    SUM(amount) AS total_expense
FROM expenses
GROUP BY TO_CHAR(expense_date, 'Month'),
         EXTRACT(MONTH FROM expense_date)
ORDER BY total_expense DESC
LIMIT 1;

--Lowest Spending Month
SELECT
    TO_CHAR(expense_date, 'Month') AS month,
    SUM(amount) AS total_expense
FROM expenses
GROUP BY TO_CHAR(expense_date, 'Month'),
         EXTRACT(MONTH FROM expense_date)
ORDER BY total_expense
LIMIT 1;

--Total Previous quarter expenditure
SELECT
    SUM(amount) AS quarterly_expense
FROM expenses;

--Window Functions

--Category Contribution to total expense
SELECT
    c.category_name,
    SUM(e.amount) AS category_expense,
    SUM(SUM(e.amount)) OVER () AS total_expense
FROM expenses e
JOIN expense_subcategories s
    ON e.subcategory_id = s.subcategory_id
JOIN expense_categories c
    ON s.category_id = c.category_id
GROUP BY c.category_name;

--Rank Expenses
SELECT
    expense_id,
    amount,
    RANK() OVER (ORDER BY amount DESC) AS expense_rank
FROM expenses;

--Partition By
SELECT
    c.category_name,
    s.subcategory_name,
    e.amount,
    RANK() OVER (
        PARTITION BY c.category_name
        ORDER BY e.amount DESC
    ) AS category_rank
FROM expenses e
JOIN expense_subcategories s
    ON e.subcategory_id = s.subcategory_id
JOIN expense_categories c
    ON s.category_id = c.category_id;

--to show only largest expense in each category
SELECT *
FROM (
    SELECT
        c.category_name,
        s.subcategory_name,
        e.amount,
        RANK() OVER (
            PARTITION BY c.category_name
            ORDER BY e.amount DESC
        ) AS category_rank
    FROM expenses e
    JOIN expense_subcategories s
        ON e.subcategory_id = s.subcategory_id
    JOIN expense_categories c
        ON s.category_id = c.category_id
) x
WHERE category_rank = 1;

-- To Prepare the next quarter budget

--calculate previous quarter spending
SELECT
    c.category_name,
    SUM(e.amount) AS previous_expense,
    ROUND(SUM(e.amount) / 3, 2) AS monthly_average,
    ROUND(SUM(e.amount), 2) AS proposed_budget
FROM expenses e
JOIN expense_subcategories s
    ON e.subcategory_id = s.subcategory_id
JOIN expense_categories c
    ON s.category_id = c.category_id
WHERE e.expense_date BETWEEN '2026-04-01' AND '2026-06-30'
GROUP BY c.category_name
ORDER BY previous_expense DESC;

--Insert the proposed  budget
INSERT INTO quarterly_budget
(category_id, budget_quarter, previous_expense, monthly_average, proposed_budget, reason)
SELECT
    c.category_id,
    'July-September 2026',
    SUM(e.amount),
    ROUND(SUM(e.amount) / 3, 2),
    ROUND(SUM(e.amount), 2),
    'Based on previous three-month average'
FROM expenses e
JOIN expense_subcategories s
    ON e.subcategory_id = s.subcategory_id
JOIN expense_categories c
    ON s.category_id = c.category_id
WHERE e.expense_date BETWEEN '2026-04-01' AND '2026-06-30'
GROUP BY c.category_id;

--view the budget
SELECT
    c.category_name,
    q.previous_expense,
    q.monthly_average,
    q.proposed_budget,
    q.reason
FROM quarterly_budget q
JOIN expense_categories c
ON q.category_id = c.category_id;


--Budget Adjustment

--view current budget
SELECT
    c.category_name,
    q.previous_expense,
    q.monthly_average,
    q.proposed_budget
FROM quarterly_budget q
JOIN expense_categories c
ON q.category_id = c.category_id
ORDER BY q.proposed_budget DESC;

--Update the Budget table
UPDATE quarterly_budget
SET proposed_budget = CASE
    WHEN category_id = 4 THEN 17600
    ELSE proposed_budget
END,
reason = CASE
    WHEN category_id = 1 THEN 'Keep same; fixed annual housing commitment'
    WHEN category_id = 2 THEN 'Keep as planned reserve for annual education expenses'
    WHEN category_id = 3 THEN 'Keep same; regular household food requirement'
    WHEN category_id = 4 THEN 'Increase slightly for medical contingency'
    WHEN category_id = 5 THEN 'Keep same; regular farm and animal requirement'
    WHEN category_id = 6 THEN 'Keep same; regular utility expenses'
    WHEN category_id = 7 THEN 'Keep same; essential household expenses'
END;

-- final budget
SELECT
    c.category_name,
    q.previous_expense,
    q.monthly_average,
    q.proposed_budget,
    q.reason
FROM quarterly_budget q
JOIN expense_categories c
ON q.category_id = c.category_id
ORDER BY q.proposed_budget DESC;


--Prepare the Next-Quarter Budget

--Calculate Previous Spending and Monthly Average
SELECT
    c.category_name,
    SUM(e.amount) AS previous_3_month_expense,
    ROUND(SUM(e.amount) / 3, 2) AS monthly_average,
    ROUND((SUM(e.amount) / 3) * 3, 2) AS expected_next_quarter
FROM expenses e
JOIN expense_subcategories s
    ON e.subcategory_id = s.subcategory_id
JOIN expense_categories c
    ON s.category_id = c.category_id
WHERE e.expense_date BETWEEN '2026-04-01' AND '2026-06-30'
GROUP BY c.category_name
ORDER BY previous_3_month_expense DESC;

--Budget Adjustment

--Update Medical Budget
UPDATE quarterly_budget
SET proposed_budget = 18000,
    reason = 'Increase slightly to maintain a medical contingency'
WHERE category_id = (
    SELECT category_id
    FROM expense_categories
    WHERE category_name = 'Medical'
);

--to verify
SELECT
    c.category_name,
    q.previous_expense,
    q.monthly_average,
    q.proposed_budget,
    q.reason
FROM quarterly_budget q
JOIN expense_categories c
ON q.category_id = c.category_id
ORDER BY q.proposed_budget DESC;

--Final July–September 2026 Budget

--Update the database
UPDATE quarterly_budget
SET proposed_budget = CASE
    WHEN category_id = 1 THEN 1092
    WHEN category_id = 2 THEN 30900
    WHEN category_id = 3 THEN 6000
    WHEN category_id = 4 THEN 18000
    WHEN category_id = 5 THEN 62500
    WHEN category_id = 6 THEN 27000
    WHEN category_id = 7 THEN 3000
END,
reason = CASE
    WHEN category_id = 1 THEN 'Keep same for regular household expenses'
    WHEN category_id = 2 THEN 'Keep based on regular food spending'
    WHEN category_id = 3 THEN 'Keep based on regular farm and animal expenses'
    WHEN category_id = 4 THEN 'Increase slightly for medical contingency'
    WHEN category_id = 5 THEN 'Set aside quarterly reserve for annual housing commitment'
    WHEN category_id = 6 THEN 'Include regular mess expense and reserve for annual education costs'
    WHEN category_id = 7 THEN 'Keep based on regular utility expenses'
END
WHERE budget_quarter = 'July-September 2026';

-- verify
SELECT
    c.category_name,
    q.previous_expense,
    q.monthly_average,
    q.proposed_budget,
    q.reason
FROM quarterly_budget q
JOIN expense_categories c
ON q.category_id = c.category_id
ORDER BY q.proposed_budget DESC;
