import marimo

__generated_with = "0.14.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import os
    import sqlalchemy

    _password = os.environ.get("MYSQL_PASSWORD", "Boss2070!")
    DATABASE_URL = f"mysql+pymysql://root:{_password}@127.0.0.1:3306/MYSQL"
    engine = sqlalchemy.create_engine(DATABASE_URL)
    return (engine,)


@app.cell
def _(engine, mo):
    _df = mo.sql(
        f"""
        USE sakila;
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo):
    _df = mo.sql(
        f"""
        SELECT DATABASE();
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, film, inventory, mo, rental):
    _df = mo.sql(
        f"""
        SELECT HOUR(r.rental_date) AS rental_hour,f.title AS film_title,COUNT(*) AS rental_count
        FROM rental r
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film f ON i.film_id = f.film_id
        GROUP BY rental_hour, film_title
        HAVING rental_count > 1
        ORDER BY rental_hour, rental_count DESC;
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, film, inventory, mo, rental):
    _df = mo.sql(
        f"""
        SELECT f.title AS film_title, r.customer_id, COUNT(*) AS total_rentals
        FROM rental r
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film f ON i.film_id = f.film_id
        GROUP BY f.title, r.customer_id
        having COUNT(*) >1
        ORDER BY film_title, total_rentals DESC;
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, film, inventory, mo, rental):
    _df = mo.sql(
        f"""
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
        """,
        engine=engine
    )
    return


@app.cell
def _(category, engine, film, film_category, inventory, mo, rental):
    db = mo.sql(
        f"""
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
        """,
        engine=engine
    )
    return (db,)


@app.cell
def _(db):
    db["category_name"].value_counts()
    return


@app.cell
def _(customer, engine, mo, rental):
    _df = mo.sql(
        f"""
        SELECT count(*)
        FROM customer c
        left join rental r
        ON c.customer_id = r.customer_id;
        """,
        engine=engine
    )
    return


@app.cell
def _(customer, engine, mo, rental):
    _df = mo.sql(
        f"""
        SELECT c.customer_id, count(*), c.first_name,c.last_name
        FROM rental r
        join customer c
        on c.customer_id = r.customer_id
        group by c.customer_id
        order by count(*) DESC;
        -- 영화 빌린 횟수 확인 148 번과 526 번 확인하면 좋겠다를 확인
        """,
        engine=engine
    )
    return


@app.cell
def _(customer, engine, film, inventory, mo, rental):
    _df = mo.sql(
        f"""
        SELECT r.rental_date,r.return_date , TIMESTAMPDIFF(DAY,r.rental_date,r.return_date) AS diff,f.title
        FROM rental r
        join customer c
        on c.customer_id = r.customer_id
        join inventory i
        on i.inventory_id = r.inventory_id
        join film f
        on f.film_id = i.film_id
        where c.customer_id = 148
        order by diff desc;
        """,
        engine=engine
    )
    return


@app.cell
def _(customer, engine, film, inventory, mo, rental):
    _df = mo.sql(
        f"""
        SELECT f.title,count(*)
        FROM rental r
        join customer c
        on c.customer_id = r.customer_id
        join inventory i
        on i.inventory_id = r.inventory_id
        join film f
        on f.film_id = i.film_id
        where c.customer_id = 148
        group by f.title
        order by count(*) desc;
        """,
        engine=engine
    )
    return


@app.cell
def _(category, customer, engine, film, film_category, inventory, mo, rental):
    _df = mo.sql(
        f"""
        SELECT cat.name,count(*)
        FROM rental r
        join customer c
        on c.customer_id = r.customer_id
        join inventory i
        on i.inventory_id = r.inventory_id
        join film f
        on f.film_id = i.film_id
        join film_category fc
        on fc.film_id = f.film_id
        join category cat
        on cat.category_id =fc.category_id
        where c.customer_id = 148
        group by cat.name
        order by count(*) DESC;

        -- 158번의 어떤카테고리를 봤냐를 볼 수 있다!
        """,
        engine=engine
    )
    return


@app.cell
def _(
    actor,
    category,
    customer,
    engine,
    film,
    film_actor,
    film_category,
    inventory,
    mo,
    rental,
):
    _df = mo.sql(
        f"""
        SELECT 
            act.first_name,
            act.last_name,
            COUNT(*)
        FROM 
            rental r
        JOIN customer c ON c.customer_id = r.customer_id
        JOIN inventory i ON i.inventory_id = r.inventory_id
        JOIN film f ON f.film_id = i.film_id
        JOIN film_category fc ON fc.film_id = f.film_id
        JOIN category cat ON cat.category_id = fc.category_id
        JOIN film_actor fa ON f.film_id = fa.film_id
        JOIN actor act ON fa.actor_id = act.actor_id
        WHERE c.customer_id = 148
        GROUP BY act.first_name, act.last_name
        order by count(*) DESC;
        """,
        engine=engine
    )
    return


@app.cell
def _(category, engine, film, film_category, inventory, mo, rental):
    _df = mo.sql(
        f"""
        SELECT
            c.name AS category_name,
            COUNT(*) AS rental_count
        FROM rental r
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film f ON i.film_id = f.film_id
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category c ON fc.category_id = c.category_id
        GROUP BY c.name
        ORDER BY rental_count DESC;
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, film, inventory, mo, rental):
    _df = mo.sql(
        f"""
        SELECT f.title, COUNT(*) AS times_rented
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
        ORDER BY times_rented DESC
        LIMIT 10;

        """,
        engine=engine
    )
    return


@app.cell
def _(category, engine, film_category, inventory, mo, rental):
    _df = mo.sql(
        f"""
        SELECT
            HOUR(r.rental_date) AS rental_hour,
            c.name AS category,
            COUNT(*) AS rental_count
        FROM rental r
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film_category fc ON i.film_id = fc.film_id
        JOIN category c ON fc.category_id = c.category_id
        GROUP BY rental_hour, category
        ORDER BY rental_hour, rental_count DESC;

        """,
        engine=engine
    )
    return


@app.cell
def _(category, engine, film_category, inventory, mo, rental):
    _df = mo.sql(
        f"""
        SELECT rental_hour, category, rental_count
        FROM (
            SELECT
                HOUR(r.rental_date) AS rental_hour,
                c.name AS category,
                COUNT(*) AS rental_count,
                ROW_NUMBER() OVER (
                    PARTITION BY HOUR(r.rental_date)
                    ORDER BY COUNT(*) DESC
                ) AS rn
            FROM rental r
            JOIN inventory i ON r.inventory_id = i.inventory_id
            JOIN film_category fc ON i.film_id = fc.film_id
            JOIN category c ON fc.category_id = c.category_id
            GROUP BY rental_hour, category
        ) ranked
        WHERE rn = 1
        ORDER BY rental_hour;

        """,
        engine=engine
    )
    return


if __name__ == "__main__":
    app.run()
