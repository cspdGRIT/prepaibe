#!/usr/bin/env python3
"""
AIBE Previous Year Questions Manager
====================================
Script to manage, filter, and integrate previous year questions
"""

import json
import random
from typing import List, Dict
from collections import Counter

class AIBEPreviousYearsManager:
    """Manager for AIBE Previous Year Questions"""
    
    def __init__(self, json_file_path='mock_tests/aibe_previous_years_collection.json'):
        """Initialize with JSON file path"""
        with open(json_file_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.questions = self.data['questions']
        
    def get_all_questions(self) -> List[Dict]:
        """Get all questions"""
        return self.questions
    
    def filter_by_year(self, year: str) -> List[Dict]:
        """
        Filter questions by year
        Examples: 'AIBE XVII', 'AIBE XVIII', 'AIBE XIX'
        """
        return [q for q in self.questions if q['year'] == year]
    
    def filter_by_subject(self, subject: str) -> List[Dict]:
        """
        Filter questions by subject
        Examples: 'Constitutional Law', 'Criminal Law - IPC', 'Contract Law'
        """
        return [q for q in self.questions if q['subject'] == subject]
    
    def filter_by_difficulty(self, difficulty: str) -> List[Dict]:
        """
        Filter by difficulty level
        Options: 'Easy', 'Medium', 'Hard'
        """
        return [q for q in self.questions if q.get('difficulty') == difficulty]
    
    def get_by_id(self, question_id: int) -> Dict:
        """Get specific question by ID"""
        for q in self.questions:
            if q['id'] == question_id:
                return q
        return None
    
    def get_random_questions(self, count: int = 10) -> List[Dict]:
        """Get random questions"""
        return random.sample(self.questions, min(count, len(self.questions)))
    
    def get_subject_wise_stats(self) -> Dict:
        """Get statistics by subject"""
        subjects = [q['subject'] for q in self.questions]
        return dict(Counter(subjects))
    
    def get_year_wise_stats(self) -> Dict:
        """Get statistics by year"""
        years = [q['year'] for q in self.questions]
        return dict(Counter(years))
    
    def get_difficulty_stats(self) -> Dict:
        """Get difficulty distribution"""
        difficulties = [q.get('difficulty', 'Medium') for q in self.questions]
        return dict(Counter(difficulties))
    
    def search_by_keyword(self, keyword: str) -> List[Dict]:
        """Search questions by keyword in question text"""
        keyword_lower = keyword.lower()
        results = []
        for q in self.questions:
            if (keyword_lower in q['question'].lower() or 
                keyword_lower in q.get('explanation', '').lower()):
                results.append(q)
        return results
    
    def get_questions_with_case_law(self) -> List[Dict]:
        """Get questions that reference case laws"""
        return [q for q in self.questions if 'case_law' in q]
    
    def create_custom_test(self, subject_distribution: Dict[str, int]) -> List[Dict]:
        """
        Create custom test with specific subject distribution
        Example: {'Constitutional Law': 10, 'Criminal Law - IPC': 8}
        """
        test_questions = []
        for subject, count in subject_distribution.items():
            subject_questions = self.filter_by_subject(subject)
            selected = random.sample(
                subject_questions, 
                min(count, len(subject_questions))
            )
            test_questions.extend(selected)
        random.shuffle(test_questions)
        return test_questions
    
    def get_sections_list(self) -> List[str]:
        """Get all unique sections/articles referenced"""
        sections = set()
        for q in self.questions:
            if 'section' in q:
                sections.add(q['section'])
        return sorted(list(sections))
    
    def print_question(self, question: Dict, show_answer: bool = False):
        """Pretty print a question"""
        print(f"\n{'='*70}")
        print(f"ID: {question['id']} | Year: {question['year']}")
        print(f"Subject: {question['subject']} | Difficulty: {question.get('difficulty', 'N/A')}")
        print(f"{'='*70}")
        print(f"\nQ. {question['question']}")
        print(f"\nOptions:")
        for i, option in enumerate(question['options']):
            marker = " ✓" if (show_answer and i == question['correct']) else ""
            print(f"   {chr(65+i)}) {option}{marker}")
        
        if show_answer:
            print(f"\n{'─'*70}")
            print(f"Correct Answer: {chr(65 + question['correct'])}")
            print(f"\nExplanation: {question['explanation']}")
            if 'section' in question:
                print(f"\nSection/Article: {question['section']}")
            if 'case_law' in question:
                print(f"Case Law: {question['case_law']}")
        print(f"{'='*70}\n")
    
    def export_to_mock_test_format(self, questions: List[Dict], 
                                   test_name: str, test_id: int = 2):
        """Export questions to mock test format"""
        mock_test = {
            "test_id": test_id,
            "test_name": test_name,
            "total_questions": len(questions),
            "duration_minutes": 210,
            "passing_marks": 40,
            "instructions": "Based on AIBE previous year questions. Each question carries 1 mark.",
            "questions": questions
        }
        
        filename = f"mock_test_{test_id}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(mock_test, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Mock test created: {filename}")
        return filename
    
    def generate_study_plan(self, weak_subjects: List[str] = None):
        """Generate study plan based on question distribution"""
        print("\n" + "="*70)
        print("📚 PERSONALIZED STUDY PLAN")
        print("="*70)
        
        stats = self.get_subject_wise_stats()
        
        print("\n1. AVAILABLE QUESTIONS BY SUBJECT:")
        print("-" * 70)
        for subject, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
            priority = "⚠️ PRIORITY" if weak_subjects and subject in weak_subjects else ""
            print(f"   {subject:.<40} {count:>3} questions {priority}")
        
        print("\n2. RECOMMENDED PRACTICE SEQUENCE:")
        print("-" * 70)
        
        if weak_subjects:
            print("   Focus on your weak subjects first:")
            for i, subject in enumerate(weak_subjects, 1):
                available = stats.get(subject, 0)
                print(f"   {i}. {subject} ({available} questions available)")
        
        print("\n3. DIFFICULTY PROGRESSION:")
        print("-" * 70)
        diff_stats = self.get_difficulty_stats()
        print(f"   Start with: {diff_stats.get('Easy', 0)} Easy questions")
        print(f"   Then try:   {diff_stats.get('Medium', 0)} Medium questions")
        print(f"   Master:     {diff_stats.get('Hard', 0)} Hard questions")
        
        print("\n4. DAILY PRACTICE PLAN:")
        print("-" * 70)
        total_q = len(self.questions)
        print(f"   Total Questions: {total_q}")
        print(f"   Week 1-2: 10 questions/day (focus on Easy)")
        print(f"   Week 3-4: 15 questions/day (mix Easy + Medium)")
        print(f"   Week 5-6: 20 questions/day (all difficulties)")
        print(f"   Week 7: Full mock tests")
        print("="*70 + "\n")


