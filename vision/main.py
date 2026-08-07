"""
vision/main.py

Vision World Model Demo

Pipeline

Webcam / Video
        ↓
YOLO Detector
        ↓
Object Tracker
        ↓
Scene Builder
        ↓
Relationship Engine
        ↓
Structured World Model
"""

import cv2
import time
import json
from shared.world_model import SharedWorldModel
from vision.input_source import InputSource
from vision.detector import ObjectDetector
from vision.tracker import ObjectTracker
from vision.scene_builder import SceneBuilder


# --------------------------------------------------
# Configuration
# --------------------------------------------------

MIN_CONFIDENCE = 0.50


# --------------------------------------------------
# Initialize
# --------------------------------------------------

camera = InputSource()

detector = ObjectDetector()

tracker = ObjectTracker()

builder = SceneBuilder()
shared_world = SharedWorldModel()
last_print = 0


# --------------------------------------------------
# Main Loop
# --------------------------------------------------

while True:

    success, frame = camera.read()

    if not success:
        break

    # ---------------------------------------------
    # Object Detection
    # ---------------------------------------------

    results = detector.detect(frame)

    result = results[0]

    detections = []

    for box in result.boxes:

        cls = int(box.cls[0])

        confidence = float(box.conf[0])

        name = result.names[cls]

        if confidence < MIN_CONFIDENCE:
            continue

        detections.append({

            "name": name,

            "confidence": confidence,

            "bbox": box.xyxy[0].tolist(),

        })

    # ---------------------------------------------
    # Update Tracker
    # ---------------------------------------------

    tracker.update(detections)

    # ---------------------------------------------
    # Build Scene
    # ---------------------------------------------

    world = builder.build(tracker)
    shared_world.update_from_vision(world)
    # ---------------------------------------------
    # Save JSON
    # ---------------------------------------------

    with open("world_model.json", "w") as file:

        json.dump(
            shared_world.export(),
            file,
            indent=4,
        )

    # ---------------------------------------------
    # Print World Model
    # ---------------------------------------------

    if time.time() - last_print >= 1:

        print("\n" + "=" * 60)
        print("VISION WORLD MODEL")
        print("=" * 60)

        print(f"Frame             : {world['frame']}")
        print(f"Visible Objects   : {world['summary']['visible_objects']}")
        print(f"Hidden Objects    : {world['summary']['hidden_objects']}")
        print(f"Confirmed Objects : {world['summary']['confirmed_objects']}")
        print(f"Likely Objects    : {world['summary']['likely_objects']}")
        print(f"Uncertain Objects : {world['summary']['uncertain_objects']}")

        print()

        print("=" * 60)
        print("OBJECTS")
        print("=" * 60)

        for obj in world["objects"]:

            print(f"Object      : {obj['name']}")
            print(f"Status      : {obj['status']}")
            print(f"Visible     : {obj['visible']}")
            print(f"Confidence  : {obj['confidence']:.2f}")
            print(f"First Seen  : {obj['first_seen']}")
            print(f"Last Seen   : {obj['last_seen']}")
            print(f"Missed      : {obj['missed_frames']}")
            print("-" * 40)

        print()

        print("=" * 60)
        print("RELATIONSHIPS")
        print("=" * 60)

        if not world["relations"]:

            print("No relationships detected.")

        else:

            for relation in world["relations"]:

                print(
                    f"{relation['subject']} "
                    f"{relation['relation']} "
                    f"{relation['object']}"
                )
            print()

            print("=" * 60)
            print("SHARED WORLD MODEL")
            print("=" * 60)

            summary = shared_world.summary()

            print(f"Entities   : {summary['entities']}")
            print(f"Relations  : {summary['relations']}")
            print(f"Properties : {summary['properties']}")

            last_print = time.time()

    # ---------------------------------------------
    # Display
    # ---------------------------------------------

    annotated = result.plot()

    cv2.imshow(
        "Vision World Model",
        annotated,
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# --------------------------------------------------
# Cleanup
# --------------------------------------------------

camera.release()

cv2.destroyAllWindows()