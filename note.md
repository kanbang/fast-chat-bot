管理员模式运行

python -m spacy download en
python -m spacy download zh_core_web_sm

python -m spacy link en_core_web_sm en
python -m spacy link zh_core_web_sm chinese


python -m PyInstaller -F -i talk.ico --additional-hooks-dir=hooks --exclude-module pyinstaller --add-data "static:static" main.py