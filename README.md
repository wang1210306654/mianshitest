1、测试路由add/

2、使用 redis数据库
使用 zset 作为数据类型
用户编号作为 name 用户分数作为 source，直接排序

当分数相同，按照先后顺序排序

3、使用我本人的服务器作为redis服务器

4、使用cookie直接记录来源编号，用于单机测试

