import json #  Импортируем Json модуль
#  Порписываем путь к файлу на локальном хранилище
PATH = r'C:\Users\User\Desktop\PyProject\Study_Tasks\1 этап\Students.json'
#  Создаем класс - студент
class Student:
    def __init__(self, name: str, id_stud: int):
        self.name = name
        self.id_stud = id_stud
        self.subjects_grades = {} # Словарь для хранения предметов и оценок

    def __str__(self): #  Строковое представление объекта студент
        gpa = self.get_gpa() #  Вызов результата функции - средняя оценка
        grade = ", ".join(f"{k}: {v}" for k, v in self.subjects_grades.items()) #  Перебор строк с предметами и оценками
        return (f'Студент {self.name}: id{self.id_stud}\n'
                f'Предметы и оценки - {grade} , \n '
                f'Средняя оценка {gpa}')


    def add_subject(self, subject):
        # Проверяем, существует ли предмет
        if subject in self.subjects_grades:
            # Если предмет уже есть — сообщаем об этом
            raise ValueError(f"Предмет '{subject}' уже существует")

        # Добавляем предмет с пустым списком оценок
        self.subjects_grades[subject] = []


    def remove_subject(self, subject):
        # Проверяем, существует ли предмет
        if subject not in self.subjects_grades:
            # Если предмета нет — выбрасываем исключение
            raise KeyError(f"Предмет '{subject}' не найден")

        # Удаляем предмет из словаря
        del self.subjects_grades[subject]


    def add_grade(self, subject, grade):
        # Проверяем, существует ли предмет
        if subject not in self.subjects_grades:
            # Если предмет не найден — ошибка
            raise KeyError(f"Предмет '{subject}' не найден")

        # Проверяем корректность оценки
        if not isinstance(grade, int) or not (1 <= grade <= 5):
            # Если оценка вне диапазона — ошибка
            raise ValueError("Оценка должна быть целым числом от 1 до 5")

        # Добавляем оценку в список оценок предмета
        self.subjects_grades[subject].append(grade)

    def get_gpa(self):
        all_grades = []

        for grades in self.subjects_grades.values():
            all_grades.extend(grades) #  Создаем список оценок перебором значения словаря self.subjects_grades

        if not all_grades: # Для исключения ошибки, когда нет оценок возращается число по умолчанию
            return 0.0

        return sum(all_grades) / len(all_grades)

    def to_json(self): #  Метод для сериализации данных. Перевод экземпляра класса Student в словарь для хранения в json
        return {'name': self.name, 'id_stud': self.id_stud,
                'subjects_grades': self.subjects_grades}

    @classmethod
    def from_json(cls, student_id, data): #  Метод для десериализации данных. Перевод словаря из json в экземпляр класса Student
        student = cls(data["name"], student_id)
        student.subjects_grades = data["subjects_grades"]
        return student

class StudentsManager: #  Класс для управления классом Student - для добавления, изменения, сохранения и загрузки данных в json-файл
    def __init__(self):
        self.students = self._load() #  Структура данных для хранения объекта класса Student

    def __str__(self):
        return "\n\n".join(str(student) for student in self.students.values())

    def _save(self): #  Метод сохраняет экземпляр класса Student в виде словаря с ключом id_stud и значением словарь Student
        data = {str(student_id): student.to_json()
            for student_id, student in self.students.items()}  #  Преобразование экземпляра класса в слвоарь

        with open(PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4) #  Запись в json-файл

    def _load(self): #  Метод загружает словарь с ключом id_stud и значением словарь Student и преобразует в экземпляр класса Student
        try:
            with open(PATH, "r", encoding="utf-8") as f:
                if f.read().strip() == "": #  Проверка json-файла на пустое значение, которое может вызвать ошибку
                    return {}
                f.seek(0)
                data = json.load(f) #  Встроенная функция загрузки данных из json, не метод _load!
           #  Перевод словаря из json-файла в экземпляр класса Student
            return {int(student_id): Student.from_json(student_id, data) for student_id, data in data.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def add_student(self, student: Student):
        if student.id_stud in self.students: # Проверка на наличие студента
            raise ValueError("Студент с таким ID уже существует")

        self.students[student.id_stud] = student # Добавление студента
        self._save()

    def remove_student(self, student_id: int):
        if student_id not in self.students: # Проверка на наличие студента
            raise KeyError("Студент не найден")

        del self.students[student_id] # Удаление студента
        self._save()

    def add_subject(self, student_id: int, subject: str):
        self._get(student_id).add_subject(subject) #  Добавление предмета
        self._save()

    def remove_subject(self, student_id: int, subject: str):
        self._get(student_id).remove_subject(subject) #  Удаление предмета
        self._save()

    def add_grade(self, student_id: int, subject: str, grade: int):
        self._get(student_id).add_grade(subject, grade) #  Добавление оценки
        self._save()

    def _get(self, student_id: int): #  Метод для вызова объекта Student, как значения словаря по ключу id
        if student_id not in self.students:  # Проверка на наличие студента
            raise KeyError("Студент не найден")
        return self.students[student_id]

    def gpa(self, student_id: int):
        #  Вывод строкового представления
        return f'Средняя оценка студента {self._get(student_id).name}: {self._get(student_id).get_gpa()}'

    def find_by_name(self, name: str): # Метод для вывода списка студентов с одинаковым именем и разными id, для сравнения и избежания ошибок
        results = [student for student in self.students.values()
            if student.name.lower() == name.lower()]

        for student in results:
            print(student.id_stud, student.name)


manager = StudentsManager()

manager.add_student(Student("Иван Иванов", 1))
manager.add_subject(1, "Математика")
manager.add_grade(1, "Математика", 5)
manager.add_grade(1, "Математика", 4)

manager.add_student(Student("Анна Петрова", 2))
manager.add_subject(2, "История")
manager.add_grade(2, "История", 5)

manager.add_student(Student("Сергей Сергеев", 3))
manager.add_subject(3, "Обществознание")
manager.add_grade(3, "Обществознание", 4 )
manager.add_grade(3,"Обществознание", 5 )

manager.add_student(Student("Вероника Никонова", 4))
manager.add_subject(4, "Дизайн")
manager.add_grade(4, "Дизайн", 4 )
manager.add_grade(4,"Дизайн", 5 )

print(manager.gpa(4))

manager.remove_subject(1, "Математика")
manager.remove_student(3)


print(manager)

