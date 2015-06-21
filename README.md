# MoodyTube
**A Django powered website that plays music according to your mood**
##Music Player:
We have used last.fm's API that allows to access their database with songs sorted by tags. Then these songs are searched on YouTube using their Data API and the first result is considered.
##Mood Detection:
There are 3 parts to this process:
###1. Pre-Processing:
**The images from training dataset are first rotated such that eyes are horizontally aligned.**<br>
For this, first eyes are detected using eye haarcascade and the eyeballs are detected by Shi-Tomasi corner detection method.
![Eye detection](/Screenshots/eye_detect.png)<br>
![Aligned Image](/Screenshots/align.png)<br><br>
**The aligned image is then resized so that distance between the eyes is equal to that of the sample image.**<br>
Sample image considered in this case:<br>
![Sample image](/Screenshots/sample.bmp)<br><br>
**The training set images are then cropped so that eyes each of the training set image coincides with eyes of the sample image**<br>
For this, coordinates of the midpoint of the eyes is calculated relative to the border of the sample image. The image is cropped along the border calculated according to midpoint of the eyes of sample image.
###2. PCA:
**Eigenfaces are calculated for training set and each image is reconstructed in eigenspace. The weights are then used to train an SVM**<br>
Example of eigenfaces used in this case:<br>
![eigenface0](/Screenshots/eigenface0.png)
![eigenface1](/Screenshots/eigenface1.png)
![eigenface2](/Screenshots/eigenface2.png)<br>
Here is an example plot of weights for images reconstructed using 3 eigenfaces:<br>
![plot](/Screenshots/plot.png)<br>
The blue points represent sad faces and red points represent happy faces.<br><br>
**Example of reconstruction weights for a sad person:**<br>
![plot_recog](/Screenshots/plot_recog.png)<br>
The black point is the person outside the training class.

