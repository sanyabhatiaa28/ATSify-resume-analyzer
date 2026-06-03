from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import PyPDF2
import re
import os

app = Flask(__name__)

app.secret_key = 'your_super_secret_key_bro'

# MySQL Configuration
app.config['MYSQL_HOST'] = os.environ.get('DB_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('DB_USER', 'root')       
app.config['MYSQL_PASSWORD'] = os.environ.get('DB_PASSWORD', 'vhivfrc#7878')       
app.config['MYSQL_DB'] = os.environ.get('DB_NAME', 'resume_analyzer_db')

mysql = MySQL(app)

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + " "
    return text

# CLEANED AND PRECISE NORMALIZATION (No more keyword leaking!)
def clean_and_normalize_text(text):
    if not text:
        return ""
    text = text.lower()
    
    # Precise 1:1 mappings or structural concept grouping without cross-contaminating distinct technologies
    normalization_map = {
        r'\bmern\b': 'mongodb express.js react.js node.js',
        r'\bmean\b': 'mongodb express.js angular node.js',
        r'\blamp\b': 'linux apache mysql php',
        
        r'\bjs\b': 'javascript',
        r'\bts\b': 'typescript',
        r'\bpy\b': 'python',
        r'\bcpp\b': 'c++',
        r'\bcs\b': 'c#',
        
        r'\bcss\b': 'css',
        r'\bhtml\b': 'html',
        r'\bnodejs\b': 'node.js',
        r'\bexpressjs\b': 'express.js',
        r'\breactjs\b': 'react.js',
        r'\bnextjs\b': 'next.js',
        r'\bvuejs\b': 'vue.js',
        r'\bbootstrap\b': 'bootstrap',
        r'\btailwind\b': 'tailwind css',
        
        r'\boops\b': 'object-oriented programming',
        r'\boop\b': 'object-oriented programming',
        r'\bdsa\b': 'data structures algorithms',
        r'\bos\b': 'operating systems',
        r'\bcn\b': 'computer networks',
        r'\bdbms\b': 'dbms', 
        r'\bdatabase design\b': 'database design',
        r'\bcrud\b': 'crud operations',
        
        r'\baws\b': 'aws', 
        r'\bgcp\b': 'google cloud',
        r'\bci\s*/\s*cd\b': 'ci/cd',
        r'\bcicd\b': 'ci/cd',
        r'\bk8s\b': 'kubernetes',
        
        r'\bapi\b': 'api development',
        r'\bapis\b': 'api development',
        r'\bjwt\b': 'jwt',
        r'\bauth\b': 'authentication authorization',
        
        r'\bqa\b': 'quality assurance',
        r'\bsde\b': 'software development',
        r'\bswe\b': 'software development',
        r'\bnlp\b': 'nlp'
    }
    
    for shorthand, full_form in normalization_map.items():
        text = re.sub(shorthand, full_form, text)

    text = re.sub(r'[^a-z0-9\s\+\#\.]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    
    hashed_password = generate_password_hash(password)
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return "Email already registered, bro!", 400
            
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                       (username, email, hashed_password))
        mysql.connection.commit()
        return "Signup successful! You can now login.", 200
    except Exception as e:
        return f"Database error: {str(e)}", 500
    finally:
        cursor.close()

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, username, password FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    
    if user and check_password_hash(user[2], password):
        session['user_id'] = user[0]
        session['username'] = user[1]
        return redirect(url_for('analyzer'))
    
    return "Invalid email or password, try again!", 401

@app.route('/analyzer')
def analyzer():
    if 'user_id' not in session:
        return redirect(url_for('home')) 
    return render_template('analyzer.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'user_id' not in session:
        return redirect(url_for('home'))
        
    if 'resume' not in request.files:
        return "No resume file uploaded, bro!", 400
        
    file = request.files['resume']
    job_description = request.form.get('job_description', '')
    
    if file.filename == '' or not job_description:
        return "Missing file or missing job description!", 400

    try:
        raw_resume_text = extract_text_from_pdf(file)
        cleaned_resume = clean_and_normalize_text(raw_resume_text)
        cleaned_jd = clean_and_normalize_text(job_description)
        
        if not cleaned_resume:
            return """<h1>Extraction Notice</h1>
                      <p style='color:#F59E0B;'>Your PDF text could not be compiled cleanly. Ensure it contains actual font formats.</p>
                      <br><a href='/analyzer'>Go Back</a>"""
        
        # PRECISE ONTOLOGY LIST - No overlapping fallback pollution
        CORE_TECH_ONTOLOGY = [
            'java', 'python', 'javascript', 'typescript', 'c++', 'c#', 'go', 'php', 'html', 'css', 
            'bootstrap', 'tailwind css', 'react.js', 'next.js', 'angular', 'vue.js', 'node.js', 'express.js', 
            'rest api', 'graphql', 'api development', 'microservices', 'sql', 'mysql', 'postgresql', 
            'mongodb', 'sqlite', 'database design', 'data structures', 'algorithms', 'object-oriented programming', 
            'operating systems', 'computer networks', 'dbms', 'system design', 'git', 'github', 'gitlab', 
            'bitbucket', 'version control', 'authentication', 'authorization', 'jwt', 'session management', 
            'aws', 'azure', 'google cloud', 'docker', 'kubernetes', 'ci/cd', 'jenkins', 'linux', 
            'unit testing', 'integration testing', 'debugging', 'test cases', 'quality assurance', 
            'software development', 'agile', 'scrum', 'code review', 'problem solving', 'software design', 
            'clean code', 'crud operations', 'natural language processing', 'nlp', 'tokenization', 
            'stopword removal', 'stemming', 'lemmatization', 'tf-idf', 'cosine similarity', 'text processing', 
            'information retrieval', 'keyword extraction', 'document similarity', 'pdf parsing', 
            'communication', 'leadership', 'teamwork', 'collaboration', 'critical thinking', 'analytical skills', 
            'time management', 'adaptability'
        ]

        requested_jd_skills = []
        for skill in CORE_TECH_ONTOLOGY:
            if re.search(rf'\b{re.escape(skill)}\b', cleaned_jd):
                requested_jd_skills.append(skill)
                
        if re.search(r'\bc\b', cleaned_jd):
            requested_jd_skills.append('c')
            
        requested_jd_skills = list(set(requested_jd_skills))

        matched_keywords = []
        missing_keywords = []
        
        for skill in requested_jd_skills:
            pattern = rf'\b{re.escape(skill)}\b' if skill != 'c' else r'\bc\b'
            if re.search(pattern, cleaned_resume):
                matched_keywords.append(skill)
            else:
                missing_keywords.append(skill)

        if 'c' in matched_keywords: matched_keywords.remove('c')
        if 'c' in missing_keywords: missing_keywords.remove('c')
        
        matched_keywords = sorted(matched_keywords)
        missing_keywords = sorted(missing_keywords)

        total_required_count = len(requested_jd_skills)
        if total_required_count > 0:
            base_intersection_score = (len(matched_keywords) / total_required_count) * 100
            
            structural_bonus = 0
            if 'data structures' in matched_keywords or 'algorithms' in matched_keywords:
                structural_bonus += 3
            if 'object-oriented programming' in matched_keywords:
                structural_bonus += 2
                
            rounded_score = round(min(base_intersection_score + structural_bonus, 100.0), 2)
        else:
            rounded_score = 50.0

        if rounded_score >= 85:
            tier, theme_color = "Excellent Match", "#14B8A6"
            msg = "Exceptional engineering keyword mapping! Your profile cleanly demonstrates deep domain knowledge matching this technical specification."
            recommendations = [
                "Your technical skill coverage is pristine. Verify your bullet points quantify your impact using numeric values.",
                "Ensure links to technical profile anchors (GitHub repositories) lead to operational, active repositories.",
                "Check that section title layouts look standard and clear to automated tracking software models."
            ]
        elif rounded_score >= 70:
            tier, theme_color = "Good Match", "#38BDF8"
            msg = "Strong profile match! Your experience covers the vast majority of core target requirements with easily adjustable vocabulary gaps."
            recommendations = [
                "Explicitly weave the remaining missing tech tags highlighted below directly into your technical summary sections.",
                "Start each project description line with strong implementation action verbs rather than general passive phrasing.",
                "Ensure common system verification headings stand out clearly to machine token models."
            ]
        elif rounded_score >= 50:
            tier, theme_color = "Fair Match", "#F59E0B"
            msg = "Base structural skills are detected, but key vocabulary additions are highly recommended before application submission."
            recommendations = [
                "Integrate the missing technical keywords smoothly into previous role sentences to build context.",
                "Increase tech stack keyword density. Do not omit crucial frameworks that the description requests repeatedly.",
                "Align phrase names with target job terms to ensure parsing tools record exact matches."
            ]
        else:
            tier, theme_color = "Weak Match", "#EF4444"
            msg = "Significant technical vocabulary mismatch. Focus on realigning bullet point descriptions directly with the target job guidelines."
            recommendations = [
                "Perform a thorough operational rewrite to map your project descriptions straight to the tech stack parameters of the role.",
                "Introduce a clear, dedicated 'Technical Stack Summary' matrix showcasing core engineering keywords you skipped.",
                "Simplify text grids. A clean, single-column design prevents keyword tokens from dropping out during extraction layers."
            ]

        matched_html = "".join([f"<span class='badge-matched'>{word}</span>" for word in matched_keywords]) or "<p style='color: #64748B;'>No primary terms matched yet.</p>"
        missing_html = "".join([f"<span class='badge-missing'>{word}</span>" for word in missing_keywords]) or "<p style='color: #64748B;'>No major missing keywords detected.</p>"
        rec_html = "".join([f"<li style='margin-bottom: 14px; display: flex; gap: 12px; align-items: flex-start; text-align: left;'><i class='fa-solid fa-circle-check' style='color: {theme_color}; margin-top: 4px; flex-shrink:0;'></i> <span>{rec}</span></li>" for rec in recommendations])

        # RETURN TEMPLATE STRING WITH FIXED THEME TOGGLES AND ESCAPED BRACES
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Analysis Result - Deep Report</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
            <link rel="stylesheet" href="/static/css/style.css">
            
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Comfortaa:wght@700&family=Fredoka:wght@600&family=Space+Grotesk:wght@700&display=swap" rel="stylesheet">
            
            <style>
                body {{ background: #f8fafc; color: #0f172a; min-height: 100vh; display: flex; flex-direction: column; transition: background 0.3s, color 0.3s; }}
                main {{ flex: 1; }}
                .report-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-top: 40px; }}
                .metric-card, .main-display-card {{ background: white; border: 1px solid #E2E8F0; border-radius: 24px; padding: 35px; box-shadow: 0 10px 30px rgba(0,0,0,0.02); transition: background 0.3s, border 0.3s; }}
                .tag-container {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 15px; }}
                ul {{ list-style: none; padding: 0; }}
                
                .badge-matched {{ background: rgba(20, 184, 166, 0.08); color: #13524b; border: 1px solid rgba(20, 184, 166, 0.2); padding: 8px 16px; border-radius: 50px; font-weight: 600; font-size: 0.9rem; text-transform: capitalize; }}
                .badge-missing {{ background: rgba(239, 68, 68, 0.08); color: #B91C1C; border: 1px solid rgba(239, 68, 68, 0.2); padding: 8px 16px; border-radius: 50px; font-weight: 600; font-size: 0.9rem; text-transform: capitalize; }}
                
                .theme-toggle-btn {{ background: none; border: none; font-size: 1.4rem; cursor: pointer; padding: 8px; border-radius: 50%; transition: transform 0.2s; }}
                .theme-toggle-btn:hover {{ transform: scale(1.1); }}
                .signout-btn {{ background: #ef4444; color: white; padding: 8px 18px; border-radius: 12px; text-decoration: none; font-weight: 600; font-size: 0.9rem; transition: background 0.2s; }}
                .signout-btn:hover {{ background: #dc2626; }}
                
                /* Dark Theme Scope Injection Overrides */
                body.dark-mode {{ background: #0b0f19 !important; color: #f8fafc !important; }}
                body.dark-mode .metric-card, body.dark-mode .main-display-card {{ background: #111827 !important; border: 1px solid #1f2937 !important; box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important; }}
                body.dark-mode h2, body.dark-mode h3, body.dark-mode span {{ color: #f1f5f9 !important; }}
                body.dark-mode p {{ color: #94a3b8 !important; }}
                body.dark-mode .badge-matched {{ background: rgba(20, 184, 166, 0.15) !important; color: #2dd4bf !important; border-color: rgba(20, 184, 166, 0.4); }}
                body.dark-mode .badge-missing {{ background: rgba(239, 68, 68, 0.15) !important; color: #f87171 !important; border-color: rgba(239, 68, 68, 0.4); }}
                
                @media(max-width: 768px) {{ .report-grid {{ grid-template-columns: 1fr; }} .metric-card {{ grid-column: span 1 !important; }} }}
            </style>
        </head>
        <body>
        <header>
            <nav class="navbar" style="padding: 24px 4%; display: flex; justify-content: space-between; align-items: center;">
                <div class="logo" style="font-weight: 800; font-size: 1.5rem; letter-spacing: -0.5px; font-family: 'Fredoka', 'Comfortaa', 'Space Grotesk', sans-serif;">ATSify</div>
                <div style="display: flex; gap: 20px; align-items: center;">
                    <button class="theme-toggle-btn">🌙</button>
                    <a href="/logout" class="signout-btn"><i class="fa-solid fa-right-from-bracket"></i> Sign Out</a>
                </div>
            </nav>
        </header>
        <main style="max-width: 1100px; margin: 40px auto; padding: 0 4%; width: 100%;">
            <div class="main-display-card" style="text-align: center; padding: 50px 40px;">
                <h2 style="font-size: 2.4rem; font-weight: 800; margin-bottom: 10px;">Optimization Analysis</h2>
                <p style="margin-bottom: 35px; font-size: 1.05rem;">Your real-time automated system checking profile breakdown metrics:</p>
                <div style="background: rgba(20, 184, 166, 0.02); border: 4px solid {theme_color}; width: 160px; height: 160px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 25px auto; box-shadow: inset 0 4px 12px rgba(0,0,0,0.03);">
                    <span style="font-size: 2.8rem; font-weight: 900;">{rounded_score}%</span>
                </div>
                <h3 style="font-size: 1.7rem; font-weight: 700; color: {theme_color}; margin-bottom: 12px;">{tier}</h3>
                <p style="max-width: 650px; margin: 0 auto; line-height: 1.6; font-size: 1.05rem;">{msg}</p>
            </div>
            <div class="report-grid">
                <div class="metric-card">
                    <h3 style="font-size: 1.25rem; font-weight: 700; display: flex; align-items: center; gap: 10px;"><i class="fa-solid fa-circle-check" style="color: #14B8A6;"></i> Matched Core Terms</h3>
                    <p style="font-size: 0.9rem; margin-top: 4px;">Technical core skills verified across both profiles:</p>
                    <div class="tag-container">{matched_html}</div>
                </div>
                <div class="metric-card">
                    <h3 style="font-size: 1.25rem; font-weight: 700; display: flex; align-items: center; gap: 10px;"><i class="fa-solid fa-circle-exclamation" style="color: #EF4444;"></i> Critical Missing Vocabulary</h3>
                    <p style="font-size: 0.9rem; margin-top: 4px;">High-value terms present in the job description that your resume missed:</p>
                    <div class="tag-container">{missing_html}</div>
                </div>
                <div class="metric-card" style="grid-column: span 2;">
                    <h3 style="font-size: 1.35rem; font-weight: 700; margin-bottom: 20px; display: flex; align-items: center; gap: 10px;"><i class="fa-solid fa-wand-magic-sparkles" style="color: #F59E0B;"></i> Actionable Tailored Optimization Plan</h3>
                    <ul style="line-height: 1.7; font-size: 1rem;">
                        {rec_html}
                    </ul>
                </div>
            </div>
            <div style="text-align: center; margin-top: 50px; margin-bottom: 20px;">
                <a href="/analyzer" class="login-btn" style="max-width: 280px; text-decoration: none; display: inline-block; text-align: center;">← Run Another Analysis</a>
            </div>
        </main>
        <footer>
            <div class="footer-content">
                <h3>ATS Resume Analyzer</h3>
                <p>Contact: sanyaa28@gmail.com</p>
                <p>© 2026 ATS Resume Analyzer. All Rights Reserved.</p>
            </div>
        </footer>

        <script>
            const themeToggleBtn = document.querySelector('.theme-toggle-btn');

            // 1. Instantly check memory on load and lock it in
            if (localStorage.getItem('theme') === 'dark') {{
                document.body.classList.add('dark-mode');
                if(themeToggleBtn) themeToggleBtn.textContent = '☀️';
            }}

            // 2. Allow active toggling right on the output screen
            if(themeToggleBtn) {{
                themeToggleBtn.addEventListener('click', () => {{
                    document.body.classList.toggle('dark-mode');
                    
                    let theme = 'light';
                    if (document.body.classList.contains('dark-mode')) {{
                        theme = 'dark';
                        themeToggleBtn.textContent = '☀️';
                    }} else {{
                        themeToggleBtn.textContent = '🌙';
                    }}
                    localStorage.setItem('theme', theme);
                }});
            }}
        </script>
        </body>
        </html>
        """
        
    except Exception as e:
        return f"<h1>Calculation Engine Failure</h1><p style='color:red;'>{str(e)}</p>", 500

@app.route('/logout')
def logout():
    session.clear() 
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)