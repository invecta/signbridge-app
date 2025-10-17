# Community Platform System
# Social features and user-generated content for SignBridge community

import json
import time
import hashlib
import uuid
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class User:
    """Community user data structure"""
    id: str
    username: str
    email: str
    display_name: str
    bio: str
    avatar_url: str
    join_date: float
    last_active: float
    reputation: int
    badges: List[str]
    preferences: Dict
    privacy_settings: Dict

@dataclass
class Post:
    """Community post data structure"""
    id: str
    author_id: str
    title: str
    content: str
    post_type: str  # tutorial, question, achievement, discussion
    tags: List[str]
    created_at: float
    updated_at: float
    likes: int
    comments: int
    views: int
    is_pinned: bool
    is_featured: bool

@dataclass
class Comment:
    """Comment data structure"""
    id: str
    post_id: str
    author_id: str
    content: str
    created_at: float
    updated_at: float
    likes: int
    parent_id: Optional[str] = None  # For replies

@dataclass
class Tutorial:
    """Tutorial data structure"""
    id: str
    author_id: str
    title: str
    description: str
    content: str
    difficulty: str  # beginner, intermediate, advanced
    language: str
    duration_minutes: int
    tags: List[str]
    created_at: float
    updated_at: float
    views: int
    likes: int
    rating: float
    steps: List[Dict]

