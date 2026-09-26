-- Product performance
SELECT
    Product,
    Category,
    COUNT(DISTINCT Order_ID) AS orders,
    SUM(Quantity) AS units_sold,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit
FROM sales
GROUP BY Product, Category
ORDER BY total_sales DESC;


-- Most profitable products
SELECT
    Product,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND(
        SUM(Profit) * 100.0 / SUM(Sales),
        2
    ) AS profit_margin_percent
FROM sales
GROUP BY Product
ORDER BY total_profit DESC;


-- Category profitability
SELECT
    Category,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND(
        SUM(Profit) * 100.0 / SUM(Sales),
        2
    ) AS profit_margin_percent
FROM sales
GROUP BY Category
ORDER BY total_profit DESC;