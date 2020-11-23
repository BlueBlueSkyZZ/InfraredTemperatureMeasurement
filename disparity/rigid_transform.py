import numpy as np
import cv2
import json

shape = (1, 10, 2)  # Needs to be a 3D array
source = np.random.randint(0, 100, shape).astype(np.int)
target = source + np.array([1, 0]).astype(np.int)


print(source)
print(target)
# transformation = cv2.estimateRigidTransform(source, target, False)
transformation = cv2.estimateAffine2D(source, target, False)
print(transformation)

