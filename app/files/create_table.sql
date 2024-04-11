    DROP TABLE IF EXISTS emp;
    DROP TABLE IF EXISTS dept;

    CREATE TABLE dept (
        dept_id INTEGER PRIMARY KEY,
        dname VARCHAR(20)
        );

    CREATE TABLE emp (
            emp_id INTEGER PRIMARY KEY,
        dept_id INTEGER,
        ename VARCHAR(15),
        salary NUMERIC(6,2)
    );

    ALTER TABLE emp
    ADD CONSTRAINT dept_pk_emp FOREIGN KEY (dept_id) REFERENCES dept;