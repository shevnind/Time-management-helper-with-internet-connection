import argparse
import asyncio

from database import login_user, register_user, run_database, add_problem, get_problems, delete_problem

async def communicate(reader, writer):
    print("Client connected")
    while True:
        byte_message = await reader.readline()
        message = byte_message.decode()
        print(message)

        if message == "!stop\n":
            break
        ans = ""
        lst = message[:-1].split("  ")
        if message[0:5] == "login":
            ans = await login_user(lst[1], lst[2])
        elif message[0:8] == "register":
            ans = await register_user(lst[1], lst[2])
        elif message[0:11] == "add problem":
            ans = await add_problem(lst[1], lst[2])
        elif message[0:12] == "get problems":
            ans = await get_problems(lst[1])
        elif message[0:14] == "delete problem":
            ans = await delete_problem(lst[1], int(lst[2]))
        ans += '\n'
        writer.write(ans.encode())
        await writer.drain()

    writer.close()
    await writer.wait_closed()
    print("Close connection")

async def main():
    await run_database()
    server = await asyncio.start_server(communicate, HOST, PORT)
    async with server:
        print('Server running...')
        await server.serve_forever()


parser = argparse.ArgumentParser()
parser.add_argument("host", help="ip-адрес сети")
parser.add_argument("port", help="порт")

args = parser.parse_args()
HOST = args.host
PORT = args.port

asyncio.run(main())
