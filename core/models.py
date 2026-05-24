# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Cargo(models.Model):
    g_id = models.AutoField(primary_key=True, verbose_name='Код груза')
    g_name = models.CharField(max_length=50, verbose_name='Наименование груза')
    g_weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Вес груза')
    g_volume = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Объём груза')
    g_type = models.CharField(max_length=20, blank=True, null=True, verbose_name='Тип груза')
    c = models.ForeignKey('Clients', models.DO_NOTHING, blank=True, null=True, verbose_name='Клиент')

    class Meta:
        managed = False
        db_table = 'cargo'
        verbose_name = 'Груз'
        verbose_name_plural = 'Грузы'

    def __str__(self):
        return self.g_name


class Clients(models.Model):
    c_id = models.AutoField(primary_key=True, verbose_name='Код клиента')
    c_type = models.CharField(max_length=2, verbose_name='Тип клиента')
    c_name = models.CharField(max_length=100, verbose_name='ФИО / наименование организации')

    class Meta:
        managed = False
        db_table = 'clients'
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.c_name


class Dispatchers(models.Model):
    d_id = models.AutoField(primary_key=True, verbose_name='Код диспетчера')
    d_name = models.CharField(max_length=50, verbose_name='ФИО диспетчера')
    d_email = models.CharField(unique=True, max_length=50, verbose_name='Email')
    d_pass = models.CharField(max_length=99, verbose_name='Пароль')

    class Meta:
        managed = False
        db_table = 'dispatchers'
        verbose_name = 'Диспетчер'
        verbose_name_plural = 'Диспетчеры'

    def __str__(self):
        return self.d_name


class DriverLicense(models.Model):
    pk = models.CompositePrimaryKey('dr_id', 'l_id')
    dr = models.ForeignKey('Drivers', models.DO_NOTHING, verbose_name='Водитель')
    l = models.ForeignKey('Licenses', models.DO_NOTHING, verbose_name='Категория прав')

    class Meta:
        managed = False
        db_table = 'driver_license'
        verbose_name = 'Категория водителя'
        verbose_name_plural = 'Категории водителей'

    def __str__(self):
        return f'{self.dr} — {self.l}'


class Drivers(models.Model):
    dr_id = models.AutoField(primary_key=True, verbose_name='Код водителя')
    dr_name = models.CharField(max_length=50, verbose_name='ФИО водителя')
    dr_tel = models.CharField(max_length=30, blank=True, null=True, verbose_name='Телефон водителя')

    class Meta:
        managed = False
        db_table = 'drivers'
        verbose_name = 'Водитель'
        verbose_name_plural = 'Водители'

    def __str__(self):
        return self.dr_name


class Individuals(models.Model):
    c = models.OneToOneField(Clients, models.DO_NOTHING, primary_key=True, verbose_name='Клиент')
    p_passp = models.CharField(max_length=50, verbose_name='Номер паспорта')
    p_date = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    p_tel = models.CharField(max_length=30, blank=True, null=True, verbose_name='Телефон')

    class Meta:
        managed = False
        db_table = 'individuals'
        verbose_name = 'Физическое лицо'
        verbose_name_plural = 'Физические лица'

    def __str__(self):
        return f'Физ. лицо: {self.c}'


class LegalEntities(models.Model):
    c = models.OneToOneField(Clients, models.DO_NOTHING, primary_key=True, verbose_name='Клиент')
    y_inn = models.BigIntegerField(unique=True, verbose_name='ИНН')
    y_tel = models.CharField(max_length=30, blank=True, null=True, verbose_name='Телефон организации')

    class Meta:
        managed = False
        db_table = 'legal_entities'
        verbose_name = 'Юридическое лицо'
        verbose_name_plural = 'Юридические лица'

    def __str__(self):
        return f'Юр. лицо: {self.c}'


class Licenses(models.Model):
    l_id = models.AutoField(primary_key=True, verbose_name='Код категории')
    l_name = models.CharField(max_length=2, verbose_name='Название категории')

    class Meta:
        managed = False
        db_table = 'licenses'
        verbose_name = 'Категория прав'
        verbose_name_plural = 'Категории прав'

    def __str__(self):
        return self.l_name


class Routes(models.Model):
    r_id = models.AutoField(primary_key=True, verbose_name='Код маршрута')
    r_from = models.CharField(max_length=50, verbose_name='Пункт отправления')
    r_to = models.CharField(max_length=50, verbose_name='Пункт назначения')
    r_dist = models.IntegerField(blank=True, null=True, verbose_name='Расстояние')
    r_time = models.IntegerField(blank=True, null=True, verbose_name='Время в пути')

    class Meta:
        managed = False
        db_table = 'routes'
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'

    def __str__(self):
        return f'{self.r_from} → {self.r_to}'


class Shipments(models.Model):
    tr_id = models.AutoField(primary_key=True, verbose_name='Код перевозки')

    cargo = models.ForeignKey(
        Cargo,
        models.DO_NOTHING,
        db_column='g_id',
        blank=True,
        null=True,
        verbose_name='Груз'
    )

    transport = models.ForeignKey(
        'Transports',
        models.DO_NOTHING,
        db_column='t_id',
        blank=True,
        null=True,
        verbose_name='Транспорт'
    )

    route = models.ForeignKey(
        Routes,
        models.DO_NOTHING,
        db_column='r_id',
        blank=True,
        null=True,
        verbose_name='Маршрут'
    )

    client = models.ForeignKey(
        Dispatchers,
        models.DO_NOTHING,
        db_column='d_id',
        blank=True,
        null=True,
        verbose_name='Диспетчер'
    )

    tr_date_start = models.DateField(verbose_name='Дата отправки')
    tr_date_end = models.DateField(blank=True, null=True, verbose_name='Дата прибытия')
    tr_status = models.CharField(max_length=20, blank=True, null=True, verbose_name='Статус перевозки')

    class Meta:
        managed = False
        db_table = 'shipments'
        verbose_name = 'Перевозка'
        verbose_name_plural = 'Перевозки'

    def __str__(self):
        return f'Перевозка №{self.tr_id}'


class Transports(models.Model):
    t_id = models.AutoField(primary_key=True, verbose_name='Код транспорта')
    t_mark = models.CharField(max_length=30, verbose_name='Марка')
    t_model = models.CharField(max_length=30, verbose_name='Модель')
    t_number = models.CharField(unique=True, max_length=15, verbose_name='Гос. номер')
    t_cap = models.IntegerField(verbose_name='Грузоподъёмность')
    dr = models.ForeignKey(Drivers, models.DO_NOTHING, blank=True, null=True, verbose_name='Водитель')

    class Meta:
        managed = False
        db_table = 'transports'
        verbose_name = 'Транспорт'
        verbose_name_plural = 'Транспорт'

    def __str__(self):
        return f'{self.t_mark} {self.t_model} ({self.t_number})'