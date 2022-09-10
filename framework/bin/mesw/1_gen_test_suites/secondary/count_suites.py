import os

# suites_dir = sys.argv[1]

suites_dir = '/home/people/12309511/test_suites/raw_suites'

# Iterate through projects, create nested dictionary
dicts = {}

for root, dirs, files in os.walk(suites_dir):

    for f in files:
        if f.endswith('.tar.bz2'):
            p_id, v_id, gen_id = f.split('-')
            gen_id = gen_id.split('.')[0]

            if p_id not in dicts:
                dicts[p_id] = {}

            if v_id not in dicts[p_id]:
                dicts[p_id][v_id] = {
                    'evosuite': 0,
                    'randoop': 0,
                    'total': 0
                }

            dicts[p_id][v_id][gen_id] += 1
            dicts[p_id][v_id]['total'] += 1

lt_5 = 0
num_5_10 = 0
eq_10 = 0
other = 0
total = 0

wf = open('/home/people/12309511/logging/1_gen_test_suites/count.log', 'w')

with wf:
    for proj, proj_dict in dicts.items():
        for ver, ver_dict in proj_dict.items():
            # print(proj + "-" + ver)
            # print(ver_dict['evosuite'])
            # print(ver_dict['randoop'])
            # print(ver_dict['total'])

            if ver_dict['total'] < 5:
                lt_5 += 1
                # Log project versions with less than 5 suites
                wf.write(proj + "-" + ver + "\n")
            elif 5 <= ver_dict['total'] < 10:
                num_5_10 += 1
            elif ver_dict['total'] == 10:
                eq_10 += 1
            else:
                other += 1

            total += 1

print("RESULTS")
print("Less than 5 suites:", lt_5)
print("5-10 suites:", num_5_10)
print("10 suites:", eq_10)
print("Other:", other)

print("Total:", total)

if total == lt_5 + num_5_10 + eq_10:
    print("Valid results")
