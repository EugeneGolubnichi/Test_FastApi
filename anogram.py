def is_input_anogram(str1, str2):
    """ Функция сравнивает две строки. Если они анаграммы - возвращает ТРУ
     Иначе - фолс"""
    if sorted(str1) == sorted(str2):
        return True
    else:
        return False