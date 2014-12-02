XML to JSON converter

Потоковый конвертер из xml в json


Пример использования:

cat xml_file.xml | python xml2json.py >json_file.json



Функциональные тесты:

cd ./functional_test/; bash run.sh


Измерить производительность/замерить потребление памяти:

cd ./functional_test/; python speedtest.py <кол-во итераций>

Паралельно можно смотреть потребление памяти


Юнит тесты:

python unit_test.py



Примечания:
- Задача решена "в лоб". Часть кода не нуждается в unit-тестировании, т.к покрывается функциональными тестами.
- Дальнейшее улучшение кода с целью покрытия юнит-тестами чрезмерно усложнит логику для такой маленькой утилиты