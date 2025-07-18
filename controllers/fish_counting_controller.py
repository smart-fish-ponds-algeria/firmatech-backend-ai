from modules.fish_counting_models import FishCountResponse
from services.roboflow_service import RoboflowService
import tempfile
import cv2
import os
import time
from utils.centroid_tracker import CentroidTracker

class FishCountController:
    def __init__(self):
        self.fish_counting_service = RoboflowService()
        self.tracker = CentroidTracker(max_disappeared=50)  # Allow fish to disappear for 50 frames

    async def count_fish(self, video_path: str, fps: int = 5) -> FishCountResponse:
        """
        Processes a video file, extracts frames at specified fps, analyzes each frame using RoboflowService,
        tracks fish across frames, and returns the total unique fish count.

        Args:
            video_path (str): Path to the video file.
            fps (int): Frames per second to sample for detection (default: 5).

        Returns:
            FishCountResponse: Object containing the total unique fish count.
        """
        # Open video file
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError("Could not open video file")

        # Get video frame rate
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(video_fps / fps) if video_fps > 0 else 1

        unique_fish_ids = set()  # Track unique fish IDs
        frame_count = 0

        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # Process every nth frame based on desired fps
                if frame_count % frame_interval == 0:
                    # Save frame to temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
                        tmp_path = tmp.name
                        cv2.imwrite(tmp_path, frame)
                        tmp.close()  # Explicitly close the file

                    try:
                        # Analyze frame
                        result = self.fish_counting_service.infer_image_detection(tmp_path)
                        predictions = self.fish_counting_service.get_predictions(result)
                        # Filter for Talipia detections
                        talipia_bboxes = [
                            pred for pred in predictions if pred.get("class") == "Talipia"
                        ]
                        # Update tracker with bounding boxes
                        object_ids = self.tracker.update(talipia_bboxes)
                        # Add new IDs to the set
                        unique_fish_ids.update(object_ids)
                    finally:
                        # Attempt to delete the temporary file with retries
                        max_retries = 3
                        for _ in range(max_retries):
                            try:
                                os.unlink(tmp_path)
                                break
                            except PermissionError:
                                time.sleep(0.1)  # Wait briefly and retry

                frame_count += 1

        finally:
            cap.release()

        return FishCountResponse(total_count=len(unique_fish_ids))