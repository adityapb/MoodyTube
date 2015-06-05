# MoodyTube
**A Django powered website that plays music according to your mood**
##Music Player:
We have used last.fm's API that allows to access their database with songs sorted by tags. Then these songs are searched on YouTube using their Data API and the first result is considered.
##Mood Detection:
Mood detection is done using PCA.
Each image from the training dataset is first rotated such that eyes are aligned horizontally. Then faces are detected and the edges of faces are adjusted such that the nose of each image is at the centre of the face.
