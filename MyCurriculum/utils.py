from random import randint


def generate_student_code() -> str:
    return str(randint(0, 2664758)).zfill(7) + ['A', 'B', 'C'][randint(0, 2)]