def main():
    """Main function with examples"""
    
    print("\n" + "="*70)
    print("🎓 AIBE Previous Year Questions Manager")
    print("="*70)
    
    # Initialize manager
    manager = AIBEPreviousYearsManager()
    
    print(f"\n📊 Collection Overview:")
    print(f"   Total Questions: {len(manager.questions)}")
    print(f"   Years Covered: {', '.join(manager.data['years_covered'])}")
    
    # Subject-wise stats
    print(f"\n📚 Subject Distribution:")
    for subject, count in sorted(
        manager.get_subject_wise_stats().items(), 
        key=lambda x: x[1], 
        reverse=True
    ):
        print(f"   {subject}: {count}")
    
    # Year-wise stats
    print(f"\n📅 Year Distribution:")
    for year, count in sorted(manager.get_year_wise_stats().items()):
        print(f"   {year}: {count}")
    
    # Examples
    print(f"\n" + "="*70)
    print("💡 USAGE EXAMPLES")
    print("="*70)
    
    # Example 1: Get questions by subject
    print("\n1️⃣ Constitutional Law Questions:")
    const_questions = manager.filter_by_subject('Constitutional Law')
    print(f"   Found {len(const_questions)} questions")
    
    # Example 2: Get by year
    print("\n2️⃣ AIBE XVIII Questions:")
    xviii_questions = manager.filter_by_year('AIBE XVIII')
    print(f"   Found {len(xviii_questions)} questions")
    
    # Example 3: Get easy questions
    print("\n3️⃣ Easy Questions:")
    easy_questions = manager.filter_by_difficulty('Easy')
    print(f"   Found {len(easy_questions)} questions")
    
    # Example 4: Show a sample question
    print("\n4️⃣ Sample Question:")
    sample = manager.get_by_id(1)
    manager.print_question(sample, show_answer=True)
    
    # Example 5: Create custom test
    print("\n5️⃣ Creating Custom Test:")
    custom_dist = {
        'Constitutional Law': 5,
        'Criminal Law - IPC': 3,
        'Contract Law': 2
    }
    custom_test = manager.create_custom_test(custom_dist)
    print(f"   Created test with {len(custom_test)} questions")
    
    # Example 6: Search by keyword
    print("\n6️⃣ Search 'section 34':")
    results = manager.search_by_keyword('section 34')
    print(f"   Found {len(results)} questions")
    
    # Example 7: Generate study plan
    manager.generate_study_plan(weak_subjects=[
        'Constitutional Law', 
        'Criminal Procedure Code'
    ])
    
    print("\n" + "="*70)
    print("✅ Demo Complete!")
    print("="*70)
    print("\n💡 Integration Ideas:")
    print("   1. Load questions into your mock exam system")
    print("   2. Create topic-wise practice tests")
    print("   3. Build a flashcard system from Q&A")
    print("   4. Generate daily practice quizzes")
    print("   5. Track progress by difficulty level")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()


