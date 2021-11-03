import tensorflow as tf
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint

def build_model(train_directory, model_filename):
  train_datagen = ImageDataGenerator(validation_split=0.3, rescale=1./255)
  train_generator = train_datagen.flow_from_directory(train_directory, class_mode='categorical', target_size=(150, 150), batch_size=32, subset='training', follow_links=True, shuffle=True)
  validation_generator = train_datagen.flow_from_directory(train_directory, class_mode='categorical', target_size=(150, 150), batch_size=32, subset='validation', follow_links=True, shuffle=True)

  model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(len(train_generator.class_indices), activation='softmax')
  ])

  model.compile(loss='categorical_crossentropy', optimizer=tf.optimizers.Adam(), metrics=['categorical_accuracy'])

  filepath = "models/" + model_filename + ".hdf5" #change the model name after 'model-' to the zip filename
  checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
  desired_callbacks = [checkpoint]

  model.fit( train_generator, steps_per_epoch=12, epochs=8, validation_data=validation_generator, validation_steps=12, verbose=1, callbacks=desired_callbacks)

def main():
  build_model('output/modelBuilder/comicgirls/', 'comic-girls')

if __name__=="__main__":
  main()