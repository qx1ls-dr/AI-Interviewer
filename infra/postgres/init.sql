-- Две раздельные базы (п. 4.8.1 ТЗ):
--   identity  - учётные записи, приглашения, согласия, исходные ответы;
--   analytics - только обезличенные данные, без идентификаторов пользователей.
CREATE DATABASE identity;
CREATE DATABASE analytics;

\connect analytics
CREATE EXTENSION IF NOT EXISTS vector;
