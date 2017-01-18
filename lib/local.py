from lib.brick.audio import Audio
from lib.brick.group import Group
from lib.brick.power import Power
from lib.brick.start import Start
from lib.brick.state import State
from lib.brick.store import Store

GROUP_TEARD = Group(
    'Teardown'
)


POWER = dict(hostname='z1013')
POWER_LAMP0 = Power(
    'Light_Rack', GROUP_TEARD, prime='1', **POWER
)
POWER_LAMP1 = Power(
    'Light_Desk', GROUP_TEARD, prime='2', **POWER
)
POWER_LAMP2 = Power(
    'Light_Side', GROUP_TEARD, prime='4', **POWER
)
POWER_TONE0 = Power(
    'Stereo', GROUP_TEARD, prime='6', **POWER
)
POWER_LAMP3 = Power(
    'Light_Tone', GROUP_TEARD, prime='8', **POWER
)
POWER_DISK0 = Power(
    'Kleinhirn', GROUP_TEARD, prime='10', **POWER
)
POWER_DISK1 = Power(
    'Großhirn', GROUP_TEARD, prime='12', **POWER
)
POWER_AUX_0 = Power(
    'AUX_0', GROUP_TEARD, prime='14', **POWER
)
POWER_LAMP4 = Power(
    'Light_Sofa', GROUP_TEARD, prime='16', **POWER
)
POWER_AUX_1 = Power(
    'AUX_1', GROUP_TEARD, prime='18', **POWER
)
POWER_AUX_2 = Power(
    'AUX_2', GROUP_TEARD, prime='20', **POWER
)
POWER_AUX_3 = Power(
    'AUX_3', GROUP_TEARD, prime='22', **POWER
)


STORE = dict(eject_retry=3, eject_wait=5, power_delay=30)
STORE_DISK0 = Store(
    'Kleinhirn', POWER_DISK0, **STORE
)
STORE_DISK1 = Store(
    'Großhirn', POWER_DISK1, **STORE
)


AUDIO_TONE0 = Audio(
    'Krawallschachtel', POWER_TONE0, delay=3
)


START_PHOTO = Start(
    'Photos', STORE_DISK0
)
START_LIGHT = Start(
    'Lightroom', STORE_DISK0, prime='Adobe Photoshop Lightroom 4'
)
START_ITUNE = Start(
    'iTunes', STORE_DISK0, AUDIO_TONE0
)
START_DEEZE = Start(
    'Deezer', AUDIO_TONE0
)
START_MOVIS = Start(
    'Movist', STORE_DISK0, STORE_DISK1, AUDIO_TONE0
)
START_BKUP0 = Start(
    'Rsync_K_G', STORE_DISK0, STORE_DISK1,
    prime='/Volumes/Großhirn/disk_fetch.sh', script=True
)


STATE_SLEEP = State(
    'Sleep', GROUP_TEARD, command='sleep_now'
)
STATE_SCOFF = State(
    'Screensleep', command='sleep_screen'
)
STATE_SCLCK = State(
    'Screenlock', command='lock_screen'
)
STATE_SCSAV = State(
    'Screensaver', command='save_screen'
)
STATE_LOGOU = State(
    'Logout', command='log_out'
)
STATE_RESTA = State(
    'Restart', command='re_start'
)
STATE_SHUTD = State(
    'Shutdown', command='shut_down'
)
