from subprocess import Popen, PIPE
from os.path import dirname, isfile, join

def parse_results(raw_res):
    if "EV OOP" in raw_res[0]:
        return {"_".join(raw_res[idx].split()[:-1]).strip(":").lower():
                    float(raw_res[idx].split()[-1]) for idx in range(len(raw_res)) }
    else:
        raise ValueError("Incorrect results format: {}".format(raw_res[0]))

def pick_criterion(optimize_oop=False, worst_case=False):
    if optimize_oop:
        if worst_case:
            return 'mes_ip'
        else:
            return 'ev_ip'
    else:
        if worst_case:
            return 'mes_oop'
        else:
            return 'ev_oop'

def get_results(solver_path, script_name, number_of_steps, save=False):
    solver = Popen(solver_path, stdin=PIPE, stdout=PIPE, stderr=PIPE,
          cwd=dirname(solver_path), universal_newlines=True)

    save_command = ""
    if save:
        save_command = """
dump_tree scripts/best_result.cfr no_turns"""

    output, errors = solver.communicate("""load_script scripts/{}
    go {} steps
    wait_for_solver
    calc_results{}
    exit""".format(script_name, number_of_steps, save_command))
    results = parse_results(
        output.split('\n')[-8:-3] if save
        else output.split('\n')[-7:-2])
    # TODO: make it find the results instead of depending on line numbering
    results.update({'label':script_name})
    print(results)
    return results

    #solver.poll()
    #if solver.returncode is not None:
    #    print("Solver has now terminated.")
    #else:
    #    print("Warning: solver has not terminated as expected.")

    #input("Press enter to exit: ")

while True:
    solver_path = input("Enter full path to solver file: ")
    if isfile(solver_path):
        break
    else:
        print("Incorrect path, try again.")

while True:
    script_list = input("Enter script filenames (in /scripts/ subfolder) separated with spaces: ").split()
    for script_name in script_list[:]:
        if not isfile(join(dirname(solver_path),"scripts",script_name)):
            script_list.remove(script_name)
    if script_list:
        break

while True:
    try:
        number_of_prelim_steps = int(input("Enter number of preliminary steps: "))
        break
    except ValueError:
        print("Incorrect number, try again.")

if input("Optimize for OOP player? y/N: ").lower() == 'y':
    optimize_oop = True
else:
    optimize_oop = False

if input("Minimize opponent's MES (worst case) instead of EV? y/N: ").lower() == 'y':
    worst_case = True
else:
    worst_case = False

while True:
    try:
        number_of_final_steps = int(input("Enter number of final steps: "))
        break
    except ValueError:
        print("Incorrect number, try again.")

print('---')
all_results = [get_results(solver_path, script_name, number_of_prelim_steps) for script_name in script_list]

best = sorted(all_results, key=lambda x: x[pick_criterion(optimize_oop,worst_case)])[0]

print('---\nBest result:')
best_results = get_results(solver_path, best['label'], number_of_final_steps, save=True)

input("Enter to exit: ")