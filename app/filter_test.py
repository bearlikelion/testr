import os
from re import match
from cvpysdk.commcell import Commcell
from AutomationUtils.machine import Machine

cs = Commcell('auto-dev.idx.commvault.com', 'admin', 'Builder!12')
machine = Machine('auto-dev', cs)
automation_log_file = cs.commserv_client.log_directory + os.sep + 'Automation' + os.sep + 'Automation.log'

automation_log = machine.read_file(automation_log_file)

with open(automation_log_file) as f:
    for line in f:
        pass
    last_line = line

pid = last_line.split('  ')[0]
pid_log = match(pid + '  ', automation_log)

print(pid_log.string)

if "[FAILED]." in pid_log.string:
    print('FAILED')
elif "[PASSED]." in pid_log.string:
    print('PASSED')