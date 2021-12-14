#import asyncio
#import asyncpg

#async def run():
#    conn = await asyncpg.connect(user='horse', password='horse',
#                                 database='horse_db', host='127.0.0.1')
#    values = await conn.fetch(
#        'SELECT * FROM devices'
#    )
#    print(values)
#    await conn.close()

#loop = asyncio.get_event_loop()
#loop.run_until_complete(run())
