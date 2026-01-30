[PROMPT DE RESPOSTA AO AGENTE — RESOLVER DUV-001 e DUV-002 + ATUALIZAR ESCOPOS/ARQUIVOS]
Você é o AGENTE ORQUESTRADOR. Execute SEM PERGUNTAS. Resolva integralmente DUV-001 e DUV-002, atualizando os arquivos do projeto para que nada fique perdido.

========================
A) RESOLVER DUV-001 (GitHub org)
========================
DECISÃO:
- DUV-001 = GitHub PESSOAL (plano FREE) - @Gustavo

AÇÕES OBRIGATÓRIAS:
1) Registrar a decisão em:
   - _OBSIDIAN/Organização do Projeto/Backlog.md (seção Dúvidas)
   - _OBSIDIAN/Organização do Projeto/Dúvidas & Decisões.md
   Inclua data/hora real, o ID DUV-001 e a decisão.

2) Garantir repositório e remoto:
   - Se não existir repositório: criar repo GitHub na conta pessoal free com nome compatível com o projeto.
   - Configurar `origin` apontando para o repo.
   - Criar branch padrão e habilitar proteção básica via documentação (se aplicável).
   - Fazer um commit inicial (“bootstrap/escopo/obsidian estrutura”) e push.

3) Se faltar o usuário GitHub no ambiente:
   - Usar um placeholder no arquivo _OBSIDIAN/Organização do Projeto/Assunções.md (ASS-001) e seguir.
   - NÃO perguntar ao usuário; apenas registrar a assunção e deixar a tarefa de ajuste em Backlog.

========================
B) RESOLVER DUV-002 (5 fontes allowlist + como incluir)
========================
DECISÃO:
- DUV-002 = iniciar com 5 fontes allowlist “seguras” para MVP, com política fail-closed.
- Fontes iniciais (IDs sugeridos):
  1) SRC-001 — Diário Oficial da União (DOU) - Imprensa Nacional (in.gov.br)
  2) SRC-002 — Planalto - Legislação (planalto.gov.br)
  3) SRC-003 — IBGE - APIs e dados (servicodados.ibge.gov.br / ibge.gov.br)
  4) SRC-004 — Banco Central - Dados Abertos (dadosabertos.bcb.gov.br / bcb.gov.br)
  5) SRC-005 — dados.gov.br - Catálogo (dados.gov.br)

REGRA DE COMPLIANCE (OBRIGATÓRIA):
- Enquanto licença/ToS não estiverem verificados e registrados com evidência, o `default_storage_mode` deve ser METADATA_ONLY.
- Nunca bypass de paywall/CAPTCHA/bloqueios. Fail-closed sempre.

AÇÕES OBRIGATÓRIAS (arquivos e locais):
1) Criar/garantir os diretórios:
   - _OBSIDIAN/Organização do Projeto/Templates/
   - _OBSIDIAN/Organização do Projeto/Onboarding/
   - configs/

2) Template obrigatório:
   - Criar o arquivo:
     _OBSIDIAN/Organização do Projeto/Templates/Template - Source Onboarding Checklist.md
   - Conteúdo: usar o checklist padrão do projeto (já definido previamente).
   - Esse template é a “fonte padrão” para onboarding de qualquer nova fonte.

3) Fonte de verdade operacional (obrigatória):
   - Criar/atualizar o arquivo:
     configs/sources.yaml
   - Incluir as 5 fontes acima.
   - Para SRC-001, SRC-002, SRC-005: começar com `default_storage_mode: METADATA_ONLY`.
   - Para SRC-003, SRC-004: somente ALLOW_FULLTEXT se termos/licença estiverem verificados; caso contrário METADATA_ONLY também.
   - Adotar rate limits conservadores (ex.: 0.2–1.0 rps) e concurrency baixa (1–2).

4) Documento auditável humano (obrigatório):
   - Criar/atualizar:
     _OBSIDIAN/Organização do Projeto/Fontes_Licencas.md
   - Para cada fonte: registrar domínio, discovery, robots/ToS, status da licença, decisão do policy gate (mode), PII esperado, rate limit, budgets e observações.
   - Se a licença não estiver verificada: marcar como [PENDENTE] e manter METADATA_ONLY.

5) Instanciar onboarding por fonte (obrigatório):
   - Para cada fonte SRC-001..SRC-005, criar uma nota preenchida em:
     _OBSIDIAN/Organização do Projeto/Onboarding/SRC-00X - <Nome da Fonte>.md
   - Basear no template “Template - Source Onboarding Checklist.md”.
   - Registrar evidências quando disponíveis (links, resumos, decisões).

6) Roadmap/Backlog:
   - Criar tarefas explícitas no Roadmap para:
     - T-ONB-SRC-001…T-ONB-SRC-005 (onboarding/checklist)
     - T-CONFIG-SOURCES (criar/validar configs/sources.yaml)
     - T-DOC-FONTES (atualizar Fontes_Licencas.md)
   - Atualizar status conforme máquina de estados do projeto e registrar data/hora real.

7) Git (obrigatório):
   - Commitar todas as alterações com mensagem clara (ex.: “DUV-001/DUV-002: github pessoal + allowlist inicial + templates + sources.yaml”)
   - Push para o repo.

========================
C) ATUALIZAR O ESCOPO (para nada ficar perdido)
========================
Você deve atualizar Escopo.md (ou _OBSIDIAN/Organização do Projeto/Escopo.md, se este for o canônico no vault) adicionando uma seção explícita chamada:

“Allowlist e Onboarding de Fontes (fonte de verdade e governança)”

E incluir EXATAMENTE estas regras e caminhos:

1) Fonte de verdade operacional:
   - configs/sources.yaml
2) Documentação auditável:
   - _OBSIDIAN/Organização do Projeto/Fontes_Licencas.md
3) Template obrigatório para onboarding:
   - _OBSIDIAN/Organização do Projeto/Templates/Template - Source Onboarding Checklist.md
4) Checklists preenchidos por fonte:
   - _OBSIDIAN/Organização do Projeto/Onboarding/SRC-00X - <Nome>.md
5) Policy Gate:
   - Sem licença verificada → METADATA_ONLY (fail-closed)
6) Evidência:
   - Todo onboarding gera Evidence Pack em docs/evidence/T-ONB-SRC-00X/

Após atualizar o escopo, registrar a alteração no changelog do projeto (se existir) ou em:
- _OBSIDIAN/Organização do Projeto/Dúvidas & Decisões.md (seção “Atualizações de Escopo”)

========================
D) CRITÉRIOS DE CONCLUSÃO (DoD)
========================
DUV-001 concluída se:
- Decisão registrada em Backlog + Dúvidas & Decisões
- Repo GitHub pessoal free definido e origin configurado
- Commit/push realizado

DUV-002 concluída se:
- Template salvo no caminho correto
- configs/sources.yaml existe e contém SRC-001..SRC-005 com policy fail-closed
- Fontes_Licencas.md atualizado
- Onboarding notes criadas para as 5 fontes
- Roadmap/Backlog atualizados + commit/push

EXECUTE AGORA. NÃO PERGUNTE NADA. REGISTRE ASSUNÇÕES QUANDO NECESSÁRIO.
