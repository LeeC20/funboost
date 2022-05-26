import copy

from funboost import boost,IdeAutoCompleteHelper,ConcurrentModeEnum


def add(a, b):
    print(a + b)

# deco(a=100)(f)(x=1,y=2)的结果  和f被deco(100)装饰 然后f(x=1,y=2)效果是一样的，这是装饰器基本本质，这里不展开啰嗦了。
add_boost = boost('queue_test_f01c',  qps=0.2,concurrent_mode= ConcurrentModeEnum.THREADING,log_level=20)(add)   # type: IdeAutoCompleteHelper

add2 = lambda a,b:add(a,b)

#
def add3(a,b):
    return add(a,b)


add_boost2 = boost('queue_test_f02c',  qps=0.2,concurrent_mode= ConcurrentModeEnum.THREADING)(add2)

print(add_boost.queue_name)
print(add_boost2.queue_name)

if __name__ == '__main__':
    for i in range(10, 20):
        add_boost.push(a=i, b=i * 2)  # consumer.publisher_of_same_queue.publish 发布任务
        add_boost2.push(i*10,i*20)
    # add_boost.consume()  # 当前进程内启动消费,多线程消费
    # add_boost.multi_process_consume(2) #  启动单独的2个进程叠加多线程并发