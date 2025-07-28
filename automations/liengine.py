# Enhanced LinkedIn Automation with Configurable Variables
import sys
import os
import asyncio
import csv
import json
from typing import List, Optional, Dict, Any
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime

from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from browser_use import ActionResult, Agent, Browser, Controller
from .company_tracker import HighVolumeApplicationManager

load_dotenv()

# ======================== CONFIGURATION CLASSES ========================

@dataclass
class PersonalInfo:
    """Personal information for job applications"""
    full_name: str = "Your Full Name"
    email: str = "your.email@example.com"
    phone: str = "+1 (555) 123-4567"
    linkedin_url: str = "https://linkedin.com/in/yourprofile"
    github_url: str = "https://github.com/yourusername"
    portfolio_url: str = "https://yourportfolio.com"
    address: str = "City, State, Country"
    nationality: str = "Your Nationality"

@dataclass
class Experience:
    """Professional experience details"""
    years_of_experience: str = "3-5 years"
    current_role: str = "Software Engineer"
    current_company: str = "Current Company"
    key_skills: List[str] = None
    programming_languages: List[str] = None
    frameworks: List[str] = None
    certifications: List[str] = None
    
    def __post_init__(self):
        if self.key_skills is None:
            self.key_skills = ["Python", "Machine Learning", "AI", "Data Analysis"]
        if self.programming_languages is None:
            self.programming_languages = ["Python", "JavaScript", "SQL", "R"]
        if self.frameworks is None:
            self.frameworks = ["TensorFlow", "PyTorch", "React", "FastAPI"]
        if self.certifications is None:
            self.certifications = ["AWS Certified", "Google Cloud Professional"]

@dataclass
class Education:
    """Educational background"""
    degree: str = "Bachelor's in Computer Science"
    university: str = "University Name"
    graduation_year: str = "2021"
    gpa: str = "3.8/4.0"
    relevant_coursework: List[str] = None
    
    def __post_init__(self):
        if self.relevant_coursework is None:
            self.relevant_coursework = ["Machine Learning", "Data Structures", "Algorithms", "Statistics"]

@dataclass
class JobPreferences:
    """Job search preferences and requirements"""
    desired_roles: List[str] = None
    preferred_locations: List[str] = None
    work_arrangements: List[str] = None
    salary_range_min: str = "$80,000"
    salary_range_max: str = "$120,000"
    notice_period: str = "2 weeks"
    availability_date: str = "Immediately"
    willing_to_relocate: bool = True
    visa_sponsorship_needed: bool = False
    
    def __post_init__(self):
        if self.desired_roles is None:
            self.desired_roles = ["Software Engineer", "ML Engineer", "Data Scientist"]
        if self.preferred_locations is None:
            self.preferred_locations = ["Remote", "San Francisco", "New York"]
        if self.work_arrangements is None:
            self.work_arrangements = ["Remote", "Hybrid", "On-site"]

@dataclass
class CoverLetterTemplates:
    """Cover letter templates for different types of applications"""
    default_template: str = """
Dear Hiring Manager,

I am excited to apply for the {job_title} position at {company_name}. With {experience_years} of experience in {key_skills}, I am confident I can contribute significantly to your team.

In my current role as {current_role} at {current_company}, I have successfully {key_achievement}. My expertise in {technical_skills} aligns perfectly with your requirements.

I am particularly drawn to {company_name} because of {company_reason}. I would welcome the opportunity to discuss how my background in {relevant_experience} can benefit your organization.

Thank you for your consideration.

Best regards,
{full_name}
"""
    
    startup_template: str = """
Hi {hiring_manager_name},

I'm thrilled to apply for the {job_title} role at {company_name}! As someone passionate about {relevant_field}, I'm excited about the opportunity to contribute to your innovative team.

With {experience_years} of hands-on experience in {key_technologies}, I've built {specific_projects} that directly relate to your needs. I thrive in fast-paced environments and love wearing multiple hats.

What excites me most about {company_name} is {startup_specific_reason}. I'd love to discuss how my {unique_skill} can help drive your mission forward.

Looking forward to hearing from you!

Best,
{full_name}
"""
    
    tech_giant_template: str = """
Dear {company_name} Hiring Team,

I am writing to express my strong interest in the {job_title} position. With a solid foundation in {technical_expertise} and {experience_years} of progressive experience, I am eager to contribute to {company_name}'s continued innovation.

My background includes {specific_achievements} and deep expertise in {core_technologies}. I have consistently delivered {quantifiable_results} while working on {project_scale} projects.

I am particularly impressed by {company_name}'s commitment to {company_values} and would be honored to contribute to your team's success.

Sincerely,
{full_name}
"""

