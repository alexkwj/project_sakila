-- Active: 1752194844357@@127.0.0.1@3306@sakila
USE sakila;

--나라별대여순위
SELECT 
    co.country,
    COUNT(*) AS rental_count
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category cat ON fc.category_id = cat.category_id
JOIN customer c ON r.customer_id = c.customer_id
JOIN address a ON c.address_id = a.address_id
JOIN city ci ON a.city_id = ci.city_id
JOIN country co ON ci.country_id = co.country_id
GROUP BY co.country
ORDER BY rental_count DESC;

-- 나라별 top3 카테고리
CREATE OR REPLACE VIEW rental_category_country_view AS
SELECT
    r.rental_id,
    co.country,
    cat.name AS category_name
FROM rental AS r
JOIN inventory AS i ON r.inventory_id = i.inventory_id
JOIN film AS f ON i.film_id = f.film_id
JOIN film_category AS fc ON f.film_id = fc.film_id
JOIN category AS cat ON fc.category_id = cat.category_id
JOIN customer AS cu ON r.customer_id = cu.customer_id
JOIN address AS a ON cu.address_id = a.address_id
JOIN city AS ci ON a.city_id = ci.city_id
JOIN country AS co ON ci.country_id = co.country_id;

CREATE OR REPLACE VIEW country_category_rental_count_view AS
SELECT
    country,
    category_name,
    COUNT(*) AS rental_count
FROM rental_category_country_view
GROUP BY country, category_name;

CREATE OR REPLACE VIEW top3_category_by_country_view AS
SELECT
    country,
    category_name,
    rental_count
FROM (
    SELECT
        country,
        category_name,
        rental_count,
        RANK() OVER (PARTITION BY country ORDER BY rental_count DESC) AS rnk
    FROM country_category_rental_count_view
) ranked
WHERE rnk <= 3;

SELECT * 
FROM top3_category_by_country_view
ORDER BY country, rental_count DESC;

SELECT * FROM top3_category_by_country_view
WHERE rental_count >20
ORDER BY country, rental_count DESC;

-- 영화별 재고수량
SELECT f.title, COUNT(i.inventory_id) AS 재고수량
FROM inventory AS i
JOIN film AS f USING(film_id)
GROUP BY f.title
ORDER BY 재고수량 DESC;

SELECT f.title, f.replacement_cost
FROM film AS f;
