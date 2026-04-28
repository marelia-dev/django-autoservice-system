# Django Autoservice System 🔧🚗

**Autoserviso valdymo sistema, sukurta naudojant Django framework**

Pilnavertė Django web aplikacija, skirta automobilių serviso veiklos valdymui — klientų, transporto priemonių, užsakymų ir remonto darbų apskaitai.

## Galimybės
- Klientų ir automobilių registravimas
- Remonto užsakymų kūrimas ir valdymas
- Darbų ir dalių apskaita
- Užsakymų būsenos sekimas
- Administravimo panelė (Django admin)
- Responsyvus dizainas (CSS / Bootstrap)

## Technologijos
- Python 3
- Django framework
- HTML, CSS, Bootstrap
- JavaScript
- SQLite
- Git

## Kaip paleisti
```bash
git clone https://github.com/marelia-dev/django-autoservice-system.git
cd django-autoservice-system

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Autorius
**Marijanas Molis** — Python / Django Developer
