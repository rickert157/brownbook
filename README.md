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


