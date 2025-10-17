# Analytics & Insights System
# Enterprise-grade analytics and performance monitoring

import json
import time
import sqlite3
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Performance metrics data structure"""
    timestamp: float
    endpoint: str
    response_time: float
    status_code: int
    user_id: str
    api_key: str
    error_message: Optional[str] = None

@dataclass
class UserActivity:
    """User activity data structure"""
    user_id: str
    timestamp: float
    action: str
    details: Dict
    session_id: str
    ip_address: str

@dataclass
class SignRecognitionMetrics:
    """Sign recognition metrics"""
    timestamp: float
    sign: str
    confidence: float
    processing_time: float
    language: str
    user_id: str
    accuracy: float

class AnalyticsEngine:
    """Enterprise analytics and insights engine"""
    
    def __init__(self, db_path: str = "data/analytics.db"):
        """Initialize analytics engine"""
        self.db_path = db_path
        self.db_connection = None
        
        # Analytics configuration
        self.config = {
            "retention_days": 365,
            "batch_size": 1000,
            "real_time_enabled": True,
            "privacy_mode": True,  # GDPR compliance
            "anonymization": True
        }
        
        # Initialize database
        self._init_database()
        
        # Analytics cache
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes
        
        print("âœ… Analytics Engine initialized")
        print(f"ðŸ“Š Database: {db_path}")
        print(f"ðŸ”’ Privacy mode: {self.config['privacy_mode']}")
        print(f"âš¡ Real-time: {self.config['real_time_enabled']}")
    
    def _init_database(self):
        """Initialize analytics database"""
        try:
            # Ensure data directory exists
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
            
            self.db_connection = sqlite3.connect(self.db_path)
            cursor = self.db_connection.cursor()
            
            # Create tables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    endpoint TEXT,
                    response_time REAL,
                    status_code INTEGER,
                    user_id TEXT,
                    api_key TEXT,
                    error_message TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_activity (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    timestamp REAL,
                    action TEXT,
                    details TEXT,
                    session_id TEXT,
                    ip_address TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sign_recognition_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    sign TEXT,
                    confidence REAL,
                    processing_time REAL,
                    language TEXT,
                    user_id TEXT,
                    accuracy REAL
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    metric_name TEXT,
                    metric_value REAL,
                    tags TEXT
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_performance_timestamp ON performance_metrics(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_performance_endpoint ON performance_metrics(endpoint)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_activity_timestamp ON user_activity(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_sign_recognition_timestamp ON sign_recognition_metrics(timestamp)')
            
            self.db_connection.commit()
            print("âœ… Database tables created successfully")
            
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
            raise
    
    def log_performance_metric(self, metric: PerformanceMetrics):
        """Log performance metric"""
        try:
            cursor = self.db_connection.cursor()
            cursor.execute('''
                INSERT INTO performance_metrics 
                (timestamp, endpoint, response_time, status_code, user_id, api_key, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                metric.timestamp,
                metric.endpoint,
                metric.response_time,
                metric.status_code,
                metric.user_id,
                metric.api_key,
                metric.error_message
            ))
            self.db_connection.commit()
            
            # Real-time processing
            if self.config["real_time_enabled"]:
                self._process_real_time_metric(metric)
                
        except Exception as e:
            logger.error(f"Performance metric logging error: {e}")
    
    def log_user_activity(self, activity: UserActivity):
        """Log user activity"""
        try:
            cursor = self.db_connection.cursor()
            cursor.execute('''
                INSERT INTO user_activity 
                (user_id, timestamp, action, details, session_id, ip_address)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                activity.user_id,
                activity.timestamp,
                activity.action,
                json.dumps(activity.details),
                activity.session_id,
                activity.ip_address
            ))
            self.db_connection.commit()
            
        except Exception as e:
            logger.error(f"User activity logging error: {e}")
    
    def log_sign_recognition(self, metric: SignRecognitionMetrics):
        """Log sign recognition metric"""
        try:
            cursor = self.db_connection.cursor()
            cursor.execute('''
                INSERT INTO sign_recognition_metrics 
                (timestamp, sign, confidence, processing_time, language, user_id, accuracy)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                metric.timestamp,
                metric.sign,
                metric.confidence,
                metric.processing_time,
                metric.language,
                metric.user_id,
                metric.accuracy
            ))
            self.db_connection.commit()
            
        except Exception as e:
            logger.error(f"Sign recognition logging error: {e}")
    
    def _process_real_time_metric(self, metric: PerformanceMetrics):
        """Process real-time performance metric"""
        # Update real-time dashboards
        # Send alerts if thresholds exceeded
        # Update cache
        
        if metric.response_time > 5.0:  # Alert threshold
            self._send_alert("High response time", {
                "endpoint": metric.endpoint,
                "response_time": metric.response_time,
                "timestamp": metric.timestamp
            })
    
    def _send_alert(self, alert_type: str, data: Dict):
        """Send alert notification"""
        logger.warning(f"ALERT: {alert_type} - {data}")
        # In a real implementation, this would send to monitoring systems
    
    def get_performance_analytics(self, start_time: Optional[float] = None, 
                                 end_time: Optional[float] = None) -> Dict:
        """Get performance analytics"""
        try:
            if start_time is None:
                start_time = time.time() - 86400  # Last 24 hours
            if end_time is None:
                end_time = time.time()
            
            cursor = self.db_connection.cursor()
            
            # Basic performance metrics
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_requests,
                    AVG(response_time) as avg_response_time,
                    MAX(response_time) as max_response_time,
                    MIN(response_time) as min_response_time,
                    COUNT(CASE WHEN status_code >= 400 THEN 1 END) as error_count
                FROM performance_metrics 
                WHERE timestamp BETWEEN ? AND ?
            ''', (start_time, end_time))
            
            basic_metrics = cursor.fetchone()
            
            # Endpoint breakdown
            cursor.execute('''
                SELECT 
                    endpoint,
                    COUNT(*) as request_count,
                    AVG(response_time) as avg_response_time,
                    COUNT(CASE WHEN status_code >= 400 THEN 1 END) as error_count
                FROM performance_metrics 
                WHERE timestamp BETWEEN ? AND ?
                GROUP BY endpoint
                ORDER BY request_count DESC
            ''', (start_time, end_time))
            
            endpoint_metrics = cursor.fetchall()
            
            # Hourly breakdown
            cursor.execute('''
                SELECT 
                    strftime('%H', datetime(timestamp, 'unixepoch')) as hour,
                    COUNT(*) as request_count,
                    AVG(response_time) as avg_response_time
                FROM performance_metrics 
                WHERE timestamp BETWEEN ? AND ?
                GROUP BY hour
                ORDER BY hour
            ''', (start_time, end_time))
            
            hourly_metrics = cursor.fetchall()
            
            return {
                "time_range": {
                    "start": start_time,
                    "end": end_time,
                    "duration_hours": (end_time - start_time) / 3600
                },
                "basic_metrics": {
                    "total_requests": basic_metrics[0],
                    "avg_response_time": basic_metrics[1],
                    "max_response_time": basic_metrics[2],
                    "min_response_time": basic_metrics[3],
                    "error_count": basic_metrics[4],
                    "error_rate": basic_metrics[4] / max(basic_metrics[0], 1)
                },
                "endpoint_breakdown": [
                    {
                        "endpoint": row[0],
                        "request_count": row[1],
                        "avg_response_time": row[2],
                        "error_count": row[3]
                    }
                    for row in endpoint_metrics
                ],
                "hourly_breakdown": [
                    {
                        "hour": row[0],
                        "request_count": row[1],
                        "avg_response_time": row[2]
                    }
                    for row in hourly_metrics
                ]
            }
            
        except Exception as e:
            logger.error(f"Performance analytics error: {e}")
            return {}
    
    def get_user_analytics(self, start_time: Optional[float] = None,
                          end_time: Optional[float] = None) -> Dict:
        """Get user analytics"""
        try:
            if start_time is None:
                start_time = time.time() - 86400  # Last 24 hours
            if end_time is None:
                end_time = time.time()
            
            cursor = self.db_connection.cursor()
            
            # User activity summary
            cursor.execute('''
                SELECT 
                    COUNT(DISTINCT user_id) as unique_users,
                    COUNT(*) as total_activities,
                    COUNT(DISTINCT session_id) as unique_sessions
                FROM user_activity 
                WHERE timestamp BETWEEN ? AND ?
            ''', (start_time, end_time))
            
            activity_summary = cursor.fetchone()
            
            # Top users by activity
            cursor.execute('''
                SELECT 
                    user_id,
                    COUNT(*) as activity_count,
                    COUNT(DISTINCT session_id) as session_count
                FROM user_activity 
                WHERE timestamp BETWEEN ? AND ?
                GROUP BY user_id
                ORDER BY activity_count DESC
                LIMIT 10
            ''', (start_time, end_time))
            
            top_users = cursor.fetchall()
            
            # Activity breakdown by action
            cursor.execute('''
                SELECT 
                    action,
                    COUNT(*) as count
                FROM user_activity 
                WHERE timestamp BETWEEN ? AND ?
                GROUP BY action
                ORDER BY count DESC
            ''', (start_time, end_time))
            
            activity_breakdown = cursor.fetchall()
            
            return {
                "time_range": {
                    "start": start_time,
                    "end": end_time,
                    "duration_hours": (end_time - start_time) / 3600
                },
                "summary": {
                    "unique_users": activity_summary[0],
                    "total_activities": activity_summary[1],
                    "unique_sessions": activity_summary[2]
                },
                "top_users": [
                    {
                        "user_id": row[0],
                        "activity_count": row[1],
                        "session_count": row[2]
                    }
                    for row in top_users
                ],
                "activity_breakdown": [
                    {
                        "action": row[0],
                        "count": row[1]
                    }
                    for row in activity_breakdown
                ]
            }
            
        except Exception as e:
            logger.error(f"User analytics error: {e}")
            return {}
    
    def get_sign_recognition_analytics(self, start_time: Optional[float] = None,
                                     end_time: Optional[float] = None) -> Dict:
        """Get sign recognition analytics"""
        try:
            if start_time is None:
                start_time = time.time() - 86400  # Last 24 hours
            if end_time is None:
                end_time = time.time()
            
            cursor = self.db_connection.cursor()
            
            # Recognition summary
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_recognitions,
                    AVG(confidence) as avg_confidence,
                    AVG(processing_time) as avg_processing_time,
                    AVG(accuracy) as avg_accuracy,
                    COUNT(DISTINCT sign) as unique_signs,
                    COUNT(DISTINCT language) as languages_used
                FROM sign_recognition_metrics 
                WHERE timestamp BETWEEN ? AND ?
            ''', (start_time, end_time))
            
            recognition_summary = cursor.fetchone()
            
            # Most recognized signs
            cursor.execute('''
                SELECT 
                    sign,
                    COUNT(*) as recognition_count,
                    AVG(confidence) as avg_confidence,
                    AVG(accuracy) as avg_accuracy
                FROM sign_recognition_metrics 
                WHERE timestamp BETWEEN ? AND ?
                GROUP BY sign
                ORDER BY recognition_count DESC
                LIMIT 20
            ''', (start_time, end_time))
            
            popular_signs = cursor.fetchall()
            
            # Language breakdown
            cursor.execute('''
                SELECT 
                    language,
                    COUNT(*) as recognition_count,
                    AVG(confidence) as avg_confidence
                FROM sign_recognition_metrics 
                WHERE timestamp BETWEEN ? AND ?
                GROUP BY language
                ORDER BY recognition_count DESC
            ''', (start_time, end_time))
            
            language_breakdown = cursor.fetchall()
            
            # Confidence distribution
            cursor.execute('''
                SELECT 
                    CASE 
                        WHEN confidence >= 0.9 THEN 'High (0.9+)'
                        WHEN confidence >= 0.7 THEN 'Medium (0.7-0.9)'
                        WHEN confidence >= 0.5 THEN 'Low (0.5-0.7)'
                        ELSE 'Very Low (<0.5)'
                    END as confidence_range,
                    COUNT(*) as count
                FROM sign_recognition_metrics 
                WHERE timestamp BETWEEN ? AND ?
                GROUP BY confidence_range
                ORDER BY count DESC
            ''', (start_time, end_time))
            
            confidence_distribution = cursor.fetchall()
            
            return {
                "time_range": {
                    "start": start_time,
                    "end": end_time,
                    "duration_hours": (end_time - start_time) / 3600
                },
                "summary": {
                    "total_recognitions": recognition_summary[0],
                    "avg_confidence": recognition_summary[1],
                    "avg_processing_time": recognition_summary[2],
                    "avg_accuracy": recognition_summary[3],
                    "unique_signs": recognition_summary[4],
                    "languages_used": recognition_summary[5]
                },
                "popular_signs": [
                    {
                        "sign": row[0],
                        "recognition_count": row[1],
                        "avg_confidence": row[2],
                        "avg_accuracy": row[3]
                    }
                    for row in popular_signs
                ],
                "language_breakdown": [
                    {
                        "language": row[0],
                        "recognition_count": row[1],
                        "avg_confidence": row[2]
                    }
                    for row in language_breakdown
                ],
                "confidence_distribution": [
                    {
                        "range": row[0],
                        "count": row[1]
                    }
                    for row in confidence_distribution
                ]
            }
            
        except Exception as e:
            logger.error(f"Sign recognition analytics error: {e}")
            return {}
    
    def get_system_health(self) -> Dict:
        """Get system health metrics"""
        try:
            cursor = self.db_connection.cursor()
            
            # Recent performance
            recent_time = time.time() - 3600  # Last hour
            cursor.execute('''
                SELECT 
                    COUNT(*) as requests_last_hour,
                    AVG(response_time) as avg_response_time,
                    COUNT(CASE WHEN status_code >= 400 THEN 1 END) as errors_last_hour
                FROM performance_metrics 
                WHERE timestamp > ?
            ''', (recent_time,))
            
            recent_performance = cursor.fetchone()
            
            # Database health
            cursor.execute('SELECT COUNT(*) FROM performance_metrics')
            total_metrics = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM user_activity')
            total_activities = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM sign_recognition_metrics')
            total_recognitions = cursor.fetchone()[0]
            
            return {
                "timestamp": time.time(),
                "status": "healthy",
                "recent_performance": {
                    "requests_last_hour": recent_performance[0],
                    "avg_response_time": recent_performance[1],
                    "errors_last_hour": recent_performance[2],
                    "error_rate": recent_performance[2] / max(recent_performance[0], 1)
                },
                "database_health": {
                    "total_metrics": total_metrics,
                    "total_activities": total_activities,
                    "total_recognitions": total_recognitions,
                    "database_size_mb": Path(self.db_path).stat().st_size / (1024 * 1024)
                },
                "system_status": {
                    "real_time_enabled": self.config["real_time_enabled"],
                    "privacy_mode": self.config["privacy_mode"],
                    "retention_days": self.config["retention_days"]
                }
            }
            
        except Exception as e:
            logger.error(f"System health error: {e}")
            return {"status": "error", "error": str(e)}
    
    def generate_insights(self) -> Dict:
        """Generate actionable insights"""
        try:
            insights = []
            
            # Performance insights
            perf_analytics = self.get_performance_analytics()
            if perf_analytics.get("basic_metrics", {}).get("avg_response_time", 0) > 2.0:
                insights.append({
                    "type": "performance",
                    "severity": "warning",
                    "title": "High Response Time",
                    "description": f"Average response time is {perf_analytics['basic_metrics']['avg_response_time']:.2f}s",
                    "recommendation": "Consider optimizing slow endpoints or scaling infrastructure"
                })
            
            # Sign recognition insights
            sign_analytics = self.get_sign_recognition_analytics()
            avg_confidence = sign_analytics.get("summary", {}).get("avg_confidence", 0)
            if avg_confidence < 0.8:
                insights.append({
                    "type": "accuracy",
                    "severity": "info",
                    "title": "Sign Recognition Accuracy",
                    "description": f"Average confidence is {avg_confidence:.2f}",
                    "recommendation": "Consider retraining model or improving data quality"
                })
            
            # User engagement insights
            user_analytics = self.get_user_analytics()
            unique_users = user_analytics.get("summary", {}).get("unique_users", 0)
            if unique_users > 100:
                insights.append({
                    "type": "engagement",
                    "severity": "success",
                    "title": "High User Engagement",
                    "description": f"{unique_users} unique users in the last 24 hours",
                    "recommendation": "Consider expanding features or scaling infrastructure"
                })
            
            return {
                "timestamp": time.time(),
                "total_insights": len(insights),
                "insights": insights,
                "summary": {
                    "performance_issues": len([i for i in insights if i["type"] == "performance"]),
                    "accuracy_issues": len([i for i in insights if i["type"] == "accuracy"]),
                    "engagement_opportunities": len([i for i in insights if i["type"] == "engagement"])
                }
            }
            
        except Exception as e:
            logger.error(f"Insights generation error: {e}")
            return {"error": str(e)}
    
    def export_analytics(self, start_time: float, end_time: float, 
                        format: str = "json") -> str:
        """Export analytics data"""
        try:
            export_data = {
                "export_timestamp": time.time(),
                "time_range": {"start": start_time, "end": end_time},
                "performance_analytics": self.get_performance_analytics(start_time, end_time),
                "user_analytics": self.get_user_analytics(start_time, end_time),
                "sign_recognition_analytics": self.get_sign_recognition_analytics(start_time, end_time),
                "system_health": self.get_system_health(),
                "insights": self.generate_insights()
            }
            
            if format == "json":
                return json.dumps(export_data, indent=2)
            elif format == "csv":
                # Convert to CSV format
                import csv
                import io
                output = io.StringIO()
                writer = csv.writer(output)
                
                # Write performance metrics
                writer.writerow(["Metric", "Value"])
                for key, value in export_data["performance_analytics"]["basic_metrics"].items():
                    writer.writerow([key, value])
                
                return output.getvalue()
            
        except Exception as e:
            logger.error(f"Analytics export error: {e}")
            return ""

# Example usage and testing
def test_analytics_engine():
    """Test analytics engine features"""
    print("ðŸ§ª Testing Analytics Engine")
    print("=" * 40)
    
    # Initialize analytics engine
    analytics = AnalyticsEngine("data/test_analytics.db")
    
    # Test performance metrics logging
    print("\nðŸ“Š Testing Performance Metrics:")
    for i in range(5):
        metric = PerformanceMetrics(
            timestamp=time.time(),
            endpoint=f"/api/v1/test{i}",
            response_time=0.1 + i * 0.1,
            status_code=200,
            user_id=f"user_{i}",
            api_key="test_key"
        )
        analytics.log_performance_metric(metric)
    print("âœ… Performance metrics logged")
    
    # Test user activity logging
    print("\nðŸ‘¥ Testing User Activity:")
    for i in range(3):
        activity = UserActivity(
            user_id=f"user_{i}",
            timestamp=time.time(),
            action="sign_recognition",
            details={"sign": "hello", "confidence": 0.9},
            session_id=f"session_{i}",
            ip_address="127.0.0.1"
        )
        analytics.log_user_activity(activity)
    print("âœ… User activities logged")
    
    # Test sign recognition metrics
    print("\nðŸ¤Ÿ Testing Sign Recognition Metrics:")
    for i in range(4):
        metric = SignRecognitionMetrics(
            timestamp=time.time(),
            sign=["hello", "yes", "no", "thank_you"][i],
            confidence=0.8 + i * 0.05,
            processing_time=0.2 + i * 0.1,
            language="asl",
            user_id=f"user_{i}",
            accuracy=0.85 + i * 0.03
        )
        analytics.log_sign_recognition(metric)
    print("âœ… Sign recognition metrics logged")
    
    # Test analytics retrieval
    print("\nðŸ“ˆ Testing Analytics Retrieval:")
    
    # Performance analytics
    perf_analytics = analytics.get_performance_analytics()
    print(f"âœ… Performance analytics: {perf_analytics.get('basic_metrics', {}).get('total_requests', 0)} requests")
    
    # User analytics
    user_analytics = analytics.get_user_analytics()
    print(f"âœ… User analytics: {user_analytics.get('summary', {}).get('unique_users', 0)} unique users")
    
    # Sign recognition analytics
    sign_analytics = analytics.get_sign_recognition_analytics()
    print(f"âœ… Sign recognition analytics: {sign_analytics.get('summary', {}).get('total_recognitions', 0)} recognitions")
    
    # System health
    health = analytics.get_system_health()
    print(f"âœ… System health: {health.get('status', 'unknown')}")
    
    # Insights generation
    insights = analytics.generate_insights()
    print(f"âœ… Insights generated: {insights.get('total_insights', 0)} insights")
    
    # Analytics export
    export_data = analytics.export_analytics(time.time() - 3600, time.time())
    print(f"âœ… Analytics exported: {len(export_data)} characters")
    
    print("\nðŸŽ‰ Analytics engine test completed!")
    print("ðŸ“Š Ready for enterprise monitoring!")

if __name__ == "__main__":
    test_analytics_engine()
