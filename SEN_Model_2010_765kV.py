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
    '''pp.create_line(net,from_bus-1,to_bus-1,length_km=length,std_type="NAYY 4x50 SE",
                                   name='Line %s' % line_num)'''
print(net.line) # show line table
    
### Shunt ###
shunts = pd.read_csv('data/Shunt.csv',names=['bus_num','power_rating','voltage_rating','freq_rating',
                                             'conductance','susceptance'],index_col=False)
for shunt in shunts.itertuples(index=True, name='Pandas'):
    bus_num = getattr(shunt, "bus_num")
    q_mvar = getattr(shunt, "susceptance")
    shunt_num = getattr(shunt, "Index")
    pp.create_shunt(net, bus_num-1, p_mw=0, q_mvar=q_mvar, name='Shunt %s' % shunt_num)
print(net.shunt) # show shunt table

### Swing ###
swings = pd.read_csv('data/SW.csv',names=['bus_num','power_rating','voltage_rating','voltage_mag','ref_angle',
                                         'q_max','q_min','v_max','v_min','p_init','loss_coeff','area','region'],index_col=False)
for swing in swings.itertuples(index=True, name='Pandas'):
    bus_num = getattr(swing, "bus_num")
    vm_pu = getattr(swing, "voltage_mag")
    va_degree = getattr(swing, "ref_angle")
    pp.create_ext_grid(net, bus_num-1, vm_pu=vm_pu, va_degree=va_degree, name='Slack Bus')
print(net.ext_grid) # show swing table

### PV ###
pvs = pd.read_csv('data/PV.csv',names=['bus_num','power_rating','voltage_rating','active_power','voltage_mag',
                                         'q_max','q_min','v_max','v_min','p_init','loss_coeff'],index_col=False)
for pv in pvs.itertuples(index=True, name='Pandas'):
    bus_num = getattr(pv, "bus_num")
    vm_pu = getattr(pv, "voltage_mag")
    p_mw = getattr(pv, "active_power")
    pv_num = getattr(pv, "Index")
    pp.create_gen(net, bus_num-1, vm_pu=vm_pu, p_mw=p_mw, name='Gen %s' % pv_num)
print(net.gen) # show gen table

### PQ ###
pqs = pd.read_csv('data/PQ.csv',names=['bus_num','power_rating','voltage_rating','active_power','reactive_power',
                                     'v_max','v_min','conv_imp','area'],index_col=False)
for pq in pqs.itertuples(index=True, name='Pandas'):
    bus_num = getattr(pq, "bus_num")
    p_mw = getattr(pq, "active_power")
    q_mvar = getattr(pq, "reactive_power")
    pq_num = getattr(pq, "Index")
    pp.create_load(net, bus_num-1, p_mw=p_mw, q_mvar=q_mvar, name='Load %s' % pq_num)
print(net.load) # show loads table

### PQgen ###
pqgens = pd.read_csv('data/PQgen.csv',names=['bus_num','power_rating','voltage_rating','active_power','reactive_power',
                                            'v_max','v_min','conv_imp','area'],index_col=False)
for pqgen in pqgens.itertuples(index=True, name='Pandas'):
    bus_num = getattr(pqgen, "bus_num")
    try:
        mask=pqs[pqs['bus_num']==bus_num].index.tolist()[0]
        raise ValueError("Attention static gens and loads at the same bus. Manually modify database")
    except:
        p_mw = getattr(pqgen, "active_power")
        q_mvar = getattr(pqgen, "reactive_power")
        sn_mva = getattr(pqgen, "power_rating")
        pqgen_num = getattr(pqgen, "Index")
        pp.create_sgen(net, bus_num-1, p_mw=p_mw, q_mvar=q_mvar, sn_mva=sn_mva, name='StatGen %s' % pqgen_num)
        #pp.create_load(net, bus_num-1, p_mw=p_mw, q_mvar=q_mvar, name='StatGen %s' % pqgen_num)
print(net.sgen) # show static gen table

### Diagnosis ###
pp.diagnostic(net, report_style='detailed', warnings_only=False, return_result_dict=True, overload_scaling_factor=0.001, min_r_ohm=0.001, min_x_ohm=0.001, min_r_pu=1e-05, min_x_pu=1e-05, nom_voltage_tolerance=0.3, numba_tolerance=1e-05)

### Run Power Flow ###
pp.runpp(net, algorithm="iwamoto_nr", calculate_voltage_angles="auto", init="dc", check_connectivity=True, v_debug=True) #, init_vm_pu=True, init_va_degree=True
print(net)