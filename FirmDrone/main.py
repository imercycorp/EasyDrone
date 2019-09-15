from core import nexus
from core import FW

n = nexus("1111", "123")
n.checkMDP()
v = n.getVersion()
print(v)

f = FW(n.returnKey(), n.returnMDP(), "1241", n.getVersion())
f.getFW()