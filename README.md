# LAB 5 — Резервація столика

   ![Jinja](https://img.shields.io/badge/jinja-%237E0C1B.svg?style=for-the-badge&logo=jinja&logoColor=white)
   ![Python](https://img.shields.io/badge/python-%233670A0.svg?style=for-the-badge&logo=python&logoColor=ffdd54)
   ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
   ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
   ![CSS](https://img.shields.io/badge/css-%23663399.svg?style=for-the-badge&logo=css&logoColor=white)
   
## Вимоги

- Python 3.9 або новіший
- pip (встановлюється разом із Python)
- термінал: Terminal / iTerm на macOS, PowerShell або CMD на Windows

Перевірити версію Python:

```bash
python3 --version    # macOS
py --version         # Windows
```

## macOS

1. Перейдіть у теку проєкту:

   ```bash
   cd /шлях/до/LAB5
   ```

2. Створіть віртуальне середовище:

   ```bash
   python3 -m venv .venv
   ```

3. Активуйте його:

   ```bash
   source .venv/bin/activate
   ```

   У рядку термінала має з'явитися префікс `(.venv)`.

4. Встановіть залежності:

   ```bash
   pip install -r requirements.txt
   ```

5. Запустіть сервер:

   ```bash
   python3 app.py
   ```

6. Відкрийте у браузері:

   ```text
   http://127.0.0.1:5001
   ```

> **Чому порт 5001, а не 5000.** На macOS порт 5000 займає служба AirPlay
> (Receiver), тому застосунок на ньому не запуститься або віддаватиме
> помилку 403. Порт 5001 вільний.

## Windows

1. Перейдіть у теку проєкту:

   ```powershell
   cd C:\шлях\до\LAB5
   ```

2. Створіть віртуальне середовище:

   ```powershell
   py -m venv .venv
   ```

   Якщо команда `py` недоступна, використайте `python -m venv .venv`.

3. Активуйте середовище.

   **PowerShell:**

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   **CMD:**

   ```bat
   .venv\Scripts\activate.bat
   ```

4. Якщо PowerShell блокує запуск скриптів, дозвольте його лише для поточного
   сеансу:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```

   Після цього повторіть активацію. Системні налаштування не змінюються.

5. Встановіть залежності:

   ```powershell
   pip install -r requirements.txt
   ```

6. Запустіть сервер:

   ```powershell
   py app.py
   ```

7. Відкрийте у браузері:

   ```text
   http://127.0.0.1:5001
   ```

## Зупинка сервера

У терміналі з запущеним Flask натисніть `Ctrl+C`.

## Де зберігаються дані

Заявки записуються у теку `data/` у форматі JSON — один файл на одну
резервацію. Тека створюється автоматично під час першого збереження, тому
заздалегідь її створювати не потрібно. Вміст `data/` не потрапляє в Git
тому після клонування репозиторію список заявок буде порожнім.
