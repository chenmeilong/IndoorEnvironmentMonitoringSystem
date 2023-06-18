
import tensorflow as tf

def getevr (temp,humi,qual):
  data = []
  data.append(float(temp))
  data.append(float(humi))
  data.append(float(qual))
  data=[data]
  with tf.Session() as sess:
    new_saver = tf.train.import_meta_graph('log/model.meta')
    new_saver.restore(sess, 'log/model')
    pred = tf.get_collection('pred_network')[0]             ## tf.get_collection() 返回一个list. 但是这里只要第一个参数即可
    graph = tf.get_default_graph()                          #读取图
    input_x = graph.get_operation_by_name('input_x').outputs[0]     #获取 输入 占位符
    dir=sess.run(pred, feed_dict={input_x:data })          #input_x   #[[ 14.  45. 808.]]  输入类型
    dir=tf.argmax(dir, 1)
    pred=sess.run(dir[0])
    pred=int(pred)
    if  pred==0:
      qual=4
    if  pred==1:
      qual=3
    if  pred==2:
      qual=2
    if pred ==3:
      qual=1
    return qual
def main():
  value = getevr(25, 90, 200)
  print(value)

if __name__ == '__main__':
  main()









