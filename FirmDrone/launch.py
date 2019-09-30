from core import nexus
from core import FW
from core import manageData
from core import security
from core import analytics

m = manageData()
n = nexus(m.returnKey(), m.returnMDP())

if n.checkMDP() == 1:
    print("[AUTH] Le mot de passe est parfaitement configuré !")
else:
    print("[AUTH] {ERROR - 0001} Problème dans la configuration !")