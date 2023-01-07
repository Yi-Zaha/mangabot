cd /app
rm -rf mangabot
git clone https://github.com/Rajbhaiya/mangabot/
cd mangabot
pip install --quiet -r requirements.txt
python main.py
