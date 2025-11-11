from dataclasses import dataclass
import csv

CONTRATO_TOTAL = 2000.00

@dataclass
class Orcamento:
    tipo: str  # 'apartamento', 'casa', 'estudio'
    quartos: int
    vagas: int
    possui_criancas: bool
    parcelas_contrato: int

    def calcular_valor_aluguel(self) -> float:
        tipo = self.tipo.lower()
        if tipo == 'apartamento':
            valor = 700.0
            if self.quartos == 2:
                valor += 200.0
            if self.vagas > 0:
                valor += 300.0 * self.vagas
            if not self.possui_criancas:
                valor *= 0.95
        elif tipo == 'casa':
            valor = 900.0
            if self.quartos == 2:
                valor += 250.0
            if self.vagas > 0:
                valor += 300.0 * self.vagas
        elif tipo in ['estudio', 'estúdio']:
            valor = 1200.0
            if self.vagas >= 2:
                valor += 250.0
                if self.vagas > 2:
                    valor += 60.0 * (self.vagas - 2)
        else:
            raise ValueError('Tipo de imóvel inválido')

        return round(valor, 2)

    def parcela_contrato(self) -> float:
        if not (1 <= self.parcelas_contrato <= 5):
            raise ValueError('Parcelas do contrato devem ser entre 1 e 5')
        return round(CONTRATO_TOTAL / self.parcelas_contrato, 2)

    def gerar_planilha_12_meses(self, filename: str) -> None:
        aluguel = self.calcular_valor_aluguel()
        parcela = self.parcela_contrato()
        with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['mes', 'aluguel_mensal', 'parcela_contrato', 'total_mes'])
            for mes in range(1, 13):
                parc = parcela if mes <= self.parcelas_contrato else 0.0
                total = round(aluguel + parc, 2)
                writer.writerow([mes, f'{aluguel:.2f}', f'{parc:.2f}', f'{total:.2f}'])

    def resumo(self) -> dict:
        aluguel = self.calcular_valor_aluguel()
        parcela = self.parcela_contrato()
        return {
            'tipo': self.tipo,
            'quartos': self.quartos,
            'vagas': self.vagas,
            'possui_criancas': self.possui_criancas,
            'aluguel_sem_parcela': aluguel,
            'parcela_contrato': parcela,
            'total_primeiro_mes': round(aluguel + parcela, 2)
        }


if __name__ == '__main__':
    orc = Orcamento(tipo='apartamento', quartos=2, vagas=1, possui_criancas=False, parcelas_contrato=5)
    print('Resumo:', orc.resumo())
    orc.gerar_planilha_12_meses('orcamento_12_meses.csv')
    print('Arquivo csv gerado com sucesso!')

