import tensorflow as tf

# https://blog.csdn.net/thriving_fcl/article/details/75213361
sess = tf.Session(graph=tf.Graph())
meta_graph = tf.saved_model.loader.load(sess,[tf.saved_model.tag_constants.SERVING],'export_ext')

input = sess.graph.get_tensor_by_name(
    meta_graph.signature_def['Infer'].inputs["inputs"].name)

infer_method = sess.graph.get_tensor_by_name(
    meta_graph.signature_def['Infer'].outputs["outputs"].name)

def infer(_input):
    return sess.run(infer_method, feed_dict={input:_input})