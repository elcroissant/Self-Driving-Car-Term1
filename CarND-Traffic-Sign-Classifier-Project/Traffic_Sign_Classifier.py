
# coding: utf-8

# # Self-Driving Car Engineer Nanodegree
# 
# ## Deep Learning
# 
# ## Project: Build a Traffic Sign Recognition Classifier
# 
# In this notebook, a template is provided for you to implement your functionality in stages, which is required to successfully complete this project. If additional code is required that cannot be included in the notebook, be sure that the Python code is successfully imported and included in your submission if necessary. 
# 
# > **Note**: Once you have completed all of the code implementations, you need to finalize your work by exporting the iPython Notebook as an HTML document. Before exporting the notebook to html, all of the code cells need to have been run so that reviewers can see the final implementation and output. You can then export the notebook by using the menu above and navigating to  \n",
#     "**File -> Download as -> HTML (.html)**. Include the finished document along with this notebook as your submission. 
# 
# In addition to implementing code, there is a writeup to complete. The writeup should be completed in a separate file, which can be either a markdown file or a pdf document. There is a [write up template](https://github.com/udacity/CarND-Traffic-Sign-Classifier-Project/blob/master/writeup_template.md) that can be used to guide the writing process. Completing the code template and writeup template will cover all of the [rubric points](https://review.udacity.com/#!/rubrics/481/view) for this project.
# 
# The [rubric](https://review.udacity.com/#!/rubrics/481/view) contains "Stand Out Suggestions" for enhancing the project beyond the minimum requirements. The stand out suggestions are optional. If you decide to pursue the "stand out suggestions", you can include the code in this Ipython notebook and also discuss the results in the writeup file.
# 
# 
# >**Note:** Code and Markdown cells can be executed using the **Shift + Enter** keyboard shortcut. In addition, Markdown cells can be edited by typically double-clicking the cell to enter edit mode.

# ---
# ## Step 0: Load The Data

# In[1]:

# Load pickled data
import pickle

# TODO: Fill this in based on where you saved the training and testing data

training_file = 'train.p'
validation_file= 'valid.p'
testing_file = 'test.p'

with open(training_file, mode='rb') as f:
    train = pickle.load(f)
with open(validation_file, mode='rb') as f:
    valid = pickle.load(f)
with open(testing_file, mode='rb') as f:
    test = pickle.load(f)
    
X_train_un, y_train = train['features'], train['labels']
X_valid_un, y_valid = valid['features'], valid['labels']
X_test_un, y_test = test['features'], test['labels']


# ---
# 
# ## Step 1: Dataset Summary & Exploration
# 
# The pickled data is a dictionary with 4 key/value pairs:
# 
# - `'features'` is a 4D array containing raw pixel data of the traffic sign images, (num examples, width, height, channels).
# - `'labels'` is a 1D array containing the label/class id of the traffic sign. The file `signnames.csv` contains id -> name mappings for each id.
# - `'sizes'` is a list containing tuples, (width, height) representing the original width and height the image.
# - `'coords'` is a list containing tuples, (x1, y1, x2, y2) representing coordinates of a bounding box around the sign in the image. **THESE COORDINATES ASSUME THE ORIGINAL IMAGE. THE PICKLED DATA CONTAINS RESIZED VERSIONS (32 by 32) OF THESE IMAGES**
# 
# Complete the basic data summary below. Use python, numpy and/or pandas methods to calculate the data summary rather than hard coding the results. For example, the [pandas shape method](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.shape.html) might be useful for calculating some of the summary results. 

# ### Provide a Basic Summary of the Data Set Using Python, Numpy and/or Pandas

# In[2]:

### Replace each question mark with the appropriate value. 
### Use python, pandas or numpy methods rather than hard coding the results
import numpy as np

# TODO: Number of training examples
n_train = X_train_un.shape[0]

# TODO: Number of validation examples
n_validation = X_valid_un.shape[0]

# TODO: Number of testing examples.
n_test = X_test_un.shape[0]

# TODO: What's the shape of an traffic sign image?
image_shape = X_train_un.shape[1:4]

# TODO: How many unique classes/labels there are in the dataset.
n_classes = np.unique(y_train).size

#len(set(y_train))


