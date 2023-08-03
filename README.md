#Content-Based-Image-Retrieval
Content-based image retrieval (CBIR) using Texture and Colour Moments is a technique that allows users to search and retrieve images similar to query images from a large database based on their visual content. CBIR systems use various features extracted from images, such as colour, texture, shape, and spatial relationships, to represent and compare images.

#Methods and Model
1. Colour Moments
The colour moments are a set of statistical measures that describe the colour distribution of an image. We calculate the first, second, and third-order moments of the colour channels of an image (here, HSV scheme of Hue, Saturation and Value), which provide information about the Mean, Variance, and Skewness of the colour distribution.

2. Linear Binary Patterns (LBPs)
Linear Binary Patterns (LBP) is a widely used texture descriptor in image processing and computer vision. LBP is a simple yet effective descriptor that encodes an image’s local texture information by comparing the pixel values of a central pixel to its surrounding neighbours in a pre-defined, circular or rectangular region. For each pixel in the region, a binary value is assigned based on whether the intensity value is greater or less than the intensity value of the central pixel. These binary values are then concatenated to form a binary pattern that describes the texture of the region.
https://user-images.githubusercontent.com/73419394/258059133-abd9bcc5-c09b-4491-ba07-d31610ee2c6c.png


Binary equivalent: 00010111 and Decimal equivalent: 23. So, 23 will be the LBP value for the circled pixel.
Similarly, for each pixel, corresponding values are calculated using which a histogram is plotted that is used as a feature vector for the image to compare it with other images.

3. Similarity Measures
Similarity measures are used to compare two or more images and determine how similar or different they are.

Euclidean Distance
It measures the distance between the feature vector values (considered points in n-D space) of two images. The lower value of Euclidean distance signifies that the two images are more similar or less dissimilar than the others having larger values.

https://user-images.githubusercontent.com/73419394/258060602-0c0d4fbd-8495-4079-9b8c-b087610615c4.png

Cosine Similarity
It is mathematically defined as the dot product of the feature vectors divided by their magnitude. The higher cosine similarity value signifies that the two images are more similar or less dissimilar than the others with lesser values. A negative value means that the two images are opposite vectors or not identical.

https://user-images.githubusercontent.com/73419394/258061237-17700622-f464-42fe-a715-89bba7aa78cc.png

4. Model
https://user-images.githubusercontent.com/73419394/258062493-ff1d68dc-6c75-4e46-8831-17391ee2b502.png

#Results
So, overall the average precision and recall for each class were calculated using different methods are:

https://user-images.githubusercontent.com/73419394/258063034-98a47838-7419-4b3f-8c7f-8cab54f209e6.png
#Analysis
After applying the proposed model to all ten different classes and calculating the average precision and recall by taking random query images from the dataset, we get:

https://user-images.githubusercontent.com/73419394/258063313-c1ada15f-b881-4d3c-9cd8-d0f32f5a7ee0.png

Our model has achieved satisfactory precision by using Colour Moments and Texture features. It can be improved by taking more features into account, like shape, edges and texture features, making the feature vector more robust to differentiate between images more precisely.
