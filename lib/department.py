from __init__ import CURSOR, CONN


class Department:

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"

    @classmethod
    def create_table(cls):
        """Create the "departments" table in the database"""
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY,
                name TEXT,
                location TEXT
            )
        """

        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drop the "departments" table from the database"""
        sql = """
            DROP TABLE IF EXISTS departments
        """

        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """Save the attributes of this Department instance as a new row in the "departments" table"""
        if self.id is None:
            sql = """
                INSERT INTO departments (name, location)
                VALUES (?, ?)
            """

            CURSOR.execute(sql, (self.name, self.location))
            self.id = CURSOR.lastrowid

        else:
            sql = """
                UPDATE departments
                SET name = ?, location = ?
                WHERE id = ?
            """

            CURSOR.execute(sql, (self.name, self.location, self.id))

        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to this Department instance"""
        sql = """
            DELETE FROM departments
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        self.id = None
        self.name = None
        self.location = None

    @classmethod
    def create(cls, name, location):
        """Create a new Department instance and save it to the database"""
        department = cls(name, location)
        department.save()
        return department

    @classmethod
    def get_all(cls):
        """Retrieve all Department instances from the database as a list"""
        sql = """
            SELECT *
            FROM departments
        """

        CURSOR.execute(sql)
        rows = CURSOR.fetchall()

        departments = []

        for row in rows:
            department = cls(*row)
            departments.append(department)

        return departments

    @classmethod
    def find(cls, id):
        """Retrieve a Department instance with the given id from the database

        Args:
            id (int): The id of the Department instance to retrieve

        Returns:
            Department: A Department instance with the given id, or None if
            no match is found.

        """

        sql = """
            SELECT *
            FROM departments
            WHERE id = ?
        """

        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()

        if row is not None:
            department = cls(*row)
            return department
        else:
            # Return None if no match is found
            return None