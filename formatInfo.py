# 获得网络的详细信息


def format_flux(flux):
    flux = int(flux)
    if flux > 1024 * 1024 * 1024:
        return str(int(flux / (1024 * 1024 * 1024) * 100) / 100)  + 'GB'
    elif flux > 1024 * 1024:
        return str(int(flux / (1024 * 1024)) / 100) + 'MB'
    elif flux > 1024:
        return str(int(flux / 1024) / 100) + 'KB'
    else:
        return str(int(flux) / 100) + 'B'


def format_time(time):
    time = int(time)
    h = time / 3600
    m = (time % 3600) / 60
    s = time % 3600 % 60
    return "%02d:%02d:%02d" % (h, m, s)
