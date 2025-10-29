-- Drop existing Tables (safe reset)
DROP TABLE IF EXISTS award CASCADE;

-- Create Enums
CREATE TYPE AWARD_TYPE AS ENUM('best', 'most_sold', 'revelation');

-- Create Tables
CREATE TABLE award (
    id SERIAL PRIMARY KEY,
    year SMALLINT NOT NULL DEFAULT date_part('year', NOW()),
    award_type AWARD_TYPE NOT NULL,
    product_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL
);

CREATE TABLE review (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    rating NUMERIC(1, 0) NOT NULL CHECK(rating >= 1) CHECK(rating <=5),
    comment TEXT DEFAULT NULL,
    created TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE used_points (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    points INTEGER NOT NULL
);

CREATE TABLE loyalty (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    points INTEGER NOT NULL
);
