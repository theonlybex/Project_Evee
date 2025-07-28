# Company Tracker for High-Volume LinkedIn Applications
import json
import csv
import os
from datetime import datetime, timedelta
from typing import Dict, Set, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class ApplicationRecord:
    """Record of a job application"""
    company_name: str
    job_title: str
    job_link: str
    application_date: str
    status: str = "applied"
    notes: str = ""

class CompanyTracker:
    """Tracks companies we've applied to for deduplication"""
    
    def __init__(self, storage_file: str = "applied_companies.json"):
        self.storage_file = storage_file
        self.applied_companies: Dict[str, List[ApplicationRecord]] = self._load_data()
    
    def _load_data(self) -> Dict[str, List[ApplicationRecord]]:
        """Load existing application data"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                # Convert dict back to ApplicationRecord objects
                result = {}
                for company, records in data.items():
                    result[company] = [ApplicationRecord(**record) for record in records]
                return result
            except Exception as e:
                print(f"Warning: Could not load {self.storage_file}: {e}")
        return {}
    
    def _save_data(self):
        """Save application data to file"""
        try:
            # Convert ApplicationRecord objects to dict for JSON serialization
            data = {}
            for company, records in self.applied_companies.items():
                data[company] = [asdict(record) for record in records]
            
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save {self.storage_file}: {e}")
    
    def has_applied_to_company(self, company_name: str) -> bool:
        """Check if we've already applied to this company"""
        company_key = company_name.lower().strip()
        return company_key in self.applied_companies
    
    def add_application(self, company_name: str, job_title: str, job_link: str) -> bool:
        """Add a new application record. Returns True if successfully added."""
        company_key = company_name.lower().strip()
        
        # Check if we've already applied to this company
        if company_key in self.applied_companies:
            # Check if it's the same job (by link)
            for record in self.applied_companies[company_key]:
                if record.job_link == job_link:
                    print(f"⚠️ Already applied to this exact job at {company_name}")
                    return False
            
            print(f"⚠️ Already applied to {company_name} for a different position")
            return False
        
        # Add new application
        record = ApplicationRecord(
            company_name=company_name,
            job_title=job_title,
            job_link=job_link,
            application_date=datetime.now().isoformat()
        )
        
        self.applied_companies[company_key] = [record]
        self._save_data()
        print(f"✅ Recorded application to {company_name} for {job_title}")
        return True
    
    def get_applications_count(self) -> int:
        """Get total number of applications"""
        total = 0
        for records in self.applied_companies.values():
            total += len(records)
        return total
    
    def get_companies_applied_to(self) -> List[str]:
        """Get list of company names we've applied to"""
        return [records[0].company_name for records in self.applied_companies.values()]
    
    def export_to_csv(self, filename: str):
        """Export all applications to CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Company', 'Job Title', 'Job Link', 'Application Date', 'Status', 'Notes'])
            
            for records in self.applied_companies.values():
                for record in records:
                    writer.writerow([
                        record.company_name,
                        record.job_title,
                        record.job_link,
                        record.application_date,
                        record.status,
                        record.notes
                    ])
        print(f"📄 Exported {self.get_applications_count()} applications to {filename}")

class HighVolumeApplicationManager:
    """Manages high-volume job applications with rate limiting and tracking"""
    
    def __init__(self, daily_limit: int = 50, session_limit: int = 25):
        self.daily_limit = daily_limit
        self.session_limit = session_limit
        self.session_count = 0
        self.company_tracker = CompanyTracker()
        self.session_start = datetime.now()
        
    def can_apply_more(self) -> bool:
        """Check if we can submit more applications in this session"""
        return self.session_count < self.session_limit
    
    def should_apply_to_company(self, company_name: str) -> bool:
        """Check if we should apply to this company (not a duplicate)"""
        return not self.company_tracker.has_applied_to_company(company_name)
    
    def record_application(self, company_name: str, job_title: str, job_link: str) -> bool:
        """Record a new application and increment counters"""
        if not self.can_apply_more():
            print(f"🛑 Session limit reached ({self.session_limit} applications)")
            return False
        
        if self.company_tracker.add_application(company_name, job_title, job_link):
            self.session_count += 1
            print(f"📊 Session progress: {self.session_count}/{self.session_limit}")
            return True
        
        return False
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get current session statistics"""
        session_duration = datetime.now() - self.session_start
        return {
            'session_applications': self.session_count,
            'session_limit': self.session_limit,
            'total_applications': self.company_tracker.get_applications_count(),
            'session_duration': str(session_duration).split('.')[0],  # Remove microseconds
            'can_apply_more': self.can_apply_more(),
            'companies_applied_to': len(self.company_tracker.applied_companies)
        }
    
    def print_session_summary(self):
        """Print a summary of the current session"""
        stats = self.get_session_stats()
        print("\n" + "="*50)
        print("📊 APPLICATION SESSION SUMMARY")
        print("="*50)
        print(f"🎯 This Session: {stats['session_applications']}/{stats['session_limit']} applications")
        print(f"📈 Total Applications: {stats['total_applications']}")
        print(f"🏢 Companies Applied To: {stats['companies_applied_to']}")
        print(f"⏱️  Session Duration: {stats['session_duration']}")
        print(f"✅ Can Apply More: {'Yes' if stats['can_apply_more'] else 'No'}")
        print("="*50)
    
    def export_session_data(self, filename: Optional[str] = None):
        """Export session data to CSV"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"session_applications_{timestamp}.csv"
        
        self.company_tracker.export_to_csv(filename)
        return filename

# Example usage and testing
if __name__ == "__main__":
    print("🧪 Testing Company Tracker...")
    
    # Test the company tracker
    tracker = CompanyTracker("test_companies.json")
    
    # Test adding applications
    print("\n📝 Adding test applications...")
    tracker.add_application("Google", "Software Engineer", "https://careers.google.com/job1")
    tracker.add_application("Microsoft", "AI Engineer", "https://careers.microsoft.com/job1") 
    tracker.add_application("Google", "Data Scientist", "https://careers.google.com/job2")  # Should be rejected
    
    print(f"\n📊 Total applications: {tracker.get_applications_count()}")
    print(f"🏢 Companies: {tracker.get_companies_applied_to()}")
    
    # Test the high-volume manager
    print("\n🚀 Testing High-Volume Manager...")
    manager = HighVolumeApplicationManager(daily_limit=5, session_limit=3)
    
    # Test applications
    manager.record_application("Apple", "iOS Developer", "https://jobs.apple.com/job1")
    manager.record_application("Tesla", "Software Engineer", "https://tesla.com/job1")
    manager.record_application("SpaceX", "Backend Engineer", "https://spacex.com/job1")
    manager.record_application("Netflix", "ML Engineer", "https://netflix.com/job1")  # Should hit limit
    
    manager.print_session_summary()
    
    # Export data
    filename = manager.export_session_data()
    print(f"\n📄 Data exported to: {filename}")
    
    # Cleanup test files
    for test_file in ["test_companies.json", filename]:
        if os.path.exists(test_file):
            os.remove(test_file)
            print(f"🧹 Cleaned up: {test_file}") 