print("Number of training examples =", n_train)
print("Number of validation examples =", n_validation)
print("Number of testing examples =", n_test)
print("Image data shape =", image_shape)
print("Number of classes =", n_classes)


# ### Include an exploratory visualization of the dataset

# Visualize the German Traffic Signs Dataset using the pickled file(s). This is open ended, suggestions include: plotting traffic sign images, plotting the count of each sign, etc. 
# 
# The [Matplotlib](http://matplotlib.org/) [examples](http://matplotlib.org/examples/index.html) and [gallery](http://matplotlib.org/gallery.html) pages are a great resource for doing visualizations in Python.
# 
# **NOTE:** It's recommended you start with something simple first. If you wish to do more, come back to it after you've completed the rest of the sections. It can be interesting to look at the distribution of classes in the training, validation and test set. Is the distribution the same? Are there more examples of some classes than others?

# In[3]:

### Data exploration visualization code goes here.
### Feel free to use as many code cells as needed.
import matplotlib.pyplot as plt
# Visualizations will be shown in the notebook.
#get_ipython().magic('matplotlib inline')

import numpy as np
from scipy import stats

y_train_dist = sorted(y_train)  
y_valid_dist = sorted(y_valid)  
y_test_dist = sorted(y_test)  


y_train_fit = stats.norm.pdf(y_train_dist, np.mean(y_train_dist), np.std(y_train_dist))
y_valid_fit = stats.norm.pdf(y_valid_dist, np.mean(y_valid_dist), np.std(y_valid_dist))
y_test_fit = stats.norm.pdf(y_test_dist, np.mean(y_test_dist), np.std(y_test_dist))


#plt.subplot(3, 1, 1)
#plt.plot(y_train_dist,y_train_fit,'ko-')
#plt.hist(y_train_dist,normed=True)      #use this to draw histogram of your data
#plt.title('German Traffic Signs Dataset')
#plt.ylabel('Training set')
#
#plt.subplot(3, 1, 2)
#plt.plot(y_valid_dist,y_valid_fit,'ko-')
#plt.hist(y_valid_dist,normed=True)      #use this to draw histogram of your data
#plt.ylabel('Validation set')
#
#plt.subplot(3, 1, 3)
#plt.plot(y_test_dist,y_test_fit,'ko-')
#plt.hist(y_test_dist, normed=True)     #use this to draw histogram of your data
#plt.xlabel('Classes')
#plt.ylabel('Test set')
#
#
#plt.show()
#
#
## ----
# 
# ## Step 2: Design and Test a Model Architecture
# 
# Design and implement a deep learning model that learns to recognize traffic signs. Train and test your model on the [German Traffic Sign Dataset](http://benchmark.ini.rub.de/?section=gtsrb&subsection=dataset).
# 
# The LeNet-5 implementation shown in the [classroom](https://classroom.udacity.com/nanodegrees/nd013/parts/fbf77062-5703-404e-b60c-95b78b2f3f9e/modules/6df7ae49-c61c-4bb2-a23e-6527e69209ec/lessons/601ae704-1035-4287-8b11-e2c2716217ad/concepts/d4aca031-508f-4e0b-b493-e7b706120f81) at the end of the CNN lesson is a solid starting point. You'll have to change the number of classes and possibly the preprocessing, but aside from that it's plug and play! 
# 
# With the LeNet-5 solution from the lecture, you should expect a validation set accuracy of about 0.89. To meet specifications, the validation set accuracy will need to be at least 0.93. It is possible to get an even higher accuracy, but 0.93 is the minimum for a successful project submission. 
# 
# There are various aspects to consider when thinking about this problem:
# 
# - Neural network architecture (is the network over or underfitting?)
# - Play around preprocessing techniques (normalization, rgb to grayscale, etc)
# - Number of examples per label (some have more than others).
# - Generate fake data.
# 
# Here is an example of a [published baseline model on this problem](http://yann.lecun.com/exdb/publis/pdf/sermanet-ijcnn-11.pdf). It's not required to be familiar with the approach used in the paper but, it's good practice to try to read papers like these.

# ### Pre-process the Data Set (normalization, grayscale, etc.)

