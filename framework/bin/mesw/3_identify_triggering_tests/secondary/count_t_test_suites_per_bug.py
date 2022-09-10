import os

trig_test_dir = '/home/people/12309511/triggering_tests'
fixed_suites_dir = '/home/people/12309511/test_suites/fixed_suites'

# Iterate through projects, create nested dictionary
dicts = {}

# Initiate empty dicts based on fixed suites
for root, dirs, files in os.walk(fixed_suites_dir):
    for f in files:
        if f.endswith('.tar.bz2'):
            p_id, v_id, gen_id = f.split('-')
            gen = gen_id.split('.')[0]

            if p_id not in dicts:
                dicts[p_id] = {}

            if v_id not in dicts[p_id]:
                dicts[p_id][v_id] = {
                    'trig_suites': 0
                }

# Iterate through triggering test files updating dicts
for root, dirs, files in os.walk(trig_test_dir):
    for f in files:
        if f.endswith('.properties'):
            p_id, v_id, gen_id = f.split('-')
            gen = gen_id.split('.')[0]

            # if p_id not in dicts:
            #     dicts[p_id] = {}
            #
            # if v_id not in dicts[p_id]:
            #     dicts[p_id][v_id] = {
            #         'trig_suites': 0
            #     }

            dicts[p_id][v_id]['trig_suites'] += 1

wf = open('/home/people/12309511/logging/3_run_bug_det_thomas/count_t_test_suites.log', 'w')
wf2 = open('/home/people/12309511/logging/3_run_bug_det_thomas/bugs_wo_t_tests.log', 'w')

eq_0 = 0
eq_1 = 0
lt_5 = 0
num_5_10 = 0
eq_10 = 0
other = 0
total = 0

with wf, wf2:
    for proj, proj_dict in dicts.items():
        for ver, ver_dict in proj_dict.items():

            print(proj + "-" + ver + ": " + str(ver_dict['trig_suites']))

            if ver_dict['trig_suites'] == 0:
                eq_0 += 1
                wf2.write(proj + "-" + ver + "\n")
            elif ver_dict['trig_suites'] == 1:
                eq_1 += 1
            elif ver_dict['trig_suites'] < 5:
                lt_5 += 1
            elif ver_dict['trig_suites'] < 10:
                num_5_10 += 1
            elif ver_dict['trig_suites'] == 10:
                eq_10 += 1
            else:
                other += 1
            total += 1

    wf.write("Triggering test suites per bug\n")
    wf.write("0: " + str(eq_0) + "\n")
    wf.write("1: " + str(eq_1) + "\n")
    wf.write("<5: " + str(lt_5) + "\n")
    wf.write("5-10: " + str(num_5_10) + "\n")
    wf.write("10: " + str(eq_10) + "\n")
    wf.write("other: " + str(other) + "\n")
    wf.write("total: " + str(total) + "\n")

    wf.close()
    wf2.close()

print("0: ", eq_0)
print("1: ", eq_1)
print("<5: ", lt_5)
print("5-10: ", num_5_10)
print("10: ", eq_10)
print("other: ", other)
print("total: ", total)

if total == eq_0 + eq_1 + eq_10 + lt_5 + num_5_10:
    print("Valid results")
