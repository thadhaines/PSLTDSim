def findGlobalSlack(mirror):
    """Locates and sets the global slack generator"""
    #NOTE: Not even close to complete
    if len(mirror.Slack) < 2:
        mirror.Slack[0].globalSlack = 1
    else:
        print("More than 1 slack generator found... Setting first to global... ")
        mirror.Slack[0].globalSlack = 1