# Minimally, the image data should be normalized so that the data has mean zero and equal variance. For image data, `(pixel - 128)/ 128` is a quick way to approximately normalize the data and can be used in this project. 
# 
# Other pre-processing steps are optional. You can try different techniques to see if it improves performance. 
# 
# Use the code cell (or multiple code cells, if necessary) to implement the first step of your project.

# In[4]:

import cv2
def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

def normalize(data):
    const = 128
    image = data.astype(np.float)
    image = (image - const) / const
    #np.reshape(image, (32,32,1))
    #cv2.normalize(image, dst, alpha=-1, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)     
    return image

def preprocess(data):
    preprocessed_data = []
    dst = np.zeros(shape=(32,32,3))
    const = 128
    for image in data:
        image = grayscale(image)
        image = normalize(image)
        
        preprocessed_data.append(image)
    return np.array(preprocessed_data)


# In[5]:

### Preprocess the data here. It is required to normalize the data. Other preprocessing steps could include 
### converting to grayscale, etc.
### Feel free to use as many code cells as needed.

from sklearn.utils import shuffle
X_train_un, y_train = shuffle(X_train_un, y_train)

#print (X_train[0])
#X_train_norm = stats.norm.pdf(X_train[0], np.mean(X_train[0]), np.std(X_train[0]))
#print (X_train_norm)
#X_train = stats.norm.pdf(X_train, np.mean(X_train), np.std(X_train))

import random
import numpy as np
import matplotlib.pyplot as plt
from numpy import newaxis
#get_ipython().magic('matplotlib inline')

X_train = preprocess(X_train_un)
X_train = X_train[..., newaxis]

X_valid = preprocess(X_valid_un)
X_valid = X_valid[..., newaxis]

X_test = preprocess(X_test_un)
X_test = X_test[..., newaxis]

#print (X_train_un[0].shape, X_train_un[0].dtype, type(X_train_un[0]))

index = random.randint(0, len(X_train))

image = X_train[index].squeeze()
image2 = X_train_un[index].squeeze()

#plt.figure(figsize=(1,1))
#plt.imshow(image, cmap='gray')

#plt.figure(figsize=(1,2))
#plt.imshow(image2, cmap='gray')

print(y_train[index])


# ### Model Architecture

# In[6]:

### Define your architecture here.
### Feel free to use as many code cells as needed.
import tensorflow as tf

EPOCHS = 30
BATCH_SIZE = 64

from tensorflow.contrib.layers import flatten

def MyNet(x):    
    # Arguments used for tf.truncated_normal, randomly defines variables for the weights and biases for each layer
    mu = 0
    sigma = 0.1
    
    ch_conv1 = 64
    # SOLUTION: Layer 1: Convolutional. Input = 32x32x1. Output = 28x28x6.
    conv1_W = tf.Variable(tf.truncated_normal(shape=(3, 3, 1, ch_conv1), mean = mu, stddev = sigma))
    conv1_b = tf.Variable(tf.zeros(ch_conv1))
    conv1   = tf.nn.conv2d(x, conv1_W, strides=[1, 1, 1, 1], padding='VALID') + conv1_b

    # SOLUTION: Activation.
    conv1 = tf.nn.relu(conv1)
    
    #conv1 = tf.nn.dropout(conv1, keep_prob)

    # SOLUTION: Pooling. Input = 28x28x6. Output = 14x14x6.
    conv1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='VALID')

    # SOLUTION: Layer 2: Convolutional. Output = 10x10x16.
    ch_conv2 = 64
    conv2_W = tf.Variable(tf.truncated_normal(shape=(3, 3, ch_conv1, ch_conv2), mean = mu, stddev = sigma))
    conv2_b = tf.Variable(tf.zeros(ch_conv2))
    conv2   = tf.nn.conv2d(conv1, conv2_W, strides=[1, 1, 1, 1], padding='VALID') + conv2_b
    
    # SOLUTION: Activation.
    conv2 = tf.nn.relu(conv2)
    #conv2 = tf.nn.dropout(conv2, keep_prob)

    # SOLUTION: Pooling. Input = 10x10x16. Output = 5x5x16.
    conv2 = tf.nn.max_pool(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='VALID')

    
    ch_conv3 = 64
    conv3_W = tf.Variable(tf.truncated_normal(shape=(3, 3, ch_conv2, ch_conv3), mean = mu, stddev = sigma))
    conv3_b = tf.Variable(tf.zeros(ch_conv3))
    conv3   = tf.nn.conv2d(conv2, conv3_W, strides=[1, 1, 1, 1], padding='VALID') + conv3_b
    
    # SOLUTION: Activation.
    conv3 = tf.nn.relu(conv3)
    
    
    # SOLUTION: Flatten. Input = 5x5x16. Output = 400.
    fc0   = flatten(conv3)
    
    # SOLUTION: Layer 3: Fully Connected. Input = 400. Output = 120.
    fc1_W = tf.Variable(tf.truncated_normal(shape=(1024, 120), mean = mu, stddev = sigma))
    fc1_b = tf.Variable(tf.zeros(120))
    fc1   = tf.matmul(fc0, fc1_W) + fc1_b
    
    # SOLUTION: Activation.
    fc1    = tf.nn.relu(fc1)
    fc1    = tf.nn.dropout(fc1, keep_prob)


    # SOLUTION: Layer 4: Fully Connected. Input = 120. Output = 84.
    fc2_W  = tf.Variable(tf.truncated_normal(shape=(120, 84), mean = mu, stddev = sigma))
    fc2_b  = tf.Variable(tf.zeros(84))
    fc2    = tf.matmul(fc1, fc2_W) + fc2_b
    
    # SOLUTION: Activation.
    fc2    = tf.nn.relu(fc2)
    fc2    = tf.nn.dropout(fc2, keep_prob)

    # SOLUTION: Layer 5: Fully Connected. Input = 84. Output = 10.
    fc3_W  = tf.Variable(tf.truncated_normal(shape=(84, 43), mean = mu, stddev = sigma))
    fc3_b  = tf.Variable(tf.zeros(43))
    logits = tf.matmul(fc2, fc3_W) + fc3_b
    
    return logits