# ======================== PYDANTIC MODELS ========================

class Job(BaseModel):
    title: str
    link: str
    company: str
    salary: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    posted_date: Optional[str] = None
    application_deadline: Optional[str] = None

class Jobs(BaseModel):
    jobs: List[Job]

class ApplicationConfig(BaseModel):
    """Complete configuration for job applications"""
    personal_info: Dict[str, Any]
    experience: Dict[str, Any]
    education: Dict[str, Any]
    job_preferences: Dict[str, Any]
    cover_letter_templates: Dict[str, str]
    cv_file_path: str = "cv_04_24.pdf"
    max_applications_per_session: int = 200
    application_delay_seconds: int = 30
    auto_apply_enabled: bool = True
    save_applied_jobs: bool = True

# ======================== CONFIGURATION MANAGER ========================

class ConfigManager:
    """Manages job application configuration"""
    
    def __init__(self, config_file: str = "job_application_config.json"):
        self.config_file = config_file
        self.config = self._load_or_create_config()
    
    def _load_or_create_config(self) -> ApplicationConfig:
        """Load existing config or create default one"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                return ApplicationConfig(**config_data)
            except Exception as e:
                print(f"Error loading config: {e}. Creating default config.")
        
        # Create default configuration
        default_config = ApplicationConfig(
            personal_info=asdict(PersonalInfo()),
            experience=asdict(Experience()),
            education=asdict(Education()),
            job_preferences=asdict(JobPreferences()),
            cover_letter_templates=asdict(CoverLetterTemplates())
        )
        
        self.save_config(default_config)
        return default_config
    
    def save_config(self, config: ApplicationConfig):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(config.dict(), f, indent=2)
        print(f"Configuration saved to {self.config_file}")
    
    def update_personal_info(self, **kwargs):
        """Update personal information"""
        for key, value in kwargs.items():
            if key in self.config.personal_info:
                self.config.personal_info[key] = value
        self.save_config(self.config)
    
    def update_experience(self, **kwargs):
        """Update experience information"""
        for key, value in kwargs.items():
            if key in self.config.experience:
                self.config.experience[key] = value
        self.save_config(self.config)
    
    def get_cover_letter(self, template_type: str = "default", **kwargs) -> str:
        """Generate customized cover letter"""
        template = self.config.cover_letter_templates.get(f"{template_type}_template", 
                                                         self.config.cover_letter_templates["default_template"])
        
        # Merge all config data for template formatting
        format_data = {
            **self.config.personal_info,
            **self.config.experience,
            **self.config.education,
            **kwargs  # Allow override of any values
        }
        
        try:
            return template.format(**format_data)
        except KeyError as e:
            print(f"Missing template variable: {e}")
            return template

# ======================== ENHANCED CONTROLLER ACTIONS ========================

# Initialize global configuration with test config file
config_manager = ConfigManager("test_config_25.json")
controller = Controller()

# Initialize company tracking for 25-application test
app_manager = HighVolumeApplicationManager(daily_limit=25, session_limit=25)

@controller.action(description='Save jobs to file with detailed information', param_model=Jobs)
def save_jobs(params: Jobs) -> None:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'jobs_{timestamp}.csv'
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(['Title', 'Company', 'Link', 'Salary', 'Location', 'Job Type', 'Posted Date', 'Deadline'])
        
        for job in params.jobs:
            writer.writerow([
                job.title, job.company, job.link, job.salary or 'N/A', 
                job.location or 'N/A', job.job_type or 'N/A', 
                job.posted_date or 'N/A', job.application_deadline or 'N/A'
            ])
    
    print(f"Saved {len(params.jobs)} jobs to {filename}")

@controller.action(description="Read jobs from CSV file")
def read_jobs() -> str:
    try:
        with open('jobs.csv', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "No jobs file found. Please search for jobs first."

@controller.action(description='Get my personal information for applications')
def get_personal_info() -> ActionResult:
    info = config_manager.config.personal_info
    formatted_info = f"""
