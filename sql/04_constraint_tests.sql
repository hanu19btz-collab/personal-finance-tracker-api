-- Constraint tests – BOTH statements are expected to FAIL

-- Test 1: foreign key – category 99 does not exist
-- Expected: ERROR 23503 violates foreign key constraint "transactions_category_id_fkey"
INSERT INTO transactions (category_id, amount, transaction_date)
VALUES (99, 10.00, '2026-10-08');

-- Test 2: CHECK constraint – negative amount
-- Expected: ERROR 23514 violates check constraint "transactions_amount_check"
INSERT INTO transactions (category_id, amount, transaction_date)
VALUES (4, -5.00, '2026-10-08');
