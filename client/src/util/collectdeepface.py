import os
import shutil
from pathlib import Path
import sys

def initialize_weights():
    # 1. Determine where we are (Bundled vs Development)
    if hasattr(sys, '_MEIPASS'):
        bundle_dir = sys._MEIPASS
    else:
        bundle_dir = os.path.abspath(".")

    # 2. Define DeepFace's expected weights directory
    home = str(Path.home())
    deepface_home = os.path.join(home, ".deepface", "weights")

    if not os.path.exists(deepface_home):
        os.makedirs(deepface_home)

    # 3. Source of weights inside your bundle (defined in .spec)
    bundled_weights_path = os.path.join(bundle_dir, "deepface_weights")

    # 4. Copy weights if they aren't already in the user's home folder
    for weight_file in ["age_model_weights.h5", "retinaface.h5"]:
        target_path = os.path.join(deepface_home, weight_file)
        if not os.path.exists(target_path):
            source_path = os.path.join(bundled_weights_path, weight_file)
            shutil.copy(source_path, target_path)
            print(f"Initialized {weight_file}")

# Call this at the very start of your app
