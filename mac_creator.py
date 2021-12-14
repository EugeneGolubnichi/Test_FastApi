import random

def mac_creator():
    #создаем рандомный мас-адрес
    mac = ':'.join(("%012x" % random.randint(0, 0xFFFFFFFFFFFF))[i:i+2] for i in range(0, 12, 2))
    print(mac)
    return str(mac)


def device_creator():
    # создаем рандомный тип устройства
    list_of_device = ['emeter', 'zigbee', 'lora', 'gsm']
    type_d = random.choice(list_of_device)
    print(type_d)
    return type_d


