import re

def state_formatter(s):
    final_vals_lst = []
    val_lst = re.split("\;", s)
    desired_val_inds = [0,1,2,9]
    for i in desired_val_inds:
        final_vals_lst.append(val_lst[i].split(":")[1])
    return final_vals_lst

def main():
    print(state_formatter('pitch:0;roll:0;yaw:121;vgx:0;vgy:0;vgz:0;templ:93;temph:96;tof:6553;h:0;bat:72;baro:-51.69;time:0;agx:-1.00;agy:2.00;agz:-1000.00;\r\n'))

if __name__ == '__main__':
    main()