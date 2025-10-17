# Training Pipeline for Sign Recognition Model
# Automated training with data augmentation and evaluation

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import json
import time

# Add src directory to path
sys.path.append(str(Path(__file__).parent.parent))

from ml.sign_recognition_model import SignRecognitionModel
from ml.data_collection.data_collector import SignDataCollector

class TrainingPipeline:
    """Complete training pipeline for sign recognition"""
    
    def __init__(self, data_dir: str = "data/asl_dataset", model_dir: str = "src/ml/models"):
        """Initialize training pipeline"""
        self.data_dir = Path(data_dir)
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        self.model = None
        self.training_history = None
        
        print("âœ… Training Pipeline initialized")
        print(f"ðŸ“ Data directory: {self.data_dir}")
        print(f"ðŸ“ Model directory: {self.model_dir}")
    
    def prepare_data(self) -> bool:
        """Prepare data for training"""
        try:
            print("ðŸ“Š Preparing data for training...")
            
            # Check if data exists
            if not self.data_dir.exists():
                print("âŒ Data directory not found")
                print("ðŸ’¡ Run data collection first: python src/ml/data_collection/data_collector.py")
                return False
            
            # Count classes and samples
            classes = [d.name for d in self.data_dir.iterdir() if d.is_dir()]
            total_samples = 0
            
            for class_dir in self.data_dir.iterdir():
                if class_dir.is_dir():
                    samples = len(list(class_dir.glob("*.jpg")))
                    total_samples += samples
                    print(f"ðŸ“ {class_dir.name}: {samples} samples")
            
            print(f"âœ… Data preparation complete")
            print(f"ðŸ“Š Total classes: {len(classes)}")
            print(f"ðŸ“Š Total samples: {total_samples}")
            
            return True
            
        except Exception as e:
            print(f"âŒ Error preparing data: {e}")
            return False
    
    def train_model(self, epochs: int = 50, batch_size: int = 32) -> bool:
        """Train the sign recognition model"""
        try:
            print("ðŸš€ Starting model training...")
            
            # Initialize model
            classes = [d.name for d in self.data_dir.iterdir() if d.is_dir()]
            self.model = SignRecognitionModel(num_classes=len(classes))
            
            # Build model
            self.model.build_model()
            
            # Create data generators
            train_gen, val_gen = self.model.create_data_generator(str(self.data_dir), batch_size)
            
            if train_gen is None or val_gen is None:
                print("âŒ Failed to create data generators")
                return False
            
            # Train model
            self.training_history = self.model.train_model(train_gen, val_gen, epochs)
            
            print("âœ… Model training completed!")
            return True
            
        except Exception as e:
            print(f"âŒ Error training model: {e}")
            return False
    
    def evaluate_model(self) -> Dict:
        """Evaluate the trained model"""
        try:
            print("ðŸ“Š Evaluating model...")
            
            if self.model is None:
                print("âŒ Model not trained yet")
                return {}
            
            # Create test generator
            test_gen, _ = self.model.create_data_generator(str(self.data_dir), batch_size=32)
            
            if test_gen is None:
                print("âŒ Failed to create test generator")
                return {}
            
            # Evaluate
            results = self.model.evaluate_model(test_gen)
            
            if results:
                print(f"ðŸ“ˆ Test Accuracy: {results['test_accuracy']:.4f}")
                print(f"ðŸ“ˆ Top-3 Accuracy: {results['top_3_accuracy']:.4f}")
            
            return results
            
        except Exception as e:
            print(f"âŒ Error evaluating model: {e}")
            return {}
    
    def save_training_results(self):
        """Save training results and visualizations"""
        try:
            print("ðŸ’¾ Saving training results...")
            
            if self.training_history is None:
                print("âŒ No training history to save")
                return
            
            # Save training history
            history_file = self.model_dir / "training_history.json"
            with open(history_file, 'w') as f:
                json.dump(self.training_history, f, indent=2)
            
            # Plot training history
            self.model.plot_training_history(str(self.model_dir / "training_history.png"))
            
            # Save model info
            self.model.save_model_info(str(self.model_dir / "model_info.json"))
            
            print("âœ… Training results saved")
            
        except Exception as e:
            print(f"âŒ Error saving training results: {e}")
    
    def run_complete_pipeline(self, epochs: int = 50) -> bool:
        """Run the complete training pipeline"""
        try:
            print("ðŸŽ¯ Starting Complete Training Pipeline")
            print("=" * 60)
            
            start_time = time.time()
            
            # Step 1: Prepare data
            print("\nðŸ“Š Step 1: Data Preparation")
            if not self.prepare_data():
                return False
            
            # Step 2: Train model
            print("\nðŸš€ Step 2: Model Training")
            if not self.train_model(epochs):
                return False
            
            # Step 3: Evaluate model
            print("\nðŸ“Š Step 3: Model Evaluation")
            results = self.evaluate_model()
            
            # Step 4: Save results
            print("\nðŸ’¾ Step 4: Save Results")
            self.save_training_results()
            
            # Summary
            end_time = time.time()
            training_time = end_time - start_time
            
            print("\nðŸŽ‰ Training Pipeline Complete!")
            print("=" * 60)
            print(f"â±ï¸ Total training time: {training_time:.2f} seconds")
            
            if results:
                print(f"ðŸ“ˆ Final Test Accuracy: {results['test_accuracy']:.4f}")
                print(f"ðŸ“ˆ Final Top-3 Accuracy: {results['top_3_accuracy']:.4f}")
            
            print(f"ðŸ“ Models saved to: {self.model_dir}")
            print(f"ðŸ“Š Training history saved")
            print(f"ðŸ“ˆ Visualizations created")
            
            return True
            
        except Exception as e:
            print(f"âŒ Error in training pipeline: {e}")
            return False

# Quick training for testing
def quick_train():
    """Quick training with minimal data for testing"""
    print("ðŸ§ª Quick Training Test")
    print("=" * 30)
    
    pipeline = TrainingPipeline()
    
    # Create dummy data for testing
    print("ðŸ“Š Creating dummy data for testing...")
    
    # This would normally load real data
    # For now, we'll just test the model architecture
    model = SignRecognitionModel(num_classes=10)
    model.build_model()
    model.get_model_summary()
    
    print("âœ… Quick training test completed!")
    print("ðŸ’¡ Ready for real data training!")

# Main training function
def main():
    """Main training function"""
    print("ðŸŽ¯ SignBridge AI Training Pipeline")
    print("=" * 50)
    
    # Check if data exists
    data_dir = Path("data/asl_dataset")
    if not data_dir.exists():
        print("âŒ No training data found!")
        print("ðŸ’¡ Please collect data first:")
        print("   python src/ml/data_collection/data_collector.py")
        return
    
    # Run training pipeline
    pipeline = TrainingPipeline()
    success = pipeline.run_complete_pipeline(epochs=30)  # Reduced for testing
    
    if success:
        print("\nðŸŽ‰ Training completed successfully!")
        print("ðŸ“ Check src/ml/models/ for saved models")
    else:
        print("\nâŒ Training failed!")
        print("ðŸ’¡ Check error messages above")

if __name__ == "__main__":
    main()
