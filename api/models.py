from django.db import models


class Total_Comex(models.Model):
    Nome_Arquivo = models.CharField('Nome do Arquivo', max_length=100, unique=True)
    Movement = models.CharField('Tipo de movimentação', max_length=30)
    Ano = models.CharField('Ano', max_length=4)
    Total = models.BigIntegerField('Total')  # LEMBRAR DE COLOCAR TOLTAL EM LETRA MINUSCULA

    def __str__(self):
        return '%s - %s' % (self.Movement, self.Ano)

    class Meta:
        verbose_name = 'Total_Comex'
        verbose_name_plural = 'Total_Comex'


class Products_SH6(models.Model):
    COD_SH6 = models.CharField('COD_SH6', max_length=100, unique=True)
    COD_SH2 = models.CharField('COD_SH2', max_length=100, blank=True, null=True)
    NM_SH2 = models.CharField('COD_SH6', max_length=300, blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.COD_SH6, self.NM_SH2)

    class Meta:
        verbose_name = 'Produto_SH6'
        verbose_name_plural = 'Produtos_SH6'


class Products_NCM(models.Model):
    COD_NCM = models.CharField('COD_NCM', max_length=100, unique=True)
    NM_NCM = models.CharField('NM_NCM', max_length=300, blank=True, null=True)
    COD_SH6 = models.ForeignKey(Products_SH6, on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.COD_NCM, self.NM_NCM)

    class Meta:
        verbose_name = 'Produto_NCM'
        verbose_name_plural = 'Produtos_NCM'


class Via(models.Model):
    COD_VIA = models.CharField('COD_NCM', max_length=100, unique=True)
    NM_VIA = models.CharField('NM_NCM', max_length=300, blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.COD_VIA, self.NM_VIA)

    class Meta:
        verbose_name = 'Via'
        verbose_name_plural = 'Vias'


class Valor_Movimentado(models.Model):
    MOVEMENT = models.CharField('Tipo de movimentação', max_length=30)
    COD_NCM = models.CharField('NM_NCM', max_length=10, blank=True, null=True)
    COD_VIA = models.CharField('NM_NCM', max_length=10, blank=True, null=True)
    ANO = models.CharField('Ano', max_length=4)
    VL_FOB = models.CharField('NM_NCM', max_length=100, blank=True, null=True)
    MONTH = models.CharField('NM_NCM', max_length=2, blank=True, null=True)
    SG_UF = models.CharField('NM_NCM', max_length=2, blank=True, null=True)

    def __str__(self):
        return '%s - %s - %s' % (self.MOVEMENT, self.COD_NCM, self.ANO)

    class Meta:
        verbose_name = 'Movimento'
        verbose_name_plural = 'Movimentações'


