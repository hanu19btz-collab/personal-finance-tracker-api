-- Reporting queries (verified against manually calculated values)

-- 1. Income vs expenses per month
SELECT TO_CHAR(t.transaction_date, 'YYYY-MM') AS month,
       c.type,
       SUM(t.amount) AS total
FROM transactions t
JOIN categories c ON t.category_id = c.id
GROUP BY month, c.type
ORDER BY month, c.type;

-- 2. Spending by category for one month (October 2026)
SELECT c.name,
       SUM(t.amount) AS total
FROM transactions t
JOIN categories c ON t.category_id = c.id
WHERE c.type = 'expense'
  AND t.transaction_date BETWEEN '2026-10-01' AND '2026-10-31'
GROUP BY c.name
ORDER BY total DESC;

-- 3. Net balance trend per month
SELECT TO_CHAR(t.transaction_date, 'YYYY-MM') AS month,
       SUM(CASE WHEN c.type = 'income' THEN t.amount
                ELSE -t.amount END) AS net_balance
FROM transactions t
JOIN categories c ON t.category_id = c.id
GROUP BY month
ORDER BY month;
