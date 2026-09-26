-- Total sales
SELECT
    SUM(Sales) AS total_sales
FROM sales;


-- Total profit
SELECT
    SUM(Profit) AS total_profit
FROM sales;


-- Total orders
SELECT
    COUNT(DISTINCT Order_ID) AS total_orders
FROM sales;


-- Average order value
SELECT
    AVG(Sales) AS average_order_value
FROM sales;


-- Sales by region
SELECT
    Region,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit
FROM sales
GROUP BY Region
ORDER BY total_sales DESC;


-- Sales by category
SELECT
    Category,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit
FROM sales
GROUP BY Category
ORDER BY total_sales DESC;