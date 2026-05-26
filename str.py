class Wizard:
    def __init__(self, name, mana=100):
        self.name = name
        self.mana = mana

    def cast(self):
        print(f"{self.name} — маг третьего класса.")


class IceWizard(Wizard):
    print(f"Замораживает воду! ❄️")


class WaterWizard(Wizard):
    print(f"Управляет водой! 🌊")


water = WaterWizard("Канне")
ice = IceWizard("Лавине")

ice.cast()
water.cast()