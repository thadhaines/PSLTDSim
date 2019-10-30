def distACE(BA):
    """ Handles distributing ACE to BA area """
    BA.cv['distStep'] = 1
    ACE2dist = BA.cv['ACE2dist']

    # Distribute Ace as a negative
    for gen in BA.ctrlMachines:

        if gen.distType.lower() == 'step':
            if gen.gov_model == False:
                # distribute Negative ACE to Pmech
                gen.cv['Pm'] -= ACE2dist*gen.ACEpFactor
                if gen.cv['Pm'] > gen.Pmax:
                    gen.cv['Pm'] = gen.Pmax
            else:
                # distribute Negative ACE % to Pref
                gen.cv['Pref'] -= ACE2dist*gen.ACEpFactor
                if gen.cv['Pref'] > gen.Pmax:
                    gen.cv['Pref'] = gen.Pmax

        elif gen.distType.lower() == 'rampa':
            # Ramp value instead of step
            if gen.gov_model == False:
                # distribute Negative ACE to Pmech
                # NOTE: Don't forget this makese a ton of Agents!
                if gen.gov_model.mwCap < gen.gov_model.Pref -ACE2dist*gen.ACEpFactor:
                    AGCramp = ltd.perturbance.RampAgent(BA.mirror, 
                                                    gen, ['Pm',BA.mirror.cv['t'],
                                                            BA.rampTime, gen.gov_model.mwCap, 'abs'])
                else:
                    AGCramp = ltd.perturbance.RampAgent(BA.mirror, 
                                                    gen, ['Pm',BA.mirror.cv['t'],
                                                            BA.rampTime, -ACE2dist*gen.ACEpFactor, 'rel'])
                BA.mirror.AGCramp.append(AGCramp)
            else:
                # distribute Negative ACE % to Pref
                # NOTE: Don't forget this makese a ton of Agents!
                if gen.gov_model.mwCap < gen.gov_model.Pref -ACE2dist*gen.ACEpFactor:
                    AGCramp = ltd.perturbance.RampAgent(BA.mirror, 
                                                    gen, ['Pref',BA.mirror.cv['t'],
                                                            BA.rampTime, gen.gov_model.mwCap, 'abs'])
                else:
                    AGCramp = ltd.perturbance.RampAgent(BA.mirror, 
                                                    gen, ['Pref',BA.mirror.cv['t'],
                                                            BA.rampTime, -ACE2dist*gen.ACEpFactor, 'rel'])
                BA.mirror.AGCramp.append(AGCramp)