Personal Information:
- Name: {info['full_name']}
- Email: {info['email']}
- Phone: {info['phone']}
- LinkedIn: {info['linkedin_url']}
- GitHub: {info['github_url']}
- Portfolio: {info['portfolio_url']}
- Location: {info['address']}
"""
    return ActionResult(extracted_content=formatted_info, include_in_memory=True)

@controller.action(description='Get my experience and skills for applications')
def get_experience_info() -> ActionResult:
    exp = config_manager.config.experience
    formatted_exp = f"""
Professional Experience:
- Years of Experience: {exp['years_of_experience']}
- Current Role: {exp['current_role']} at {exp['current_company']}
- Key Skills: {', '.join(exp['key_skills'])}
- Programming Languages: {', '.join(exp['programming_languages'])}
- Frameworks: {', '.join(exp['frameworks'])}
- Certifications: {', '.join(exp['certifications'])}
"""
    return ActionResult(extracted_content=formatted_exp, include_in_memory=True)

@controller.action(description='Generate customized cover letter for application')
def generate_cover_letter(job_title: str, company_name: str, template_type: str = "default") -> ActionResult:
    cover_letter = config_manager.get_cover_letter(
        template_type=template_type,
        job_title=job_title,
        company_name=company_name,
        key_achievement="led multiple successful projects",
        company_reason="your innovative approach to technology",
        relevant_experience="software development and machine learning"
    )
    
    return ActionResult(extracted_content=cover_letter, include_in_memory=True)

@controller.action(description='Ask me for help with specific information')
def ask_human(question: str) -> str:
    return input(f'\n{question}\nInput: ')

@controller.action(description='Read my CV for context to fill forms')
def read_cv() -> ActionResult:
    cv_path = config_manager.config.cv_file_path
    try:
        pdf = PdfReader(cv_path)
        text = ''
        for page in pdf.pages:
            text += page.extract_text() or ''
        return ActionResult(extracted_content=text, include_in_memory=True)
    except FileNotFoundError:
        return ActionResult(extracted_content=f"CV file not found: {cv_path}", include_in_memory=True)

@controller.action(description='Upload CV to application form')
async def upload_cv(index: int, browser: Browser) -> str:
    await close_file_dialog(browser)
    element = await browser.get_element_by_index(index=index)
    cv_path = Path.cwd() / config_manager.config.cv_file_path
    
    if not element:
        raise Exception(f'Element with index {index} not found')
    
    if not cv_path.exists():
        raise Exception(f'CV file not found: {cv_path}')
    
    await element.set_input_files(files=[str(cv_path.absolute())])
    return f'Uploaded CV to element at index {index}'

@controller.action(description='Close file dialog')
async def close_file_dialog(browser: Browser) -> None:
    page = await browser.get_current_page()
    await page.keyboard.press(key='Escape')

@controller.action(description='Fill application form with my information')
async def fill_application_form(form_fields: Dict[str, str], browser: Browser) -> str:
    """Fill application form fields with configured information"""
    personal_info = config_manager.config.personal_info
    experience = config_manager.config.experience
    
    # Mapping of common form fields to config values
    field_mappings = {
        'first_name': personal_info['full_name'].split()[0],
        'last_name': ' '.join(personal_info['full_name'].split()[1:]),
        'full_name': personal_info['full_name'],
        'email': personal_info['email'],
        'phone': personal_info['phone'],
        'linkedin': personal_info['linkedin_url'],
        'github': personal_info['github_url'],
        'portfolio': personal_info['portfolio_url'],
        'years_experience': experience['years_of_experience'],
        'current_company': experience['current_company'],
        'current_role': experience['current_role'],
    }
    
    filled_fields = []
    for field_name, element_index in form_fields.items():
        if field_name in field_mappings:
            try:
                element = await browser.get_element_by_index(index=int(element_index))
                if element:
                    await element.fill(field_mappings[field_name])
                    filled_fields.append(field_name)
            except Exception as e:
                print(f"Error filling field {field_name}: {e}")
    
    return f"Filled fields: {', '.join(filled_fields)}"

# ======================== COMPANY TRACKING ACTIONS ========================

@controller.action(description='Check if we should apply to this company (prevents duplicates)')
def should_apply_to_company(company_name: str) -> bool:
    """Check if we should apply to this company (prevents duplicates)"""
    can_apply = app_manager.should_apply_to_company(company_name)
    if can_apply:
        print(f"✅ New company: {company_name} - Will apply")
    else:
        print(f"⚠️  Already applied to: {company_name} - Skipping")
    return can_apply

@controller.action(description='Record successful application to company')
def record_application(company_name: str, job_title: str, job_link: str) -> bool:
    """Record that we successfully applied to this company"""
    success = app_manager.record_application(company_name, job_title, job_link)
    if success:
        stats = app_manager.get_session_summary()
        print(f"📊 Progress: {stats['session_applications']}/{stats['session_limit']} applications today")
    return success

@controller.action(description='Get current application statistics')
def get_application_stats() -> str:
    """Get current application statistics"""
    summary = app_manager.get_session_summary()
    stats_text = f"""
