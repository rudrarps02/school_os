from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

# Initialize application factory context
app = create_app()

with app.app_context():
    print("🚀 Initializing production database deployment check...")
    
    # 1. Look for an existing Administrator account to protect production data
    admin_exists = User.query.filter_by(role='Admin').first()
    
    if admin_exists:
        print("⚠️ [Skipped] An Admin account already exists in the database.")
        print("ℹ️ To preserve production data records, no new profiles were generated.")
    else:
        print("🔒 Generating pristine System Administrator root security profile...")
        
        # Define secure master supervisor configurations
        production_admin = User(
            username='school_admin',
            password_hash=generate_password_hash('ChangeThisSecurePasswordOnFirstLogin2026!', method='pbkdf2:sha256'),
            role='Admin'
        )
        
        try:
            db.session.add(production_admin)
            db.session.commit()
            print("\n" + "="*60)
            print("✅ SYSTEM INITIALIZATION SUCCESSFUL!")
            print("="*60)
            print("Master Username: school_admin")
            print("Master Password: ChangeThisSecurePasswordOnFirstLogin2026!")
            print("👉 CRITICAL: Log in immediately and change this password in production.")
            print("="*60 + "\n")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error occurred during data initialization: {str(e)}")
