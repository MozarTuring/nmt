from utils import misc_utils as utils
from word_split import word_split
def run_prediction(input_file_path, output_file_path):
  infile = 'input_file'
  word_split(input_file_path, infile, jieba_split)
  
  model_dir = 'jb_attention'
  hparams = utils.load_hparams(model_dir)
  hparams.inference_indices = [i for i in range(150)]
  sample_src_dataset = inference.load_data(infile)
  log_device_placement = hparams.log_device_placement
  
  if not hparams.attention:
    model_creator = nmt_model.Model
  else:
    if (hparams.encoder_type == 'gnmt' or hparams.attention_architecture in ['gnmt','gnmt_v2']):
      model_creator = gnmt_model.GNMTModel
    elif hparams.attention_architecture == 'standard':
      model_creator = attention_model.AttentionModel
    else:
      raise ValueError('Unknown attention architecture %s' % (hparams.attention_architecture))

  infer_model = model_helper.create_infer_model(model_creator, hparams, scope=None)

  config_proto = utils.get_config_proto(log_device_placement=log_device_placement, num_intra_threads=hparams.num_intra_threads, num_inter_threads=hparams.num_inter_threads)

  infer_sess = tf.Session(target='', config=config_proto, graph=infer_model.graph)

  with infer_model.graph.as_default():
    loaded_infer_model, global_step = model_helper.create_or_load_model(infer_model.model, model_dir, infer_sess, 'infer')

  iterator_feed_dict = {infer_model.src_placeholder:sample_src_dataset, infer_model.batch_size_placeholder:1,}
  infer_sess.run(infer_model.iterator.initalizer, feed_dict=iterator_feed_dict)
 
  while True:
    try:
      nmt_outputs, _ = infer_model.decode(infer_sess)
    except tf.errors.OutOfRangeError:
      break


    
