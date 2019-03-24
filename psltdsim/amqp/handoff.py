def handoff(mirror,msg):
    """Handle PY3<->IPY handoff messages"""
    hType = msg['HandoffType']

    if hType == 'PY3toIPY':
        # calc deltaP_pert and Pacc
        # Sum system loads to Account for any load changes from Perturbances
        mirror.prevPload = mirror.ss_Pload
        mirror.ss_Pload = ltd.mirror.sumLoad(mirror)[0]
        if mirror.debug:
            print('prev P load: %f' % mirror.prevPload)
            print('current P load: %f' % mirror.ss_Pload)
        
        ss_Pert_Pdelta = mirror.ss_Pload - mirror.prevPload

        mirror.ss_Pm = ltd.mirror.sumPm(mirror)

        # Calculate current system Pacc
        mirror.ss_Pacc = mirror.ss_Pm - mirror.ss_Pe - ss_Pert_Pdelta
        if mirror.debug:
            print("Pert delta : %f \tPacc %f " %(ss_Pert_Pdelta, mirror.ss_Pacc))
        # Verify mirror value match
        if msg['Pert_Pdelta'] == ss_Pert_Pdelta:
            if mirror.debug:
                print('Perturbance P delta Match')
            if msg['Pacc'] == mirror.ss_Pacc:
                if mirror.debug:
                    print('Pacc Match')
                return 1

    elif hType == 'IPYtoPY3':
        # calc sum Pe
        mirror.ss_Pe = ltd.mirror.sumPe(mirror)
        # verify match
        if msg['ss_Pe'] == mirror.ss_Pe:
            if mirror.debug:
                print('Pe match')
            return 1

    return 0