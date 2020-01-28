#import the pandapower module
import pandapower as pp
import pandas as pd
import math

#create an empty network 
net = pp.create_empty_network()
freq = 60 # Hz 

### Buses ###
buses = pd.read_csv('data/Bus.csv',names=['bus_num','bus_volt','volt_init','angle_init','area','region']) # , sep=';', header=0, decimal=','
buses_names = pd.read_csv('data/Bus_names.csv',names=['name'],index_col=False).astype('str') # , sep=';', header=0, decimal=','
buses = pd.concat([buses, buses_names], axis=1)
for bus in buses.itertuples(index=True, name='Pandas'):
    bus_voltage = getattr(bus, "bus_volt")
    bus_name = getattr(bus, "name")
    pp.create_bus(net, name=bus_name, vn_kv=bus_voltage, type='b')
print(net.bus) # show bus table

### Lines ###
lines = pd.read_csv('data/Line.csv',names=['from_bus','to_bus','power_rating','voltage_rating',
                                           'freq_rating','length','-','r','x','b','--','---','i_max','p_max','s_max','area'])
for line in lines.itertuples(index=True, name='Pandas'):
    from_bus = getattr(line, "from_bus")
    to_bus = getattr(line, "to_bus")
    length = getattr(line, "length")
    r_ohm_per_km = getattr(line, "r")
    x_ohm_per_km = getattr(line, "x")
    c_nf_per_km = getattr(line, "r")/(2*math.pi*freq)
    max_i_ka = getattr(line, "i_max")/1e3
    line_num = getattr(line, "Index")
    pp.create_line_from_parameters(net,from_bus-1,to_bus-1, 
                                   length_km=length,r_ohm_per_km=r_ohm_per_km,x_ohm_per_km=x_ohm_per_km,
                                   c_nf_per_km=c_nf_per_km,max_i_ka=max_i_ka,name='Line %s' % line_num)
print(net.line) # show line table
    
### Shunt ###
shunts = pd.read_csv('data/Shunt.csv',names=['bus_num','power_rating','voltage_rating','freq_rating',
                                             'conductance','susceptance'],index_col=False)
#pp.create_shunt(net, pp.get_element_index(net, "bus", 'Bus HV1'), p_mw=0, q_mvar=0.960, name='Shunt')

### Swing ###
swing = pd.read_csv('data/SW.csv',names=['bus_num','power_rating','voltage_rating','voltage_mag','ref_angle',
                                         'q_max','q_min','v_max','v_min','p_init','loss_coeff','area','region'],index_col=False)
#pp.create_ext_grid(net, pp.get_element_index(net, "bus", 'Double Busbar 1'), vm_pu=1.03, va_degree=0, name='External grid',
#                   s_sc_max_mva=10000, rx_max=0.1, rx_min=0.1)

### PV ###
pv = pd.read_csv('data/PV.csv',names=['bus_num','power_rating','voltage_rating','active_power','voltage_mag',
                                         'q_max','q_min','v_max','v_min','p_init','loss_coeff'],index_col=False)
#pp.create_gen(net, pp.get_element_index(net, "bus", 'Bus HV4'), vm_pu=1.03, p_mw=100, name='Gas turbine')

### PQ ###
pq = pd.read_csv('data/PQ.csv',names=['bus_num','power_rating','voltage_rating','active_power','reactive_power',
                                     'v_max','v_min','conv_imp','area'],index_col=False)
#pp.create_load(net, bus_idx, p_mw=load.p, q_mvar=load.q, name=load.load_name)

### PQgen ###
pqgen = pd.read_csv('data/PQgen.csv',names=['bus_num','power_rating','voltage_rating','active_power','reactive_power',
                                            'v_max','v_min','conv_imp','area'],index_col=False)
#pp.create_sgen(net, pp.get_element_index(net, "bus", 'Bus SB 5'), p_mw=20, q_mvar=4, sn_mva=45, 
#               type='WP', name='Wind Park')


### Run Power Flow ###
#pp.runpp(net, calculate_voltage_angles=True, init="dc")
#print(net)