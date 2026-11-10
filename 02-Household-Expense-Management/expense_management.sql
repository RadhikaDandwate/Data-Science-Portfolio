SELECT current_database();

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

SELECT * FROM expense_data;