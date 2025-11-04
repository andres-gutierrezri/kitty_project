-- -------------------
-- Base de Datos MySQL
-- -------------------

-- Consultas en la Base de Datos de MySQL

-- Consultar la versión de MySQL
SELECT VERSION() AS "Version MySQL";

-- Mostrar información sobre la conexión actual
SHOW STATUS;

-- Consultar la zona horaria
SELECT @@system_time_zone AS "Time Zone";

-- Consultar los plugins instalados
SHOW plugins;

-- Consultar las bases de datos
SHOW DATABASES;

-- Mostrar las tablas de la base de datos
-- USE `DB_NAME`;
-- SHOW tables;

-- Mostrar las tablas de todas las bases de datos
/*
SELECT TABLE_SCHEMA AS "Database", TABLE_NAME AS "Tables"
FROM information_schema.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_SCHEMA, TABLE_NAME;
*/

-- Consultar la codificación de caracteres y cotejamiento de una base de datos
/*
SELECT DEFAULT_CHARACTER_SET_NAME AS "Character Set", DEFAULT_COLLATION_NAME AS "Collation"
FROM information_schema.SCHEMATA
WHERE SCHEMA_NAME = 'DB_NAME';
*/

-- Consultar la codificación de caracteres y cotejamiento de una tabla
/*
SELECT TABLE_NAME AS "Table", CCSA.character_set_name AS "Character Set", CCSA.collation_name AS "Collation"
FROM information_schema.TABLES T
JOIN information_schema.COLLATION_CHARACTER_SET_APPLICABILITY CCSA
ON T.TABLE_COLLATION = CCSA.COLLATION_NAME
WHERE T.TABLE_SCHEMA = 'DB_NAME' AND T.TABLE_NAME = 'TABLE_NAME';
*/

-- Consultar la codificación de caracteres y cotejamiento de una columna
/*
SELECT COLUMN_NAME AS "Column", CHARACTER_SET_NAME AS "Character Set", COLLATION_NAME AS "Collation"
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = 'DB_NAME' AND TABLE_NAME = 'TABLE_NAME';
*/

-- -------------------
-- Fin del script
-- -------------------
