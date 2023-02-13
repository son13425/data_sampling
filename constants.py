from pathlib import Path

BASE_DIR = Path(__file__).parent
FILENAME_BD = 'Ribbon1.csv'
FILENAME_REQUEST = 'data_test.csv'
DATETIME_FORMAT = '%d %m %Y г. %H:%M:%S.%f мсек'
MONCH_DICT = {
    'января': '01',
    'февраля': '02',
    'марта': '03',
    'апреля': '04',
    'мая': '05',
    'июня': '06',
    'июля': '07',
    'августа': '08',
    'сентября': '09',
    'октября': '10',
    'ноября': '11',
    'декабря': '12'
}
MONCH_DICT_FOR_STR = {
    '01': 'января',
    '02': 'февраля',
    '03': 'марта',
    '04': 'апреля',
    '05': 'мая',
    '06': 'июня',
    '07': 'июля',
    '08': 'августа',
    '09': 'сентября',
    '10': 'октября',
    '11': 'ноября',
    '12': 'декабря'
}
DT_FORMAT = '%Y-%m-%d_%H-%M-%S'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
