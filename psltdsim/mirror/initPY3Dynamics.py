def initPY3Dynamics(mirror):
    """Initialize PY3 specific Dynamics"""

    # Run All individual agent inits
    for dynamic in mirror.Dynamics:
        dynamic.stepInitDynamics()
