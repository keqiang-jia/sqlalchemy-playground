SELECT sales.id AS sales_id, sales.product_id AS sales_product_id, sales.customer_id AS sales_customer_id, sales.store_id AS sales_store_id, sales.quantity AS sales_quantity, sales.total_price AS sales_total_price, customers.id AS customers_id, customers.name AS customers_name, customers.email AS customers_email, products.id AS products_id, products.name AS products_name, products.price AS products_price, stores.id AS stores_id, stores.name AS stores_name, stores.location AS stores_location, products_1.id AS products_1_id, products_1.name AS products_1_name, products_1.price AS products_1_price, customers_1.id AS customers_1_id, customers_1.name AS customers_1_name, customers_1.email AS customers_1_email, stores_1.id AS stores_1_id, stores_1.name AS stores_1_name, stores_1.location AS stores_1_location
FROM sales JOIN customers ON customers.id = sales.customer_id JOIN products ON products.id = sales.product_id JOIN stores ON stores.id = sales.store_id LEFT OUTER JOIN products AS products_1 ON products_1.id = sales.product_id LEFT OUTER JOIN customers AS customers_1 ON customers_1.id = sales.customer_id LEFT OUTER JOIN stores AS stores_1 ON stores_1.id = sales.store_id
WHERE
(lower(customers.name) LIKE lower(?)
    OR lower(products.name) LIKE lower(?)
    OR lower(stores.name) LIKE lower(?))
AND (lower(customers.name) LIKE lower(?)
    OR lower(products.name) LIKE lower(?)
    OR lower(stores.name) LIKE lower(?))