# ### Train, Validate and Test the Model

# A validation set can be used to assess how well the model is performing. A low accuracy on the training and validation
# sets imply underfitting. A high accuracy on the training set but low accuracy on the validation set implies overfitting.

# In[7]:

### Train your model here.
### Calculate and report the accuracy on the training and validation set.
### Once a final model architecture is selected, 
### the accuracy on the test set should be calculated and reported as well.
### Feel free to use as many code cells as needed.

## Features and Labels
## Train LeNet to classify German traffic signs data.
## x is a placeholder for a batch of input images. y is a placeholder for a batch of output labels.

x = tf.placeholder(tf.float32, (None, 32, 32, 1))
y = tf.placeholder(tf.int32, (None))
keep_prob = tf.placeholder(tf.float32)
one_hot_y = tf.one_hot(y, 43)


# In[8]:

rate = 0.001

logits = MyNet(x)
cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels=one_hot_y, logits=logits)
loss_operation = tf.reduce_mean(cross_entropy)
optimizer = tf.train.AdamOptimizer(learning_rate = rate)
training_operation = optimizer.minimize(loss_operation)


# In[9]:

###Model Evaluation
#Evaluate how well the loss and accuracy of the model for a given dataset.

#You do not need to modify this section.

correct_prediction = tf.equal(tf.argmax(logits, 1), tf.argmax(one_hot_y, 1))
accuracy_operation = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
saver = tf.train.Saver()

def evaluate(X_data, y_data):
    num_examples = len(X_data)
    total_accuracy = 0
    sess = tf.get_default_session()
    for offset in range(0, num_examples, BATCH_SIZE):
        batch_x, batch_y = X_data[offset:offset+BATCH_SIZE], y_data[offset:offset+BATCH_SIZE]
        accuracy = sess.run(accuracy_operation, feed_dict={x: batch_x, y: batch_y, keep_prob : 1.0})
        total_accuracy += (accuracy * len(batch_x))
    return total_accuracy / num_examples


# In[10]:

