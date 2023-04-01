# NoteTakingApp

Note-taking application that mimics how you take notes in real life

Get organized with notebooks containing pages, which in turn contain content as you wish

Use NoteTakingApp's Rich Text Editor to add styles to the content you add to your pages.

Built with 🧡 by [DrInfinite](https://github.com/DrInfinite)

## Build it yourself

### Requirements

- The [backend](https://github.com/DrInfinite/TK-WS-NoteTakingApp/tree/master/backend) repository

1. Clone the repository to it's own folder and switch to the backend folder

```BASH
git clone https://github.com/DrInfinite/TK-WS-NoteTakingApp
cd backend
python -m venv venv
```

Windows:

```
venv\Scripts\activate.bat
```

POSIX/Unix/MacOS:

```BASH
source venv/bin/activate
```

and finally install requirements

```
pip install -r requirements.txt
```

1. Switch to the frontend folder

```BASH
cd ../    # to get to project root
cd frontend
```

3. Install all NPM modules and setup environment files

```BASH
npm i
```

Edit the `.env` file here

```ENV
VITE_API_URL='http://localhost:5000/api/'
```

4. Start the Flask server

```BASH
cd backend
python flask_app.py
```

5. Start the front-end vite project

```
npm run dev
```

And enjoy!
