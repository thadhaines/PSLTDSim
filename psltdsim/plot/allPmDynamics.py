def allPmDynamics(mirror, blkFlag=True):
    """Plot all dynamic responses from generators
    does not block by default - blkFlag ignored
    """
    import matplotlib.pyplot as plt
    import numpy as np

    mir = mirror
    xend = max(mir.r_t)

 
    for c_dyn in mir.Dynamics:
        fig, ax = plt.subplots(nrows=2, ncols=1,)
        ax[0].set_title('Governed Generator on Bus %d %s Power Output' 
                        % (c_dyn.Busnum, c_dyn.Busnam,))
        ax[1].set_title('Governor States')

        ax[0].plot(mir.r_t, c_dyn.Gen.r_Pe, 
                    marker = 'o',
                    #markerfill = 'None',
                    linestyle = ':',
                    label = 'Pe')
        ax[0].plot(mir.r_t, c_dyn.Gen.r_Pm, 
                    marker = '+',
                    linestyle = '--',
                    label = 'Pm')

        ax[1].plot(mir.r_t, c_dyn.r_x1, 
                    marker = '1',
                    linestyle = '--',
                    label = 'x1')
        ax[1].plot(mir.r_t, c_dyn.r_x2, 
                    marker = '2',
                    linestyle = ':',
                    label = 'x2')

        ax[0].set_xlabel('Time [sec]')
        ax[1].set_xlabel('Time [sec]')
        ax[0].set_ylabel('MW')
        ax[1].set_ylabel('State')
        # Global Plot settings
        for x in np.ndarray.flatten(ax):
            x.set_xlim(0,xend)
            x.legend()
            x.grid(True)

        fig.tight_layout()

        plt.show(block = False)