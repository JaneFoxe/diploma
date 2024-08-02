-- Database: codeforces

-- DROP DATABASE IF EXISTS codeforces;

CREATE DATABASE codeforces
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'ru_RU.UTF-8'
    LC_CTYPE = 'ru_RU.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    TEMPLATE template0;



CREATE TABLE IF NOT EXISTS public.problem
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    id_problem character varying(20) COLLATE pg_catalog."default",
    name character varying(250) COLLATE pg_catalog."default",
    index character varying(10) COLLATE pg_catalog."default",
    url character varying(100) COLLATE pg_catalog."default",
    rating integer,
    tags character varying(250) COLLATE pg_catalog."default",
    contestid character varying(10) COLLATE pg_catalog."default",
    solvedcount integer

)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.problem
    OWNER to postgres;


CREATE TABLE IF NOT EXISTS public.problem_tags
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    id_problem character varying(20) COLLATE pg_catalog."default",
    tag character varying(100) COLLATE pg_catalog."default"

)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.problem_tags
    OWNER to postgres;
