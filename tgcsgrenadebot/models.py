from django.db import models


class Map(models.Model):
    name = models.CharField(max_length=15, null=False)

    def __str__(self):
        return self.name


class Grenade(models.Model):
    class TeamSideEnum(models.TextChoices):

        CT_SIDE = "CT"
        T_SIDE = "T"

    class GrenadeTypeEnum(models.TextChoices):
        MOLY = "MOLY"
        SMOKE = "SMOKE"
        FLASH = "FLASH"
        HE = "HE"

    class PlantEnum(models.TextChoices):
        PLANT_A = "A"
        PLANT_B = "B"

    name = models.CharField(max_length=30)

    side = models.CharField(max_length=15, choices=TeamSideEnum.choices)

    map = models.ForeignKey(Map, on_delete=models.CASCADE)

    image_example = models.ImageField(null=False)

    grenade_type = models.CharField(max_length=15, choices=GrenadeTypeEnum.choices)

    plant = models.CharField(max_length=15, choices=PlantEnum.choices, null=True)

    def __str__(self) -> str:
        return " ".join((self.side, self.grenade_type, self.plant, self.name))
