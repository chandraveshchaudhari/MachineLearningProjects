"""
Usage:

!python Generate_tfrecord.py --comma_input=/home/chaudharyubuntu/Desktop/2/annotation.csv --picture_dir=/home/chaudharyubuntu/Desktop/2/new_train_pics  --Outtf_path=/home/chaudharyubuntu/Desktop/2/tfrecord/train.tfrecord


!python Generate_tfrecord.py --comma_input=/home/chaudharyubuntu/Desktop/2/VALannotation.csv --picture_dir=/home/chaudharyubuntu/Desktop/2/new_val_pic/  --Outtf_path=/home/chaudharyubuntu/Desktop/2/tfrecord/val.tfrecord
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import pandas as pd
import tensorflow as tf

from PIL import Image
#from utils import dataset_util
from collections import namedtuple, OrderedDict

from absl import app
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_string('comma_input', '', 'Path to the CSV input')
flags.DEFINE_string('Outtf_path', '', 'Path to output TFRecord')
flags.DEFINE_string('picture_dir', '', 'Path to images')


# TO-DO replace this with label map
def class_text_to_int(row_label):
    if row_label == 'lavesh':
        return 1
    if row_label == 'chandravesh':
        return 2
    if row_label == 'prashant':
        return 3
    if row_label == 'nagendra':
        return 0
    else:
        pass


def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]

# The following functions can be used to convert a value to a type compatible
# with tf.Example.

def bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def int64_list_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))

def create_tf_example(group, path):
    with tf.io.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)

    filename = group.filename.encode('utf8')
    classes = []
    
    for index, row in group.object.iterrows():
        classes.append(class_text_to_int(row['label']))
        
    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/filename':  bytes_feature(filename),
        'image/encoded':  bytes_feature(encoded_jpg),
        'image/object/class/label':  int64_list_feature(classes),
    }))
    return tf_example


def main(_):
    writer = tf.io.TFRecordWriter(FLAGS.Outtf_path)
    path = os.path.join(FLAGS.picture_dir)
    examples = pd.read_csv(FLAGS.comma_input)
    grouped = split(examples, 'filename')
    for group in grouped:
        tf_example = create_tf_example(group, path)
        writer.write(tf_example.SerializeToString())

    writer.close()
    output_path = os.path.join(os.getcwd(), FLAGS.Outtf_path)
    print('Successfully created the TFRecords: {}'.format(FLAGS.Outtf_path))


if __name__ == '__main__':
    app.run(main)