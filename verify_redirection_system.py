#!/usr/bin/env python3
"""
Redirection System Verification
Verifies the redirection logic in the Flask routes without running the application.
"""

import os
import sys
import ast
import re

def analyze_route_file(file_path):
    """Analyze a route file for redirection patterns"""
    print(f"\n🔍 Analyzing: {file_path}")
    print("-" * 50)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all route definitions
        route_pattern = r'@bp\.route\([\'"]([^\'"]+)[\'"](?:,\s*methods=\[([^\]]+)\])?\)\s*\ndef\s+(\w+)'
        routes = re.findall(route_pattern, content)
        
        redirection_issues = []
        redirection_successes = []
        
        for route_path, methods, func_name in routes:
            print(f"📍 Route: {route_path} -> {func_name}")
            
            # Find the function definition
            func_pattern = rf'def\s+{func_name}\s*\([^)]*\):.*?(?=def\s+\w+\s*\(|$)'
            func_match = re.search(func_pattern, content, re.DOTALL)
            
            if func_match:
                func_body = func_match.group(0)
                
                # Check for redirection patterns
                if 'redirect(' in func_body:
                    redirects = re.findall(r'redirect\(url_for\([\'"]([^\'"]+)', func_body)
                    for redirect in redirects:
                        print(f"   ➡️  Redirects to: {redirect}")
                        redirection_successes.append((route_path, redirect))
                
                # Check for potential issues
                if 'isinstance(current_user, Customer)' in func_body:
                    print(f"   ✅ Customer type check found")
                
                if 'isinstance(current_user, User)' in func_body:
                    print(f"   ✅ User type check found")
                
                # Check for missing user type checks
                if '@login_required' in func_body and 'isinstance' not in func_body:
                    if 'customer_dashboard' in func_body or 'admin_profile' in func_body:
                        redirection_issues.append(f"Route {route_path} may need user type checking")
        
        return redirection_issues, redirection_successes
        
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return [], []
    except Exception as e:
        print(f"❌ Error analyzing {file_path}: {e}")
        return [], []

def check_template_consistency():
    """Check template consistency for redirection"""
    print(f"\n🔍 Checking Template Consistency")
    print("-" * 50)
    
    template_dir = "app/templates"
    issues = []
    
    if not os.path.exists(template_dir):
        print(f"❌ Template directory not found: {template_dir}")
        return issues
    
    # Check base templates
    base_templates = ['admin_base.html', 'customer_base.html']
    for template in base_templates:
        template_path = os.path.join(template_dir, template)
        if os.path.exists(template_path):
            print(f"✅ Found: {template}")
            
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for proper navigation links
            if template == 'admin_base.html':
                if '/dashboard' in content:
                    print(f"   ✅ Admin dashboard link found")
                else:
                    issues.append(f"Admin base template missing dashboard link")
                    
            elif template == 'customer_base.html':
                if '/customer_dashboard' in content:
                    print(f"   ✅ Customer dashboard link found")
                else:
                    issues.append(f"Customer base template missing customer dashboard link")
        else:
            print(f"❌ Missing: {template}")
            issues.append(f"Missing template: {template}")
    
    return issues

def verify_login_template():
    """Verify login template has proper tabs"""
    print(f"\n🔍 Checking Login Template")
    print("-" * 50)
    
    login_template = "app/templates/login.html"
    issues = []
    
    if os.path.exists(login_template):
        print(f"✅ Found: {login_template}")
        
        with open(login_template, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for login tabs
        if 'Customer Login' in content and 'Admin Login' in content:
            print(f"   ✅ Login tabs found")
        else:
            issues.append("Login template missing proper tabs")
        
        # Check for form types
        if 'login_type' in content:
            print(f"   ✅ Login type field found")
        else:
            issues.append("Login template missing login_type field")
            
    else:
        print(f"❌ Missing: {login_template}")
        issues.append(f"Missing login template")
    
    return issues

def main():
    """Main verification function"""
    print("🔍 Flavi Dairy Forecasting AI - Redirection System Verification")
    print("=" * 70)
    
    # Analyze main routes
    main_routes = "app/routes/main.py"
    auth_routes = "app/routes/auth.py"
    
    all_issues = []
    all_successes = []
    
    # Check main routes
    issues, successes = analyze_route_file(main_routes)
    all_issues.extend(issues)
    all_successes.extend(successes)
    
    # Check auth routes
    issues, successes = analyze_route_file(auth_routes)
    all_issues.extend(issues)
    all_successes.extend(successes)
    
    # Check templates
    template_issues = check_template_consistency()
    all_issues.extend(template_issues)
    
    # Check login template
    login_issues = verify_login_template()
    all_issues.extend(login_issues)
    
    # Summary
    print(f"\n📊 VERIFICATION SUMMARY")
    print("=" * 70)
    print(f"✅ Successful redirections found: {len(all_successes)}")
    print(f"⚠️  Issues found: {len(all_issues)}")
    
    if all_successes:
        print(f"\n✅ Redirection Successes:")
        for route, redirect in all_successes:
            print(f"   {route} -> {redirect}")
    
    if all_issues:
        print(f"\n⚠️  Issues to Address:")
        for issue in all_issues:
            print(f"   • {issue}")
    else:
        print(f"\n🎉 No issues found! Redirection system looks good.")
    
    # Key redirection patterns to verify
    print(f"\n🔑 Key Redirection Patterns to Verify:")
    print("1. Customer login -> /customer_dashboard")
    print("2. Admin login -> /dashboard")
    print("3. Customer accessing /dashboard -> redirect to /customer_dashboard")
    print("4. Admin accessing /customer_dashboard -> redirect to /dashboard")
    print("5. /profile -> redirect based on user type")
    print("6. Logout -> redirect to /index")
    
    print(f"\n📋 Next Steps:")
    print("1. Run the application: python run.py")
    print("2. Test customer login flow")
    print("3. Test admin login flow")
    print("4. Verify all redirections work as expected")

if __name__ == "__main__":
    main() 