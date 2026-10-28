-- Test data: 6 categories and 15 transactions (August–October 2026)

INSERT INTO categories (name, type)
VALUES
    ('Salary', 'income'),
    ('Freelance', 'income'),
    ('Rent', 'expense'),
    ('Groceries', 'expense'),
    ('Transport', 'expense'),
    ('Entertainment', 'expense');

INSERT INTO transactions (category_id, amount, description, transaction_date)
VALUES
    (1, 2200.00, 'Monthly salary', '2026-08-01'),
    (3, 850.00, 'Rent August', '2026-08-02'),
    (4, 64.30, 'Weekly shop', '2026-08-09'),
    (5, 45.00, 'Bus pass', '2026-08-10'),
    (6, 30.00, 'Cinema', '2026-08-22'),
    (1, 2200.00, 'Monthly salary', '2026-09-01'),
    (3, 850.00, 'Rent September', '2026-09-02'),
    (5, 45.00, 'Bus pass', '2026-09-10'),
    (4, 71.85, 'Weekly shop', '2026-09-13'),
    (2, 300.00, 'Website project', '2026-09-18'),
    (1, 2200.00, 'Monthly salary', '2026-10-01'),
    (3, 850.00, 'Rent October', '2026-10-02'),
    (4, 58.20, 'Weekly shop', '2026-10-04'),
    (6, 18.50, 'Streaming subscription', '2026-10-05'),
    (5, 12.40, 'Taxi', '2026-10-07');
