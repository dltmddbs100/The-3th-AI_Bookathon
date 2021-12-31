# This is the custom code on the server
# only can apply to MindsLap server

def top_p_tok_k_logits(logits, p, k):
 with tf.variable_scope('top_p_top_k_logits'):
  logits_sort = tf.sort(logits, direction='DESCENDING')
  probs_sort = tf.nn.softmax(logits_sort)
  indices = tf.constant(np.tile(np.arange(logits.shape[1].value), (logits.shape[0].values,1)))
  probs_sums = tf.cumsum(probs_sort, axis=-1, exclusive=True)
  
  logits_masked = tf.where((probs_sums < p) & (indeices < k), logits_sortm, tf.ones_like(logits_sort)*1000)
  min_logits = tf.reduce_min(logits_masked, axis=1, keepdims=True)
  
  return tf.where(
   logits < min_logits,
   tf.ones_like(logits, dtype=logits.dtype) * -1e10,
   logits
  )