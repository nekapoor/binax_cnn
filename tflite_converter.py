"""
	tflite_converter.py
	cnn_malaria

	Created by Ben (benkim96@gmail.com) on 11/22/19.
	Description:
            script converts model.h5 file to a model.tflite file
            dependency:
                tensorflow==2.0
"""
import tensorflow as tf

model = tf.keras.models.load_model('model.h5')
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tfmodel = converter.convert()
open ("model.tflite" , "wb") .write(tfmodel)