class CommunityPlatform:
    """SignBridge community platform"""
    
    def __init__(self, data_dir: str = "data/community"):
        """Initialize community platform"""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Community configuration
        self.config = {
            "max_post_length": 10000,
            "max_comment_length": 2000,
            "max_tags_per_post": 10,
            "reputation_system": True,
            "moderation_enabled": True,
            "content_filtering": True,
            "privacy_by_default": True
        }
        
        # Data storage (in production, use proper database)
        self.users = {}
        self.posts = {}
        self.comments = {}
        self.tutorials = {}
        self.follows = {}  # user_id -> list of followed user_ids
        self.likes = {}   # post_id -> list of user_ids who liked
        self.reports = {} # reported content
        
        # Load existing data
        self._load_data()
        
        print("âœ… Community Platform initialized")
        print(f"ðŸ‘¥ Users: {len(self.users)}")
        print(f"ðŸ“ Posts: {len(self.posts)}")
        print(f"ðŸ’¬ Comments: {len(self.comments)}")
        print(f"ðŸ“š Tutorials: {len(self.tutorials)}")
        print(f"ðŸ”’ Moderation: {self.config['moderation_enabled']}")
    
    def _load_data(self):
        """Load community data from files"""
        try:
            # Load users
            users_file = self.data_dir / "users.json"
            if users_file.exists():
                with open(users_file, 'r', encoding='utf-8') as f:
                    users_data = json.load(f)
                    for user_id, user_data in users_data.items():
                        self.users[user_id] = User(**user_data)
            
            # Load posts
            posts_file = self.data_dir / "posts.json"
            if posts_file.exists():
                with open(posts_file, 'r', encoding='utf-8') as f:
                    posts_data = json.load(f)
                    for post_id, post_data in posts_data.items():
                        self.posts[post_id] = Post(**post_data)
            
            # Load comments
            comments_file = self.data_dir / "comments.json"
            if comments_file.exists():
                with open(comments_file, 'r', encoding='utf-8') as f:
                    comments_data = json.load(f)
                    for comment_id, comment_data in comments_data.items():
                        self.comments[comment_id] = Comment(**comment_data)
            
            # Load tutorials
            tutorials_file = self.data_dir / "tutorials.json"
            if tutorials_file.exists():
                with open(tutorials_file, 'r', encoding='utf-8') as f:
                    tutorials_data = json.load(f)
                    for tutorial_id, tutorial_data in tutorials_data.items():
                        self.tutorials[tutorial_id] = Tutorial(**tutorial_data)
            
            print("âœ… Community data loaded successfully")
            
        except Exception as e:
            logger.error(f"Data loading error: {e}")
    
    def _save_data(self):
        """Save community data to files"""
        try:
            # Save users
            users_data = {user_id: asdict(user) for user_id, user in self.users.items()}
            with open(self.data_dir / "users.json", 'w', encoding='utf-8') as f:
                json.dump(users_data, f, indent=2, ensure_ascii=False)
            
            # Save posts
            posts_data = {post_id: asdict(post) for post_id, post in self.posts.items()}
            with open(self.data_dir / "posts.json", 'w', encoding='utf-8') as f:
                json.dump(posts_data, f, indent=2, ensure_ascii=False)
            
            # Save comments
            comments_data = {comment_id: asdict(comment) for comment_id, comment in self.comments.items()}
            with open(self.data_dir / "comments.json", 'w', encoding='utf-8') as f:
                json.dump(comments_data, f, indent=2, ensure_ascii=False)
            
            # Save tutorials
            tutorials_data = {tutorial_id: asdict(tutorial) for tutorial_id, tutorial in self.tutorials.items()}
            with open(self.data_dir / "tutorials.json", 'w', encoding='utf-8') as f:
                json.dump(tutorials_data, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Data saving error: {e}")
    
    def register_user(self, username: str, email: str, display_name: str, 
                     bio: str = "", avatar_url: str = "") -> User:
        """Register new community user"""
        try:
            # Check if username exists
            if any(user.username == username for user in self.users.values()):
                raise ValueError("Username already exists")
            
            # Check if email exists
            if any(user.email == email for user in self.users.values()):
                raise ValueError("Email already exists")
            
            # Create new user
            user_id = str(uuid.uuid4())
            user = User(
                id=user_id,
                username=username,
                email=email,
                display_name=display_name,
                bio=bio,
                avatar_url=avatar_url,
                join_date=time.time(),
                last_active=time.time(),
                reputation=0,
                badges=[],
                preferences={
                    "language": "asl",
                    "notifications": True,
                    "public_profile": True
                },
                privacy_settings={
                    "show_email": False,
                    "show_activity": True,
                    "allow_messages": True
                }
            )
            
            self.users[user_id] = user
            self.follows[user_id] = []
            self._save_data()
            
            print(f"âœ… User registered: {username}")
            return user
            
        except Exception as e:
            logger.error(f"User registration error: {e}")
            raise
    
    def create_post(self, author_id: str, title: str, content: str, 
                   post_type: str, tags: List[str]) -> Post:
        """Create new community post"""
        try:
            if author_id not in self.users:
                raise ValueError("Author not found")
            
            if len(content) > self.config["max_post_length"]:
                raise ValueError(f"Content too long (max {self.config['max_post_length']} characters)")
            
            if len(tags) > self.config["max_tags_per_post"]:
                raise ValueError(f"Too many tags (max {self.config['max_tags_per_post']})")
            
            # Content filtering
            if self.config["content_filtering"]:
                content = self._filter_content(content)
            
            post_id = str(uuid.uuid4())
            post = Post(
                id=post_id,
                author_id=author_id,
                title=title,
                content=content,
                post_type=post_type,
                tags=tags,
                created_at=time.time(),
                updated_at=time.time(),
                likes=0,
                comments=0,
                views=0,
                is_pinned=False,
                is_featured=False
            )
            
            self.posts[post_id] = post
            self.likes[post_id] = []
            
            # Update user activity
            self.users[author_id].last_active = time.time()
            
            # Award reputation points
            if self.config["reputation_system"]:
                self._award_reputation(author_id, 5, "post_created")
            
            self._save_data()
            
            print(f"âœ… Post created: {title}")
            return post
            
        except Exception as e:
            logger.error(f"Post creation error: {e}")
            raise
    
    def create_comment(self, post_id: str, author_id: str, content: str, 
                      parent_id: Optional[str] = None) -> Comment:
        """Create new comment"""
        try:
            if post_id not in self.posts:
                raise ValueError("Post not found")
            
            if author_id not in self.users:
                raise ValueError("Author not found")
            
            if len(content) > self.config["max_comment_length"]:
                raise ValueError(f"Comment too long (max {self.config['max_comment_length']} characters)")
            
            # Content filtering
            if self.config["content_filtering"]:
                content = self._filter_content(content)
            
            comment_id = str(uuid.uuid4())
            comment = Comment(
                id=comment_id,
                post_id=post_id,
                author_id=author_id,
                content=content,
                created_at=time.time(),
                updated_at=time.time(),
                likes=0,
                parent_id=parent_id
            )
            
            self.comments[comment_id] = comment
            
            # Update post comment count
            self.posts[post_id].comments += 1
            self.posts[post_id].updated_at = time.time()
            
            # Update user activity
            self.users[author_id].last_active = time.time()
            
            # Award reputation points
            if self.config["reputation_system"]:
                self._award_reputation(author_id, 2, "comment_created")
            
            self._save_data()
            
            print(f"âœ… Comment created on post {post_id}")
            return comment
            
        except Exception as e:
            logger.error(f"Comment creation error: {e}")
            raise
    
    def create_tutorial(self, author_id: str, title: str, description: str, 
                       content: str, difficulty: str, language: str, 
                       duration_minutes: int, tags: List[str], 
                       steps: List[Dict]) -> Tutorial:
        """Create new tutorial"""
        try:
            if author_id not in self.users:
                raise ValueError("Author not found")
            
            if difficulty not in ["beginner", "intermediate", "advanced"]:
                raise ValueError("Invalid difficulty level")
            
            tutorial_id = str(uuid.uuid4())
            tutorial = Tutorial(
                id=tutorial_id,
                author_id=author_id,
                title=title,
                description=description,
                content=content,
                difficulty=difficulty,
                language=language,
                duration_minutes=duration_minutes,
                tags=tags,
                created_at=time.time(),
                updated_at=time.time(),
                views=0,
                likes=0,
                rating=0.0,
                steps=steps
            )
            
            self.tutorials[tutorial_id] = tutorial
            
            # Update user activity
            self.users[author_id].last_active = time.time()
            
            # Award reputation points
            if self.config["reputation_system"]:
                self._award_reputation(author_id, 10, "tutorial_created")
            
            self._save_data()
            
            print(f"âœ… Tutorial created: {title}")
            return tutorial
            
        except Exception as e:
            logger.error(f"Tutorial creation error: {e}")
            raise
    
    def like_post(self, post_id: str, user_id: str) -> bool:
        """Like/unlike a post"""
        try:
            if post_id not in self.posts:
                raise ValueError("Post not found")
            
            if user_id not in self.users:
                raise ValueError("User not found")
            
            if post_id not in self.likes:
                self.likes[post_id] = []
            
            if user_id in self.likes[post_id]:
                # Unlike
                self.likes[post_id].remove(user_id)
                self.posts[post_id].likes -= 1
                action = "unliked"
            else:
                # Like
                self.likes[post_id].append(user_id)
                self.posts[post_id].likes += 1
                action = "liked"
            
            # Award reputation points
            if self.config["reputation_system"] and action == "liked":
                self._award_reputation(self.posts[post_id].author_id, 1, "post_liked")
            
            self._save_data()
            
            print(f"âœ… Post {action}: {post_id}")
            return action == "liked"
            
        except Exception as e:
            logger.error(f"Like post error: {e}")
            raise
    
    def follow_user(self, follower_id: str, following_id: str) -> bool:
        """Follow/unfollow a user"""
        try:
            if follower_id not in self.users or following_id not in self.users:
                raise ValueError("User not found")
            
            if follower_id == following_id:
                raise ValueError("Cannot follow yourself")
            
            if follower_id not in self.follows:
                self.follows[follower_id] = []
            
            if following_id in self.follows[follower_id]:
                # Unfollow
                self.follows[follower_id].remove(following_id)
                action = "unfollowed"
            else:
                # Follow
                self.follows[follower_id].append(following_id)
                action = "followed"
            
            self._save_data()
            
            print(f"âœ… User {action}: {following_id}")
            return action == "followed"
            
        except Exception as e:
            logger.error(f"Follow user error: {e}")
            raise
    
    def _filter_content(self, content: str) -> str:
        """Filter inappropriate content"""
        # Simple content filtering (in production, use ML-based filtering)
        inappropriate_words = ["spam", "hate", "abuse"]  # Simplified list
        
        filtered_content = content
        for word in inappropriate_words:
            filtered_content = filtered_content.replace(word, "*" * len(word))
        
        return filtered_content
    
    def _award_reputation(self, user_id: str, points: int, reason: str):
        """Award reputation points to user"""
        if user_id in self.users:
            self.users[user_id].reputation += points
            
            # Check for badge eligibility
            self._check_badge_eligibility(user_id)
    
    def _check_badge_eligibility(self, user_id: str):
        """Check if user is eligible for new badges"""
        user = self.users[user_id]
        new_badges = []
        
        # Reputation-based badges
        if user.reputation >= 100 and "contributor" not in user.badges:
            new_badges.append("contributor")
        
        if user.reputation >= 500 and "expert" not in user.badges:
            new_badges.append("expert")
        
        if user.reputation >= 1000 and "master" not in user.badges:
            new_badges.append("master")
        
        # Add new badges
        for badge in new_badges:
            if badge not in user.badges:
                user.badges.append(badge)
                print(f"ðŸŽ–ï¸ Badge earned: {badge}")
    
    def get_feed(self, user_id: str, limit: int = 20) -> List[Dict]:
        """Get personalized feed for user"""
        try:
            if user_id not in self.users:
                raise ValueError("User not found")
            
            # Get posts from followed users and popular posts
            followed_users = self.follows.get(user_id, [])
            feed_posts = []
            
            # Posts from followed users
            for post in self.posts.values():
                if post.author_id in followed_users:
                    feed_posts.append({
                        "type": "post",
                        "data": asdict(post),
                        "author": asdict(self.users[post.author_id]),
                        "score": post.likes + post.comments * 2
                    })
            
            # Popular posts
            popular_posts = sorted(
                [post for post in self.posts.values() if post.author_id not in followed_users],
                key=lambda x: x.likes + x.comments * 2,
                reverse=True
            )[:limit//2]
            
            for post in popular_posts:
                feed_posts.append({
                    "type": "post",
                    "data": asdict(post),
                    "author": asdict(self.users[post.author_id]),
                    "score": post.likes + post.comments * 2
                })
            
            # Sort by score and return limited results
            feed_posts.sort(key=lambda x: x["score"], reverse=True)
            return feed_posts[:limit]
            
        except Exception as e:
            logger.error(f"Feed generation error: {e}")
            return []
    
    def search_content(self, query: str, content_type: str = "all") -> List[Dict]:
        """Search community content"""
        try:
            results = []
            query_lower = query.lower()
            
            if content_type in ["all", "posts"]:
                for post in self.posts.values():
                    if (query_lower in post.title.lower() or 
                        query_lower in post.content.lower() or
                        any(query_lower in tag.lower() for tag in post.tags)):
                        results.append({
                            "type": "post",
                            "data": asdict(post),
                            "author": asdict(self.users[post.author_id]),
                            "relevance_score": self._calculate_relevance(query, post.title + " " + post.content)
                        })
            
            if content_type in ["all", "tutorials"]:
                for tutorial in self.tutorials.values():
                    if (query_lower in tutorial.title.lower() or 
                        query_lower in tutorial.description.lower() or
                        any(query_lower in tag.lower() for tag in tutorial.tags)):
                        results.append({
                            "type": "tutorial",
                            "data": asdict(tutorial),
                            "author": asdict(self.users[tutorial.author_id]),
                            "relevance_score": self._calculate_relevance(query, tutorial.title + " " + tutorial.description)
                        })
            
            # Sort by relevance score
            results.sort(key=lambda x: x["relevance_score"], reverse=True)
            return results
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []
    
    def _calculate_relevance(self, query: str, content: str) -> float:
        """Calculate relevance score for search results"""
        query_words = query.lower().split()
        content_lower = content.lower()
        
        score = 0
        for word in query_words:
            if word in content_lower:
                score += 1
        
        return score / len(query_words) if query_words else 0
    
    def get_community_stats(self) -> Dict:
        """Get community statistics"""
        return {
            "total_users": len(self.users),
            "total_posts": len(self.posts),
            "total_comments": len(self.comments),
            "total_tutorials": len(self.tutorials),
            "total_likes": sum(post.likes for post in self.posts.values()),
            "active_users_24h": len([
                user for user in self.users.values() 
                if time.time() - user.last_active < 86400
            ]),
            "top_contributors": sorted(
                [(user.display_name, user.reputation) for user in self.users.values()],
                key=lambda x: x[1],
                reverse=True
            )[:10],
            "popular_tags": self._get_popular_tags(),
            "recent_activity": self._get_recent_activity()
        }
    
    def _get_popular_tags(self) -> List[Tuple[str, int]]:
        """Get popular tags"""
        tag_counts = {}
        for post in self.posts.values():
            for tag in post.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        return sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:20]
    
    def _get_recent_activity(self) -> List[Dict]:
        """Get recent community activity"""
        activities = []
        
        # Recent posts
        recent_posts = sorted(
            self.posts.values(),
            key=lambda x: x.created_at,
            reverse=True
        )[:5]
        
        for post in recent_posts:
            activities.append({
                "type": "post",
                "action": "created",
                "user": self.users[post.author_id].display_name,
                "content": post.title,
                "timestamp": post.created_at
            })
        
        # Recent tutorials
        recent_tutorials = sorted(
            self.tutorials.values(),
            key=lambda x: x.created_at,
            reverse=True
        )[:3]
        
        for tutorial in recent_tutorials:
            activities.append({
                "type": "tutorial",
                "action": "created",
                "user": self.users[tutorial.author_id].display_name,
                "content": tutorial.title,
                "timestamp": tutorial.created_at
            })
        
        # Sort by timestamp
        activities.sort(key=lambda x: x["timestamp"], reverse=True)
        return activities[:10]

# Example usage and testing
def test_community_platform():
    """Test community platform features"""
    print("ðŸ§ª Testing Community Platform")
    print("=" * 40)
    
    # Initialize community platform
    community = CommunityPlatform("data/test_community")
    
    # Test user registration
    print("\nðŸ‘¥ Testing User Registration:")
    user1 = community.register_user("alice", "alice@example.com", "Alice Johnson", "ASL teacher")
    user2 = community.register_user("bob", "bob@example.com", "Bob Smith", "Deaf community advocate")
    print(f"âœ… Users registered: {len(community.users)}")
    
    # Test post creation
    print("\nðŸ“ Testing Post Creation:")
    post1 = community.create_post(
        user1.id, 
        "Welcome to SignBridge Community!", 
        "This is our community for sharing sign language knowledge.",
        "discussion",
        ["welcome", "community", "sign-language"]
    )
    post2 = community.create_post(
        user2.id,
        "Tips for Learning ASL",
        "Here are some helpful tips for beginners learning American Sign Language.",
        "tutorial",
        ["asl", "learning", "tips", "beginner"]
    )
    print(f"âœ… Posts created: {len(community.posts)}")
    
    # Test comment creation
    print("\nðŸ’¬ Testing Comment Creation:")
    comment1 = community.create_comment(post1.id, user2.id, "Great to be here!")
    comment2 = community.create_comment(post2.id, user1.id, "Very helpful tips!")
    print(f"âœ… Comments created: {len(community.comments)}")
    
    # Test tutorial creation
    print("\nðŸ“š Testing Tutorial Creation:")
    tutorial1 = community.create_tutorial(
        user1.id,
        "Basic ASL Greetings",
        "Learn how to greet people in American Sign Language",
        "Step-by-step guide to basic greetings",
        "beginner",
        "asl",
        15,
        ["greetings", "basic", "asl"],
        [
            {"step": 1, "title": "Hello", "description": "Wave your hand"},
            {"step": 2, "title": "Goodbye", "description": "Wave hand away"}
        ]
    )
    print(f"âœ… Tutorials created: {len(community.tutorials)}")
    
    # Test likes and follows
    print("\nðŸ‘ Testing Likes and Follows:")
    community.like_post(post1.id, user2.id)
    community.like_post(post2.id, user1.id)
    community.follow_user(user1.id, user2.id)
    community.follow_user(user2.id, user1.id)
    print("âœ… Likes and follows processed")
    
    # Test feed generation
    print("\nðŸ“° Testing Feed Generation:")
    feed = community.get_feed(user1.id, limit=5)
    print(f"âœ… Feed generated: {len(feed)} items")
    
    # Test search
    print("\nðŸ” Testing Search:")
    search_results = community.search_content("ASL", "all")
    print(f"âœ… Search results: {len(search_results)} items")
    
    # Test community stats
    print("\nðŸ“Š Testing Community Stats:")
    stats = community.get_community_stats()
    print(f"âœ… Total users: {stats['total_users']}")
    print(f"âœ… Total posts: {stats['total_posts']}")
    print(f"âœ… Total comments: {stats['total_comments']}")
    print(f"âœ… Total tutorials: {stats['total_tutorials']}")
    print(f"âœ… Active users (24h): {stats['active_users_24h']}")
    
    print("\nðŸŽ‰ Community platform test completed!")
    print("ðŸ‘¥ Ready for community building!")

if __name__ == "__main__":
    test_community_platform()
