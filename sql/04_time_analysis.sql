-- Monthly sales and profit
SELECT
    Year,
    Month,
    Month_Name,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit
FROM sales
GROUP BY Year, Month, Month_Name
ORDER BY Year, Month;


-- Monthly order volume
SELECT
    Year,
    Month,
    COUNT(DISTINCT Order_ID) AS total_orders
FROM sales
GROUP BY Year, Month
ORDER BY Year, Month;


-- Regional performance
SELECT
    Region,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    COUNT(DISTINCT Order_ID) AS total_orders
FROM sales
GROUP BY Region
ORDER BY total_sales DESC;