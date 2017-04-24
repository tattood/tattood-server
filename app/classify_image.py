from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os.path
import re
# import functools

import numpy as np
from PIL import Image
import tensorflow as tf


# pylint: disable=line-too-long
# pylint: enable=line-too-long


class NodeLookup(object):
    def __init__(self):
        label_lookup_path = os.path.join('models', 'imagenet_2012_challenge_label_map_proto.pbtxt')
        uid_lookup_path = os.path.join('models', 'imagenet_synset_to_human_label_map.txt')
        self.node_lookup = self.load(label_lookup_path, uid_lookup_path)

    def load(self, label_lookup_path, uid_lookup_path):
        proto_as_ascii_lines = tf.gfile.GFile(uid_lookup_path).readlines()
        uid_to_human = {}
        p = re.compile(r'[n\d]*[ \S,]*')
        for line in proto_as_ascii_lines:
            parsed_items = p.findall(line)
            uid = parsed_items[0]
            human_string = parsed_items[2]
            uid_to_human[uid] = human_string
        node_id_to_uid = {}
        proto_as_ascii = tf.gfile.GFile(label_lookup_path).readlines()
        for line in proto_as_ascii:
            if line.startswith('  target_class:'):
                target_class = int(line.split(': ')[1])
            if line.startswith('  target_class_string:'):
                target_class_string = line.split(': ')[1]
                node_id_to_uid[target_class] = target_class_string[1:-2]
        # Loads the final mapping of integer node ID to human-readable string
        node_id_to_name = {}
        for key, val in node_id_to_uid.items():
            name = uid_to_human[val]
            node_id_to_name[key] = name
        return node_id_to_name

    def id_to_string(self, node_id):
        if node_id not in self.node_lookup:
            return ''
        return self.node_lookup[node_id]


def create_graph():
    with tf.gfile.FastGFile(os.path.join('models', 'classify_image_graph_def.pb'), 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def classify(image, *, N=5, threshold=0.1):
    image = Image.open(image)
    image_data = np.array(image)[:, :, 0:3]  # Select RGB channels only.
    node_lookup = NodeLookup()
    create_graph()
    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
        predictions = sess.run(softmax_tensor, {'DecodeJpeg:0': image_data})
        predictions = np.squeeze(predictions)
        top_k = predictions.argsort()[-N:][::-1]
        for node in top_k:
            print("{}:{}".format(node_lookup.id_to_string(node), predictions[node]))
        top_k = filter(lambda x: predictions[x] >= threshold, top_k)
        return [node_lookup.id_to_string(node_id) for node_id in top_k]
