from typing import Dict, List
from collections import OrderedDict
import numpy as np

class CentroidTracker:
    def __init__(self, max_disappeared: int = 50):
        """
        Initialize the centroid tracker.

        Args:
            max_disappeared (int): Maximum number of frames an object can be missing before deregistering.
        """
        self.next_object_id = 0
        self.objects: Dict[int, np.ndarray] = OrderedDict()  # Object ID -> Centroid (x, y)
        self.disappeared: Dict[int, int] = OrderedDict()  # Object ID -> Frames disappeared
        self.max_disappeared = max_disappeared

    def register(self, centroid: np.ndarray):
        """Register a new object with its centroid."""
        self.objects[self.next_object_id] = centroid
        self.disappeared[self.next_object_id] = 0
        self.next_object_id += 1

    def deregister(self, object_id: int):
        """Remove an object that has disappeared for too long."""
        del self.objects[object_id]
        del self.disappeared[object_id]

    def update(self, bboxes: List[dict]) -> List[int]:
        """
        Update tracker with new bounding boxes.

        Args:
            bboxes: List of bounding boxes with 'x', 'y', 'width', 'height'.

        Returns:
            List of object IDs for the current frame.
        """
        if not bboxes:
            # Increment disappeared count for all objects
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            return []

        # Compute centroids from bounding boxes
        centroids = []
        for bbox in bboxes:
            cx = bbox["x"]
            cy = bbox["y"]
            centroids.append(np.array([cx, cy]))
        centroids = np.array(centroids)

        if not self.objects:
            # Register all centroids if tracker is empty
            for centroid in centroids:
                self.register(centroid)
        else:
            # Compute distances between existing objects and new centroids
            object_ids = list(self.objects.keys())
            object_centroids = np.array(list(self.objects.values()))
            distances = np.linalg.norm(object_centroids[:, np.newaxis] - centroids, axis=2)
            
            # Match centroids to objects (smallest distance first)
            rows = distances.min(axis=1).argsort()
            cols = distances.argmin(axis=1)[rows]
            
            used_rows = set()
            used_cols = set()
            for row, col in zip(rows, cols):
                if row in used_rows or col in used_cols:
                    continue
                object_id = object_ids[row]
                self.objects[object_id] = centroids[col]
                self.disappeared[object_id] = 0
                used_rows.add(row)
                used_cols.add(col)
            
            # Register new centroids
            unused_cols = set(range(centroids.shape[0])) - used_cols
            for col in unused_cols:
                self.register(centroids[col])
            
            # Increment disappeared count for unmatched objects
            unused_rows = set(range(len(object_centroids))) - used_rows
            for row in unused_rows:
                object_id = object_ids[row]
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)

        return list(self.objects.keys())