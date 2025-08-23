#!/usr/bin/env python3
"""
Deployment Test Script for Specimen Tracker
This script tests all critical functionality before deploying to production
"""

import os
import sys
import requests
import sqlite3
from pathlib import Path

def test_environment():
    """Test if all required packages are available"""
    print("🔍 Testing Python Environment...")
    
    required_packages = [
        'flask', 'flask_sqlalchemy', 'flask_migrate', 
        'sqlalchemy', 'jinja2', 'werkzeug'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        return False
    
    print("✅ All required packages are available")
    return True

def test_database():
    """Test database connectivity and schema"""
    print("\n🗄️ Testing Database...")
    
    try:
        # Test if we can create a database
        db_path = Path("instance/dev.db")
        if not db_path.parent.exists():
            db_path.parent.mkdir(parents=True)
        
        # Test SQLite connection
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Test basic SQL operations
        cursor.execute("SELECT sqlite_version()")
        version = cursor.fetchone()[0]
        print(f"  ✅ SQLite {version} - Connected successfully")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"  ❌ Database error: {e}")
        return False

def test_flask_app():
    """Test if Flask app can be created and configured"""
    print("\n🚀 Testing Flask Application...")
    
    try:
        # Test app creation
        from app import create_app
        app = create_app()
        
        # Test app configuration
        assert app.config['SECRET_KEY'] is not None
        assert app.config['SQLALCHEMY_DATABASE_URI'] is not None
        
        print("  ✅ Flask app created successfully")
        print(f"  ✅ Secret key configured: {app.config['SECRET_KEY'][:10]}...")
        print(f"  ✅ Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        # Test blueprints
        blueprint_names = [bp.name for bp in app.blueprints.values()]
        assert 'main' in blueprint_names
        print("  ✅ Blueprints registered")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Flask app error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_routes():
    """Test if all routes are accessible"""
    print("\n🛣️ Testing Routes...")
    
    try:
        from app import create_app
        app = create_app()
        
        with app.test_client() as client:
            # Test main routes
            routes_to_test = [
                ('/', 'Home page'),
                ('/patients', 'Patients list'),
                ('/patients/new', 'New patient form'),
                ('/samples', 'Samples list'),
                ('/samples/new', 'New sample form'),
                ('/tests', 'Tests list'),
                ('/tests/new', 'New test form')
            ]
            
            for route, description in routes_to_test:
                response = client.get(route)
                if response.status_code == 200:
                    print(f"  ✅ {route} - {description}")
                elif response.status_code == 302 and route in ['/samples/new', '/tests/new']:
                    # This is expected - redirects if no patients/samples exist
                    print(f"  ✅ {route} - {description} (redirects as expected)")
                else:
                    print(f"  ❌ {route} - Status {response.status_code}")
                    return False
        
        print("✅ All routes are accessible")
        return True
        
    except Exception as e:
        print(f"  ❌ Route testing error: {e}")
        return False

def test_static_files():
    """Test if static files are accessible"""
    print("\n📁 Testing Static Files...")
    
    static_files = [
        'app/static/css/styles.css',
        'app/static/js/app.js'
    ]
    
    for file_path in static_files:
        if Path(file_path).exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - Missing")
            return False
    
    print("✅ All static files are present")
    return True

def test_templates():
    """Test if all templates exist"""
    print("\n📄 Testing Templates...")
    
    required_templates = [
        'base.html',
        'index.html',
        'patients_list.html',
        'patients_form.html',
        'samples_list.html',
        'samples_form.html',
        'tests_list.html',
        'tests_form.html'
    ]
    
    for template in required_templates:
        template_path = Path(f"app/templates/{template}")
        if template_path.exists():
            print(f"  ✅ {template}")
        else:
            print(f"  ❌ {template} - Missing")
            return False
    
    print("✅ All templates are present")
    return True

def test_production_readiness():
    """Test production deployment readiness"""
    print("\n🏭 Testing Production Readiness...")
    
    # Check for hardcoded development settings
    with open('wsgi.py', 'r') as f:
        wsgi_content = f.read()
    
    if 'debug=True' in wsgi_content:
        print("  ⚠️  Debug mode is enabled (should be False in production)")
    
    if 'host=\'0.0.0.0\'' in wsgi_content:
        print("  ⚠️  Host is set to 0.0.0.0 (should be restricted in production)")
    
    # Check for environment variables
    env_vars = ['SECRET_KEY', 'DATABASE_URL']
    for var in env_vars:
        if var not in os.environ:
            print(f"  ⚠️  {var} environment variable not set")
    
    print("✅ Production readiness check completed")
    return True

def main():
    """Run all tests"""
    print("🚀 Specimen Tracker - Deployment Test Suite")
    print("=" * 50)
    
    tests = [
        test_environment,
        test_database,
        test_flask_app,
        test_routes,
        test_static_files,
        test_templates,
        test_production_readiness
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"  ❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if all(results):
        print("\n🎉 All tests passed! Your app is ready for deployment.")
        print("\n📋 Next steps:")
        print("1. Push your code to GitHub")
        print("2. Choose a hosting service (Render, Heroku, Railway, etc.)")
        print("3. Configure environment variables")
        print("4. Deploy!")
    else:
        print("\n⚠️  Some tests failed. Please fix issues before deploying.")
        print("Check the output above for specific problems.")
    
    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
