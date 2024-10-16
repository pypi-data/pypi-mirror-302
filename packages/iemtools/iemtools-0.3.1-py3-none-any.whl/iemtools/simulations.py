import numpy as np
import random as rd

def simulate_WT_SA( training_sequences ):
    """
    Input:  list of lists of actual mice positions in Y maze
    Output: a list of simulated positions
    """
    
    sequences = []
    a_count , b_count , c_count , lens = [] , [] , [] , []

    #read training_sequences, count occurances per length; base probability weights on the counts
    for line in training_sequences:
        seq = line[1]
        sequences.append(seq)
        lens.append( len(seq) )
        a_count.append( seq.count("A")/len(seq) )
        b_count.append( seq.count("B")/len(seq) )
        c_count.append( seq.count("C")/len(seq) )
    sequences_str = []
    for seq in sequences:
        s = str()
        for letter in seq:
            s += letter
        sequences_str.append(s)
    weight_a , weight_b , weight_c = np.mean(a_count) , np.mean(b_count) , np.mean(c_count)
    len_min = min(lens)
    len_max = max(lens)

    #count occurences of duplets and triplets
    ab = []
    ac = []
    aa = []
    ba = []
    bc = []
    bb = []
    ca = []
    cb = []
    cc = []
    for seq in sequences_str:
        ab.append( seq.count("AB")/len(seq) )
        ac.append( seq.count("AC")/len(seq) )
        aa.append( seq.count("AA")/len(seq) )
        ba.append( seq.count("BA")/len(seq) )
        bc.append( seq.count("BC")/len(seq) )
        bb.append( seq.count("BB")/len(seq) )
        ca.append( seq.count("CA")/len(seq) )
        cb.append( seq.count("CB")/len(seq) )
        cc.append( seq.count("CC")/len(seq) )
    w_ab = np.mean(ab)
    w_ac = np.mean(ac)
    w_aa = np.mean(aa)
    w_ba = np.mean(ba)
    w_bc = np.mean(bc)
    w_bb = np.mean(bb)
    w_ca = np.mean(ca)
    w_cb = np.mean(cb)
    w_cc = np.mean(cc)
    
    aaa = []
    bbb = []
    ccc = []
    for seq in sequences_str:
        aaa.append( seq.count("AAA")/len(seq) )
        bbb.append( seq.count("BBB")/len(seq) )
        ccc.append( seq.count("CCC")/len(seq) )
    w_aaa = np.mean(aaa)*3
    w_bbb = np.mean(bbb)*3
    w_ccc = np.mean(ccc)*3

    #count occurances of SA
    spont_alt = []
    for seq in sequences_str:
        spont_alt.append( seq.count("ABC")/len(seq) )
        spont_alt.append( seq.count("ACB")/len(seq) )
        spont_alt.append( seq.count("BAC")/len(seq) )
        spont_alt.append( seq.count("BCA")/len(seq) )
        spont_alt.append( seq.count("CAB")/len(seq) )
        spont_alt.append( seq.count("CBA")/len(seq) )
    w_spont_alt = np.mean(spont_alt)*3

    #SIMULATION PROPER
    sim_pos = []
    i = 0
    w_a , w_b , w_c = weight_a , weight_b , weight_c
    
    while i < rd.randint( len_min , len_max ):
        
        position = rd.choices( ["A","B","C"] , weights=[w_a , w_b , w_c] )[0]
        sim_pos.append( position )
        if position == "A":
            w_a , w_b , w_c = w_aa , w_ab , w_ac
        elif position == "B":
            w_a , w_b , w_c = w_ba , w_bb , w_bc
        else: w_a , w_b , w_c = w_ca , w_cb , w_cc
            
        if position == "A" and sim_pos[i-1] == "A":
            w_a = w_aaa
        elif position == "B" and sim_pos[i-1] == "B":
            w_b = w_bbb
        elif position == "C" and sim_pos[i-1] == "C":
            w_c = w_ccc
        else: pass
        
        if position == "A" and sim_pos[i-1] == "B":
            w_c = w_spont_alt
        elif position == "A" and sim_pos[i-1] == "C":
            w_b = w_spont_alt
        elif position == "B" and sim_pos[i-1] == "A":
            w_c = w_spont_alt
        elif position == "B" and sim_pos[i-1] == "C":
            w_a = w_spont_alt
        elif position == "C" and sim_pos[i-1] == "A":
            w_b = w_spont_alt
        elif position == "C" and sim_pos[i-1] == "B":
            w_a = w_spont_alt
        else: pass
         
        i += 1

    return sim_pos