# ATSify — Resume Analyzer

A straightforward Flask web application designed to analyze resumes against technical job descriptions. ATSify extracts relevant keywords, identifies missing skills, and provides an ATS compatibility score to help job seekers improve their resumes and increase their chances of getting shortlisted.

---

## What It Does

* **Keyword Matching:** Detects missing technologies, skills, tools, and libraries from a job description that are not present in the resume.
* **ATS Score Analysis:** Calculates a compatibility score and categorizes the resume into match levels such as Excellent, Good, Fair, or Weak.
* **Resume Recommendations:** Provides actionable suggestions to improve resume-job alignment.
* **Technical Keyword Processing:** Handles abbreviations and common technical terminology for better matching accuracy.
* **Theme Toggle:** Supports Light and Dark mode with persistent user preferences.

---

## Tech Stack

### Backend

* Python
* Flask

### Database

* MySQL

### Resume Parsing

* PyPDF2
* Regular Expressions (Regex)

### Frontend

* HTML5
* CSS3
* JavaScript

---

## Project Structure

```text
ATSify-resume-analyzer/
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── theme.js
│
├── templates/
│   ├── analyzer.html
│   ├── login.html
│   └── signup.html
│
│
├── app.py
├── schema.sql
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Local Setup

### 1. Clone the Project

```bash
git clone https://github.com/sanyabhatiaa28/ATSify-resume-analyzer.git
cd ATSify-resume-analyzer
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
```

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database

Open MySQL Workbench and execute the SQL statements inside:

```text
schema.sql
```

This will create the required database and authentication tables.

### 5. Run the Application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

---

## Future Improvements

* NLP-based similarity scoring
* TF-IDF keyword weighting
* Resume history tracking
* Advanced ATS recommendations
* Skill gap analysis
* Multiple resume comparison

---

## Author

**Sanya Bhatia**

ATSify — Transforming resumes into ATS-friendly resumes.
