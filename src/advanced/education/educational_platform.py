# Educational Platform System
# Learning and teaching tools for sign language education

import json
import time
import random
from typing import Dict, List, Optional, Tuple
from pathlib import Path

class EducationalPlatform:
    """Educational platform for sign language learning"""
    
    def __init__(self):
        """Initialize educational platform"""
        self.lessons = self._create_lesson_structure()
        self.students = {}
        self.teachers = {}
        self.progress_tracker = {}
        self.assessments = self._create_assessments()
        self.gamification = self._create_gamification_system()
        
        print("âœ… Educational Platform initialized")
        print(f"ðŸ“š Lessons: {len(self.lessons)}")
        print(f"ðŸŽ¯ Assessments: {len(self.assessments)}")
        print(f"ðŸŽ® Gamification: Active")
    
    def _create_lesson_structure(self) -> Dict:
        """Create structured lesson plan"""
        return {
            "beginner": {
                "level": 1,
                "title": "Beginner ASL",
                "description": "Learn basic ASL signs and gestures",
                "lessons": [
                    {
                        "id": "lesson_1",
                        "title": "Basic Greetings",
                        "description": "Learn hello, goodbye, please, thank you",
                        "signs": ["hello", "goodbye", "please", "thank_you"],
                        "duration_minutes": 15,
                        "difficulty": "easy",
                        "prerequisites": [],
                        "learning_objectives": [
                            "Recognize basic greeting signs",
                            "Perform greeting signs correctly",
                            "Understand cultural context"
                        ]
                    },
                    {
                        "id": "lesson_2",
                        "title": "Yes and No",
                        "description": "Learn affirmation and negation",
                        "signs": ["yes", "no", "maybe", "okay"],
                        "duration_minutes": 10,
                        "difficulty": "easy",
                        "prerequisites": ["lesson_1"],
                        "learning_objectives": [
                            "Distinguish between yes and no signs",
                            "Use appropriate affirmation/negation",
                            "Practice with different contexts"
                        ]
                    },
                    {
                        "id": "lesson_3",
                        "title": "Basic Needs",
                        "description": "Learn signs for essential needs",
                        "signs": ["water", "food", "bathroom", "help"],
                        "duration_minutes": 20,
                        "difficulty": "easy",
                        "prerequisites": ["lesson_1", "lesson_2"],
                        "learning_objectives": [
                            "Express basic needs",
                            "Recognize emergency signs",
                            "Practice in real scenarios"
                        ]
                    }
                ]
            },
            "intermediate": {
                "level": 2,
                "title": "Intermediate ASL",
                "description": "Build on basic skills with more complex signs",
                "lessons": [
                    {
                        "id": "lesson_4",
                        "title": "Emotions",
                        "description": "Learn emotional expressions",
                        "signs": ["happy", "sad", "angry", "surprised", "love"],
                        "duration_minutes": 25,
                        "difficulty": "medium",
                        "prerequisites": ["lesson_1", "lesson_2", "lesson_3"],
                        "learning_objectives": [
                            "Express emotions clearly",
                            "Recognize emotional signs",
                            "Use appropriate emotional context"
                        ]
                    },
                    {
                        "id": "lesson_5",
                        "title": "Family and Relationships",
                        "description": "Learn family-related signs",
                        "signs": ["family", "friend", "mother", "father", "brother", "sister"],
                        "duration_minutes": 30,
                        "difficulty": "medium",
                        "prerequisites": ["lesson_4"],
                        "learning_objectives": [
                            "Describe family relationships",
                            "Use appropriate family signs",
                            "Understand cultural family concepts"
                        ]
                    }
                ]
            },
            "advanced": {
                "level": 3,
                "title": "Advanced ASL",
                "description": "Master complex signs and conversations",
                "lessons": [
                    {
                        "id": "lesson_6",
                        "title": "Professional Communication",
                        "description": "Learn workplace and professional signs",
                        "signs": ["work", "meeting", "presentation", "deadline", "project"],
                        "duration_minutes": 40,
                        "difficulty": "hard",
                        "prerequisites": ["lesson_5"],
                        "learning_objectives": [
                            "Communicate in professional settings",
                            "Use appropriate workplace signs",
                            "Handle professional conversations"
                        ]
                    },
                    {
                        "id": "lesson_7",
                        "title": "Medical Communication",
                        "description": "Learn medical and healthcare signs",
                        "signs": ["doctor", "nurse", "hospital", "medicine", "pain", "emergency"],
                        "duration_minutes": 45,
                        "difficulty": "hard",
                        "prerequisites": ["lesson_6"],
                        "learning_objectives": [
                            "Communicate medical needs",
                            "Recognize emergency signs",
                            "Handle healthcare situations"
                        ]
                    }
                ]
            }
        }
    
    def _create_assessments(self) -> Dict:
        """Create assessment system"""
        return {
            "quiz_1": {
                "title": "Basic Signs Quiz",
                "level": "beginner",
                "questions": [
                    {
                        "question": "What is the sign for 'hello'?",
                        "options": ["Wave hand", "Thumbs up", "Point finger", "Clap hands"],
                        "correct_answer": 0,
                        "explanation": "Hello is signed by waving your hand in a greeting motion"
                    },
                    {
                        "question": "How do you sign 'yes'?",
                        "options": ["Shake head", "Make fist and nod", "Point up", "Clap"],
                        "correct_answer": 1,
                        "explanation": "Yes is signed by making a fist and nodding up and down"
                    }
                ],
                "passing_score": 70
            },
            "quiz_2": {
                "title": "Emotions Quiz",
                "level": "intermediate",
                "questions": [
                    {
                        "question": "What is the sign for 'love'?",
                        "options": ["Heart shape", "Thumbs up", "Wave", "Point"],
                        "correct_answer": 0,
                        "explanation": "Love is signed by forming a heart shape with your hands"
                    }
                ],
                "passing_score": 80
            }
        }
    
    def _create_gamification_system(self) -> Dict:
        """Create gamification elements"""
        return {
            "points_system": {
                "lesson_completion": 100,
                "quiz_correct": 50,
                "perfect_score": 200,
                "daily_practice": 25,
                "streak_bonus": 50
            },
            "badges": {
                "first_lesson": "ðŸŽ“ First Steps",
                "perfect_quiz": "â­ Perfect Score",
                "week_streak": "ðŸ”¥ Week Warrior",
                "month_streak": "ðŸ† Monthly Master",
                "all_lessons": "ðŸŽ¯ Course Complete"
            },
            "levels": {
                "novice": {"min_points": 0, "max_points": 500},
                "apprentice": {"min_points": 500, "max_points": 1000},
                "expert": {"min_points": 1000, "max_points": 2000},
                "master": {"min_points": 2000, "max_points": 5000},
                "grandmaster": {"min_points": 5000, "max_points": 10000}
            }
        }
    
    def register_student(self, student_id: str, name: str, email: str) -> bool:
        """Register a new student"""
        try:
            self.students[student_id] = {
                "name": name,
                "email": email,
                "registration_date": time.time(),
                "current_level": "beginner",
                "current_lesson": "lesson_1",
                "points": 0,
                "badges": [],
                "streak_days": 0,
                "last_activity": time.time()
            }
            
            # Initialize progress tracking
            self.progress_tracker[student_id] = {
                "lessons_completed": [],
                "quizzes_taken": [],
                "total_time_spent": 0,
                "accuracy_scores": []
            }
            
            print(f"âœ… Student {name} registered successfully")
            return True
            
        except Exception as e:
            print(f"âŒ Error registering student: {e}")
            return False
    
    def register_teacher(self, teacher_id: str, name: str, email: str, qualifications: List[str]) -> bool:
        """Register a new teacher"""
        try:
            self.teachers[teacher_id] = {
                "name": name,
                "email": email,
                "qualifications": qualifications,
                "registration_date": time.time(),
                "students": [],
                "classes_taught": 0
            }
            
            print(f"âœ… Teacher {name} registered successfully")
            return True
            
        except Exception as e:
            print(f"âŒ Error registering teacher: {e}")
            return False
    
    def get_lesson(self, lesson_id: str) -> Optional[Dict]:
        """Get lesson information"""
        for level_data in self.lessons.values():
            for lesson in level_data["lessons"]:
                if lesson["id"] == lesson_id:
                    return lesson
        return None
    
    def get_next_lesson(self, student_id: str) -> Optional[Dict]:
        """Get next lesson for student"""
        if student_id not in self.students:
            return None
        
        student = self.students[student_id]
        current_level = student["current_level"]
        current_lesson = student["current_lesson"]
        
        # Find current lesson
        current_lesson_data = self.get_lesson(current_lesson)
        if not current_lesson_data:
            return None
        
        # Find next lesson in same level
        level_data = self.lessons[current_level]
        current_index = -1
        for i, lesson in enumerate(level_data["lessons"]):
            if lesson["id"] == current_lesson:
                current_index = i
                break
        
        if current_index >= 0 and current_index < len(level_data["lessons"]) - 1:
            return level_data["lessons"][current_index + 1]
        
        # Move to next level
        level_order = ["beginner", "intermediate", "advanced"]
        current_level_index = level_order.index(current_level)
        if current_level_index < len(level_order) - 1:
            next_level = level_order[current_level_index + 1]
            next_level_data = self.lessons[next_level]
            if next_level_data["lessons"]:
                return next_level_data["lessons"][0]
        
        return None
    
    def complete_lesson(self, student_id: str, lesson_id: str, accuracy: float, time_spent: int) -> bool:
        """Mark lesson as completed"""
        try:
            if student_id not in self.students:
                return False
            
            student = self.students[student_id]
            progress = self.progress_tracker[student_id]
            
            # Add to completed lessons
            if lesson_id not in progress["lessons_completed"]:
                progress["lessons_completed"].append(lesson_id)
            
            # Update accuracy scores
            progress["accuracy_scores"].append(accuracy)
            progress["total_time_spent"] += time_spent
            
            # Award points
            points_earned = self.gamification["points_system"]["lesson_completion"]
            if accuracy >= 0.9:
                points_earned += self.gamification["points_system"]["perfect_score"]
                # Award perfect score badge
                if "perfect_quiz" not in student["badges"]:
                    student["badges"].append("perfect_quiz")
            
            student["points"] += points_earned
            
            # Update streak
            current_time = time.time()
            if current_time - student["last_activity"] < 86400:  # 24 hours
                student["streak_days"] += 1
            else:
                student["streak_days"] = 1
            
            student["last_activity"] = current_time
            
            # Check for level up
            self._check_level_up(student_id)
            
            # Update current lesson
            next_lesson = self.get_next_lesson(student_id)
            if next_lesson:
                student["current_lesson"] = next_lesson["id"]
            
            print(f"âœ… Lesson {lesson_id} completed by student {student_id}")
            print(f"ðŸ“Š Accuracy: {accuracy:.1%}, Points earned: {points_earned}")
            
            return True
            
        except Exception as e:
            print(f"âŒ Error completing lesson: {e}")
            return False
    
    def take_quiz(self, student_id: str, quiz_id: str, answers: List[int]) -> Dict:
        """Take a quiz and get results"""
        try:
            if quiz_id not in self.assessments:
                return {"success": False, "error": "Quiz not found"}
            
            quiz = self.assessments[quiz_id]
            questions = quiz["questions"]
            
            if len(answers) != len(questions):
                return {"success": False, "error": "Invalid number of answers"}
            
            # Calculate score
            correct_answers = 0
            results = []
            
            for i, (question, answer) in enumerate(zip(questions, answers)):
                is_correct = answer == question["correct_answer"]
                if is_correct:
                    correct_answers += 1
                
                results.append({
                    "question": question["question"],
                    "user_answer": answer,
                    "correct_answer": question["correct_answer"],
                    "is_correct": is_correct,
                    "explanation": question["explanation"]
                })
            
            score = (correct_answers / len(questions)) * 100
            passed = score >= quiz["passing_score"]
            
            # Award points
            points_earned = 0
            if student_id in self.students:
                student = self.students[student_id]
                points_earned = correct_answers * self.gamification["points_system"]["quiz_correct"]
                if passed:
                    points_earned += self.gamification["points_system"]["perfect_score"]
                
                student["points"] += points_earned
                
                # Add to quiz history
                if student_id in self.progress_tracker:
                    self.progress_tracker[student_id]["quizzes_taken"].append({
                        "quiz_id": quiz_id,
                        "score": score,
                        "timestamp": time.time()
                    })
            
            return {
                "success": True,
                "score": score,
                "passed": passed,
                "correct_answers": correct_answers,
                "total_questions": len(questions),
                "results": results,
                "points_earned": points_earned
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _check_level_up(self, student_id: str):
        """Check if student should level up"""
        if student_id not in self.students:
            return
        
        student = self.students[student_id]
        points = student["points"]
        
        # Find current level
        current_level = None
        for level_name, level_data in self.gamification["levels"].items():
            if level_data["min_points"] <= points < level_data["max_points"]:
                current_level = level_name
                break
        
        if current_level and current_level != student.get("level", "novice"):
            student["level"] = current_level
            print(f"ðŸŽ‰ Student {student_id} leveled up to {current_level}!")
    
    def get_student_progress(self, student_id: str) -> Optional[Dict]:
        """Get student progress report"""
        if student_id not in self.students:
            return None
        
        student = self.students[student_id]
        progress = self.progress_tracker.get(student_id, {})
        
        # Calculate statistics
        total_lessons = len(progress.get("lessons_completed", []))
        total_quizzes = len(progress.get("quizzes_taken", []))
        avg_accuracy = sum(progress.get("accuracy_scores", [])) / max(len(progress.get("accuracy_scores", [])), 1)
        
        return {
            "student_info": student,
            "progress": {
                "lessons_completed": total_lessons,
                "quizzes_taken": total_quizzes,
                "total_time_spent": progress.get("total_time_spent", 0),
                "average_accuracy": avg_accuracy,
                "current_level": student.get("level", "novice"),
                "points": student["points"],
                "badges": student["badges"],
                "streak_days": student["streak_days"]
            }
        }
    
    def get_teacher_dashboard(self, teacher_id: str) -> Optional[Dict]:
        """Get teacher dashboard data"""
        if teacher_id not in self.teachers:
            return None
        
        teacher = self.teachers[teacher_id]
        students = teacher.get("students", [])
        
        # Calculate class statistics
        total_students = len(students)
        active_students = 0
        total_progress = 0
        
        for student_id in students:
            progress = self.get_student_progress(student_id)
            if progress:
                total_progress += progress["progress"]["lessons_completed"]
                if progress["progress"]["lessons_completed"] > 0:
                    active_students += 1
        
        return {
            "teacher_info": teacher,
            "class_statistics": {
                "total_students": total_students,
                "active_students": active_students,
                "total_lessons_completed": total_progress,
                "average_progress": total_progress / max(total_students, 1)
            }
        }
    
    def get_platform_statistics(self) -> Dict:
        """Get overall platform statistics"""
        total_students = len(self.students)
        total_teachers = len(self.teachers)
        total_lessons = sum(len(level_data["lessons"]) for level_data in self.lessons.values())
        total_quizzes = len(self.assessments)
        
        return {
            "total_students": total_students,
            "total_teachers": total_teachers,
            "total_lessons": total_lessons,
            "total_quizzes": total_quizzes,
            "gamification_active": True,
            "levels_available": len(self.gamification["levels"]),
            "badges_available": len(self.gamification["badges"])
        }

# Example usage and testing
def test_educational_platform():
    """Test educational platform features"""
    print("ðŸ§ª Testing Educational Platform")
    print("=" * 50)
    
    # Initialize platform
    platform = EducationalPlatform()
    
    # Test student registration
    print("\nðŸ‘¨â€ðŸŽ“ Testing Student Registration:")
    platform.register_student("S001", "Alice Johnson", "alice@example.com")
    platform.register_student("S002", "Bob Smith", "bob@example.com")
    
    # Test teacher registration
    print("\nðŸ‘¨â€ðŸ« Testing Teacher Registration:")
    platform.register_teacher("T001", "Dr. Sarah Wilson", "sarah@example.com", ["ASL Certified", "Deaf Education"])
    
    # Test lesson completion
    print("\nðŸ“š Testing Lesson Completion:")
    platform.complete_lesson("S001", "lesson_1", 0.95, 900)  # 15 minutes
    platform.complete_lesson("S001", "lesson_2", 0.88, 600)  # 10 minutes
    
    # Test quiz taking
    print("\nðŸ“ Testing Quiz Taking:")
    quiz_results = platform.take_quiz("S001", "quiz_1", [0, 1])  # Correct answers
    if quiz_results["success"]:
        print(f"âœ… Quiz score: {quiz_results['score']:.1f}%")
        print(f"âœ… Passed: {quiz_results['passed']}")
        print(f"âœ… Points earned: {quiz_results['points_earned']}")
    
    # Test progress tracking
    print("\nðŸ“Š Testing Progress Tracking:")
    progress = platform.get_student_progress("S001")
    if progress:
        print(f"âœ… Lessons completed: {progress['progress']['lessons_completed']}")
        print(f"âœ… Points: {progress['progress']['points']}")
        print(f"âœ… Level: {progress['progress']['current_level']}")
    
    # Test platform statistics
    print("\nðŸ“ˆ Testing Platform Statistics:")
    stats = platform.get_platform_statistics()
    print(f"âœ… Total students: {stats['total_students']}")
    print(f"âœ… Total teachers: {stats['total_teachers']}")
    print(f"âœ… Total lessons: {stats['total_lessons']}")
    print(f"âœ… Total quizzes: {stats['total_quizzes']}")
    
    print("\nðŸŽ‰ Educational platform test completed!")

if __name__ == "__main__":
    test_educational_platform()
