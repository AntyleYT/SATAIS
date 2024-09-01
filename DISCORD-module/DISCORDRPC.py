from pypresence import Presence
import time

print("connection...")
client_id = '1255924932110454796'
RPC = Presence(client_id)
RPC.connect()
print("connected!")
print("Updating RPC...")
RPC.update(
    state="SATAIS",
    details="Join SATAIS Now !",
    large_image="https://cdn.discordapp.com/avatars/1255924932110454796/46c03ccb3ba73bb185329a1f5b7782aa.png",
    large_text="SATAIS",
    small_text="https://discord.gg/dd8TzgCK8Z",

    start=time.time()
)

print("RPC apply correctly! | SATAIS © HAISDIP ")

try:
    while True:
        time.sleep(15)
except KeyboardInterrupt:
    print("RPC stopped correctly| SATAIS © HAISDIP ")
    RPC.clear()
    RPC.close()
