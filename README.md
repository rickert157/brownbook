# parser template 

## Установка
```sh
git clone https://github.com/rickert157/brownbook.git
```
```sh
cd brownbook && python3 -m venv venv && ./venv/bin/pip install -r requirements.txt && ./venv/bin/pip freeze
```
### Режим отладки
Относится больше к фреймворку, вокруг которого написал инструмент  
Для отладки можно парсить по одной странице, указывая параметр --test-url с url
```sh
python3 __main__.py --test-url=https://github.com
```

## Сбор sitemap
Первичные ссылки - 30шт всего
```sh
python3 __main__.py --sitemap=sitemap-level-1
```
Ссылки второго уровня, парсер будет ходить по ссылкам с первого уровня и писать их в отдельный файл
```sh
python3 __main__.py --sitemap=sitemap-level-2
```

## Тест парсинга страницы компании
```sh
python3 -m modules.parser_page https://www.brownbook.net/business/21220618/dennis-a-rosene-ins-agency-inc-state-farm-insurance-agent/
```

## Обработка промежуточных результатов
Фактически сбор всех компаний занял более суток непрерывной работы, было собрано 43 миллионов внутренних ссылок на компании.  
Для удобства следует их разделить на 200 частей. Для этого я через sqlbrowser импортировал sqlite таблицу в CSV(самому удобнее так работать). После этого можно разбить на 200 файлов(из рассчета 20 виртуальных машин, на каждой из которых будет по 10 контейнеров)   
Этот модуль разобьет всю базу на 20 директорий(по одной деректории на каждую машину) и на 10 файлов для каждой машины
```sh
python3 -m modules.divide_list_companies
```
