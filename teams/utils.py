from datetime import datetime, timedelta
from rest_framework.response import Response

class InvalidTitles(Exception):
    def __init__(self, message):
        self.message = message


class InvalidYearCupError(Exception):
    def __init__(self, message):
        self.message = message


class ImpossibleTitlesError(Exception):
    def __init__(self, message):
        self.message = message

class NegativeTitlesError(Exception):
    def __init__(self, message):
        self.message = message

def validate_titles(titles):
    if titles < 0:
        raise NegativeTitlesError("titles cannot be negative")
    

def validate_year(year):
    first_cup = datetime(1930,7,13)
    year_formated = datetime.strptime(year, "%Y-%m-%d")
    result = year_formated - first_cup
    years = round(result.days/365.2425)
    if years % 4 != 0 or years < 0:
        raise InvalidYearCupError("there was no world cup this year")


def validate_wins(titles, first_cup):
    first_cup = datetime.strptime(first_cup, "%Y-%m-%d")
    today = datetime.now()
    cups = today - first_cup
    years = round(cups.days/365.2425) / 4
    int_titles = int(titles)
    if int_titles > years:
        raise ImpossibleTitlesError("impossible to have more titles than disputed cups")


def data_processing(dict):
    try:
        validate_titles(dict['titles'])
    except NegativeTitlesError as err:
        return Response({'error': err.message}, 404)
    validate_year(dict['first_cup'])
    validate_wins(dict['titles'], dict['first_cup'])


# data = {
#     "name": "França",
#     "titles": -3,
#     "top_scorer": "Zidane",
#     "fifa_code": "FRA",
#     "first_cup": "2000-10-18"
# }

# print(data_processing(data))

# data = {
#     "name": "França",
#     "titles": 3,
#     "top_scorer": "Zidane",
#     "fifa_code": "FRA",
#     "first_cup": "1911-10-18"
# }

# print(data_processing(data))

# data = {
#     "name": "França",
#     "titles": 3,
#     "top_scorer": "Zidane",
#     "fifa_code": "FRA",
#     "first_cup": "1932-10-18"
# }

# print(data_processing(data))

# data = {
#     "name": "França",
#     "titles": 9,
#     "top_scorer": "Zidane",
#     "fifa_code": "FRA",
#     "first_cup": "2002-10-18",
# }

# print(data_processing(data))