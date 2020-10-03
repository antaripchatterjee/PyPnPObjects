from pypnpobjects.pypnpobjects import WMIStorePNPObjects
import sys

if __name__ == "__main__":
    with WMIStorePNPObjects() as wmipnp:
        proc_res = wmipnp.load()
        if proc_res[0] == 0 and proc_res[1] is None:
            devs = wmipnp.query('*', status='ok', case_sensitive_comparision = False, comparision_operator = 'equal')
            for dev in devs:
                sys.stdout.write('Device %s is %s\n'%(dev.Name))
        else:
            sys.stderr.write('Error with code %d : %s\n'%(proc_res))
    