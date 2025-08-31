from Configuration.config import Config


class StudentModel:
    @staticmethod
    def get_all_students():
        try:
            conn = Config.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Student_")

            students = []
            for row in cursor.fetchall():
                students.append({
                    "id": row[0],
                    "name": row[1],
                    "age": row[2],
                    "grade": row[3]
                })

            cursor.close()
            conn.close()
            return students

        except Exception as e:
            return {"error": str(e)}


    @staticmethod
    def insert_user_and_student(data):
        try:
            conn = Config.get_connection()
            cursor = conn.cursor()

            # Insert into User table
            insert_user_query = """
                INSERT INTO [Users] (User_ID, name, phone_number, email, location, password)
                OUTPUT INSERTED.User_ID
                VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(insert_user_query, (
                data["User_ID"],
                data["name"],
                data["phone_number"],
                data["email"],
                data["location"],
                data["password"]
            ))

            # Get the new User_ID
            user_id = cursor.fetchone()[0]

            # Insert into Student_ table
            insert_student_query = "INSERT INTO Student_ (User_ID) VALUES (?)"
            cursor.execute(insert_student_query, (user_id,))

            conn.commit()
            cursor.close()
            conn.close()

            return {"message": "Student registered successfully", "User_ID": user_id}

        except Exception as e:
            return {"error": str(e)}
