from app import create_app, db
from app.models import Hospital, Doctor, Patient, User

app = create_app()

with app.app_context():
    # create tables if they don't exist
    db.create_all()

    # seed hospitals only if none exist
    if not Hospital.query.first():
        h1 = Hospital(name='Central Hospital', address='123 Main St', phone='111-222-3333', rooms_total=30)
        h2 = Hospital(name='City Clinic', address='45 West Ave', phone='444-555-6666', rooms_total=10)
        h3 = Hospital(name='Care & Cure', address='7 Health Plaza', phone='777-888-9999', rooms_total=20)
        db.session.add_all([h1, h2, h3])
        db.session.commit()  # commit so h1.id, etc. are available

        # NOTE: use the exact attribute names your model expects.
        # I used `specialization` because that's what you used in this script.
        # If your model uses `specialty`, change it accordingly.
        d1 = Doctor(
            hospital_id=h1.id,
            name='Dr. A Kumar',
            specialization='Cardiology',
            schedule='Mon-Fri 9:00-13:00',
            age=55,
            gender='male'
        )
        d2 = Doctor(
            hospital_id=h1.id,
            name='Dr. S Rao',
            specialization='Neurology',
            schedule='Tue-Thu 10:00-16:00',
            age=30,
            gender='male'
        )
        d3 = Doctor(
            hospital_id=h2.id,
            name='Dr. Ramya V',
            specialization='Pediatrics',
            schedule='Mon-Wed 9:00-15:00',
            age=45,
            gender='female'
        )
        db.session.add_all([d1, d2, d3])
        db.session.commit()

    # seed admin user only if not present
    if not User.query.filter_by(email='admin@hospital.com').first():
        u = User(username='admin', email='admin@hospital.com')
        u.set_password('Admin@123')
        db.session.add(u)
        db.session.commit()
        print("Seeded admin and hospitals")
    else:
        print("Admin already exists")
