import orm
import asyncio
from models import User, Blog, Comment


async def test(loop):
    await orm.create_pool(loop=loop, host='8.129.132.234', user='root', password='admin123', db='test')
    u = User(name='Test3', email='test3@qq.com', passwd='1234567893', image='about:blank')
    await u.save()

    orm.__pool.close()
    await orm.__pool.wait_closed()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test(loop))
    loop.close()
