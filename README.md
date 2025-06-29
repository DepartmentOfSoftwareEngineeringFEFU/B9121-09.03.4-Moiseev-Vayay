## Добро пожаловать
![image](https://github.com/user-attachments/assets/95a54fb7-343c-406c-b288-662c90e76f3c)

# Ифнормация
Tема диплома: РАЗРАБОТКА АВТОМАТИЗИРОВАННОЙ СИСТЕМЫ ПОИСКА АРБИТРАЖНЫХ СИТУАЦИЙ НА ФИНАНСОВЫХ РЫНКАХ

Авторы: Моисеев Дмитрий Александрович , Ваяй Михаил Сергеевич 

Группа: Б9121-09.03.04

Научный руководитель: Профессор ДПИиИИ, Доктор технических наук, профессор Артемьева И. Л.

### Стек технологий
### Backend
- Python 3.11 

- Django 

- Django REST Framework 

- SQLite 

- Tinkoff Invest API (gRPC) 

- FinamTradeApiPy 

- asyncio 

- Pydantic 

### Frontend
- HTML5, CSS3 

- JavaScript (ES6+) 

- Plotly.js 

- AJAX (Fetch API) 


## 🔧 Требования

- Anaconda или Miniconda
- Python 3.10+
- Git
## 🚀 Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/DepartmentOfSoftwareEngineeringFEFU/B9121-09.03.4-Moiseev-Vayay.git
cd arbitrage-project
```

 2. Установка Conda

Если на компьютере ещё не установлен `conda`, необходимо установить:

- 👉 [Anaconda (всё в комплекте, большой размер)](https://www.anaconda.com/products/distribution#download-section)
- или 👉 [Miniconda (лёгкий, только менеджер пакетов)](https://docs.conda.io/en/latest/miniconda.html)

✅ Рекомендуется **Miniconda**, если не нужен весь пакет Anaconda.

После установки:
```bash
conda --version
```


3. Создайте и активируйте окружение:
```bash
conda env create -f environment.yml
conda activate my_env_arb
```
4.  Примените миграции:
```bash
python manage.py migrate
```
5. Создайте суперпользователя(опционально)
```bash
python manage.py createsuperuser
```
6.Запустите проект
```bash
python manage.py runserver
```
7. Откройте в браузере
```bash
http://127.0.0.1:8000/login/
```


