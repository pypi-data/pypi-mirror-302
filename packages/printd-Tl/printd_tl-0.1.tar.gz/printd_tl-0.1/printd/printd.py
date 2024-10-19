
def printd(experiment_number):
    if experiment_number == 1:
        experiment_code = """
# Experiment 1 Code:

!pip install opendatasets -qq

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from keras.utils import image_dataset_from_directory
from tensorflow.keras.layers import Conv2D, MaxPooling2D, BatchNormalization, Dropout, Flatten, Dense, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
import opendatasets as od

od.download('https://www.kaggle.com/datasets/hemendrasr/pizza-vs-ice-cream')

train_dir = r'/content/pizza-vs-ice-cream/dataset/train'
test_dir = r'/content/pizza-vs-ice-cream/dataset/test'
val_dir = r'/content/pizza-vs-ice-cream/dataset/valid'

train_generator = image_dataset_from_directory(train_dir, image_size=(128, 128), batch_size=32)
test_generator = image_dataset_from_directory(test_dir, image_size=(128, 128), batch_size=32)
val_generator = image_dataset_from_directory(val_dir, image_size=(128, 128), batch_size=32)

plt.figure(figsize=(10, 10))
for images, labels in val_generator:
    for i in range(9):
        ax = plt.subplot(3, 3, i + 1)
        plt.imshow(images[i].numpy().astype("uint8"))
        plt.title(int(labels[i]))
        plt.axis("off")

model = Sequential([
    Conv2D(64, (3, 3), input_shape=(128, 128, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),

    Conv2D(128, (3, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),

    Conv2D(256, (3, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),

    Conv2D(512, (3, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),

    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

model.summary()

callback = EarlyStopping(
                            monitor='val_accuracy',
                            patience=5,
                            restore_best_weights=True
                        )

logs = model.fit(
                  train_generator,
                  epochs=2,
                  validation_data=val_generator,
                  callbacks=[callback],
                )

plt.title('Training Log')
plt.plot(logs.history['loss'], label='Training Loss')
plt.plot(logs.history['accuracy'], label='Training Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Score')
plt.legend()
plt.show()

plt.title('Validation Log')
plt.plot(logs.history['val_loss'], label='Validation Loss')
plt.plot(logs.history['val_accuracy'], label='Validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Score')
plt.legend()
plt.show()

from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

model.evaluate(test_generator)

y_pred = model.predict(test_generator)
y_pred_classes = np.where(y_pred > 0.5, 1, 0)
# y_pred_classes = np.argmax(y_pred, axis=1)  # For multi-class classification
y_true = np.concatenate([y for x, y in test_generator], axis=0)

import numpy as np
y_pred_classes = np.where(y_pred > 0.5, 1, 0)
y_true = np.concatenate([y for x, y in test_generator], axis=0)

cm = confusion_matrix(y_true, y_pred_classes)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

print('Classification Report')
print(classification_report(y_true, y_pred_classes))
"""
        print(experiment_code)

    elif experiment_number == 2:
        experiment_code = """
# Experiment 2 Code:
!pip install -qq opendatasets

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from keras.models import *
from keras.layers import *
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import opendatasets as od
from tensorflow.keras import layers, models
import tensorflow_hub as hub

od.download("https://www.kaggle.com/datasets/hemendrasr/pizza-vs-ice-cream")

train_dir = '/content/pizza-vs-ice-cream/dataset/train'
test_dir = '/content/pizza-vs-ice-cream/dataset/test'

from keras.utils import image_dataset_from_directory
train_dataset = image_dataset_from_directory(train_dir, image_size=(600, 600), batch_size=32)
test_dataset = image_dataset_from_directory(test_dir, image_size=(600, 600), batch_size=32)

plt.figure(figsize=(10, 10))
for images, labels in test_dataset:
    for i in range(9):
        ax = plt.subplot(3, 3, i + 1)
        plt.imshow(images[i].numpy().astype("uint8"))
        plt.title(int(labels[i]))
        plt.axis("off")

input_shape = (600, 600, 3)

base_model = tf.keras.applications.VGG16(
    input_shape=input_shape,
    include_top=False,
    weights='imagenet'
)

base_model = tf.keras.applications.InceptionV3(
    input_shape=input_shape,
    include_top=False,
    weights='imagenet'
)

base_model = tf.keras.applications.ResNet50(
    input_shape=input_shape,
    include_top=False,
    weights='imagenet'
)

base_model.trainable = False

resnet = models.Sequential([
    base_model,
    layers.Flatten(),
    layers.Dense(512, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')
])

resnet.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

history = resnet.fit(
    train_dataset,
    validation_data=test_dataset,
    epochs=1
)

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
plt.show()

from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

resnet.evaluate(test_dataset)

y_pred = resnet.predict(test_dataset)
y_pred_classes = np.where(y_pred > 0.5, 1, 0)
# y_pred_classes = np.argmax(y_pred, axis=1)  # For multi-class classification
y_true = np.concatenate([y for x, y in test_dataset], axis=0)

cm = confusion_matrix(y_true, y_pred_classes)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

print('Classification Report')
print(classification_report(y_true, y_pred_classes))
"""
        print(experiment_code)

    elif experiment_number == 3:
        experiment_code = """
# Experiment 3 Code:
# @title See data
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']

plt.figure(figsize=(10,10))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i])
    plt.xlabel(class_names[train_labels[i][0]])
plt.show()

# ------------------------>  3a  <------------------------

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models, datasets
import matplotlib.pyplot as plt

(train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()
train_images, test_images = train_images / 255.0, test_images / 255.0

model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
    layers.MaxPooling2D((2, 2)),

    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),

    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),

    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(train_images, train_labels, epochs=1,
                    validation_data=(test_images, test_labels))

test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
print(f'Test accuracy: {test_acc}')

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import numpy as np

y_pred = model.predict(test_images)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true = np.concatenate(test_labels, axis=0)

cm = confusion_matrix(y_true, y_pred_classes)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()
# Classification Report
print('Classification Report')
print(classification_report(y_true, y_pred_classes))

# ------------------------>  3b  <------------------------

import tensorflow as tf
from tensorflow.keras import datasets, layers, models
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.models import Model
import matplotlib.pyplot as plt

(train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()
train_images, test_images = train_images / 255.0, test_images / 255.0

base_model = VGG16(weights='imagenet', include_top=False, input_shape=(32, 32, 3))

x = base_model.output
x = Flatten()(x)
x = Dense(128, activation='relu')(x)
output = Dense(10, activation='softmax')(x)
model = Model(inputs=base_model.input, outputs=output)

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(train_images, train_labels, epochs=1,
                    validation_data=(test_images, test_labels))

test_loss, test_acc = model.evaluate(test_images, test_labels)
print(f'Test accuracy: {test_acc}')

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

y_pred = model.predict(test_images)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true = np.concatenate(test_labels, axis=0)

cm = confusion_matrix(y_true, y_pred_classes)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()
# Classification Report
print('Classification Report')
print(classification_report(y_true, y_pred_classes))
"""
        print(experiment_code)

    elif experiment_number == 4:
        experiment_code = """
# Experiment 4 Code:
# ------------------------>  4 DOG BREEDS classification  <------------------------
import kagglehub
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

# Download the latest version of the dataset
path = kagglehub.dataset_download("hartman/dog-breed-identification")
print("Path to dataset files:", path)

# Load the dataset
data = pd.read_csv(f'{path}/labels.csv')
data['id'] = data['id'].apply(lambda x: x + '.jpg')

# Define image size
size = (224, 224)

# Create an ImageDataGenerator for data augmentation
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    shear_range=0.2,
    zoom_range=0.2,
    validation_split=0.3,
    fill_mode='nearest',
    horizontal_flip=True
)

# Create training and validation generators
train = datagen.flow_from_dataframe(
    data,
    directory=f'{path}/train',
    x_col='id',
    y_col='breed',
    class_mode='categorical',
    target_size=size,
    batch_size=32,
    subset='training'
)

test = datagen.flow_from_dataframe(
    data,
    directory=f'{path}/train',
    x_col='id',
    y_col='breed',
    class_mode='categorical',
    target_size=size,
    batch_size=32,
    subset='validation'
)

# Build the VGG16 model
vgg = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
vgg.trainable = False  # Freeze the VGG16 layers

# Add custom layers
model = vgg.output
model = GlobalAveragePooling2D()(model)
model = Dropout(0.2)(model)
model = Dense(512, activation='relu')(model)
pred = Dense(120, activation='softmax')(model)  # Assuming 120 breeds

# Create and compile the model
mm = tf.keras.models.Model(vgg.input, pred)
mm.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model with early stopping
er = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
his = mm.fit(train, epochs=5, validation_data=test, callbacks=[er])

# Evaluate the model on the validation data
test_steps = np.ceil(test.samples / test.batch_size)
predictions = mm.predict(test, steps=test_steps)

# Get the predicted labels and true labels
predicted_labels = np.argmax(predictions, axis=1)
true_labels = test.classes

# Generate classification report
class_report = classification_report(true_labels, predicted_labels, target_names=test.class_indices.keys())
print(class_report)

# Generate confusion matrix
cm = confusion_matrix(true_labels, predicted_labels)

# Plot the confusion matrix heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=test.class_indices.keys(), yticklabels=test.class_indices.keys())
plt.title('Confusion Matrix')
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.show()

# Visualize some training images
img, label = next(train)
fig = plt.figure(figsize=(15, 10))

for i in range(12):
    fig.add_subplot(3, 4, i + 1)
    plt.imshow(img[i])
    plt.axis('off')

plt.show()

"""
        print(experiment_code)

    elif experiment_number == 5:
        experiment_code = """
# Experiment 5 Code:
# ------------------------>  5 SENTIMENT ANALYSIS  <------------------------

import pandas as pd
import re
import string
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.corpus import stopwords
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, Bidirectional, BatchNormalization
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

# Load data
df_train = pd.read_csv('/content/train.csv')
df_test = pd.read_csv('/content/test.csv')

# Preprocess text
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    return ' '.join([word for word in text.split() if word not in stop_words])

df_train['processed_text'] = df_train['0'].apply(preprocess_text)
df_test['processed_text'] = df_test['0'].apply(preprocess_text)

# Tokenize and pad sequences
tokenizer = Tokenizer(num_words=10000, oov_token='<OOV>')
tokenizer.fit_on_texts(df_train['processed_text'])
train_pad = pad_sequences(tokenizer.texts_to_sequences(df_train['processed_text']), maxlen=200, padding='post')
test_pad = pad_sequences(tokenizer.texts_to_sequences(df_test['processed_text']), maxlen=200, padding='post')

# Build and compile the model
model = Sequential([
    Embedding(10000, 16, input_length=200),
    Bidirectional(LSTM(32, return_sequences=True)),
    BatchNormalization(),
    Bidirectional(LSTM(64)),
    Dropout(0.3),
    Dense(512, activation='relu'),
    Dropout(0.3),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(train_pad, df_train['1'], epochs=10, batch_size=64, validation_split=0.1)

# Plot training history
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.legend()
plt.show()

# Evaluate the model
predictions = (model.predict(test_pad) > 0.5).astype(int)
cm = confusion_matrix(df_test['1'], predictions)

# Display results
sns.heatmap(cm, annot=True, cmap="Blues", fmt='d')
plt.show()

# Performance metrics
accuracy = accuracy_score(df_test['1'], predictions)
precision = precision_score(df_test['1'], predictions)
recall = recall_score(df_test['1'], predictions)
f1 = f1_score(df_test['1'], predictions)

print(f"Accuracy: {accuracy:.2f}, Precision: {precision:.2f}, Recall: {recall:.2f}, F1-score: {f1:.2f}")

"""
        print(experiment_code)

    elif experiment_number == 6:
        experiment_code = """
# Experiment 6 Code:
# ------------------------>  6 IMDB data with word embedding <------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow.keras.datasets import imdb
from tensorflow.keras.layers import Embedding, Dense, LSTM, Dropout, GlobalAveragePooling1D
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from tabulate import tabulate

# Load IMDB dataset
max_features = 10000  # Maximum number of words to consider
max_len = 200  # Maximum length of each review
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=max_features)

# Pad sequences to ensure uniform input length
x_train = pad_sequences(x_train, maxlen=max_len)
x_test = pad_sequences(x_test, maxlen=max_len)

# Convert labels to categorical (for binary classification)
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

# Build the model
model = Sequential([
    Embedding(input_dim=max_features, output_dim=128, input_length=max_len),
    LSTM(128, return_sequences=True),
    Dropout(0.2),
    LSTM(64),
    Dropout(0.2),
    Dense(2, activation='softmax')  # 2 classes for binary classification
])

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

# Train the model
history = model.fit(x_train, y_train, epochs=5, batch_size=64, validation_split=0.1)

# Plot training history
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Loss Over Epochs')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Accuracy Over Epochs')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

plt.show()

# Evaluate the model
predictions = model.predict(x_test)
predicted_labels = np.argmax(predictions, axis=1)
true_labels = np.argmax(y_test, axis=1)

# Confusion matrix
cm = confusion_matrix(true_labels, predicted_labels)
plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", annot_kws={"size": 16})
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
plt.show()

# Metrics
accuracy = accuracy_score(true_labels, predicted_labels)
precision = precision_score(true_labels, predicted_labels)
recall = recall_score(true_labels, predicted_labels)
f1 = f1_score(true_labels, predicted_labels)

# Display metrics in a table
table = [
    ["Accuracy", accuracy],
    ["Precision", precision],
    ["Recall", recall],
    ["F1-score", f1]
]

print(tabulate(table, headers=["Metric", "Value"], tablefmt="fancy_grid"))

"""
        print(experiment_code)

    elif experiment_number == 7:
        experiment_code = """
# Experiment 7 Code:
# ------------------------>  7 DOC SUMMARIZATION USING TRANSFER LEARNING  <------------------------
import tensorflow as tf
import tensorflow_datasets as tfds
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import nltk

# Load IMDb dataset
imdb, info = tfds.load("imdb_reviews", with_info=True, as_supervised=True)
train_data, test_data = imdb['train'], imdb['test']

# Prepare training and testing sentences and labels
train_sentences, train_labels = [], []
for s, l in train_data:
    train_sentences.append(str(s.numpy()))
    train_labels.append(l.numpy())

test_sentences, test_labels = [], []
for s, l in test_data:
    test_sentences.append(str(s.numpy()))
    test_labels.append(l.numpy())

# Tokenize and pad sequences
vocab_size = 10000
max_length = 200
embedding_dim = 16
oov_tok = "<OOV>"

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_tok)
tokenizer.fit_on_texts(train_sentences)

train_sequences = tokenizer.texts_to_sequences(train_sentences)
train_padded = pad_sequences(train_sequences, maxlen=max_length, padding='post')

test_sequences = tokenizer.texts_to_sequences(test_sentences)
test_padded = pad_sequences(test_sequences, maxlen=max_length, padding='post')

# Convert labels to numpy arrays
train_labels = np.array(train_labels)
test_labels = np.array(test_labels)

# Build the initial model
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_length),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)),
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(24, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
num_epochs = 5
model.fit(train_padded, train_labels, epochs=num_epochs, validation_data=(test_padded, test_labels))

# Save the trained model
model.save("imdb_model.h5")

# Load and freeze the trained model for transfer learning
imdb_model = tf.keras.models.load_model("imdb_model.h5")
for layer in imdb_model.layers:
    layer.trainable = False

# Prepare new corpus for summarization
corpus = [
    "The movie had a very strong start.",
    "However, the plot quickly fell apart.",
    "The acting was top-notch, especially the lead actor.",
    "But the storyline was predictable and uninspiring.",
    "Overall, the movie had good moments but was disappointing."
]

# Tokenize the new corpus
tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(corpus)
sequences = tokenizer.texts_to_sequences(corpus)
padded_sequences = pad_sequences(sequences, maxlen=max_length, padding='post')

# Create the summarization model using transfer learning
inputs = tf.keras.Input(shape=(max_length,))
x = imdb_model(inputs)
x = tf.keras.layers.Dense(64, activation='relu')(x)
x = tf.keras.layers.Dense(32, activation='relu')(x)
outputs = tf.keras.layers.Dense(1, activation='sigmoid')(x)

summarization_model = tf.keras.Model(inputs=inputs, outputs=outputs)
summarization_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Predict sentiment scores for summarization
predictions = summarization_model.predict(padded_sequences)

# Filter sentences for summary based on threshold
threshold = 0.5  # Adjust as needed
summary = [corpus[i] for i, score in enumerate(predictions) if score > threshold]

# Display the summary
print("Summary:")
for sentence in summary:
    print(sentence)

"""
        print(experiment_code)

    elif experiment_number == 8:
        experiment_code = """
# Experiment 8 Code:
# ------------------------>  8 AUDIO CLASSIFICATION  <------------------------
# Install necessary libraries
!pip install opendatasets

# Import libraries
import pandas as pd
import numpy as np
import os
import librosa
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from keras import layers, Model
from keras.applications import VGG19
import matplotlib.pyplot as plt

# Load metadata
metadata = pd.read_csv('/content/urbansound8k/data.csv')

# Function to extract MFCC features from audio files
def mfcc_extract(file):
    waveform, sample_rate = librosa.load(file)
    mfccs = librosa.feature.mfcc(y=waveform, sr=sample_rate, n_mfcc=40)
    return np.mean(mfccs, axis=1)

# Prepare dataset
features = []
for index, row in tqdm(metadata.iterrows()):
    file_name = os.path.join('/content/urbansound8k', 'fold' + str(row['fold']), row['slice_file_name'])
    mfccs = mfcc_extract(file_name)
    features.append([mfccs, row['class']])

# Create DataFrame
features_df = pd.DataFrame(features, columns=['Features', 'Class'])
X = np.array(features_df['Features'].tolist())
Y = np.array(features_df['Class'].tolist())

# Encode labels
labelencoder = LabelEncoder()
Y = to_categorical(labelencoder.fit_transform(Y))

# Train-test split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

# Define VGG19 model for transfer learning
base_model = VGG19(weights='imagenet', include_top=False, input_shape=(40, 1, 3))  # Adjusted input shape
x = base_model.output
x = layers.Flatten()(x)
x = layers.Dense(128, activation='relu')(x)
output = layers.Dense(Y.shape[1], activation='softmax')(x)
model = Model(inputs=base_model.input, outputs=output)

# Compile the model
model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')

# Train the model
history = model.fit(X_train, Y_train, validation_data=(X_test, Y_test), epochs=10)

# Evaluate the model
test_accuracy = model.evaluate(X_test, Y_test, verbose=0)[1] * 100
print(f'Validation accuracy of model: {test_accuracy:.2f}%')

# Plot training history
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.show()

"""
        print(experiment_code)

    else:
        print("Invalid Experiment Number")
