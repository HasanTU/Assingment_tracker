IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'assignment_system')
BEGIN
    CREATE DATABASE assignment_system;
END
GO