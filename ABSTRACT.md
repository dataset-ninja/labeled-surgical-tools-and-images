The **Labeled Surgical Tools and Images** was created for a master's thesis project focused on sorting surgical tools from a cluttered tray. The goal was to address object detection and occlusion reasoning using YOLOv2 and YOLOv3 neural networks.

The dataset's inspiration arose from an interview with the Chief Nurse of the Main Operating Room at the Hospital of the University of Coimbra. During the interview, concerns were raised about the time nurses spend sorting surgical tools after disinfection, which could be better utilized for patient care. This dataset was created as part of an effort to develop a robotic system that could streamline this process.

The dataset comprises a total of 3009 images, each accompanied by corresponding labels. These labels categorize the objects into four types: *scalpel #4*, *straight dissection clamp*, s*traight mayo scissor*, or *curved mayo scissor*. Additionally, each tool is classified as either "on top" (not occluded) or "at the bottom" (occluded).

To ensure a balanced division for object detection, the dataset is split into training and test groups. While the standard split ratio in machine learning is 70% for training and 30% for testing, the authors stressed the importance of maintaining a balanced proportion of every class within the dataset. To achieve this, they employed a more nuanced approach to determine the division percentages, taking into account the number of images for each combination of tools.

To construct the dataset, the authors took multiple photos of each surgical instrument individually, varying the tray's rotations, inclinations, and lighting conditions. They used BBox-Label-Tool and YoloMark for this purpose. To account for occlusion, each tool was paired with another of a different class, and the same photographic process was repeated, with one instrument occluding the other. Finally, additional photos were taken with tools from all classes without occlusion.

The division of the dataset into train and test groups was carefully considered to maintain balance, especially for images with two instruments. This involved calculating the optimal number of images for each instrument combination and ensuring that occlusion reasoning data was also appropriately divided.

To facilitate this complex division process, a Python script was developed, randomly sorting the dataset multiple times and selecting images for the test and train groups based on the calculated values.

Overall, the dataset was meticulously created to support the development of robotic systems for surgical tool sorting, addressing the challenges of object detection and occlusion reasoning in this context.
