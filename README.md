# Dark Object-relational mapping

Это небольшая самописная библиотечка, помогающая обойтись без продумывания clear SQL запросов.

### Из интересного:

> Превентивная защита от SQLInject

> Встроенный мигратор, структура ваших таблиц будет в безопасности!

> Асинхронный модуль баз данных, синхронный миграционный.

> Простая установка. Простое использование. Хорошая защита данных.

### Setup:

Установка довольно простая, но требует наличия удаленного | локального сервера PostgreSQL

TO-DO: Добавить возможность выбора SQL баз данных.

#### Папка libraries должна лежать в корне вашего проекта (рядом с запускаемым скриптом)

```bash
mkdir new-project
cd new-project
git clone https://github.com/DarkLorianPrime/DarkORM .
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd libraries
mv example.env .env
nano .env
```

В .env заполните требуемые данные

```env
shatoken= - ключ шифрования пароля (можно сделать через uuid.uuid4().hex)
user= - пользователь базы данных
db= - название базы данных
password= - пароль базы данных
host= - хост базы данных (айпи\ссылка куда обращаться за данными)
cd ../
```

Попробуйте запустить тестовый скрипт
`uvicorn example:app —host="0.0.0.0" —port="need port"`

И попробуйте сделать тестовый запрос (Используйте этот метод запуска только для разработки!)

```python 
print(requests.get("your-domen.haha:your-port/").json())

python-result: {"response":true}
fastapi-result: INFO:     IP - "GET / HTTP/1.0" 200 OK
```

# Миграции

Для миграций есть скрипт, лежащий в корне проекта `migrator.py`

Для миграции первой и обязательной таблицы - введите `python migrator.py migrate`

В директории создатся папка `migrations`, в базе данных появится таблица `migrations`

А в консоль выведет `successfully inserted migration: migration-name`

## Как создавать свои миграции

Для упрощения жизни есть команда `makemigrations`

`python migrator.py makemigrations 002_dataseller`

В папке `migrations` появится файл `002_dataseller_datetime.py`, в который вы можете вносить SQL запрос на создание
таблицы

```python
def up():  # Создание таблицы
    return """CREATE TABLE IF NOT EXISTS dataseller(id SERIAL PRIMARY KEY, name TEXT, description TEXT)"""


def down():  # Откат таблицы
    return """DROP TABLE IF EXISTS dataseller"""
```

#### Поздравляю с первой собственной миграцией! Теперь в случае окончания разработки\потери структуры таблиц - вы легко сможете вернуть базу данных к первоначальному виду

## Полный функционал мигратора

`rollback` - откат миграции назад

`rollback --step=5` - откат 5 миграций назад

`reset` - откат всех миграций назад (включая таблицу миграций)

`refresh` - откат и миграция по новой всех миграций

`migrate` - миграция ВСЕХ миграций в папке последовательно

`makemigrations` - создание шаблона в папке миграций

## Полный функционал ORM

`get_all_entries [table_name - str]` - список всех записей в таблице

`get_filtered_entries [table_name - str] [values - dict] [order_by - str]` - список записей с условием values
отсортированных по order_by в таблице

`create_one_entry [table_name - str] [values - dict]` - создает запись в таблице со значениями values (словарь
естественно)

`table_exists [table_name - str]` - проверяет, существует ли таблица

`create_many_entries [table_name - str] [values - list]` - создает много записей в таблице, values - список словарей
значений [{"user": "dima"}, {"user": "dasha"}]

`entry_exists [table_name - str] [where - dict]` - проверяет, существует ли запись с условиями переданными в where

`update [table_name - str] [values - list, dict] [where - dict]` - обновляет значения записей, подходящих по where на values. Можно передать словарь со значениями, или список словарей в таблице

`delete [table_name - str] [where - dict]` - удаляет записи, подходящие по where в таблице

## Модуль сравнивания паролей
Лайфхак: Не храните пароли в их исконном виде. Для этого в .env вы передавали shatoken.

В async_database есть встроенный модуль SHAPassword

```python
from libraries.database.async_database import SHAPassword, DatabaseORM
login = "dima"
password = "112233"
# registration
password = SHAPassword("tablename").create_password(password)
DatabaseORM().create_one_entry("tablename", values={"login": "dima", "password": password})
print(SHAPassword("tablename").check_password(password)) # True
print(SHAPassword("tablename").check_password("112233")) # False
```
В зависимости от shatoken-а один и тот же пароль (в хэшированном виде) меняется, что обеспечивает защиту от слива всех паролей.

`create_password [password - str]` - хэширует пароль токеном и возвращает его

`check_password [password - str]` - сравнивает хэшированный пароль с паролем в базе данных (предполагается что там он уже хэшированный).
