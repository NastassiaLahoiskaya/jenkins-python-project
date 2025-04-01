import pytest
import pymssql


# Параметры подключения
server = '192.168.1.248'
port = 1433
database = 'TRN'
username = "dbo_user"
password = "@11dbo_user_for_RF"

@pytest.fixture(scope="module")
def db_connection():
    connection = None
    try:
        # Подключение к SQL Server через pymssql
        connection = pymssql.connect(
            server=server,
            port=port,
            user=username,
            password=password,
            database=database
        )
        print("Connection successful!")
        yield connection
    except pymssql.OperationalError as e:
        print(f"OperationalError: {e}")
        pytest.fail("Unable to connect to the database.")
    finally:
        if connection:
            connection.close()
            print("Connection closed.")

# Test Case 1: Number of countries by region ID
def test_number_of_countries_by_region_id(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT region_id, COUNT(*) FROM [hr].[countries] GROUP BY region_id;")
    result = cursor.fetchall()
    print(f"Result: {result}")
    assert len(result) > 0, "The query result is empty (failed check for region_id and country counts)."

# Test Case 2: Australia exists as a country
def test_australia_exists_as_country(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM [hr].[countries] WHERE country_name = 'Australia';")
    result = cursor.fetchone()[0]
    print(f"Count result: {result}")
    assert result >= 1, "Country 'Australia' should exist in the database."

# Test Case 3: Minimum salary in employees table
def test_minimum_salary_in_employees(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT MIN(salary) AS min_salary FROM [hr].[employees];")
    result = cursor.fetchone()[0]
    print(f"Minimum salary: {result}")
    assert result == 2500.00, "Minimum salary should be 2500.00."

# Test Case 4: Number of employees in department 9
def test_number_of_employees_in_department_9(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM [hr].[employees] WHERE department_id = 9;")
    result = cursor.fetchone()[0]
    print(f"Count result: {result}")
    assert result == 3, "There should be exactly 3 employees in department 9."

# Test Case 5: Job roles with salary difference > 5000
def test_job_roles_with_salary_difference_greater_than_5000(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT job_title, min_salary, max_salary FROM [hr].[jobs] WHERE max_salary - min_salary > 5000;")
    result = cursor.fetchall()
    print(f"Result: {result}")
    assert len(result) > 0, "No roles found with a salary difference greater than 5000."

# Test Case 6: Job title with min_salary > 15000
def test_job_title_with_min_salary_greater_than_15000(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT job_title FROM [hr].[jobs] WHERE min_salary > 15000;")
    result = cursor.fetchall()
    job_titles = [row[0] for row in result]
    print(f"Job titles: {job_titles}")
    assert "President" in job_titles, "Job title 'President' should be in the result set."