📊 APPLICATION STATISTICS:
- Session: {summary['session_applications']}/{summary['session_limit']}
- Today: {summary['daily_applications']}/{summary['daily_limit']}
- Total Companies: {summary['total_companies']}
- Remaining: {summary['remaining_today']}
"""
    return stats_text

# ======================== MAIN EXECUTION ========================

async def run_job_search_and_apply():
    """Main function for job search and application"""
    preferences = config_manager.config.job_preferences
    
    task = f"""
    Job Search and Application Task:
    
    1. Search for {', '.join(preferences['desired_roles'])} positions
    2. Focus on locations: {', '.join(preferences['preferred_locations'])}
    3. Look for {', '.join(preferences['work_arrangements'])} opportunities
    4. Salary range: {preferences['salary_range_min']} - {preferences['salary_range_max']}
    
    5. For each suitable job:
       - Extract job details (title, company, salary, location, requirements)
       - Save job information to CSV
       - If auto-apply is enabled, apply using my configured information
       - Generate appropriate cover letter based on company type
       - Fill application forms with my personal details
       - Upload CV when required
    
    6. Apply to maximum {config_manager.config.max_applications_per_session} positions
    7. Wait {config_manager.config.application_delay_seconds} seconds between applications
    8. If you need any clarification, ask me using the ask_human function
    
    Use my configured personal information, experience, and preferences for all applications.
    """
    
    model = ChatOpenAI(model='gpt-4o')
    agent = Agent(task=task, llm=model, controller=controller)
    
    await agent.run()

def setup_configuration():
    """Display current configuration from test_config_25.json"""
    print("🔧 Current Job Application Configuration")
    print("=" * 50)
    print(f"📁 Using config file: {config_manager.config_file}")
    
    # Personal Information
    print("\n📋 Personal Information:")
    print(f"👤 Name: {config_manager.config.personal_info['full_name']}")
    print(f"📧 Email: {config_manager.config.personal_info['email']}")
    print(f"📱 Phone: {config_manager.config.personal_info['phone']}")
    print(f"🔗 LinkedIn: {config_manager.config.personal_info['linkedin_url']}")
    
    # Experience
    print("\n💼 Experience Information:")
    print(f"🏢 Current Role: {config_manager.config.experience['current_role']}")
    print(f"📅 Experience: {config_manager.config.experience['years_of_experience']}")
    print(f"💻 Skills: {', '.join(config_manager.config.experience['key_skills'][:3])}...")
    
    # Job Preferences
    print("\n🎯 Job Preferences:")
    print(f"🎯 Desired Roles: {', '.join(config_manager.config.job_preferences['desired_roles'])}")
    print(f"📍 Locations: {', '.join(config_manager.config.job_preferences['preferred_locations'])}")
    print(f"💰 Salary Range: {config_manager.config.job_preferences['salary_range_min']} - {config_manager.config.job_preferences['salary_range_max']}")
    
    # Application Settings
    print("\n⚙️ Application Settings:")
    print(f"📄 CV Path: {config_manager.config.cv_file_path}")
    print(f"📊 Max Applications: {config_manager.config.max_applications_per_session}")
    print(f"⏱️  Delay: {config_manager.config.application_delay_seconds} seconds")
    
    print("\n✅ Configuration loaded successfully from test_config_25.json!")
    print("ℹ️  To modify settings, edit the test_config_25.json file directly.")

async def run_test_mode_25():
    """Test mode for 25 applications with company deduplication"""
    print("\n🧪 TEST MODE: 25 Applications")
    print("="*50)
    
    # Show initial stats
    app_manager.print_session_summary()
    
    task = """
    TEST MODE - 25 Job Applications with Company Deduplication:
    
    IMPORTANT: Before applying to any job, ALWAYS:
    1. Use should_apply_to_company(company_name) to check if we've applied before
    2. If it returns True, proceed with application
    3. If it returns False, skip and move to next job
    4. After successful application, use record_application(company_name, job_title, job_link)
    
    Your task:
    1. Search for Software Engineer, ML Engineer, and Data Scientist positions
    2. Focus on Remote, San Francisco, and New York locations
    3. For each job found:
       - Extract company name, job title, and link
       - Check should_apply_to_company(company_name) first
       - If approved, apply using my configured information and CV
       - Record with record_application() after successful application
       - Use get_application_stats() to track progress
    
    4. Apply to maximum 25 positions (this is a test run)
    5. Use 2-minute delays between applications
    6. Stop when you reach 25 applications or run out of new companies
    7. Provide final summary with get_application_stats()
    
    Remember: Quality over quantity. Only apply to relevant positions at companies we haven't contacted before.
    """
    
    model = ChatOpenAI(model='gpt-4o')
    agent = Agent(task=task, llm=model, controller=controller)
    
    try:
        await agent.run()
    finally:
        # Final summary
        print("\n" + "="*60)
        print("🏁 TEST SESSION COMPLETE")
        print("="*60)
        app_manager.print_session_summary()
        
        # Export application history
        app_manager.company_tracker.export_to_csv('test_applications_25.csv')
        print("📄 Application history exported to test_applications_25.csv")

# ======================== ENGINE INTERFACE FUNCTIONS ========================

def get_config_info():
    """Get current configuration information"""
    return {
        'config_file': config_manager.config_file,
        'personal_info': config_manager.config.personal_info,
        'max_applications_per_session': config_manager.config.max_applications_per_session,
        'cv_file_path': config_manager.config.cv_file_path
    }

# This file can now be imported as an engine
# All the key functions are available:
# - setup_configuration()
# - run_job_search_and_apply()
# - generate_cover_letter(job_title, company, template_type)
# - run_test_mode_25()
# - get_personal_info()
# - get_experience_info()
# - read_cv()
# - get_config_info()
# - should_apply_to_company(company_name)
# - record_application(company_name, job_title, job_link)
# - get_application_stats() 