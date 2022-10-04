import argparse
import PyTango as PT
import fnmatch
from tabulate import tabulate

DATABASE = PT.Database()

def get_device_proxies(include_strings, exclude_strings):
  """Find all the devices that match any of the include_strings and none of the exclude_strings"""
  
  device_names = []
  for include_string in include_strings:
    # Find all devices that match include_string, and filter those that don't include any one of the exclude_strings
    device_names += [device_name for device_name in DATABASE.get_device_exported(include_string) if check_exclude_strings(device_name, exclude_strings)]

  proxies = {device_name: PT.futures.DeviceProxy(device_name) for device_name in device_names}
  return proxies

def check_exclude_strings(device_name, exclude_strings) -> bool:
  device_name_lower = device_name.lower()
  for exclude_string in exclude_strings:
    if fnmatch.fnmatch(device_name_lower, exclude_string): # if it matches any of our exlude strings
      return False # we don't want it
  return True

if __name__=="__main__":
  parser = argparse.ArgumentParser(description="Status Monitor Application")
  parser.add_argument("--states", 
                      nargs="+", # Take at least one, or more
                      type=str.upper, # convert the input to uppercase
                      choices=PT.DevState.names.keys(), # legal devstates
                      required=True,
                      help="Specify the TANGO DevStates to filter by")
        
  parser.add_argument("--include",
                      nargs="+", # Take one or more
                      type=str.lower, # convert input to lower case,
                      required=True,
                      help="Specify the devices to include. Wildcard: '*'")

  parser.add_argument("--exclude",
                      nargs="*", # Take zero or more
                      type=str.lower, # convert input to lower case,
                      required=False,
                      default=[], # if no arguments are passed in
                      help="Specify the devices to exclude. Wildcard: '*'")
                      
  parser.add_argument("--init",
                      action="store_true",
                      help="Send an init command to all the devices beforehand.")
                      
  args = parser.parse_args()

  proxies = get_device_proxies(args.include, args.exclude)

  allowed_states = [PT.DevState.names[state] for state in args.states]

  values_to_print = []
  
  for name, proxy in proxies.items():
    if args.init:
      proxy.init()  
    state = proxy.State()
    if state in allowed_states:
      status = proxy.Status()
      values_to_print.append((name, str(state), status))

  print("\n" + tabulate(values_to_print, headers=["Name", "State", "Status"], tablefmt="orgtbl") + "\n")
