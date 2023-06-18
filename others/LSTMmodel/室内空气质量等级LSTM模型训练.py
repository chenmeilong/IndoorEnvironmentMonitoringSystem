#float32         #  用 7W数据  迭代十次  coast 0.13   acc0.94 batch_size  = 1000  学习率0.001     70w取7w 同0.945/0.90
import tensorflow as tf
import pandas as pd
traindata = pd.read_csv('train.csv',sep = ',',index_col=0)  # 读取训练数据
testdata = pd.read_csv('test.csv',sep = ',',index_col=0)  # 读取测试数据的标签

tf.reset_default_graph()  #重置计算图，清理当前定义节点

#训练数据
data=traindata.drop(columns=['3'])
traininput = tf.constant(data.values)
#traininput = tf.expand_dims(input, 1)     #增维
#训练标签one hot
data=traindata['3']
label=data.values[:]    #只输出a列
label=label.astype(int)       #强制转化为int
target = tf.constant(label)
trainlabel = tf.one_hot(target, 4)                               #float32
#trainlabes = tf.expand_dims(trainlabes, 1)                          #增维  用于单个数据训练   批次训练 不需要
#测试数据
data=testdata.drop(columns=['3'])             #删掉标签列
testinput = tf.constant(data.values)
#input = tf.expand_dims(input, 1)     #增维
#测试标签one hot
data=testdata['3']
label=data.values[:]   #只输出a列
label=label.astype(int)       #强制转化为int
target = tf.constant(label)
testlabel = tf.one_hot(target, 4)                               #float32
#testlabel = tf.expand_dims(testlabel, 1)                         #增维  用于单个数据训练   批次训练 不需要


n_steps = 1  # timesteps 序列个数
n_hidden = 256  # hidden layer num of features隐藏层个数     细胞个数
n_classes = 4  # 优良中差四类
learning_rate = 0.001

x = tf.placeholder(tf.float64, [None, 3],name='input_x')  #data维度   30*30=900
y = tf.placeholder(tf.float64, [None, 4],name='input_y')  # 0-11 数字=>



b=[[1.0],[2.0],[3.0]]              #归一化处理
c=tf.transpose(x)
b[0]= c[0]
b[1]= c[1]
b[2]= c[2]/100
b=tf.transpose(b)
print(b)                           #  张量  (?, 3)的数据



h_conv3 = tf.reshape(b, [-1, 1, 3])      #   -1表示自动计算


x1 = tf.unstack(h_conv3, n_steps, 1)      #  30*30调整成   30个元素的list 序列      tf.unstack（）则是一个矩阵分解的函数     axis= 1按行分解

stacked_rnn = []
for i in range(3):
    stacked_rnn.append(tf.contrib.rnn.LSTMCell(n_hidden))       #建立3个LSTM的cell
mcell = tf.contrib.rnn.MultiRNNCell(stacked_rnn)                  #MultiRNNCell实例化

outputs, states = tf.contrib.rnn.static_rnn(mcell, x1, dtype=tf.float64)   #静态RNN


pred = tf.contrib.layers.fully_connected(outputs[-1], n_classes, activation_fn=None)   #全连接网络

# Define loss and optimizer
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

training_epochs = 10   # 迭代  次数
batch_size  = 500        #一个批次取1000条数据训练
display_step = 1              # 每训练一次打印中间状态
traindatanum=  52500                           #847  注意  ：一共

tf.add_to_collection('pred_network', pred)          #向当前计算图中添加张量集合
saver = tf.train.Saver()
model_path = "log/model"      #保存路径  model1

# 启动session
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())  # Initializing OP   运行初始化
    # 启动循环开始训练
    total_batch=int(traindatanum / batch_size)         #训练多少批次
    for epoch in range(training_epochs):  #迭代 xxxx次
        avg_cost = 0.
        # 遍历全部数据集
        for i  in range( total_batch ):                 #   847此处填入
            # Run optimization op (backprop) and cost op (to get loss value)

            train_data=sess.run(traininput[batch_size *i:batch_size *i+batch_size])
            train_label=sess.run(trainlabel[batch_size *i:batch_size *i+batch_size])
            _, c = sess.run([optimizer, cost], feed_dict={x:train_data,
                                                          y:train_label})
            # Compute average loss
            avg_cost += c / total_batch
        # 显示训练中的详细信息
        if (epoch + 1) % display_step == 0:
            print("Epoch:", '%04d' % (epoch + 1), "cost=", "{:.9f}".format(avg_cost))
    print(" Finished!")

    # 测试 model
    correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
    # 计算准确率
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float64))

    test_data= sess.run(testinput[0:5250])
    test_label = sess.run(testlabel[0:5250])

    #print("Accuracy:", accuracy.eval({X: , Y:  }))       #与下面的一行代码是等价的
    print("Accuracy:", sess.run(accuracy, feed_dict={x: test_data, y: test_label}))
    #     # Save model weights to disk   保存模型
    save_path = saver.save(sess, model_path)
    print("Model saved in file: %s" % save_path)
