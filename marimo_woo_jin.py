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
    _df = mo.sql(
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
    return


if __name__ == "__main__":
    app.run()
