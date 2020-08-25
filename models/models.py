# -*- coding: utf-8 -*-
from odoo import models, fields, api
import time
import re
from datetime import timedelta, date, datetime


class Frota(models.Model):
    _name = 'custom.frota'

    nome = fields.Char(string='Nome')
    status = fields.Selection([('ativo','Ativo'),('inativo','Inativo')],'Status')
    condutor_atual = fields.Many2one('custom.frota.condutor','Condutor atual')
    contato_condutor = fields.Char('Contato Condutor', related="condutor_atual.contato")
    relacao_contrato = fields.Many2one('custom.frota.contrato','Selecione o contrato')
    locadora_contrato= fields.Char('Locadora', related='relacao_contrato.locadora')
    valor_contrato= fields.Float('Valor do contrato',related='relacao_contrato.valor')
    responsavel_contrato= fields.Char('Responsável pela retirada',related='relacao_contrato.responsavel_nome')
    # responsavel_contato = fields.Char('Contato do Responsável', related="responsavel_contrato.responsavel_contato")
    data_contrato= fields.Date('Data do contrato',related='relacao_contrato.data_contrato')
    limite_contrato = fields.Integer('Limite contrato', related='relacao_contrato.limite_contrato')
    link_contrato = fields.Char('Link do contrato', related='relacao_contrato.link_contrato')
    relacao_carro = fields.Many2one('custom.frota.carro', 'Selecione o carro')
    modelo = fields.Char('Modelo', related='relacao_carro.modelo')
    categoria = fields.Char('Categoria', related = 'relacao_carro.categoria')
    cidade_retirada = fields.Char('Cidade de retirada')
    agencia_retirada = fields.Char('Agência de retirada')
    setor = fields.Char('Setor')
    gastos = fields.One2many('custom.frota.gastos', 'frota', string='Selecione os gastos')
    #
    km_utilizado_contrato = fields.Integer('KM utilizado do limite contrato', compute='get_km_contrato')
    km_inicial = fields.Integer('KM Inicial')
    km_inicial_mes = fields.Integer('KM inicial do mês')
    km_atual = fields.Integer('KM Atual')
    uso_km = fields.Integer('Uso KM', compute='get_uso_km')
    revisao = fields.Integer('Revisao')
    km_restante_revisao = fields.Integer('KM restante para revisão', compute='get_km_revisao')
    link_trajeto = fields.Char('Link do trajeto', widget='url', related="relacao_carro.link_trajeto")

    def get_uso_km(self):
        # self.ensure_one()
        for record in self:
            # if(record.km_atual):
            record.uso_km = record.km_atual - record.km_inicial

    def get_km_contrato(self):
        for record in self:
            record.km_utilizado_contrato = record.km_atual - record.km_inicial_mes

    def get_km_revisao(self):
        for record in self:
            record.km_restante_revisao = record.revisao - record.km_atual

    def name_get(self):  # ok
        result = []
        for record in self:
            result.append((record.id, ("%s") % (
                record.nome)))
        return result


    @api.model
    def create(self, vals):  # ok
        vals['status'] = 'ativo'
        vals['nome'] = self.env['ir.sequence'].next_by_code('frota.sequence')
        result = super(Frota, self).create(vals)
        return result


    def botao_ativar(self):  # ok
        if (self.status != "ativo"):
            self.status = "ativo"

    def botao_desativar(self):  # ok
        if (self.status != "inativo"):
            self.status = "inativo"

class Contrato(models.Model):
    _name= 'custom.frota.contrato'

    status = fields.Selection([('criado','Criado'),('andamento','Em Andamento'),('finalizado','Finalizado')],'Status',default='criado')
    responsavel_retirada = fields.Many2one('custom.frota.condutor', 'Responsável pela retirada')
    responsavel_nome = fields.Char('Responsável', related='responsavel_retirada.nome')
    responsavel_contato = fields.Char('Contato do Responsável', related="responsavel_retirada.contato")
    valor = fields.Float(string='Valor do contrato')
    contrato = fields.Char(string='Nome do contrato')
    limite_contrato = fields.Integer(string = 'Limite contrato')
    link_contrato = fields.Char(string='Link do Contrato')
    locadora = fields.Char(string = 'Locadora')
    data_contrato = fields.Date(string='Data do contrato')
    relacao_frota = fields.One2many('custom.frota', 'relacao_contrato', string='Selecione as frotas')

    def botao_finalizar(self):
        for record in self:
            if(record.status == 'andamento'):
                record.status = 'finalizado'
                if(len(record.relacao_frota)!=0):
                    for frt in record.relacao_frota:
                        frt.status = 'inativo'
            # if(self.status=='andamento'):
            #     self.status = 'finalizado'
            #     print(self.relacao_frota[0].nome)


    def name_get(self):  # ok
        result = []
        for record in self:
            result.append((record.id, ("%s") % (
                record.contrato)))
        return result

    @api.model
    def create(self, vals):  # ok
        vals['status'] = 'andamento'
        # vals['contrato'] = self.env['ir.sequence'].next_by_code('contrato.sequence')
        result = super(Contrato, self).create(vals)
        return result


