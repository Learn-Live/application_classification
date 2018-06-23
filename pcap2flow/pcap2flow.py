# -*- coding: utf-8 -*-
"""
    @ Pcap Converter: convert pcap to text or flows.

    return: start_time, end_time, src_ip, dst_ip, protocol, src_port, dst_port, pkts_lst=[],flow_duration, intr_tm_lst=[]

    refer to:  https://github.com/hbhzwj/pcap-converter

txt format: pcap to txt
-------------------
1   0.000000 51.142.253.91 -> 15.236.229.88 TCP 54 2555 22746
<seq no> <time stamp> <src ip> -> <dst ip> <protocol> <pkt size> <src port> <dst port>

flow format: txt to flow
--------------------
0.000429 238.227.214.84 147.47.105.20 TCP 54 0.014504
<start time stamp> <src ip> <dst ip> <protocol> <flow size> <flow duration>
"""

from __future__ import print_function, division
from subprocess import check_call


# from CythonUtil import c_parse_records_tshark


def export_to_txt(f_name, txt_f_name):
    cmd = """tshark -o gui.column.format:'"No.", "%%m", "Time", "%%t", "Source", "%%s", "Destination", "%%d", "Protocol", "%%p", "len", "%%L", "srcport", "%%uS", "dstport", "%%uD"' -r %s > %s""" % (
        f_name, txt_f_name)

    print('--> ', cmd)
    check_call(cmd, shell=True)


def parse_records_tshark(f_name):
    records = []
    NAME = ['start_time', 'src_ip', 'dst_ip', 'protocol', 'length',
            'src_port', 'dst_port']
    with open(f_name, 'r') as infile:
        for line in infile:
            line = line.strip()
            items = line.split()
            rec = (float(items[1]), items[2], items[4], items[5], int(items[6]),
                   int(items[7]), int(items[8]))
            records.append(rec)
    return records, NAME


def change_to_flows(pkts_records, name, *args, **kwargs):
    # def change_to_flows(pkts_records, name, time_out=0.1, flow_duration=1, first_n_pkts=5):
    """

    :param pkts_records: packets_records
    :param name: ['start_time','src_ip',  'dst_ip',, 'protocol','length', 'src_port', 'dst_port']
    :param time_out: the current time - the previous time
    :param flow_duration: the current time - the start time
    :param first_n_pkts: the first n packets of the flow
    :return:
    """
    print('**kwargs:', kwargs.items())
    st_idx = name.index('start_time')  # start time index
    len_idx = name.index('length')  # length index
    five_tuple_seq = [name.index(k) for k in ['src_ip', 'dst_ip', 'protocol', 'src_port', 'dst_port']]
    open_flows = dict()  # key: five_tuple, value:(start_time, end_time, length_lst, interval_time_diff_lst)
    res_flow = []
    for rec in pkts_records:
        five_tuple = tuple(rec[seq] for seq in five_tuple_seq)  # current packet's five tuple
        curr_tm = rec[st_idx]  # current time
        curr_len = rec[len_idx]  # current packet length
        intr_tm = 0.0  # Inter Arrival Time, the time between two packets sent single direction
        # check time out
        remove_flows = []
        for f_tuple, (st_tm, pre_tm, pkts_lst, intr_tm_lst) in open_flows.items():
            if kwargs.get('time_out') is not None:
                time_out = kwargs.get('time_out')
                if curr_tm - pre_tm > time_out:  # time out : curr_tm-pre_tm
                    # if t - st_tm > time_out:  # flow_duration: curr_tm-st_tm
                    flow_dur = curr_tm - st_tm  # flow_dur: flow_duration
                    res_flow.append((st_tm, curr_tm) + f_tuple + (
                        pkts_lst, flow_dur, intr_tm_lst))  # pkts_lst: the packets size in the same flow
                    # intr_tm_lst: Inter Arrival Time, the time between two packets sent single direction
                    # print('f_tuple',f_tuple)
                    remove_flows.append(f_tuple)
            elif kwargs.get('flow_duration') is not None:
                flow_duration = kwargs.get('flow_duration')
                if curr_tm - st_tm > flow_duration:  # flow_duration: curr_tm-st_tm
                    flow_dur = curr_tm - st_tm  # flow_dur: flow_duration
                    res_flow.append((st_tm, curr_tm) + f_tuple + (
                        pkts_lst, flow_dur, intr_tm_lst))  # pkts_lst: the packets size in the same flow
                    # intr_tm_lst: Inter Arrival Time, the time between two packets sent single direction
                    # print('f_tuple',f_tuple)
                    remove_flows.append(f_tuple)
            elif kwargs.get('first_n_pkts') is not None:
                first_n_pkts = kwargs.get('first_n_pkts')
                if len(pkts_lst) > first_n_pkts:
                    flow_dur = curr_tm - st_tm  # flow_dur: flow_duration
                    res_flow.append((st_tm, curr_tm) + f_tuple + (
                        pkts_lst, flow_dur, intr_tm_lst))  # pkts_lst: the packets size in the same flow
                    # intr_tm_lst: Inter Arrival Time, the time between two packets sent single direction
                    # print('f_tuple',f_tuple)
                    remove_flows.append(f_tuple)
            else:
                print('input params is not right')
                exit(-1)
        for f_tuple in remove_flows:
            # print('---f_tuple:',five_tuple)
            del open_flows[f_tuple]

        stored_rec = open_flows.get(five_tuple)
        if stored_rec is not None:  # if already exists
            (st_tm, pre_pre_tm, pre_pkts_lst, pre_intr_tm_lst) = stored_rec
            # open_flows[five_tuple] = (st_tm_pre, t, pkts_lst_pre + length)
            pre_pkts_lst.append(curr_len)  # return None
            pre_intr_tm_lst.append(curr_tm - pre_pre_tm)  # return None
            open_flows[five_tuple] = (st_tm, curr_tm, pre_pkts_lst, pre_intr_tm_lst)
            # print(open_flows[five_tuple],pkts_lst_pre.append(length),pkts_lst_pre,length)
        else:  # not exisit
            open_flows[five_tuple] = (curr_tm, curr_tm, [curr_len], [intr_tm])

    print("""
Totoal Packets: [%i]
Exported subFlows: [%i]
Remain subFlows: [%i]
            """ % (len(pkts_records), len(res_flow), len(open_flows)))

    return res_flow


