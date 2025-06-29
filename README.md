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

# Установка
## 🔧 Требования

- Anaconda или Miniconda
- Python 3.10+
- Git
## 🚀 Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/your-username/arbitrage-project.git
cd arbitrage-project

2. Создайте и активируйте окружение:

conda env create -f environment.yml
conda activate my_env_arb
3.  Примените миграции:

python manage.py migrate

4. Создайте суперпользователя(опционально)

python manage.py createsuperuser

5.Запустите проект

python manage.py runserver

6. Откройте в браузере

http://127.0.0.1:8000/login/



