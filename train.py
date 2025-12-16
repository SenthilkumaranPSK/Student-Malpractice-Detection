"""
Student Malpractice Detection System - Advanced Setup Module
"""
import os
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MalpracticeDetectionTrainer:
    def __init__(self):
        self.model_path = "models"
        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)
    
    def create_detection_parameters(self):
        logger.info("Creating advanced detection parameters...")
        detection_params = {
            "object_detection": {
                "enabled": True,
                "confidence_min": 0.55
            },
            "gaze_detection": {
                "enabled": True,
                "threshold_seconds": 3.0,
                "sensitivity": 0.8
            },
            "pose_detection": {
                "enabled": True,
                "hand_near_head_threshold_seconds": 2.0
            },
            "gesture_detection": {
                "enabled": True
            },
            "multiple_people_detection": {
                "enabled": True,
                "max_people": 1
            }
        }
        params_path = os.path.join(self.model_path, "detection_parameters.json")
        with open(params_path, 'w') as f:
            json.dump(detection_params, f, indent=4)
        logger.info(f"Advanced detection parameters saved to {params_path}")

    def run_setup_pipeline(self):
        logger.info("Starting advanced setup pipeline...")
        self.create_detection_parameters()
        logger.info("Setup pipeline completed successfully!")

def main():
    print("=" * 60)
    print("Student Malpractice Detection System - Advanced Setup")
    print("=" * 60)
    trainer = MalpracticeDetectionTrainer()
    trainer.run_setup_pipeline()
    print("\n✅ Setup completed. System is ready for main.py")

if __name__ == "__main__":
    main()