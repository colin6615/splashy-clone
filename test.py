from threading import Timer

party_yellow_light = False


def party_yellow_light_true():
    print("hi")


party_deactivation_timer = Timer(
    5,
    party_yellow_light_true,
)
party_deactivation_timer.start()
