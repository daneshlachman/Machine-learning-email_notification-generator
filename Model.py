import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np
import pandas as pd
import tensorflow as tensorflow
from tensorflow import feature_column
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split

PAD_NAAR_CSV = r"C:\Users\Danesh\Dropbox\HBO\JAAR 4\Afstudeerstage NiVo\Scriptiedocument\PoC\simulated_training_dataset.csv"

data_frame = pd.read_csv(PAD_NAAR_CSV)

train, test = train_test_split(data_frame, test_size=0.2)
train, validation = train_test_split(train, test_size=0.2)


# functie om Pandas DataFrame om te zetten naar tensorflow dataset
def df_naar_tensorflow_dataset(dataframe, shuffle=True, batch_size=32):
  dataframe = dataframe.copy()
  labels = dataframe.pop('Reden_van_uitval')
  dataset = tensorflow.data.Dataset.from_tensor_slices((dict(dataframe), labels))
  if shuffle:
    dataset = dataset.shuffle(buffer_size=len(dataframe))
  dataset = dataset.batch(batch_size)
  return dataset

feature_columns = []

# definiëren van de columns "firewall_is_uitgevallen" en "Hoeveelheid_aps_waar_rssi_laag_is" als numeric column
for header in ['firewall_is_uitgevallen', 'Hoeveelheid_aps_waar_rssi_laag_is']:
  feature_columns.append(feature_column.numeric_column(header))

# definiëren van de bucketized column "aantal_aps_die_uitvalt"
uitval_aps = feature_column.numeric_column('aantal_aps_die_uitvalt')
uitval_ap_buckets = feature_column.bucketized_column(uitval_aps, boundaries=[10, 70])
feature_columns.append(uitval_ap_buckets)

# definiëren van een feature layer om later als input te gebruiken bij het creëren van het model
feature_layer = tensorflow.keras.layers.DenseFeatures(feature_columns)

# definiëren van een training, validatie en testing dataset
batch_size = 32
training_dataset = df_naar_tensorflow_dataset(train, batch_size=batch_size)
validation_dataset = df_naar_tensorflow_dataset(validation, shuffle=False, batch_size=batch_size)
testing_dataset = df_naar_tensorflow_dataset(test, shuffle=False, batch_size=batch_size)

# configuratie van het model
model = tensorflow.keras.Sequential([
  feature_layer,
  layers.Dense(128, activation='relu'),
  layers.Dense(4)
])

# compilatie van het model
model.compile(optimizer='adam',
              loss=tensorflow.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# trainen van het model
model.fit(training_dataset,
          validation_data=validation_dataset,
          epochs=10)

# returnen van voorspelling om vervolgens email-notificatie te kunnen genereren
def return_voorspelling():
    # toevoegen van een softmax layer op het bestaande model zodat voorspellingen gedaan kunnen worden
    probability_model = tensorflow.keras.Sequential([model,
                                             tensorflow.keras.layers.Softmax()])

    voorspellingen = probability_model.predict(testing_dataset)

    return np.argmax(voorspellingen[25])