### Train the Model
# Run the training data through the training pipeline to train the model.
# Before each epoch, shuffle the training set.
# After each epoch, measure the loss and accuracy of the validation set.
# Save the model after training.
# You do not need to modify this section.

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    num_examples = len(X_train)
    
    print("Training...")
    print()
    for i in range(EPOCHS):
        X_train, y_train = shuffle(X_train, y_train)
        #print (num_examples)
        for offset in range(0, num_examples, BATCH_SIZE):
            #print ("Offset: ", offset)
            end = offset + BATCH_SIZE
            batch_x, batch_y = X_train[offset:end], y_train[offset:end]
            sess.run(training_operation, feed_dict={x: batch_x, y: batch_y, keep_prob : 0.75})
            
        validation_accuracy = evaluate(X_valid, y_valid)
        print("EPOCH {} ...".format(i+1))
        print("Validation Accuracy = {:.3f}".format(validation_accuracy))
        print()
        
    saver.save(sess, './mynet')
    print("Model saved")


# In[11]:

### Evaluate the Model
# Once you are completely satisfied with your model, evaluate the performance of the model on the test set.
# Be sure to only do this once!
# If you were to measure the performance of your trained model on the test set, then improve your model, and then measure the performance of your model on the test set again, that would invalidate your test results. You wouldn't get a true measure of how well your model would perform against real data.
# You do not need to modify this section.

with tf.Session() as sess:
    saver.restore(sess, tf.train.latest_checkpoint('.'))

    test_accuracy = evaluate(X_test, y_test)
    print("Test Accuracy = {:.3f}".format(test_accuracy))


# ---
# 
# ## Step 3: Test a Model on New Images
# 
# To give yourself more insight into how your model is working, download at least five pictures of German traffic signs from the web and use your model to predict the traffic sign type.
# 
# You may find `signnames.csv` useful as it contains mappings from the class id (integer) to the actual sign name.

# ### Load and Output the Images

# In[12]:

