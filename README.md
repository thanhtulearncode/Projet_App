# Projet_App
# 🎯 WallStreetGame - Jeu de Stratégie Combinatoire Abstrait

## 🚀 Installation

### 🔧 Prérequis

- [Node.js v18+](https://nodejs.org/)
- [Python 3.9+](https://www.python.org/)
- [Git](https://git-scm.com/)

### 📦 Configuration

1. **Cloner le dépôt :**

```bash
git clone https://github.com/thanhtulearncode/Projet_App
cd Projet_App
```

2. **Configurer le backend (Python/FastAPI) :**

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

3. **Configurer le frontend (React) :**

```bash
cd frontend
npm install
```

---

## ▶️ Exécution du Projet

1. **Lancer le terminal 1 (backend) :**

```bash
cd backend
uvicorn api:app --reload --port 8000
```

2. **Lancer le terminal 2 (frontend) :**

```bash
cd frontend
npm start
```

Ouvrir l’application sur [http://localhost:3000](http://localhost:3000)

---

## 🗂 Structure du Projet

```
Projet_App/
├── backend/
│   ├── api.py               # API FastAPI
│   ├── game_engine.py       # Logique du jeu
│   ├── game_engine.py       # L'IA
│   ...
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   │   ...
│   │   └── index.html
│   ├── src/
│   │   ├── components/      # UI Components
│   │   ...
│   │   ├── App.js
│   │   ├── index.css
│   │   └── index.js
│   └── package.json
│
└── README.md                # Ce fichier
```

---

## 🛠 Technologies Utilisées

### Frontend

- React.js

### Backend

- Python 3.9+
- FastAPI
- NumPy

### IA

- Algorithme MinMax avec élagage alpha-bêta

### Déploiement

Ouvrir l’application sur [https://wall-street-game.vercel.app/](https://wall-street-game.vercel.app/)


