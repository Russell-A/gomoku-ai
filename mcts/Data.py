import hash
import copy



IsExistKill = 0

def _init():
    global glo_var
    glo_var = {}
    # global gl_find_KillDict
    # gl_find_KillDict = {}
    # global gl_StateDict
    # gl_StateDict = {}
    # global gl_KillDict
    # gl_KillDict = {}
    # global global_hashtable
    # global_hashtable = hash.hash(20, 20)


# def set_find_kill(find_dic):
#     gl_find_KillDict = copy.deepcopy(find_dic)
#
#
# def set_kill_dict():
#     import copy
#     gl_KillDict = copy.deepcopy(gl_find_KillDict)
#
# def get_kill_dict():
#     return gl_KillDict

def set_glo(key, value):
    glo_var[key] = value

def get_glo(key):
    return glo_var[key]