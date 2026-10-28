import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd


class AppEleicoesUnicoArquivo:

    def __init__(self, root):
        self.root = root
        self.root.title("Comparativo de Eleições - 1º Turno vs 2º Turno (Arquivo Único)")
        self.root.geometry("1000x650")

        # Criando o sistema de abas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # Configuração das abas
        self.aba_geral = ttk.Frame(self.notebook)
        self.aba_estado = ttk.Frame(self.notebook)
        self.aba_municipio = ttk.Frame(self.notebook)
        self.aba_local = ttk.Frame(self.notebook)
        self.aba_candidato = ttk.Frame(self.notebook)
        self.aba_cem_pct = ttk.Frame(self.notebook)

        self.notebook.add(self.aba_geral, text="Total Geral (BR)")
        self.notebook.add(self.aba_estado, text="Por Estado (UF)")
        self.notebook.add(self.aba_municipio, text="Por Município")
        self.notebook.add(self.aba_local, text="Por Local de Votação")
        self.notebook.add(self.aba_candidato, text="Desempenho Candidato")
        self.notebook.add(self.aba_cem_pct, text="100% dos Votos (2ºT)")

        # Setup das interfaces
        self._setup_aba_geral()
        self._setup_aba_estado()
        self._setup_aba_municipio()
        self._setup_aba_local()
        self._setup_aba_candidato()
        self._setup_aba_cem_pct()

        # Carregamento e processamento dos dados
        self.carregar_dados()

    # --- ESTRUTURA DAS ABAS ---
    def _setup_aba_geral(self):
        lbl = tk.Label(
            self.aba_geral,
            text="Resultado Total do País (1º vs 2º Turno)",
            font=("Arial", 12, "bold"),
        )
        lbl.pack(pady=10)

        self.tabela_geral = self._criar_tabela(
            self.aba_geral,
            ("Candidato", "1º Turno", "2º Turno", "Diferença", "Variação %"),
            [320, 140, 140, 140, 120],
        )

    def _setup_aba_estado(self):
        lbl = tk.Label(
            self.aba_estado,
            text="Comparativo por Estado (UF)",
            font=("Arial", 12, "bold"),
        )
        lbl.pack(pady=10)

        frame_top = tk.Frame(self.aba_estado)
        frame_top.pack(fill="x", padx=15, pady=5)

        tk.Label(frame_top, text="Selecione o Estado:").pack(
            side="left", padx=5
        )
        self.combo_uf = ttk.Combobox(
            frame_top, state="readonly", font=("Arial", 10), width=10
        )
        self.combo_uf.pack(side="left", padx=5)
        self.combo_uf.bind("<<ComboboxSelected>>", self.exibir_votos_uf)

        self.tabela_uf = self._criar_tabela(
            self.aba_estado,
            ("Candidato", "1º Turno", "2º Turno", "Diferença", "Variação %"),
            [320, 140, 140, 140, 120],
        )

    def _setup_aba_municipio(self):
        lbl = tk.Label(
            self.aba_municipio,
            text="Comparativo por Município",
            font=("Arial", 12, "bold"),
        )
        lbl.pack(pady=10)

        frame_top = tk.Frame(self.aba_municipio)
        frame_top.pack(fill="x", padx=15, pady=5)

        tk.Label(frame_top, text="Estado:").pack(side="left", padx=2)
        self.combo_mun_uf = ttk.Combobox(
            frame_top, state="readonly", width=8, font=("Arial", 10)
        )
        self.combo_mun_uf.pack(side="left", padx=5)
        self.combo_mun_uf.bind("<<ComboboxSelected>>", self._atualizar_mun_list)

        tk.Label(frame_top, text="Filtrar Município:").pack(side="left", padx=5)
        self.ent_busca_mun = tk.Entry(frame_top, font=("Arial", 10))
        self.ent_busca_mun.pack(side="left", fill="x", expand=True, padx=5)
        self.ent_busca_mun.bind("<KeyRelease>", self.filtrar_municipios)

        self.combo_mun = ttk.Combobox(
            self.aba_municipio, state="readonly", font=("Arial", 10)
        )
        self.combo_mun.pack(fill="x", padx=15, pady=5)
        self.combo_mun.bind("<<ComboboxSelected>>", self.exibir_votos_mun)

        self.tabela_mun = self._criar_tabela(
            self.aba_municipio,
            ("Candidato", "1º Turno", "2º Turno", "Diferença", "Variação %"),
            [320, 140, 140, 140, 120],
        )

    def _setup_aba_local(self):
        lbl = tk.Label(
            self.aba_local,
            text="Comparativo por Local de Votação (Escola/Colégio)",
            font=("Arial", 12, "bold"),
        )
        lbl.pack(pady=10)

        frame_top = tk.Frame(self.aba_local)
        frame_top.pack(fill="x", padx=15, pady=5)

        tk.Label(frame_top, text="UF:").pack(side="left", padx=2)
        self.combo_loc_uf = ttk.Combobox(
            frame_top, state="readonly", width=5, font=("Arial", 10)
        )
        self.combo_loc_uf.pack(side="left", padx=5)
        self.combo_loc_uf.bind("<<ComboboxSelected>>", self._atualizar_loc_mun)

        tk.Label(frame_top, text="Município:").pack(side="left", padx=2)
        self.combo_loc_mun = ttk.Combobox(
            frame_top, state="readonly", font=("Arial", 10), width=22
        )
        self.combo_loc_mun.pack(side="left", padx=5)
        self.combo_loc_mun.bind(
            "<<ComboboxSelected>>", self._atualizar_loc_escolas
        )

        tk.Label(frame_top, text="Local:").pack(side="left", padx=2)
        self.combo_loc_escola = ttk.Combobox(
            frame_top, state="readonly", font=("Arial", 10)
        )
        self.combo_loc_escola.pack(side="left", fill="x", expand=True, padx=5)
        self.combo_loc_escola.bind(
            "<<ComboboxSelected>>", self.exibir_votos_local
        )

        self.tabela_loc = self._criar_tabela(
            self.aba_local,
            ("Candidato", "1º Turno", "2º Turno", "Diferença", "Variação %"),
            [320, 140, 140, 140, 120],
        )

    def _setup_aba_candidato(self):
        lbl = tk.Label(
            self.aba_candidato,
            text="Locais com Maior Crescimento/Diferença do Candidato",
            font=("Arial", 12, "bold"),
        )
        lbl.pack(pady=10)

        frame_top = tk.Frame(self.aba_candidato)
        frame_top.pack(fill="x", padx=15, pady=5)

        tk.Label(frame_top, text="Candidato:").pack(side="left", padx=5)
        self.combo_cand = ttk.Combobox(
            frame_top, state="readonly", font=("Arial", 10)
        )
        self.combo_cand.pack(side="left", fill="x", expand=True, padx=5)
        self.combo_cand.bind(
            "<<ComboboxSelected>>", self.exibir_desempenho_candidato
        )

        self.tabela_cand = self._criar_tabela(
            self.aba_candidato,
            (
                "UF",
                "Município",
                "Local de Votação",
                "1º Turno",
                "2º Turno",
                "Diferença",
                "Variação %",
            ),
            [40, 150, 260, 90, 90, 90, 80],
        )

    def _setup_aba_cem_pct(self):
        lbl = tk.Label(
            self.aba_cem_pct,
            text="Seções onde o Candidato obteve 100% dos Votos (Apenas 2º Turno)",
            font=("Arial", 12, "bold"),
        )
        lbl.pack(pady=10)

        frame_top = tk.Frame(self.aba_cem_pct)
        frame_top.pack(fill="x", padx=15, pady=5)

        tk.Label(frame_top, text="Selecione o Candidato:").pack(side="left", padx=5)
        self.combo_cem_cand = ttk.Combobox(
            frame_top, state="readonly", font=("Arial", 10)
        )
        self.combo_cem_cand.pack(side="left", fill="x", expand=True, padx=5)
        self.combo_cem_cand.bind(
            "<<ComboboxSelected>>", self.exibir_secoes_cem_pct
        )

        self.lbl_total_secoes = tk.Label(
            self.aba_cem_pct, text="Total de Seções: 0", font=("Arial", 10, "italic")
        )
        self.lbl_total_secoes.pack(pady=2)

        self.tabela_cem = self._criar_tabela(
            self.aba_cem_pct,
            ("UF", "Município", "Zona", "Seção", "Local de Votação", "Total Votos (100%)"),
            [50, 180, 80, 80, 320, 120],
        )

    def _criar_tabela(self, parent, colunas, larguras):
        frame = tk.Frame(parent)
        frame.pack(fill="both", expand=True, padx=15, pady=10)

        sb = ttk.Scrollbar(frame, orient="vertical")
        sb.pack(side="right", fill="y")

        tabela = ttk.Treeview(
            frame, columns=colunas, show="headings", yscrollcommand=sb.set
        )
        sb.config(command=tabela.yview)

        for col, larg in zip(colunas, larguras):
            tabela.heading(col, text=col)
            alinhamento = "w" if larg > 150 else "e" if larg <= 120 else "center"
            tabela.column(col, anchor=alinhamento, width=larg)

        tabela.pack(fill="both", expand=True)
        return tabela

    # --- PROCESSAMENTO DOS DADOS ---
    def _agrupar_por_turno(self, df, chaves):
        if chaves:
            df_t1 = df[df["NR_TURNO"] == 1].groupby(chaves + ["NM_VOTAVEL"])["QT_VOTOS"].sum().reset_index()
            df_t2 = df[df["NR_TURNO"] == 2].groupby(chaves + ["NM_VOTAVEL"])["QT_VOTOS"].sum().reset_index()
            on_cols = chaves + ["NM_VOTAVEL"]
        else:
            df_t1 = df[df["NR_TURNO"] == 1].groupby("NM_VOTAVEL")["QT_VOTOS"].sum().reset_index()
            df_t2 = df[df["NR_TURNO"] == 2].groupby("NM_VOTAVEL")["QT_VOTOS"].sum().reset_index()
            on_cols = ["NM_VOTAVEL"]

        merged = pd.merge(
            df_t1,
            df_t2,
            on=on_cols,
            how="outer",
            suffixes=("_T1", "_T2"),
        ).fillna(0)

        merged["DIFERENCA"] = merged["QT_VOTOS_T2"] - merged["QT_VOTOS_T1"]

        def calc_pct(row):
            t1 = row["QT_VOTOS_T1"]
            t2 = row["QT_VOTOS_T2"]
            if t1 == 0:
                return 100.0 if t2 > 0 else 0.0
            return ((t2 - t1) / t1) * 100.0

        merged["VARIACAO_PCT"] = merged.apply(calc_pct, axis=1)
        return merged

    def carregar_dados(self):
        nome_arquivo = "votacao_secao_2026_BR.csv"
        colunas = [
            "NR_TURNO",
            "SG_UF",
            "NM_MUNICIPIO",
            "NR_ZONA",
            "NR_SECAO",
            "NM_LOCAL_VOTACAO",
            "NM_VOTAVEL",
            "QT_VOTOS",
        ]

        try:
            df = pd.read_csv(
                nome_arquivo,
                usecols=colunas,
                sep=";",
                encoding="latin1",
                low_memory=False,
            )

            df["QT_VOTOS"] = pd.to_numeric(df["QT_VOTOS"], errors="coerce").fillna(0)
            df["NR_TURNO"] = pd.to_numeric(df["NR_TURNO"], errors="coerce").fillna(0)

            # 0. Total Geral (Brasil inteiro)
            self.df_geral = self._agrupar_por_turno(df, [])

            # 1. Agrupamento Estado (UF)
            self.df_uf = self._agrupar_por_turno(df, ["SG_UF"])

            # 2. Agrupamento Município
            self.df_mun = self._agrupar_por_turno(df, ["SG_UF", "NM_MUNICIPIO"])

            # 3. Agrupamento Local de Votação
            self.df_local = self._agrupar_por_turno(df, ["SG_UF", "NM_MUNICIPIO", "NM_LOCAL_VOTACAO"])

            # 4. Processamento Específico para Seções com 100% dos votos (Apenas 2º Turno)
            df_t2 = df[df["NR_TURNO"] == 2].copy()

            # Votos por candidato em cada seção/zona
            votos_secao_cand = (
                df_t2.groupby(["SG_UF", "NM_MUNICIPIO", "NR_ZONA", "NR_SECAO", "NM_LOCAL_VOTACAO", "NM_VOTAVEL"])["QT_VOTOS"]
                .sum()
                .reset_index()
            )

            # Total de votos da seção inteira
            totais_secao = (
                df_t2.groupby(["SG_UF", "NM_MUNICIPIO", "NR_ZONA", "NR_SECAO"])["QT_VOTOS"]
                .sum()
                .reset_index()
                .rename(columns={"QT_VOTOS": "TOTAL_SECAO"})
            )

            # Merge para identificar 100%
            merged_secoes = pd.merge(
                votos_secao_cand, totais_secao, on=["SG_UF", "NM_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
            )

            # Considera 100% se a quantidade de votos do candidato for igual ao total da seção (e total > 0)
            self.df_cem_pct = merged_secoes[
                (merged_secoes["QT_VOTOS"] == merged_secoes["TOTAL_SECAO"]) & (merged_secoes["TOTAL_SECAO"] > 0)
            ]

            # Exibir Total Geral
            self.exibir_votos_geral()

            # Povoar seletores
            ufs = sorted(self.df_uf["SG_UF"].unique().tolist())
            self.combo_uf["values"] = ufs
            self.combo_mun_uf["values"] = ufs
            self.combo_loc_uf["values"] = ufs

            candidatos = sorted(self.df_local["NM_VOTAVEL"].unique().tolist())
            self.combo_cand["values"] = candidatos
            self.combo_cem_cand["values"] = candidatos

            if ufs:
                self.combo_uf.current(0)
                self.exibir_votos_uf()
                self.combo_mun_uf.current(0)
                self._atualizar_mun_list()
                self.combo_loc_uf.current(0)
                self._atualizar_loc_mun()

            if candidatos:
                self.combo_cand.current(0)
                self.exibir_desempenho_candidato()
                self.combo_cem_cand.current(0)
                self.exibir_secoes_cem_pct()

        except FileNotFoundError:
            messagebox.showerror(
                "Erro de Arquivo",
                f"O arquivo '{nome_arquivo}' não foi encontrado na mesma pasta do script.",
            )
        except Exception as e:
            messagebox.showerror("Erro ao carregar dados", str(e))

    # --- EXIBIÇÃO NAS TABELAS ---
    def _preencher_tabela_comparativa(self, tabela, dataframe):
        for item in tabela.get_children():
            tabela.delete(item)

        for index, row in dataframe.iterrows():
            v1 = f"{int(row['QT_VOTOS_T1']):,}".replace(",", ".")
            v2 = f"{int(row['QT_VOTOS_T2']):,}".replace(",", ".")

            dif = int(row["DIFERENCA"])
            sinal = "+" if dif > 0 else ""
            dif_str = f"{sinal}{dif:,}".replace(",", ".")

            pct = row["VARIACAO_PCT"]
            sinal_pct = "+" if pct > 0 else ""
            pct_str = f"{sinal_pct}{pct:.2f}%".replace(".", ",")

            tabela.insert(
                "",
                "end",
                values=(row["NM_VOTAVEL"], v1, v2, dif_str, pct_str),
            )

    def exibir_votos_geral(self):
        dados = self.df_geral.sort_values(by="QT_VOTOS_T2", ascending=False)
        self._preencher_tabela_comparativa(self.tabela_geral, dados)

    def exibir_votos_uf(self, event=None):
        uf = self.combo_uf.get()
        dados = self.df_uf[self.df_uf["SG_UF"] == uf].sort_values(
            by="QT_VOTOS_T2", ascending=False
        )
        self._preencher_tabela_comparativa(self.tabela_uf, dados)

    def _atualizar_mun_list(self, event=None):
        uf = self.combo_mun_uf.get()
        muns = sorted(
            self.df_mun[self.df_mun["SG_UF"] == uf]["NM_MUNICIPIO"]
            .unique()
            .tolist()
        )
        self.combo_mun["values"] = muns
        if muns:
            self.combo_mun.current(0)
            self.exibir_votos_mun()

    def filtrar_municipios(self, event=None):
        uf = self.combo_mun_uf.get()
        texto = self.ent_busca_mun.get().strip().upper()
        todos = sorted(
            self.df_mun[self.df_mun["SG_UF"] == uf]["NM_MUNICIPIO"]
            .unique()
            .tolist()
        )
        filtrados = [m for m in todos if texto in str(m)] if texto else todos
        self.combo_mun["values"] = filtrados
        if filtrados:
            self.combo_mun.current(0)
            self.exibir_votos_mun()

    def exibir_votos_mun(self, event=None):
        uf = self.combo_mun_uf.get()
        mun = self.combo_mun.get()
        dados = self.df_mun[
            (self.df_mun["SG_UF"] == uf) & (self.df_mun["NM_MUNICIPIO"] == mun)
        ].sort_values(by="QT_VOTOS_T2", ascending=False)
        self._preencher_tabela_comparativa(self.tabela_mun, dados)

    def _atualizar_loc_mun(self, event=None):
        uf = self.combo_loc_uf.get()
        muns = sorted(
            self.df_local[self.df_local["SG_UF"] == uf]["NM_MUNICIPIO"]
            .unique()
            .tolist()
        )
        self.combo_loc_mun["values"] = muns
        if muns:
            self.combo_loc_mun.current(0)
            self._atualizar_loc_escolas()

    def _atualizar_loc_escolas(self, event=None):
        uf = self.combo_loc_uf.get()
        mun = self.combo_loc_mun.get()
        escolas = sorted(
            self.df_local[
                (self.df_local["SG_UF"] == uf)
                & (self.df_local["NM_MUNICIPIO"] == mun)
            ]["NM_LOCAL_VOTACAO"]
            .unique()
            .tolist()
        )
        self.combo_loc_escola["values"] = escolas
        if escolas:
            self.combo_loc_escola.current(0)
            self.exibir_votos_local()

    def exibir_votos_local(self, event=None):
        uf = self.combo_loc_uf.get()
        mun = self.combo_loc_mun.get()
        loc = self.combo_loc_escola.get()
        dados = self.df_local[
            (self.df_local["SG_UF"] == uf)
            & (self.df_local["NM_MUNICIPIO"] == mun)
            & (self.df_local["NM_LOCAL_VOTACAO"] == loc)
        ].sort_values(by="QT_VOTOS_T2", ascending=False)
        self._preencher_tabela_comparativa(self.tabela_loc, dados)

    def exibir_desempenho_candidato(self, event=None):
        cand = self.combo_cand.get()
        dados = self.df_local[self.df_local["NM_VOTAVEL"] == cand].sort_values(
            by="DIFERENCA", ascending=False
        )

        for item in self.tabela_cand.get_children():
            self.tabela_cand.delete(item)

        for index, row in dados.iterrows():
            v1 = f"{int(row['QT_VOTOS_T1']):,}".replace(",", ".")
            v2 = f"{int(row['QT_VOTOS_T2']):,}".replace(",", ".")

            dif = int(row["DIFERENCA"])
            sinal = "+" if dif > 0 else ""
            dif_str = f"{sinal}{dif:,}".replace(",", ".")

            pct = row["VARIACAO_PCT"]
            sinal_pct = "+" if pct > 0 else ""
            pct_str = f"{sinal_pct}{pct:.2f}%".replace(".", ",")

            self.tabela_cand.insert(
                "",
                "end",
                values=(
                    row["SG_UF"],
                    row["NM_MUNICIPIO"],
                    row["NM_LOCAL_VOTACAO"],
                    v1,
                    v2,
                    dif_str,
                    pct_str,
                ),
            )

    def exibir_secoes_cem_pct(self, event=None):
        cand = self.combo_cem_cand.get()
        dados = self.df_cem_pct[self.df_cem_pct["NM_VOTAVEL"] == cand].sort_values(
            by=["SG_UF", "NM_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
        )

        for item in self.tabela_cem.get_children():
            self.tabela_cem.delete(item)

        total = len(dados)
        self.lbl_total_secoes.config(text=f"Total de Seções com 100% de Votos: {total}")

        for index, row in dados.iterrows():
            votos = f"{int(row['QT_VOTOS']):,}".replace(",", ".")
            self.tabela_cem.insert(
                "",
                "end",
                values=(
                    row["SG_UF"],
                    row["NM_MUNICIPIO"],
                    row["NR_ZONA"],
                    row["NR_SECAO"],
                    row["NM_LOCAL_VOTACAO"],
                    votos,
                ),
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = AppEleicoesUnicoArquivo(root)
    root.mainloop()