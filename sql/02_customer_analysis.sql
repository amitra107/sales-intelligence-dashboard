-- Top 10 customers by revenue
SELECT
    Customer_ID,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    COUNT(DISTINCT Order_ID) AS total_orders
FROM sales
GROUP BY Customer_ID
ORDER BY total_sales DESC
LIMIT 10;


-- Customers with the highest profit
SELECT
    Customer_ID,
    ROUND(SUM(Profit), 2) AS total_profit,
    COUNT(DISTINCT Order_ID) AS total_orders
FROM sales
GROUP BY Customer_ID
ORDER BY total_profit DESC
LIMIT 10;


-- Average customer order value
SELECT
    Customer_ID,
    COUNT(DISTINCT Order_ID) AS total_orders,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(
        SUM(Sales) / COUNT(DISTINCT Order_ID),
        2
    ) AS average_order_value
FROM sales
GROUP BY Customer_ID
ORDER BY average_order_value DESC
LIMIT 10;