# Relatório Analítico - Tech Challenge Fase 1

## Sumário executivo
- Base analisada: 2.500 pedidos.
- NPS médio: 4.38; mediana: 4.40.
- NPS calculado por classes: -66.0 p.p. (promotores - detratores).
- Distribuição: 74.0% detratores, 17.9% neutros e 8.0% promotores.

## Principais achados
- A satisfação é mais sensível a fatores de fricção operacional: reclamações, atendimento, prazo de resolução e atraso logístico.
- O ponto de ruptura mais claro aparece quando o cliente acumula reclamações. A taxa de detratores sobe de forma material conforme o volume de reclamações aumenta.
- Atrasos de entrega e múltiplas tentativas de entrega reduzem a experiência percebida e devem acionar tratativas preventivas.
- O score interno de satisfação acompanha positivamente o NPS e pode funcionar como sinal antecipado, desde que não substitua a pesquisa final.

## Impacto por atraso de entrega
| delivery_delay_days | orders | avg_nps | detractor_rate |
| ------------------- | ------ | ------- | -------------- |
| 0 dias              | 277    | 6.86    | 36.46          |
| 1 dia               | 615    | 5.55    | 59.67          |
| 2-3 dias            | 1171   | 4.07    | 81.81          |
| 4+ dias             | 437    | 2.00    | 97.25          |

## Impacto por reclamações
| complaints_count | orders | avg_nps | detractor_rate |
| ---------------- | ------ | ------- | -------------- |
| 0                | 23     | 8.52    | 4.35           |
| 1-2              | 399    | 6.58    | 32.58          |
| 3-5              | 1551   | 4.28    | 78.79          |
| 6+               | 527    | 2.82    | 94.50          |

## Impacto por contatos com atendimento
| customer_service_contacts | orders | avg_nps | detractor_rate |
| ------------------------- | ------ | ------- | -------------- |
| 0                         | 554    | 5.54    | 59.21          |
| 1                         | 816    | 4.66    | 70.34          |
| 2                         | 640    | 4.12    | 79.06          |
| 3+                        | 490    | 2.94    | 90.41          |

## Regiões
| customer_region | orders | avg_nps | detractor_rate | promoter_rate |
| --------------- | ------ | ------- | -------------- | ------------- |
| Centro-Oeste    | 468    | 4.21    | 74.36          | 7.69          |
| Sudeste         | 520    | 4.37    | 74.62          | 8.27          |
| Norte           | 506    | 4.38    | 74.51          | 7.51          |
| Nordeste        | 485    | 4.42    | 74.02          | 7.01          |
| Sul             | 521    | 4.49    | 72.74          | 9.60          |


## Recomendação gerencial
- Criar uma régua de alerta para pedidos com atraso, reclamação ou múltiplos contatos com atendimento.
- Priorizar resolução rápida de problemas antes do envio da pesquisa NPS.
- Integrar logística e atendimento em uma fila única de recuperação de experiência.
- Acompanhar NPS previsto por operação, região e faixa de atraso para orientar ações preventivas.