# ============================================================================
# ADDITIONAL UTILITY FUNCTIONS
# ============================================================================

def create_aibe_mock_test_2():
    """Create Mock Test 2 from previous years questions"""
    manager = AIBEPreviousYearsManager()
    
    # Create balanced test
    distribution = {
        'Constitutional Law': 10,
        'Criminal Law - IPC': 8,
        'Criminal Procedure Code': 8,
        'Contract Law': 5,
        'Civil Procedure Code': 5,
        'Evidence Act': 6,
        'Property Law': 4,
        'Family Law': 4,
        'Torts': 4,
        'Company Law': 4,
        'Labour Law': 4,
        'Professional Ethics': 4,
        'Arbitration': 3,
        'Jurisprudence': 2
    }
    
    # Calculate remaining questions needed
    total_needed = 100
    total_distributed = sum(distribution.values())
    remaining = total_needed - total_distributed
    
    # Add random questions for remaining
    test_questions = manager.create_custom_test(distribution)
    
    if remaining > 0:
        remaining_questions = manager.get_random_questions(remaining)
        test_questions.extend(remaining_questions)
    
    # Create the mock test
    manager.export_to_mock_test_format(
        test_questions[:100],  # Ensure exactly 100
        "AIBE Mock Test 2 - Previous Years Edition",
        test_id=2
    )


def analyze_difficulty_by_subject():
    """Analyze difficulty distribution by subject"""
    manager = AIBEPreviousYearsManager()
    
    print("\n" + "="*70)
    print("📊 DIFFICULTY ANALYSIS BY SUBJECT")
    print("="*70 + "\n")
    
    subjects = set(q['subject'] for q in manager.questions)
    
    for subject in sorted(subjects):
        subject_qs = manager.filter_by_subject(subject)
        easy = len([q for q in subject_qs if q.get('difficulty') == 'Easy'])
        medium = len([q for q in subject_qs if q.get('difficulty') == 'Medium'])
        hard = len([q for q in subject_qs if q.get('difficulty') == 'Hard'])
        
        print(f"{subject}")
        print(f"  Easy: {easy} | Medium: {medium} | Hard: {hard}")
        print(f"  Total: {len(subject_qs)}")
        print()


def create_subject_wise_study_guide():
    """Create subject-wise study guide"""
    manager = AIBEPreviousYearsManager()
    
    subjects = manager.get_subject_wise_stats()
    
    print("\n" + "="*70)
    print("📚 SUBJECT-WISE STUDY GUIDE")
    print("="*70)
    
    for subject in sorted(subjects.keys()):
        print(f"\n{'='*70}")
        print(f"SUBJECT: {subject.upper()}")
        print('='*70)
        
        subject_qs = manager.filter_by_subject(subject)
        
        # Get unique sections
        sections = set()
        case_laws = set()
        
        for q in subject_qs:
            if 'section' in q:
                sections.add(q['section'])
            if 'case_law' in q:
                case_laws.add(q['case_law'])
        
        print(f"\nTotal Questions: {len(subject_qs)}")
        
        if sections:
            print(f"\nKey Sections/Articles:")
            for section in sorted(sections):
                print(f"  • {section}")
        
        if case_laws:
            print(f"\nLandmark Cases:")
            for case in sorted(case_laws):
                print(f"  • {case}")
        
        print(f"\nSample Questions:")
        for i, q in enumerate(subject_qs[:2], 1):
            print(f"\n  Q{i}. {q['question'][:100]}...")
            print(f"      (See ID: {q['id']} for full question)")


# Example usage in comments
"""
# Quick Examples:

# 1. Load the manager
manager = AIBEPreviousYearsManager()

# 2. Get all constitutional law questions
const_qs = manager.filter_by_subject('Constitutional Law')

# 3. Create a practice test with 20 random questions
practice = manager.get_random_questions(20)

# 4. Get only hard questions
hard_qs = manager.filter_by_difficulty('Hard')

# 5. Search for questions about 'section 34'
results = manager.search_by_keyword('section 34')

# 6. Create a custom mock test
manager.export_to_mock_test_format(
    manager.get_random_questions(100),
    "My Custom AIBE Mock Test"
)

# 7. Print a question with answer
q = manager.get_by_id(1)
manager.print_question(q, show_answer=True)
"""
