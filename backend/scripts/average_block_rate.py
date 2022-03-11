import time

from backend.blockchain.blockchain import Blockchain
from backend.config import SECONDS

blockchain = Blockchain()
times = []

for i in range(1000):
    start_time = time.time_ns()
    blockchain.add_block(data=i)
    end_time = time.time_ns()
    mine_time = (end_time - start_time) / SECONDS
    times.append(mine_time)

    avg_time = sum(times) / len(times)

    print(f"New difficulty: {blockchain.chain[-1].difficulty}")
    print(f"time to mine: {mine_time}s")
    print(f"Average time to mine: {avg_time}s\n")
