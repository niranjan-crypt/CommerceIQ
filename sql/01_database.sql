-- ==============================================================================
-- CommerceIQ — Database & Schema Initialization (PostgreSQL)
-- File: sql/01_database.sql
-- ==============================================================================

-- 1. Database Creation (Run from postgres/default database)
-- CREATE DATABASE commerceiq
--     WITH 
--     ENCODING = 'UTF8'
--     LC_COLLATE = 'en_US.UTF-8'
--     LC_CTYPE = 'en_US.UTF-8'
--     TEMPLATE = template0;

-- 2. Schema Namespaces
-- Using schemas separates the normalized OLTP transactional layer from the 
-- denormalized Star Schema analytical mart.
CREATE SCHEMA IF NOT EXISTS oltp;
CREATE SCHEMA IF NOT EXISTS analytics;

-- 3. Search Path Configuration
SET search_path TO oltp, analytics, public;

-- 4. Custom Enumerations / Domain Types
-- Enums enforce domain integrity directly at the database engine level.

DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'order_status_type') THEN
        CREATE TYPE oltp.order_status_type AS ENUM (
            'created',
            'approved',
            'invoiced',
            'processing',
            'shipped',
            'delivered',
            'canceled',
            'unavailable'
        );
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'payment_type_enum') THEN
        CREATE TYPE oltp.payment_type_enum AS ENUM (
            'credit_card',
            'boleto',
            'voucher',
            'debit_card',
            'not_defined'
        );
    END IF;
END $$;
