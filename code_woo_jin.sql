-- Active: 1752193176455@@127.0.0.1@3306@sakila


USE sakila;

SELECT HOUR(r.rental_date) AS rental_hour,f.title AS film_title,COUNT(*) AS rental_count
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
GROUP BY rental_hour, film_title
HAVING rental_count > 1
ORDER BY rental_hour, rental_count DESC;


SELECT f.title AS film_title, r.customer_id, COUNT(*) AS total_rentals
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
GROUP BY f.title, r.customer_id
ORDER BY film_title, total_rentals DESC;
SELECT
    f.title AS film_title,
    COUNT(*) AS rental_count
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
WHERE r.customer_id IN (
    SELECT customer_id
    FROM rental
    GROUP BY customer_id
    HAVING COUNT(*) > 20
)
GROUP BY f.title
ORDER BY rental_count DESC;


SELECT *
FROM customer



