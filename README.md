# advertisements_analyse
Gets information about advertisements from one popular site. Learning project for data analysist. Web scrapping, work with database and analyse
Описание
Проект является учебным и предназначен прежде всего для тренировки навыков анализа данных. Дополнительно в проекте демонстрируется навык парсинга web страниц и работы с базами данных средствами python, а также общее владение python.
Данные используемые в проекте - информация из активных объявлений на АВИТО о продаже автомобилей. Данные отбирались по автомобилям отечественных марок, с отметками "Не битый", "С пробегом", "Частные", "Только проверенные владельцы и партнеры". Работа кода не зависит от указанных параметров и может масштабировать мы на иные объявления о продаже автомобилей.

Проект включает в себя несколько модулей:
1) модули для парсинга NAMES. Предназначены для парсинга страниц поиска автомобилей Авито. Основной инструмент - библиотека selenium. Принимает url поисковой выдачи и парсит информацию об объявлениях, собирая информацию как с карточки объявления (функция car_page), так и с карточки основных характеристик модели. Результат по каждому отдельному объявлению добавляется в csv файл с предыдущими результами парсинга. Версия на BeautifulSoup в процессе разработки;
2) модуль работы с базой данных NAME. Реализованы функции для разбивки и переноса данных из csv файла в базу данных на postresql, а также для их извлечения из базы данных и преобразования в pandas.DataFrame, с целью проведения последующего анализа;
3) модуль очистки данных NAME. Автоматизирует часть проверок данных на корректность до включения их в базу данных
4) модуль анализа данных