#get_ipython().magic('pylab inline')
#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg
#import os
#
#path = 'examples/TrafficSigns/'
#list_of_files = os.listdir(path)
#
#list_of_path_to_files = []
#for file_name in list_of_files:
#    #TODO: remove 002.png file as it has different shape
#    #if file_name != '002.png':
#    path_to_file = path + file_name
#    list_of_path_to_files.append(path_to_file)
#
#images = []
#images_to_display = []
#horiz_figure = figure()
#number_of_files = len(list_of_path_to_files)
#for index, path in enumerate(list_of_path_to_files):
#    horiz_figure.add_subplot(1,number_of_files,index+1)
#    image = cv2.imread(list_of_path_to_files[index],0)
#    images_to_display.append(image)
#    imshow(image,cmap='gray')
#    axis('off')
#    img = cv2.resize(image, (32, 32))
#    img = normalize(img)
#    img = np.expand_dims(img, axis=3)
#    #print (img.shape)
#    images.append(img)
#
#
## ### Predict the Sign Type for Each Image
#
## In[13]:
#
#### Run the predictions here and use the model to output the prediction for each image.
#### Make sure to pre-process the images with the same pre-processing pipeline used earlier.
#### Feel free to use as many code cells as needed.
##import matplotlib.pyplot as plt
## Visualizations will be shown in the notebook.
##%matplotlib inline
#
#import csv
#
#with tf.Session() as sess:
#    saver.restore(sess, tf.train.latest_checkpoint('.'))
#    results = sess.run(logits, feed_dict={x: images, keep_prob : 1.0})
#    predictions = np.argmax(np.array(results),axis=1)
#    #print (predictions)
#    signanames = open('signnames.csv', 'r')
#    reader = csv.reader(signanames)
#    sign_dict = dict(reader)
#    
#    fig, axs = plt.subplots(nrows=5, sharex=False, figsize=(2, 10))
#    
#    for index, dict_index in enumerate(predictions):
#        axs[index].set_title(sign_dict[str(dict_index)])
#        axs[index].imshow(images_to_display[index])
#    plt.gray()
#    #    image = images_to_display[index]
#        #plt.figure(figsize=(1,index))
#    #    plt.imshow(image, cmap='gray')
#    #    imshow(image, cmap='gray')
#    #    print (sign_dict[str(dict_index)])
#        
#
#
## ### Analyze Performance
#
## In[30]:
#
#### Calculate the accuracy for these 5 new images. 
#### For example, if the model predicted 1 out of 5 signs correctly, it's 20% accurate on these new images.
#target = [16, 33, 11, 38, 1]
#print ("Accuracy: ", np.sum(target==predictions)/len(target)*100,"%")
#
#
#
#
## ### Output Top 5 Softmax Probabilities For Each Image Found on the Web
#
## For each of the new images, print out the model's softmax probabilities to show the **certainty** of the model's predictions (limit the output to the top 5 probabilities for each image). [`tf.nn.top_k`](https://www.tensorflow.org/versions/r0.12/api_docs/python/nn.html#top_k) could prove helpful here. 
## 
## The example below demonstrates how tf.nn.top_k can be used to find the top k predictions for each image.
## 
## `tf.nn.top_k` will return the values and indices (class ids) of the top k predictions. So if k=3, for each sign, it'll return the 3 largest probabilities (out of a possible 43) and the correspoding class ids.
## 
## Take this numpy array as an example. The values in the array represent predictions. The array contains softmax probabilities for five candidate images with six possible classes. `tk.nn.top_k` is used to choose the three classes with the highest probability:
## 
## ```
## # (5, 6) array
## a = np.array([[ 0.24879643,  0.07032244,  0.12641572,  0.34763842,  0.07893497,
##          0.12789202],
##        [ 0.28086119,  0.27569815,  0.08594638,  0.0178669 ,  0.18063401,
##          0.15899337],
##        [ 0.26076848,  0.23664738,  0.08020603,  0.07001922,  0.1134371 ,
##          0.23892179],
##        [ 0.11943333,  0.29198961,  0.02605103,  0.26234032,  0.1351348 ,
##          0.16505091],
##        [ 0.09561176,  0.34396535,  0.0643941 ,  0.16240774,  0.24206137,
##          0.09155967]])
## ```
## 
## Running it through `sess.run(tf.nn.top_k(tf.constant(a), k=3))` produces:
## 
## ```
## TopKV2(values=array([[ 0.34763842,  0.24879643,  0.12789202],
##        [ 0.28086119,  0.27569815,  0.18063401],
##        [ 0.26076848,  0.23892179,  0.23664738],
##        [ 0.29198961,  0.26234032,  0.16505091],
##        [ 0.34396535,  0.24206137,  0.16240774]]), indices=array([[3, 0, 5],
##        [0, 1, 4],
##        [0, 5, 1],
##        [1, 3, 5],
##        [1, 4, 3]], dtype=int32))
## ```
## 
## Looking just at the first row we get `[ 0.34763842,  0.24879643,  0.12789202]`, you can confirm these are the 3 largest probabilities in `a`. You'll also notice `[3, 0, 5]` are the corresponding indices.
#
## In[82]:
#
#### Print out the top five softmax probabilities for the predictions on the German traffic sign images found on the web. 
#### Feel free to use as many code cells as needed.
#
#with tf.Session() as sess:
#    output = sess.run(tf.nn.top_k(tf.constant(results), k=5))
#    print ("Softmax probabilities:")
#    print (output.values)
#    print ("Predictions:")
#    print (output.indices)
#
#    signanames = open('signnames.csv', 'r')
#    reader = csv.reader(signanames)
#    sign_dict = dict(reader)
#
#    horiz_figure = figure()
#    
#    fig, axs = plt.subplots(nrows=5, ncols = 5, sharex=False, figsize=(6, 10))
#    
#    print ('Similarity:')
#    for plt_y_index, indices in enumerate(output.indices):
#        #print ([sign_dict[str(dict_index)] for dict_index in indices])
#        # take first element from each classes which were within top5 
#        for plt_x_index, sign_index in enumerate(indices):
#            image = X_train[y_train==sign_index][0].squeeze()
#            #axs[plt_y_index,plt_x_index].set_title(sign_dict[str(indices[0])])
#            axs[plt_y_index,plt_x_index].imshow(image, cmap='gray')
#    plt.gray()
#
#
## ### Project Writeup
## 
## Once you have completed the code implementation, document your results in a project writeup using this [template](https://github.com/udacity/CarND-Traffic-Sign-Classifier-Project/blob/master/writeup_template.md) as a guide. The writeup can be in a markdown or pdf file. 
#
## > **Note**: Once you have completed all of the code implementations and successfully answered each question above, you may finalize your work by exporting the iPython Notebook as an HTML document. You can do this by using the menu above and navigating to  \n",
##     "**File -> Download as -> HTML (.html)**. Include the finished document along with this notebook as your submission.
#
## ---
## 
## ## Step 4 (Optional): Visualize the Neural Network's State with Test Images
## 
##  This Section is not required to complete but acts as an additional excersise for understaning the output of a neural network's weights. While neural networks can be a great learning device they are often referred to as a black box. We can understand what the weights of a neural network look like better by plotting their feature maps. After successfully training your neural network you can see what it's feature maps look like by plotting the output of the network's weight layers in response to a test stimuli image. From these plotted feature maps, it's possible to see what characteristics of an image the network finds interesting. For a sign, maybe the inner network feature maps react with high activation to the sign's boundary outline or to the contrast in the sign's painted symbol.
## 
##  Provided for you below is the function code that allows you to get the visualization output of any tensorflow weight layer you want. The inputs to the function should be a stimuli image, one used during training or a new one you provided, and then the tensorflow variable name that represents the layer's state during the training process, for instance if you wanted to see what the [LeNet lab's](https://classroom.udacity.com/nanodegrees/nd013/parts/fbf77062-5703-404e-b60c-95b78b2f3f9e/modules/6df7ae49-c61c-4bb2-a23e-6527e69209ec/lessons/601ae704-1035-4287-8b11-e2c2716217ad/concepts/d4aca031-508f-4e0b-b493-e7b706120f81) feature maps looked like for it's second convolutional layer you could enter conv2 as the tf_activation variable.
## 
## For an example of what feature map outputs look like, check out NVIDIA's results in their paper [End-to-End Deep Learning for Self-Driving Cars](https://devblogs.nvidia.com/parallelforall/deep-learning-self-driving-cars/) in the section Visualization of internal CNN State. NVIDIA was able to show that their network's inner weights had high activations to road boundary lines by comparing feature maps from an image with a clear path to one without. Try experimenting with a similar test to show that your trained network's weights are looking for interesting features, whether it's looking at differences in feature maps from images with or without a sign, or even what feature maps look like in a trained network vs a completely untrained one on the same sign image.
## 
## <figure>
##  <img src="visualize_cnn.png" width="380" alt="Combined Image" />
##  <figcaption>
##  <p></p> 
##  <p style="text-align: center;"> Your output should look something like this (above)</p> 
##  </figcaption>
## </figure>
##  <p></p> 
## 
#
## In[ ]:
#
#### Visualize your network's feature maps here.
#### Feel free to use as many code cells as needed.
#
## image_input: the test image being fed into the network to produce the feature maps
## tf_activation: should be a tf variable name used during your training procedure that represents the calculated state of a specific weight layer
## activation_min/max: can be used to view the activation contrast in more detail, by default matplot sets min and max to the actual min and max values of the output
## plt_num: used to plot out multiple different weight feature map sets on the same block, just extend the plt number for each new feature map entry
#
#def outputFeatureMap(image_input, tf_activation, activation_min=-1, activation_max=-1 ,plt_num=1):
#    # Here make sure to preprocess your image_input in a way your network expects
#    # with size, normalization, ect if needed
#    # image_input =
#    # Note: x should be the same name as your network's tensorflow data placeholder variable
#    # If you get an error tf_activation is not defined it may be having trouble accessing the variable from inside a function
#    activation = tf_activation.eval(session=sess,feed_dict={x : image_input})
#    featuremaps = activation.shape[3]
#    plt.figure(plt_num, figsize=(15,15))
#    for featuremap in range(featuremaps):
#        plt.subplot(6,8, featuremap+1) # sets the number of feature maps to show on each row and column
#        plt.title('FeatureMap ' + str(featuremap)) # displays the feature map number
#        if activation_min != -1 & activation_max != -1:
#            plt.imshow(activation[0,:,:, featuremap], interpolation="nearest", vmin =activation_min, vmax=activation_max, cmap="gray")
#        elif activation_max != -1:
#            plt.imshow(activation[0,:,:, featuremap], interpolation="nearest", vmax=activation_max, cmap="gray")
#        elif activation_min !=-1:
#            plt.imshow(activation[0,:,:, featuremap], interpolation="nearest", vmin=activation_min, cmap="gray")
#        else:
#            plt.imshow(activation[0,:,:, featuremap], interpolation="nearest", cmap="gray")
#
