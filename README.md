# TCC — Ferramenta de Segmentação Automática e Visualização 3D de Tumores Cerebrais Utilizando ITK-SNAP

Este repositório contém os códigos, experimentos e materiais desenvolvidos no Trabalho de Conclusão de Curso de **Davi Lima**, cujo objetivo é a segmentação automática de tumores cerebrais em 4 regiões em imagens de ressonância magnética e sua integração com o software ITK SNAP para análise morfológica e volumétrica.

O trabalho explora diferentes configurações arquiteturais e estratégias de pré-processamento, avaliando seu impacto no desempenho da segmentação e no custo computacional.

---

## Estrutura do Repositório

A organização do projeto segue uma separação lógica entre dados, experimentos, treinamento final e interfaces gráficas:

- 1. Data/                  # Estrutura de dados, subsets e metadados
- 2. EDA/                  # Análises exploratórias dos dados
- 3. tests/                # Testes e experimentos preliminares
- 4. final_training/        # Treinamento final e inferência
- 5. GUI/                   # Interface gráfica do sistema
- Monografia_Davi_Lima.pdf # Documento final do TCC
- test_subset_*.xlsx       # Arquivos auxiliares de subsets
- README.md


Arquivos de grande porte, como volumes NIfTI (`.nii.gz`), pesos de modelos (`.pth`) e artefatos intermediários de treinamento **não são versionados**, conforme definido no `.gitignore`.

---

## Metodologia

O desenvolvimento foi conduzido majoritariamente em ambiente de nuvem, utilizando **Google Colab** e **Google Colab Enterprise**, com aceleração por GPU (NVIDIA Tesla T4 e NVIDIA A100).

Os principais experimentos realizados incluem:

- **Baseline nnU-Net 3D full resolution**
- **Redução de dimensionalidade via PCA** aplicada às modalidades de RM
- **Arquiteturas com Attention Gates**, avaliando o impacto da atenção espacial
- **Treinamento final em larga escala**, utilizando todo o conjunto BraTS disponível

As métricas de avaliação incluem Dice por classe tumoral e o **Pseudo Dice (EMA)** reportado durante o treinamento.

---

## Frameworks e Implementações Utilizadas

Este trabalho utiliza implementações consolidadas e amplamente validadas na literatura científica:

### nnU-Net (implementação oficial)
Implementação original proposta por Isensee et al., utilizada como base para os experimentos baseline e para o treinamento final.

**Referência:**

> Isensee, F., Jaeger, P. F., Kohl, S. A. A., Petersen, J., & Maier-Hein, K. H.  
> *nnU-Net: a self-configuring method for deep learning-based biomedical image segmentation*.  
> Nature Methods, 18(2), 203–211, 2021.

### Advanced nnU-Net (Attention Gates)
Para os experimentos com mecanismos de atenção espacial, foi utilizado o repositório **Advanced nnU-Net**, que estende o nnU-Net original com variações arquiteturais contendo *attention blocks*.

**Referência:**

> McConnell, N., Ndipenoch, N., Cao, Y., Miron, A., & Li, Y.  
> *Exploring advanced architectural variations of nnU-Net*.  
> Neurocomputing, 560, 126837, 2023.

### ITK-SNAP

A visualização tridimensional, inspeção qualitativa das segmentações e análises morfológicas foram realizadas utilizando o software ITK-SNAP, amplamente empregado em aplicações de segmentação médica interativa e semiautomática. O ITK-SNAP foi utilizado tanto para validação visual dos resultados quanto para apoio à interpretação clínica das regiões tumorais segmentadas.

> Yushkevich, P. A., Piven, J., Hazlett, H. C., Smith, R. G., Ho, S., Gee, J. C., & Gerig, G.  
> User-guided 3D active contour segmentation of anatomical structures: significantly improved efficiency and reliability.  
> NeuroImage, 31(3), 1116–1128, 2006.

---

## Reprodutibilidade

Todos os scripts responsáveis por:
- preparação do ambiente
- pré-processamento
- execução dos experimentos
- treinamento
- inferência

estão disponíveis neste repositório e documentados na monografia associada.  
A organização dos diretórios e a padronização seguem as convenções exigidas pelo nnU-Net, permitindo a reprodução dos experimentos mediante a disponibilização dos dados.

---

## Observações Importantes

- Os dados do BraTS **não são distribuídos neste repositório**, em conformidade com as diretrizes do desafio.
- O repositório contém apenas código, configurações e resultados agregados.
- Alguns experimentos foram interrompidos precocemente devido a limitações computacionais e de custo em nuvem, conforme detalhado no texto da monografia.

---

## Autor

**Davi Lima**  
Trabalho de Conclusão de Curso — Engenharia Elétrica