class Carro(models.Model):
    _name = 'custom.frota.carro'

    modelo = fields.Char(string='Modelo')
    categoria = fields.Char(string='Categoria')
    placa = fields.Char(string = 'Placa', min=7, max=7, size=7)
    link_trajeto = fields.Char('Link trajeto')
    def name_get(self):  # ok
        result = []
        for record in self:
            result.append((record.id, ("%s") % (
                record.placa)))
        return result

class Condutor(models.Model):
    _name= 'custom.frota.condutor'

    nome = fields.Char('Nome', required='1')
    cpf = fields.Char('CPF', required='1', size=11)
    data_nascimento = fields.Date('Data de nascimento', required='1')
    cnh = fields.Char('CNH', required='1', size=11)
    categoria_cnh = fields.Char('Categoria CNH')
    validade_cnh = fields.Date('Validade CNH', required='1')
    vencimento_cnh = fields.Char('Vencimento CNH', compute='get_vencimento')
    link_cnh = fields.Char('Link CNH')
    situacao = fields.Selection([('ativo','Ativo'), ('demitido', 'Demitido')], 'Situação',default='ativo', required='1')
    contato = fields.Char('Contato')
    def get_vencimento(self):
        hoje = datetime.now().date()
        for record in self:
            if (record.validade_cnh):
                record.vencimento_cnh = 'Faltam '+str((record.validade_cnh - hoje).days)+' dias para o vencimento da CNH.'

    # @api.onchange('validade_cnh')
    # def set_dias_vencimento(self):
    #     for rec in self:
    #         if rec.validade_cnh:
    #             self.get_vencimento()


    def name_get(self):  # ok
        result = []
        for record in self:
            result.append((record.id, ("%s") % (
                record.nome)))
        return result

class Gastos(models.Model):
    _name= 'custom.frota.gastos'

    tipo = fields.Selection([('multa', 'Multa'),('sinistro','Sinistro'),('abastecimento','Abastecimento'),('locacao','Locação'),('outro','Outro')], required='1')

    #Elementos de Multa/Sinistro/Locação
    nome = fields.Char('Nome')
    frota = fields.Many2one('custom.frota', string='Frota')
    contrato = fields.Many2one('custom.frota.contrato', string='Contrato', related='frota.relacao_contrato')
    ocorrencia = fields.Date(string='Data de ocorrência')
    emissao = fields.Date(string='Data de emissão')
    vencimento = fields.Date(string='Data de vencimento')
    baixa = fields.Date(string='Data de baixa')
    condutor = fields.Many2one('custom.frota.condutor', string='Condutor')
    # valor_contrato = fields.Float(string='Valor do contrato')
    link_fatura = fields.Char(string='Link da fatura')
    observacao = fields.Text(string = 'Observação')
    valor_locacao = fields.Float(string='Valor da locação')

    #Elementos únicos de Multa/Sinistro
    valor_fatura = fields.Float(string='Valor da fatura')
    valor_sinistro = fields.Float(string='Valor do sinistro')
    situacao = fields.Selection([('aprovado','Aprovado'),('reprovado','Reprovado'),('analise','Aguardando análise'),('paga','Paga')],string='Situação de Aprovação')
    data_envio = fields.Date(string='Data de envio de custo')
    data_analise = fields.Date(string='Data de análise')
    situacao_pagamento = fields.Selection([('paga','Paga'),('vencida','Vencida'),('cancelada','Cancelada'),('aberta','Aberta')], string='Situação de Pagamento')
    descontado_funcionario = fields.Selection([('sim','Sim'),('nao','Não'),('analise','Aguardando Análise'),('cancelada','Cancelada')],string='Descontado valor funcionário')
    valor_desconto_funcionario = fields.Float(string='Valor descontado do funcionário')

    #Elementos únicos de abastecimento
    #frota
    #Contrato
    km_mes = fields.Date('Data KM/MÊS')
    valor_km_mes = fields.Float('Valor KM/MÊS')

    valor_outro = fields.Float('Valor do gasto')

    @api.model
    def create(self, vals):  # ok
        vals['nome'] = self.env['ir.sequence'].next_by_code('gastos.sequence')
        result = super(Gastos, self).create(vals)
        return result

    def name_get(self):  # ok
        result = []
        for record in self:
            result.append((record.id, ("%s") % (
                record.nome)))
        return result

class Departamento(models.Model):
    _name= 'custom.frota.departamento'

    nome = fields.Char('Nome')