def change_to_flows_backup(pkts_records, name, first_n_pkts=5):
    """

    :param pkts_records: packets_records
    :param name: ['start_time','src_ip',  'dst_ip',, 'protocol','length', 'src_port', 'dst_port']
    :param first_n_pkts: the first n packets of the flow
    :return:
    """
    st_idx = name.index('start_time')  # start time index
    len_idx = name.index('length')  # length index
    five_tuple_seq = [name.index(k) for k in ['src_ip', 'dst_ip', 'protocol', 'src_port', 'dst_port']]
    open_flows = dict()  # key: five_tuple, value:(start_time, end_time, length_lst, interval_time_diff_lst)
    res_flow = []
    for rec in pkts_records:
        five_tuple = tuple(rec[seq] for seq in five_tuple_seq)  # current packet's five tuple
        curr_tm = rec[st_idx]  # current time
        curr_len = rec[len_idx]  # current packet length
        intr_tm = 0.0  # Inter Arrival Time, the time between two packets sent single direction
        # check time out
        remove_flows = []
        for f_tuple, (st_tm, pre_tm, pkts_lst, intr_tm_lst) in open_flows.items():
            # if curr_tm - pre_tm > time_out:  # time out : curr_tm-pre_tm
            if len(pkts_lst) > first_n_pkts:
                # if t - st_tm > time_out:  # flow_duration: curr_tm-st_tm
                flow_dur = curr_tm - st_tm  # flow_dur: flow_duration
                res_flow.append((st_tm, curr_tm) + f_tuple + (
                    pkts_lst, flow_dur, intr_tm_lst))  # pkts_lst: the packets size in the same flow
                # intr_tm_lst: Inter Arrival Time, the time between two packets sent single direction
                # print('f_tuple',f_tuple)
                remove_flows.append(f_tuple)
        for f_tuple in remove_flows:
            # print('---f_tuple:',five_tuple)
            del open_flows[f_tuple]

        stored_rec = open_flows.get(five_tuple)
        if stored_rec is not None:  # if already exists
            (st_tm, pre_pre_tm, pre_pkts_lst, pre_intr_tm_lst) = stored_rec
            # open_flows[five_tuple] = (st_tm_pre, t, pkts_lst_pre + length)
            pre_pkts_lst.append(curr_len)  # return None
            pre_intr_tm_lst.append(curr_tm - pre_pre_tm)  # return None
            open_flows[five_tuple] = (st_tm, curr_tm, pre_pkts_lst, pre_intr_tm_lst)
            # print(open_flows[five_tuple],pkts_lst_pre.append(length),pkts_lst_pre,length)
        else:  # not exisit
            open_flows[five_tuple] = (curr_tm, curr_tm, [curr_len], [intr_tm])

    print("""
Totoal Packets: [%i]
Exported subFlows: [%i]
Remain subFlows: [%i]
            """ % (len(pkts_records), len(res_flow), len(open_flows)))

    return res_flow


def save_flow(flows, f_name):
    with open(f_name, 'w') as fid:
        for f in flows:
            # print(f)
            fid.write(' '.join([str(v) for v in f]) + '\n')


def pcap2flow(pcap_file_name, flow_file_name, *args, **kwargs):
    if kwargs.get('time_out') is not None:
        time_out = kwargs.get('time_out')
        txt_f_name = pcap_file_name.rsplit('.pcap')[0] + '_time_out_' + str(time_out) + '_tshark.txt'
        param_str = 'time_out=%f' % time_out
    elif kwargs.get('flow_duration') is not None:
        flow_duration = kwargs.get('flow_duration')
        txt_f_name = pcap_file_name.rsplit('.pcap')[0] + '_flow_duration_' + str(flow_duration) + '_tshark.txt'
        param_str = 'flow_duration=%f' % flow_duration
    elif kwargs.get('first_n_pkts') is not None:
        first_n_pkts = kwargs.get('first_n_pkts')
        txt_f_name = pcap_file_name.rsplit('.pcap')[0] + '_first_n_pkts_' + str(first_n_pkts) + '_tshark.txt'
        param_str = 'first_n_pkts=%d' % first_n_pkts
    else:
        print('input params is not right.')
        exit(-1)
    # txt_f_name = pcap_file_name.rsplit('.pcap')[0] + '_first_n_pkts_' + str('5') + '_tshark.txt'
    export_to_txt(pcap_file_name, txt_f_name)
    records, name = parse_records_tshark(txt_f_name)
    res_flows = change_to_flows(records, name, **kwargs)
    save_flow(res_flows, flow_file_name)


if __name__ == '__main__':
    input_file = '../data/WorldOfWarcraft.pcap'
    # output_file = './time_out=0.01+flow.txt'
    # pcap2flow(input_file, output_file, time_out=0.01)  # 0.01s
    output_file = './first_n_pkts=5+flow.txt'
    pcap2flow(input_file, output_file, first_n_pkts=1)  # the first n packets of the same flow
    # output_file = './low_duration=0.1+flow.txt'
    # pcap2flow(input_file, output_file, flow_duration=0.1)  # current_time - start_time>0.1
    #
