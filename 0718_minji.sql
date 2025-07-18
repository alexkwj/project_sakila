
use sakila;

-- 대여횟수 순위
CREATE OR REPLACE VIEW 대여순위 AS 
SELECT F.film_id, F.title, count(R.rental_id) 대여횟수
FROM inventory I
JOIN rental R USING (inventory_id)
JOIN film F USING (film_id)
GROUP BY film_id;


CREATE OR REPLACE VIEW 카테고리 AS 
SELECT F.film_id, F.title, C.name
FROM film F
JOIN film_category FC USING (film_id)
JOIN category C USING (category_id);




SELECT *
FROM 대여순위;

SELECT *
FROM 카테고리;


SELECT 카테고리.film_id, 카테고리.title, 카테고리.name, 대여순위.대여횟수
FROM 카테고리
JOIN 대여순위 USING (film_id)
ORDER BY 대여횟수 DESC;


