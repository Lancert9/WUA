__author__ = 'j-lijiawei'


def find(attack_address, a_record):
    with open(attack_address, 'rb') as inputfile:
        for line in inputfile:
            if a_record in line and "deviceid" in line:
                print line
                break
        print "Not found."

if __name__ == '__main__':
    record = "[]"
    input_attack_address = "E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container\\Input_Attack\\skyeye-sensor_attack_20151112_31"
    find(input_attack_address, record)
