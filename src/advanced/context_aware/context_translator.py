# Context-Aware Translation System
# Smart conversation understanding and context preservation

import json
import time
import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path

class ContextAwareTranslator:
    """Context-aware translation system for smart conversation understanding"""
    
    def __init__(self):
        """Initialize context-aware translator"""
        self.conversation_context = {}
        self.emotion_detector = self._initialize_emotion_detector()
        self.grammar_analyzer = self._initialize_grammar_analyzer()
        self.context_history = []
        self.topic_tracker = {}
        self.sentiment_analyzer = self._initialize_sentiment_analyzer()
        
        print("âœ… Context-Aware Translator initialized")
        print("ðŸ§  Emotion detection: Active")
        print("ðŸ“ Grammar analysis: Active")
        print("ðŸ’­ Context tracking: Active")
        print("ðŸ“Š Sentiment analysis: Active")
    
    def _initialize_emotion_detector(self) -> Dict:
        """Initialize emotion detection system"""
        return {
            "emotion_keywords": {
                "happy": ["happy", "joy", "excited", "pleased", "delighted", "cheerful"],
                "sad": ["sad", "depressed", "upset", "crying", "mourning", "grief"],
                "angry": ["angry", "mad", "furious", "rage", "irritated", "annoyed"],
                "fear": ["afraid", "scared", "fear", "terrified", "worried", "anxious"],
                "surprise": ["surprised", "shocked", "amazed", "astonished", "startled"],
                "disgust": ["disgusted", "revolted", "sick", "nauseated", "repulsed"],
                "neutral": ["okay", "fine", "normal", "regular", "usual", "standard"]
            },
            "emotion_signs": {
                "happy": ["happy", "smile", "laugh", "joy"],
                "sad": ["sad", "cry", "tears", "depressed"],
                "angry": ["angry", "mad", "furious", "rage"],
                "fear": ["afraid", "scared", "fear", "worried"],
                "surprise": ["surprised", "shocked", "amazed"],
                "disgust": ["disgusted", "sick", "nauseated"],
                "neutral": ["neutral", "okay", "fine"]
            },
            "confidence_threshold": 0.7
        }
    
    def _initialize_grammar_analyzer(self) -> Dict:
        """Initialize grammar analysis system"""
        return {
            "sentence_patterns": {
                "question": r"^(what|where|when|why|how|who|which|is|are|do|does|did|can|could|would|will|shall)",
                "statement": r"^(i|you|he|she|it|we|they|this|that|the|a|an)",
                "command": r"^(please|help|stop|go|come|wait|give|take|put|get)",
                "exclamation": r"(!|wow|oh|ah|oh no|great|terrible|amazing)"
            },
            "grammar_rules": {
                "subject_verb_agreement": True,
                "tense_consistency": True,
                "pronoun_reference": True,
                "sentence_structure": True
            },
            "context_clues": {
                "pronouns": ["i", "you", "he", "she", "it", "we", "they", "this", "that"],
                "time_markers": ["now", "today", "yesterday", "tomorrow", "always", "never", "sometimes"],
                "location_markers": ["here", "there", "home", "work", "school", "hospital"],
                "relationship_markers": ["family", "friend", "doctor", "teacher", "boss"]
            }
        }
    
    def _initialize_sentiment_analyzer(self) -> Dict:
        """Initialize sentiment analysis system"""
        return {
            "positive_words": ["good", "great", "excellent", "wonderful", "amazing", "fantastic", "love", "like", "enjoy"],
            "negative_words": ["bad", "terrible", "awful", "horrible", "hate", "dislike", "angry", "sad", "upset"],
            "neutral_words": ["okay", "fine", "normal", "regular", "usual", "standard", "average"],
            "intensity_modifiers": {
                "very": 1.5,
                "extremely": 2.0,
                "slightly": 0.5,
                "somewhat": 0.7,
                "quite": 1.2,
                "really": 1.3
            }
        }
    
    def analyze_emotion(self, text: str, signs: List[str]) -> Tuple[str, float]:
        """Analyze emotion from text and signs"""
        emotion_scores = {}
        
        # Analyze text emotion
        text_lower = text.lower()
        for emotion, keywords in self.emotion_detector["emotion_keywords"].items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
            emotion_scores[emotion] = score
        
        # Analyze sign emotion
        for emotion, sign_keywords in self.emotion_detector["emotion_signs"].items():
            for sign in signs:
                if sign in sign_keywords:
                    emotion_scores[emotion] = emotion_scores.get(emotion, 0) + 1
        
        # Find dominant emotion
        if emotion_scores:
            dominant_emotion = max(emotion_scores, key=emotion_scores.get)
            confidence = min(emotion_scores[dominant_emotion] / 3.0, 1.0)  # Normalize to 0-1
            
            if confidence >= self.emotion_detector["confidence_threshold"]:
                return dominant_emotion, confidence
        
        return "neutral", 0.5
    
    def analyze_sentiment(self, text: str) -> Tuple[str, float]:
        """Analyze sentiment of text"""
        text_lower = text.lower()
        words = text_lower.split()
        
        positive_score = 0
        negative_score = 0
        neutral_score = 0
        
        for i, word in enumerate(words):
            # Check for intensity modifiers
            intensity = 1.0
            if i > 0 and words[i-1] in self.sentiment_analyzer["intensity_modifiers"]:
                intensity = self.sentiment_analyzer["intensity_modifiers"][words[i-1]]
            
            if word in self.sentiment_analyzer["positive_words"]:
                positive_score += intensity
            elif word in self.sentiment_analyzer["negative_words"]:
                negative_score += intensity
            elif word in self.sentiment_analyzer["neutral_words"]:
                neutral_score += intensity
        
        total_score = positive_score + negative_score + neutral_score
        if total_score > 0:
            if positive_score > negative_score and positive_score > neutral_score:
                return "positive", positive_score / total_score
            elif negative_score > positive_score and negative_score > neutral_score:
                return "negative", negative_score / total_score
            else:
                return "neutral", neutral_score / total_score
        
        return "neutral", 0.5
    
    def analyze_grammar(self, text: str) -> Dict:
        """Analyze grammar and sentence structure"""
        analysis = {
            "sentence_type": "statement",
            "grammar_errors": [],
            "context_clues": [],
            "complexity_score": 0.0
        }
        
        text_lower = text.lower().strip()
        
        # Determine sentence type
        for pattern_name, pattern in self.grammar_analyzer["sentence_patterns"].items():
            if re.match(pattern, text_lower):
                analysis["sentence_type"] = pattern_name
                break
        
        # Extract context clues
        words = text_lower.split()
        for word in words:
            if word in self.grammar_analyzer["context_clues"]["pronouns"]:
                analysis["context_clues"].append(f"pronoun: {word}")
            elif word in self.grammar_analyzer["context_clues"]["time_markers"]:
                analysis["context_clues"].append(f"time: {word}")
            elif word in self.grammar_analyzer["context_clues"]["location_markers"]:
                analysis["context_clues"].append(f"location: {word}")
            elif word in self.grammar_analyzer["context_clues"]["relationship_markers"]:
                analysis["context_clues"].append(f"relationship: {word}")
        
        # Calculate complexity score
        analysis["complexity_score"] = len(words) / 20.0  # Normalize to 0-1
        
        return analysis
    
    def update_context(self, speaker: str, text: str, signs: List[str], timestamp: float):
        """Update conversation context"""
        context_entry = {
            "speaker": speaker,
            "text": text,
            "signs": signs,
            "timestamp": timestamp,
            "emotion": self.analyze_emotion(text, signs)[0],
            "sentiment": self.analyze_sentiment(text)[0],
            "grammar": self.analyze_grammar(text)
        }
        
        self.context_history.append(context_entry)
        
        # Keep only last 20 entries
        if len(self.context_history) > 20:
            self.context_history.pop(0)
        
        # Update topic tracking
        self._update_topic_tracking(context_entry)
        
        print(f"âœ… Context updated: {speaker} - {context_entry['emotion']} - {context_entry['sentiment']}")
    
    def _update_topic_tracking(self, context_entry: Dict):
        """Update topic tracking based on context"""
        text = context_entry["text"].lower()
        signs = context_entry["signs"]
        
        # Simple topic detection based on keywords
        topics = {
            "health": ["doctor", "hospital", "medicine", "pain", "sick", "health"],
            "family": ["family", "mother", "father", "brother", "sister", "parent"],
            "work": ["work", "job", "office", "meeting", "boss", "colleague"],
            "education": ["school", "teacher", "student", "learn", "study", "class"],
            "food": ["food", "eat", "hungry", "restaurant", "cooking", "meal"],
            "travel": ["travel", "trip", "vacation", "hotel", "airplane", "car"]
        }
        
        for topic, keywords in topics.items():
            for keyword in keywords:
                if keyword in text or keyword in signs:
                    if topic not in self.topic_tracker:
                        self.topic_tracker[topic] = 0
                    self.topic_tracker[topic] += 1
                    break
    
    def get_context_summary(self) -> Dict:
        """Get current conversation context summary"""
        if not self.context_history:
            return {"message": "No conversation context available"}
        
        recent_context = self.context_history[-5:]  # Last 5 entries
        
        # Analyze recent emotions
        recent_emotions = [entry["emotion"] for entry in recent_context]
        dominant_emotion = max(set(recent_emotions), key=recent_emotions.count)
        
        # Analyze recent sentiment
        recent_sentiments = [entry["sentiment"] for entry in recent_context]
        dominant_sentiment = max(set(recent_sentiments), key=recent_sentiments.count)
        
        # Get current topics
        current_topics = sorted(self.topic_tracker.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            "conversation_length": len(self.context_history),
            "recent_entries": len(recent_context),
            "dominant_emotion": dominant_emotion,
            "dominant_sentiment": dominant_sentiment,
            "current_topics": current_topics,
            "last_speaker": recent_context[-1]["speaker"] if recent_context else None,
            "last_message": recent_context[-1]["text"] if recent_context else None
        }
    
    def generate_contextual_response(self, input_text: str, input_signs: List[str]) -> Dict:
        """Generate contextual response based on conversation history"""
        # Analyze input
        emotion, emotion_confidence = self.analyze_emotion(input_text, input_signs)
        sentiment, sentiment_confidence = self.analyze_sentiment(input_text)
        grammar = self.analyze_grammar(input_text)
        
        # Get context summary
        context_summary = self.get_context_summary()
        
        # Generate appropriate response
        response = {
            "input_analysis": {
                "emotion": emotion,
                "emotion_confidence": emotion_confidence,
                "sentiment": sentiment,
                "sentiment_confidence": sentiment_confidence,
                "grammar": grammar
            },
            "context_summary": context_summary,
            "suggested_response": self._generate_suggested_response(emotion, sentiment, context_summary),
            "recommended_signs": self._get_recommended_signs(emotion, sentiment, context_summary),
            "context_preservation": self._preserve_context(input_text, input_signs)
        }
        
        return response
    
    def _generate_suggested_response(self, emotion: str, sentiment: str, context_summary: Dict) -> str:
        """Generate suggested response based on context"""
        if emotion == "happy" and sentiment == "positive":
            return "I'm glad to hear that! It sounds like things are going well."
        elif emotion == "sad" and sentiment == "negative":
            return "I'm sorry to hear that. Is there anything I can do to help?"
        elif emotion == "angry" and sentiment == "negative":
            return "I understand you're upset. Let's work through this together."
        elif emotion == "fear" and sentiment == "negative":
            return "It's okay to feel scared. You're safe here."
        elif emotion == "surprise" and sentiment == "positive":
            return "That's wonderful news! I'm excited for you."
        else:
            return "I understand. Thank you for sharing that with me."
    
    def _get_recommended_signs(self, emotion: str, sentiment: str, context_summary: Dict) -> List[str]:
        """Get recommended signs based on context"""
        recommended = []
        
        if emotion == "happy":
            recommended.extend(["happy", "smile", "joy", "love"])
        elif emotion == "sad":
            recommended.extend(["sad", "sorry", "comfort", "hug"])
        elif emotion == "angry":
            recommended.extend(["angry", "calm", "breathe", "help"])
        elif emotion == "fear":
            recommended.extend(["afraid", "safe", "protect", "help"])
        
        if sentiment == "positive":
            recommended.extend(["yes", "good", "great", "wonderful"])
        elif sentiment == "negative":
            recommended.extend(["no", "bad", "help", "support"])
        
        return list(set(recommended))  # Remove duplicates
    
    def _preserve_context(self, text: str, signs: List[str]) -> Dict:
        """Preserve important context information"""
        return {
            "key_entities": self._extract_entities(text),
            "important_signs": signs,
            "conversation_flow": self._analyze_conversation_flow(),
            "context_continuity": self._check_context_continuity(text)
        }
    
    def _extract_entities(self, text: str) -> List[str]:
        """Extract important entities from text"""
        # Simple entity extraction (in a real system, use NER)
        entities = []
        words = text.lower().split()
        
        # Look for capitalized words (potential proper nouns)
        for word in text.split():
            if word[0].isupper() and len(word) > 1:
                entities.append(word)
        
        return entities
    
    def _analyze_conversation_flow(self) -> str:
        """Analyze the flow of conversation"""
        if len(self.context_history) < 2:
            return "beginning"
        
        recent_types = [entry["grammar"]["sentence_type"] for entry in self.context_history[-3:]]
        
        if "question" in recent_types:
            return "question_answer"
        elif "command" in recent_types:
            return "instruction_following"
        elif "exclamation" in recent_types:
            return "emotional_expression"
        else:
            return "conversational"
    
    def _check_context_continuity(self, text: str) -> bool:
        """Check if current input maintains context continuity"""
        if not self.context_history:
            return True
        
        last_entry = self.context_history[-1]
        
        # Check for pronoun references
        pronouns = ["it", "this", "that", "they", "he", "she"]
        text_lower = text.lower()
        
        for pronoun in pronouns:
            if pronoun in text_lower:
                # Check if pronoun has a clear antecedent
                if any(word in last_entry["text"].lower() for word in ["it", "this", "that", "they", "he", "she"]):
                    return True
        
        return True  # Default to maintaining continuity
    
    def export_context_data(self, file_path: str):
        """Export context data to JSON file"""
        try:
            context_data = {
                "context_history": self.context_history,
                "topic_tracker": self.topic_tracker,
                "export_timestamp": time.time()
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(context_data, f, indent=2, ensure_ascii=False)
            
            print(f"âœ… Context data exported to {file_path}")
        except Exception as e:
            print(f"âŒ Error exporting context data: {e}")
    
    def get_system_statistics(self) -> Dict:
        """Get context-aware translator statistics"""
        return {
            "total_context_entries": len(self.context_history),
            "active_topics": len(self.topic_tracker),
            "emotion_detection_active": True,
            "sentiment_analysis_active": True,
            "grammar_analysis_active": True,
            "context_tracking_active": True,
            "system_status": "active"
        }

# Example usage and testing
def test_context_aware_translator():
    """Test context-aware translator features"""
    print("ðŸ§ª Testing Context-Aware Translator")
    print("=" * 50)
    
    # Initialize translator
    translator = ContextAwareTranslator()
    
    # Test emotion detection
    print("\nðŸ˜Š Testing Emotion Detection:")
    emotion, confidence = translator.analyze_emotion("I am so happy today!", ["happy", "smile"])
    print(f"âœ… Emotion: {emotion} (confidence: {confidence:.2f})")
    
    emotion, confidence = translator.analyze_emotion("I feel really sad", ["sad", "cry"])
    print(f"âœ… Emotion: {emotion} (confidence: {confidence:.2f})")
    
    # Test sentiment analysis
    print("\nðŸ“Š Testing Sentiment Analysis:")
    sentiment, confidence = translator.analyze_sentiment("This is absolutely wonderful!")
    print(f"âœ… Sentiment: {sentiment} (confidence: {confidence:.2f})")
    
    sentiment, confidence = translator.analyze_sentiment("This is terrible and awful")
    print(f"âœ… Sentiment: {sentiment} (confidence: {confidence:.2f})")
    
    # Test grammar analysis
    print("\nðŸ“ Testing Grammar Analysis:")
    grammar = translator.analyze_grammar("What is your name?")
    print(f"âœ… Sentence type: {grammar['sentence_type']}")
    print(f"âœ… Context clues: {grammar['context_clues']}")
    
    # Test context updating
    print("\nðŸ’­ Testing Context Updates:")
    translator.update_context("user", "Hello, how are you?", ["hello", "how"], time.time())
    translator.update_context("assistant", "I'm doing well, thank you!", ["good", "thank_you"], time.time())
    translator.update_context("user", "That's great to hear!", ["great", "hear"], time.time())
    
    # Test context summary
    print("\nðŸ“‹ Testing Context Summary:")
    summary = translator.get_context_summary()
    print(f"âœ… Conversation length: {summary['conversation_length']}")
    print(f"âœ… Dominant emotion: {summary['dominant_emotion']}")
    print(f"âœ… Dominant sentiment: {summary['dominant_sentiment']}")
    print(f"âœ… Current topics: {summary['current_topics']}")
    
    # Test contextual response generation
    print("\nðŸ¤– Testing Contextual Response Generation:")
    response = translator.generate_contextual_response("I'm feeling excited about my new job!", ["excited", "work"])
    print(f"âœ… Suggested response: {response['suggested_response']}")
    print(f"âœ… Recommended signs: {response['recommended_signs']}")
    
    # Test system statistics
    print("\nðŸ“ˆ Testing System Statistics:")
    stats = translator.get_system_statistics()
    print(f"âœ… Total context entries: {stats['total_context_entries']}")
    print(f"âœ… Active topics: {stats['active_topics']}")
    print(f"âœ… System status: {stats['system_status']}")
    
    print("\nðŸŽ‰ Context-aware translator test completed!")

if __name__ == "__main__":
    test_context_aware_translator()
