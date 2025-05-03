# 🗺️ TaskMap — Карта знаний по языкам программирования

**TaskMap** — это платформа для изучения языков программирования, которая объединяет теорию, практику и тесты в одном приложении. Пользователь может выбрать язык, пройти темы и проверить знания с помощью встроенных интерактивных заданий.

![TaskMap Preview](assets/taskmap-preview.gif)

---

## 📘 Описание

Проект создан для объединения:

- 📚 **Материалов и теории** по каждому языку программирования
- 🧠 **Тестов** и заданий для закрепления
- 🗺️ **Интерактивной карты** тем и прогресса
- 🎓 **Системы обучения** с отслеживанием результатов

---

## 🧩 Технологии

| Раздел     | Технология          |
|------------|---------------------|
| 🎯 Backend  | Django (Python)     |
| 💻 Frontend | Vue.js / Node.js    |
| 🗃️ API      | Django REST Framework |
| 💾 База     | PostgreSQL / SQLite / MongoDB |
| 🌐 Хостинг  | Vercel / Render / GitHub Pages |

---

## ⚙️ Установка

### 1. Клонируй проект

```bash
git clone https://github.com/yourusername/TaskMap.git
cd TaskMap
```

### 2. Запуск backend (Django)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 3. Запуск frontend (Vue.js или Node.js)
```bash
cd frontend
npm install
npm run dev
```

## 📄 Лицензия

[MIT License](LICENSE) © 2025 [Бекзат Убниев](https://github.com/dunanhub)
