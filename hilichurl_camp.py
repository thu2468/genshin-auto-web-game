# Autoplay Genshin's "Hilichurl Camp" web game.

import dwebhook
from get_session import SESSION
import sys
import time
import os

uid = ''
if 'UID' in os.environ:
    uid = f"&uid={os.environ['UID']}"
#GET
RECIPE_LIST = f'https://hk4e-api-os.mihoyo.com/event/e20210421homeland/web/user/furniture?lang=en-us{uid}&region=os_usa&is_app=0'
TASK_LIST = f'https://hk4e-api-os.mihoyo.com/event/e20210421homeland/web/task/list?lang=en-us{uid}&region=os_usa&is_app=0'
DATA = f'https://hk4e-api-os.mihoyo.com/event/e20210421homeland/web/event/index?lang=en-us{uid}&region=os_usa&is_app=0'
FURN_LIST = f'https://hk4e-api-os.mihoyo.com/event/e20210421homeland/web/user/furniture?lang=en-us{uid}&region=os_usa&is_app=0'
#POST
TASK_COMPLETE = f'https://hk4e-api-os.mihoyo.com/event/e20210421homeland/web/task/complete?lang=en-us{uid}&region=os_usa&is_app=0'
TASK_REWARD = f'https://hk4e-api-os.mihoyo.com/event/e20210421homeland/web/task/reward?lang=en-us{uid}&region=os_usa&is_app=0'
CRAFT_ITEM = f'https://hk4e-api-os.mihoyo.com/event/e20210421homeland/web/make/start?lang=en-us{uid}&region=os_usa&is_app=0'
FINISH_CRAFT = f'https://hk4e-api-os.mihoyo.com/event/e20210421homeland/web/make/finish?lang=en-us{uid}&region=os_usa&is_app=0'
MILESTONE_REWARD = f'https://hk4e-api-os.mihoyo.com/event/e20210421homeland/web/milestone/reward?lang=en-us{uid}&region=os_usa&is_app=0'

def complete_tasks():
    with SESSION.get(TASK_LIST) as r:
        tasks = r.json()
    task_list = tasks['data']['task_list']
    for task in task_list:
        if task['task_status'] == 0:
            SESSION.post(TASK_COMPLETE, json = {'task_id': task['task_id']})
        if task['task_status'] == 1:
            SESSION.post(TASK_REWARD, json = {'task_id': task['task_id']})
    with SESSION.get(TASK_LIST) as r:
        tasks = r.json()
    task_list = tasks['data']['task_list']
    print(f'Daily tasks completed: {len([task for task in task_list if task["task_status"] == 2])}/{len(task_list)}')

def craft_something():
    with SESSION.get(DATA) as r:
        data = r.json()
    mats = data['data']['user_material_list']
    mat_list = {mat['material_id']:mat['material_num'] for mat in mats}
    used_recipes = data['data']['used_formula_list']
    with SESSION.get(FURN_LIST) as r:
        furniture = r.json()
    furn = furniture['data']['furniture_list']
    furn = [f for f in furn if not f['is_unlock']]
    full_formula = None
    for piece in furn:
        full_formula = None
        formula = ''
        for mat in piece['formula_item_list']:
            if mat in mat_list:
                formula += mat
        mats_sorted = sorted(mat_list.keys())
        for mat in mats_sorted[mats_sorted.index(formula[-1]):]:
            # try appending different materials to formula
            full_formula = formula + mat
            if ''.join(sorted(full_formula)) not in used_recipes:
                for matname in mat_list:
                    if full_formula.count(matname) > mat_list[matname]:
                        # not enough available mats to use this recipe
                        full_formula = None
                        break
                else:
                    break
        else:
            continue
        break
    if full_formula:
        print('Crafting items using formula:',full_formula)
        with SESSION.post(CRAFT_ITEM, json = {'formula_item_list': list(full_formula)}) as r:
            res = r.json()
        if res['retcode'] == 0 and res['message'] == 'OK':
            print(f'Craft started successfully, waiting {res["data"]["left_time"]} seconds.')
            return res['data']['make_id'],res['data']['left_time']
        else:
            print(res['message'])
            return None,None
    else:
        print('No recipes possible (out of materials)')
        return None,None

def milestone_rewards():
    with SESSION.get(DATA) as r:
        data = r.json()
    milestones = data['data']['milestone_list']
    for ms in milestones:
        if ms['status'] == 1:
            SESSION.post(MILESTONE_REWARD, json = {'milestone_gear': ms['milestone_gear']})

if __name__ == '__main__':
    try:
        with SESSION.get(DATA) as r:
            data = r.json()
        if data['retcode'] == -104 or ('data' in data and data['data']['is_end']):
            print('Event is over.')
            exit(-104)
        # do daily tasks:
        print('#'*50)
        complete_tasks()
        print('#'*50)
        while 1:
            # craft furniture until out of mats
            make_id, seconds = craft_something()
            if make_id == None:
                break
            time.sleep(seconds+5)
            SESSION.post(FINISH_CRAFT, json = {'make_id': make_id})
        # claim milestone rewards
        milestone_rewards()
    finally:
        sys.stdout.publish()