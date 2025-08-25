source agentvenv/bin/activate
python -m db.init_db

node index.js   
npm run start