-- Active: 1752193176455@@127.0.0.1@3306@sakila


USE sakila;
-- 6번에 관하여
SELECT HOUR(r.rental_date) AS rental_hour,f.title AS film_title,COUNT(*) AS rental_count
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
GROUP BY rental_hour, film_title
HAVING rental_count > 1
ORDER BY rental_hour, rental_count DESC;

-- 7번에 관하여
SELECT f.title AS film_title, r.customer_id, COUNT(*) AS total_rentals
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
GROUP BY f.title, r.customer_id
HAVING COUNT(*) >1
ORDER BY film_title, total_rentals DESC;


-- 8번에 관하여
SELECT
    f.title AS film_title,
    COUNT(*) AS rental_count,
    c.name AS category_name
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category c ON fc.category_id = c.category_id
WHERE r.customer_id IN (
    SELECT customer_id
    FROM rental
    GROUP BY customer_id
    HAVING COUNT(*) > 20
)
GROUP BY f.title, c.name
ORDER BY rental_count DESC;

-- 새로운 관점

