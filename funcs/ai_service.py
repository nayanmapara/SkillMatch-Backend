import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Initialize Google AI Model
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def enhance_resume(resume_content, job_description):
    chat_session = model.start_chat(
        history=[
        ]
    )

    input_text = r"""
    Enhance the following resume content based on the provided job description and format it in LaTeX as specified below.

    Resume Content:""" + resume_content + """

    Job Description: """ + job_description + r"""

    LaTeX Template:
    \\documentclass[letterpaper,11pt]{{article}}
    \\usepackage{{latexsym,fullpage,titlesec,marvosym,color,enumitem,hyperref,fancyhdr,babel,tabularx}}
    \\input{{glyphtounicode}}
    \\usepackage[sfdefault]{{roboto}}

    \\pagestyle{{fancy}}
    \\fancyhf{{}}
    \\renewcommand{{\\headrulewidth}}{{0pt}}
    \\renewcommand{{\\footrulewidth}}{{0pt}}
    \\addtolength{{\\oddsidemargin}}{{-0.5in}}
    \\addtolength{{\\evensidemargin}}{{-0.5in}}
    \\addtolength{{\\textwidth}}{{1in}}
    \\addtolength{{\\topmargin}}{{-.5in}}
    \\addtolength{{\\textheight}}{{1.0in}}
    \\urlstyle{{same}}
    \\raggedbottom
    \\raggedright
    \\setlength{{\\tabcolsep}}{{0in}}

    \\titleformat{{\\section}}{{\\vspace{{-4pt}}\\scshape\\raggedright\\large}}{{}}{{0em}}{{}}[\\color{{black}}\\titlerule \\vspace{{-5pt}}]
    \\pdfgentounicode=1

    % Custom commands
    \\newcommand{{\\resumeItem}}[1]{{\\item\\small{{#1 \\vspace{{-2pt}}}}}}
    \\newcommand{{\\resumeSubheading}}[4]{{\\vspace{{-2pt}}\\item\\begin{{tabular*}}{{0.97\\textwidth}}[t]{{l@{{\\extracolsep{{\\fill}}}}r}}\\textbf{{#1}} & #2 \\\\ \\textit{{\\small#3}} & \\textit{{\\small #4}} \\\\ \\end{{tabular*}}\\vspace{{-7pt}}}}
    \\newcommand{{\\resumeProjectHeading}}[2]{{\\item\\begin{{tabular*}}{{0.97\\textwidth}}{{l@{{\\extracolsep{{\\fill}}}}r}}\\small#1 & #2 \\\\ \\end{{tabular*}}\\vspace{{-7pt}}}}
    \\renewcommand\\labelitemii{{$\\vcenter{{\\hbox{{\\tiny$\\bullet$}}}}}}

    \\begin{{document}}

    \\begin{{center}}
        \\textbf{{\\Huge \\scshape [Your Name]}} \\\\ \\vspace{{1pt}}
        \\small [Your Phone Number] $|$ \\href{{mailto:[your.email@example.com]}}{{\\underline{{your.email@example.com}}}} $|$ 
        \\href{{https://linkedin.com/in/yourlinkedin}}{{\\underline{{linkedin.com/in/yourlinkedin}}}} $|$
        \\href{{https://github.com/yourgithub}}{{\\underline{{github.com/yourgithub}}}} $|$
        \\href{{http://yourportfolio.com}}{{\\underline{{yourportfolio.com}}}}
    \\end{{center}}

    \\section{{Education}}
    \\resumeSubheading{{Your Degree}}{{Expected Graduation Date}}{{Your University}}{{Your Location}}
    \\resumeSubheading{{Your Previous Degree}}{{Graduation Date}}{{Your University}}{{Your Location}}

    \\section{{Experience}}
    \\resumeSubheading{{Your Job Title}}{{Start Date -- End Date}}{{Your Company}}{{Your Location}}
    \\resumeItem{{Description of your responsibilities and achievements.}}
    \\resumeItem{{Description of your responsibilities and achievements.}}
    \\resumeItem{{Description of your responsibilities and achievements.}}

    \\resumeSubheading{{Your Job Title}}{{Start Date -- End Date}}{{Your Company}}{{Your Location}}
    \\resumeItem{{Description of your responsibilities and achievements.}}
    \\resumeItem{{Description of your responsibilities and achievements.}}
    \\resumeItem{{Description of your responsibilities and achievements.}}

    \\section{{Projects}}
    \\resumeProjectHeading{{\\textbf{{Project Name}} $|$ \\emph{{Technologies Used}}}}{{}}
    \\resumeItem{{Description of the project and its achievements.}}
    \\resumeProjectHeading{{\\textbf{{Project Name}} $|$ \\emph{{Technologies Used}}}}{{}}
    \\resumeItem{{Description of the project and its achievements.}}
    \\resumeProjectHeading{{\\textbf{{Project Name}} $|$ \\emph{{Technologies Used}}}}{{}}
    \\resumeItem{{Description of the project and its achievements.}}

    \\section{{Awards \\& Certifications}}
    \\resumeProjectHeading{{Award or Certification Title}}{{Date}}
    \\resumeProjectHeading{{Award or Certification Title}}{{Date}}

    \\section{{Skills}}
    \\begin{{itemize}}[leftmargin=0.15in, label={{}}]
        \\small{{\\item{{
        \\textbf{{Languages}}{: List of languages} \\\\
        \\textbf{{Frameworks \\& Libraries}}{: List of frameworks and libraries} \\\\
        \\textbf{{Cloud}}{: List of cloud services} \\\\
        \\textbf{{DevOps}}{: List of DevOps tools} \\\\
        \\textbf{{Interpersonal Skills}}{: List of interpersonal skills} \\\\
        \\textbf{{Other Skills}}{: List of other skills}
        }}}}
    \\end{{itemize}}

    \\end{{document}}
    """

    response = chat_session.send_message(input_text)

    return response.text
