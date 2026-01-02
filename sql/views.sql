
CREATE VIEW vw_books_overview AS
SELECT
    b.id,
    b.title,
    a.name AS author,
    b.price,
    b.available,
    b.published_date
FROM book b
JOIN author a ON b.author_id = a.id;


CREATE VIEW vw_loan_report AS
SELECT
    u.full_name,
    COUNT(l.id) AS total_loans,
    SUM(CASE WHEN l.returned = 0 THEN 1 ELSE 0 END) AS active_loans,
    MAX(l.loan_date) AS last_loan_date
FROM library_user u
LEFT JOIN loan l ON u.id = l.user_id
GROUP BY u.full_name;

