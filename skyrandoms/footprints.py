from collections import OrderedDict, namedtuple
FootPrint = namedtuple('FootPrint', 'region ra_lim dec_lim') 

__all__ = ['hsc']

hsc = OrderedDict([
    ('r1', FootPrint(region=1, ra_lim=[28, 42], dec_lim=[-8, -1])),
    ('r2',FootPrint(region=2, ra_lim=[126, 143], dec_lim=[-3, 6])),
    ('r3', FootPrint(region=3, ra_lim=[175, 184], dec_lim=[-3, 2])),
    ('r4', FootPrint(region=4, ra_lim=[208, 228], dec_lim=[-3, 2.5])),
    ('r5', FootPrint(region=5, ra_lim=[234, 250], dec_lim=[-3, 2.5])),
    ('r6', FootPrint(region=6, ra_lim=[328, 346], dec_lim=[-2, 4]))
])
