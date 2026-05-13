# 1. Инициализация
mkdir wardrobe-app && cd wardrobe-app
git init

# 2. Создай файлы выше (requirements.txt, app.py, templates/index.html, README.md)

# 3. Добавь и закоммить
echo "static/uploads/" > .gitignore
echo "static/processed/" >> .gitignore
echo "__pycache__/" >> .gitignore
git add .
git commit -m "initial commit: базовый конструктор с удалением фона"

# 4. Залей в GitHub (замени USER и REPO)
git remote add origin https://github.com/USER/wardrobe-app.git
git push -u origin main
