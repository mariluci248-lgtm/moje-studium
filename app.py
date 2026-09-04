import streamlit as st
import pandas as pd
import os
import io

st.set_page_config(page_title="Studijní Manažer BC", layout="wide")

st.title("🎓 Plánovač Bakalářského Studia (MA + INF)")
st.caption("UJEP | Kompletní studijní plán ze STAGu | S počítadlem kreditů i počtu předmětů")

VYCHOZI_DATA = """Kod,Nazev,Kredity,Typ,Semestr,STAG_Rocnik,Muj_Plan_Rocnik,Stav,Znamka,Profesor,Statnice,Prerekvizita
KI/KAPR1,Algoritmizace a programování I,4,A,ZS,1,1,Splněno,S,Škvor,Ano,-
KI/KMPG,Multimédia a základy počítačové grafiky,2,A,ZS,1,1,Splněno,S,Pecina,Ne,-
KI/KPCA,Architektura počítačů,4,A,ZS,1,1,Splněno,1,Škvor,Ano,-
KMA/KCA1,Matematická analýza I,6,A,ZS,1,2,Nesplněno,N,Eisenmann,Ano,-
KMA/KLAG,Lineární algebra,5,A,ZS,1,2,Nesplněno,N,Kuřil,Ano,-
KMA/KMT1,Matematika I,4,A,ZS,1,1,Splněno,S,Lacková,Ne,-
KMA/KZAM,Základy matematiky,5,A,ZS,1,2,Nesplněno,N,Eisenmann,Ano,-
KMA/MEX,Matematický exkurz,1,B,ZS,1,1,Nezačato,-,Katedra KMA,Ne,-
KMA/KRPC,Repetitorium matematiky,1,C,ZS,1,2,Nesplněno,N,Krupka,Ne,-
KFHS/KB305,Úvod do filozofie,2,A,LS,1,1,Splněno,S,Anderle,Ne,-
KI/KAPR2,Algoritmizace a programování II,5,A,LS,1,1,Zapsáno,S,Škvor,Ano,KI/KAPR1
KI/KMSW,Matematický software,2,A,LS,1,1,Splněno,S,Simonyi,Ne,-
KI/KZZD,Základy zpracování dat,2,A,LS,1,2,Nesplněno,N,Škvor,Ne,-
KMA/KAGE,Aplikovaná geometrie,5,A,LS,1,2,Nezačato,-,Katedra KMA,Ano,-
KMA/KCA2,Matematická analýza II,5,A,LS,1,2,Nezačato,-,Eisenmann,Ano,KMA/KCA1
KMA/KKGR,Kombinatorika a grafy,4,A,LS,1,2,Nesplněno,N,Krupka,Ano,-
KMA/KMT2,Matematika II,5,A,LS,1,1,Splněno,1,Lacková,Ne,-
KMA/KOPM,Odborné prezentace v matematice,1,A,LS,1,1,Splněno,S,Lacková,Ne,-
KMA/KAAP,Algebra s aplikacemi,4,B,LS,1,1,Splněno,3,Eisenmann,Ano,-
KMA/KLTX,Úvod do Latexu,2,B,LS,1,1,Splněno,S,Krupka,Ne,-
CJP/7210,Cizí jazyk I,2,A,ZS,2,2,Nezačato,-,Katedra CJP,Ne,-
CPPV/KPPOB,Příprava na pedagogickou praxi a oborové objevování,1,A,ZS,2,2,Nezačato,-,Katedra PP,Ne,-
KI/KIKT1,Informační a komunikační technologie I,1,A,ZS,2,2,Nezačato,-,Pecina,Ne,-
KI/KIKT2,Informační a komunikační technologie II,1,A,ZS,2,2,Nezačato,-,Pecina,Ne,-
KI/KNUM,Numerické metody,2,A,ZS,2,2,Nezačato,-,Katedra INF,Ne,-
KI/KTZI1,Teoretické základy informatiky I,4,A,ZS,2,2,Nezačato,-,Škvor,Ano,-
KI/KZEL,Základy elektroniky,4,A,ZS,2,2,Nezačato,-,Katedra INF,Ne,-
KMA/KGE1,Geometrie I,4,A,ZS,2,2,Nezačato,-,Eisenmann,Ano,KMA/KLAG
KMA/KPST,Pravděpodobnost a statistika,5,A,ZS,2,2,Nezačato,-,Lacková,Ano,-
KMA/KUSW,Úvod do softwaru pro matematiky,2,A,ZS,2,2,Nezačato,-,Katedra KMA,Ne,-
KPAD/7230,Pedagogika I,2,A,ZS,2,2,Nezačato,-,Katedra PAD,Ne,-
KPS/7230,Psychologie I,4,A,ZS,2,2,Nezačato,-,Katedra PS,Ne,-
CPPV/KKPP,Souvislá pedagogická praxe,1,A,LS,2,2,Nezačato,-,Katedra PP,Ne,-
KI/KOPS,Operační systémy,2,A,LS,2,2,Nezačato,-,Škvor,Ano,KI/KPCA
KI/KROB,Robotika ve výuce,2,A,LS,2,2,Nezačato,-,Pecina,Ne,-
KI/KTZI2,Teoretické základy informatiky II,3,A,LS,2,2,Nezačato,-,Škvor,Ano,KI/KTZI1
KI/KURDB,Úvod do databází,3,A,LS,2,2,Nezačato,-,Škvor,Ano,-
KI/KZKB,Základy kybernetické bezpečnosti,3,A,LS,2,2,Nezačato,-,Katedra INF,Ne,-
KMA/KALG,Algebra,5,A,LS,2,2,Nezačato,-,Kuřil,Ano,KMA/KLAG
KMA/KMA3,Matematická analýza III,5,A,LS,2,3,Nezačato,-,Eisenmann,Ano,KMA/KCA2
KMA/KMRU,Matematické rovnice a jejich užití,2,A,LS,2,2,Nezačato,-,Katedra KMA,Ne,-
KMA/KPSPP,Psychologie pro pedagogy,1,A,LS,2,2,Nezačato,-,Katedra PP,Ne,-
KPAD/7240,Pedagogika II,4,A,LS,2,2,Nezačato,-,Katedra PAD,Ne,-
KMA/KCAS,Časové řady a statistický software,2,B,LS,2,2,Nezačato,-,Lacková,Ne,-
CPPV/KAPP,Asistenční pedagogická praxe,2,A,ZS,3,3,Nezačato,-,Katedra PP,Ne,-
KI/KAIIT,Aplikovaná informatika a technologie,2,A,ZS,3,3,Nezačato,-,Katedra INF,Ne,-
KI/KANE,Počítačové sítě,2,A,ZS,3,3,Nezačato,-,Škvor,Ano,-
KI/KDPG,Didaktika programování,2,A,ZS,3,3,Nezačato,-,Pecina,Ne,KI/KAPR2
KI/KRDBS,Relační databázové systémy,4,A,ZS,3,3,Nezačato,-,Škvor,Ano,KI/KURDB
KI/KZPS,Zpracování signálů a obrazu,4,A,ZS,3,3,Nezačato,-,Katedra INF,Ne,-
KMA/KGE2,Geometrie II,6,A,ZS,3,3,Nezačato,-,Eisenmann,Ano,KMA/KGE1
KMA/KSBP,Seminář k bakalářské práci,2,A,ZS,3,3,Nezačato,-,Katedra KMA,Ne,-
KMA/KTAR,Teorie čísel a aritmetika,5,A,ZS,3,3,Nezačato,-,Kuřil,Ano,KMA/KZAM
KMA/KUDM,Úvod do diskrétní matematiky,3,A,ZS,3,3,Nezačato,-,Krupka,Ne,-
KI/KAIE,Informační etika,1,A,LS,3,3,Nezačato,-,Katedra INF,Ne,-
KI/KAOS,Pokročilé operační systémy,2,A,LS,3,3,Nezačato,-,Škvor,Ne,KI/KOPS
KI/KITP,Informační technologie v praxi,4,A,LS,3,3,Nezačato,-,Pecina,Ne,-
KI/KPGR,Počítačová grafika,3,A,LS,3,3,Nezačato,-,Pecina,Ne,-
KI/SZZIV,Státní závěrečná zkouška - Informatika,0,A,LS,3,3,Nezačato,-,Komise,Ano,-
KMA/BP2O,Bakalářská práce,6,A,LS,3,3,Nezačato,-,Katedra KMA,Ne,-
KMA/KAMU,Aplikace matematiky v umění,2,A,LS,3,3,Nezačato,-,Katedra KMA,Ne,-
KMA/KMSB,Matematické simulace a modelování,2,A,LS,3,3,Nezačato,-,Katedra KMA,Ne,-
KMA/KRSPP,Reflexe pedagogické praxe,1,A,LS,3,3,Nezačato,-,Katedra PP,Ne,-
KMA/SZZMV,Státní závěrečná zkouška - Matematika,0,A,LS,3,3,Nezačato,-,Komise,Ano,-
KMA/KTHE,Teorie grafů a heuristiky,5,B,LS,3,3,Nezačato,-,Krupka,Ne,-
KMA/SZZO,Státní závěrečná zkouška - Společný základ,0,A,X,4,4,Nezačato,-,Komise,Ano,-"""

SOUBOR = "studium_data.csv"

def nacti_data():
    if not os.path.exists(SOUBOR):
        with open(SOUBOR, "w", encoding="utf-8") as f:
            f.write(VYCHOZI_DATA)
    
    df = pd.read_csv(SOUBOR, encoding="utf-8")
    df.columns = df.columns.str.strip()
    
    if 'Prerekvizita' not in df.columns:
        df_ref = pd.read_csv(io.StringIO(VYCHOZI_DATA))
        df_ref.columns = df_ref.columns.str.strip()
        df = pd.merge(df, df_ref[['Kod', 'Prerekvizita']], on='Kod', how='left')
        df.to_csv(SOUBOR, index=False, encoding="utf-8")
        
    return df

df = nacti_data()

limit_r1 = 30
limit_r2 = 85
limit_r3 = 125

# ---------------------------------------------------------
# BOČNÍ PANEL (FILTRY)
# ---------------------------------------------------------
st.sidebar.header("🔍 Filtrovat předměty")

mozne_rocniky = [1, 2, 3, 4]
mozne_stavy = ["Splněno", "Zapsáno", "Nesplněno", "Nezačato"]
mozne_semestry = list(df['Semestr'].unique())
mozne_typy = list(df['Typ'].unique())

vybrany_rocnik = st.sidebar.multiselect("Filtrovat mé plánované ročníky:", options=mozne_rocniky, default=mozne_rocniky)
vybrany_stav = st.sidebar.multiselect("Stav předmětu:", options=mozne_stavy, default=mozne_stavy)
vybrany_semestr = st.sidebar.multiselect("Semestr:", options=mozne_semestry, default=mozne_semestry)
vybrany_typ = st.sidebar.multiselect("Typ (A/B/C):", options=mozne_typy, default=mozne_typy)

jen_statnice = st.sidebar.checkbox("🎓 Jen státnicové předměty")

st.sidebar.divider()

if st.sidebar.button("🔄 Resetovat na kompletní plán ze STAGu"):
    with open(SOUBOR, "w", encoding="utf-8") as f:
        f.write(VYCHOZI_DATA)
    st.rerun()

# ---------------------------------------------------------
# APLIKACE FILTRŮ
# ---------------------------------------------------------
df_filtrovano = df[
    (df['Muj_Plan_Rocnik'].isin(vybrany_rocnik)) &
    (df['Stav'].isin(vybrany_stav)) &
    (df['Semestr'].isin(vybrany_semestr)) &
    (df['Typ'].isin(vybrany_typ))
]

if jen_statnice:
    df_filtrovano = df_filtrovano[df_filtrovano['Statnice'] == 'Ano']

# ---------------------------------------------------------
# HORNÍ METRIKY (CELKOVÉ STUDIUM)
# ---------------------------------------------------------
ziskane_kredity = pd.to_numeric(df[df['Stav'] == 'Splněno']['Kredity'], errors='coerce').sum()
celkove_planovane = pd.to_numeric(df['Kredity'], errors='coerce').sum()
cil_kreditu = 180
procento = min(float(ziskane_kredity / cil_kreditu), 1.0)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Získané kredity (Celkem)", f"{int(ziskane_kredity)} / {cil_kreditu}")
col2.metric("Chybí do Bc. titulu", f"{int(cil_kreditu - ziskane_kredity)} kr.")
col3.metric("Celkem v plánu", f"{int(celkove_planovane)} kr.")
col4.metric("Splněno ze všech", f"{int(procento * 100)} %")

st.write("### Celkový postup studiem (Cíl: 180 kreditů)")
st.progress(procento)

st.divider()

# ---------------------------------------------------------
# KONTROLA PREREKVIZIT & KONTROLA LIMITŮ
# ---------------------------------------------------------
st.write("### 📋 Kontrola postupových podmínek a prerekvizit")

col_p1, col_p2, col_p3 = st.columns(3)

with col_p1:
    st.markdown("#### Postup do 2. ročníku")
    if ziskane_kredity >= limit_r1:
        st.success(f"✅ **SPLNĚNO!** Získala jsi {int(ziskane_kredity)} / {limit_r1} kreditů.")
    else:
        st.warning(f"⚠️ **NEDOSTATEK KREDITŮ.** Máš {int(ziskane_kredity)} kr. Chybí ti ještě **{int(limit_r1 - ziskane_kredity)} kr.** do minima ({limit_r1} kr.).")

with col_p2:
    st.markdown("#### Postup do 3. ročníku")
    if ziskane_kredity >= limit_r2:
        st.success(f"✅ **SPLNĚNO!** Máš {int(ziskane_kredity)} / {limit_r2} kreditů.")
    else:
        st.info(f"⏳ **Plánuje se.** Celkem získáno {int(ziskane_kredity)} kr. Do postupového minima ({limit_r2} kr.) chybí **{int(limit_r2 - ziskane_kredity)} kr.**")

with col_p3:
    st.markdown("#### Postup do 4. roč. (Bc.)")
    if ziskane_kredity >= limit_r3:
        st.success(f"✅ **SPLNĚNO!** Máš {int(ziskane_kredity)} / {limit_r3} kreditů.")
    else:
        st.info(f"⏳ **Plánuje se.** Celkem získáno {int(ziskane_kredity)} kr. Do hranice ({limit_r3} kr.) chybí **{int(limit_r3 - ziskane_kredity)} kr.**")

# Kontrola konfliktů v návaznostech
konflikty = []
kody_rocniky = dict(zip(df['Kod'], df['Muj_Plan_Rocnik']))
kody_stavy = dict(zip(df['Kod'], df['Stav']))

for idx, row in df.iterrows():
    prer = row['Prerekvizita']
    if prer != '-' and pd.notna(prer):
        if prer in kody_rocniky:
            prer_rocnik = kody_rocniky[prer]
            prer_stav = kody_stavy[prer]
            muj_rocnik = row['Muj_Plan_Rocnik']
            
            if muj_rocnik <= prer_rocnik and prer_stav != 'Splněno':
                konflikty.append(f"⚠️ **{row['Kod']} ({row['Nazev']})** máš v {muj_rocnik}. ročníku, ale jeho prerekvizitu **{prer}** plánuješ až do {prer_rocnik}. ročníku!")

if konflikty:
    st.error("### 🚨 Pozor na návaznosti (Prerekvizity)!")
    for k in konflikty:
        st.write(k)
else:
    st.success("✅ **Návaznosti jsou v pořádku!** Žádný předmět není naplánovaný dřív než jeho povinná prerekvizita.")

st.divider()

# ---------------------------------------------------------
# INTERAKTIVNÍ EDITOVATELNÁ TABULKA S POČTEM PŘEDMĚTŮ I KREDITŮ
# ---------------------------------------------------------
st.write("### ✏️ Nastavení mého ročníkového plánu, stavu předmětů a známek")

# DYNAMICKÉ VÝPOČTY (SOUČET KREDITŮ I POČET PŘEDMĚTŮ)
df_spl = df_filtrovano[df_filtrovano['Stav'] == 'Splněno']
df_zap = df_filtrovano[df_filtrovano['Stav'] == 'Zapsáno']
df_chyb = df_filtrovano[df_filtrovano['Stav'].isin(['Nezačato', 'Nesplněno'])]

pocet_celkem = len(df_filtrovano)
kredity_celkem = int(pd.to_numeric(df_filtrovano['Kredity'], errors='coerce').sum())

pocet_splneno = len(df_spl)
kredity_splneno = int(pd.to_numeric(df_spl['Kredity'], errors='coerce').sum())

pocet_zapsano = len(df_zap)
kredity_zapsano = int(pd.to_numeric(df_zap['Kredity'], errors='coerce').sum())

pocet_chybi = len(df_chyb)
kredity_chybi = int(pd.to_numeric(df_chyb['Kredity'], errors='coerce').sum())

# Přehledné kartičky ukazující jak Počet předmětů, tak Kredity
f_col1, f_col2, f_col3, f_col4 = st.columns(4)
f_col1.info(f"📊 **Celkem ve výběru:**\n\n**{pocet_celkem} předmětů** ({kredity_celkem} kr.)")
f_col2.success(f"🟢 **Splněno:**\n\n**{pocet_splneno} předmětů** ({kredity_splneno} kr.)")
f_col3.warning(f"🟠 **Zapsáno:**\n\n**{pocet_zapsano} předmětů** ({kredity_zapsano} kr.)")
f_col4.error(f"🔵 **Nezačato / Chybí:**\n\n**{pocet_chybi} předmětů** ({kredity_chybi} kr.)")

upravena_data = st.data_editor(
    df_filtrovano, 
    use_container_width=True,
    num_rows="dynamic",
    column_config={
        "Kod": st.column_config.TextColumn("Kód", disabled=True),
        "Nazev": st.column_config.TextColumn("Název předmětu", disabled=True),
        "Kredity": st.column_config.NumberColumn("Kredity", disabled=True),
        "STAG_Rocnik": st.column_config.NumberColumn("STAG Ročník", disabled=True),
        "Muj_Plan_Rocnik": st.column_config.SelectboxColumn("Můj plán (Ročník)", options=[1, 2, 3, 4], required=True),
        "Stav": st.column_config.SelectboxColumn("Stav", options=["Splněno", "Zapsáno", "Nesplněno", "Nezačato"], required=True),
        "Znamka": st.column_config.TextColumn("Známka"),
        "Semestr": st.column_config.SelectboxColumn("Semestr", options=["ZS", "LS", "X"], required=True),
        "Typ": st.column_config.SelectboxColumn("Typ", options=["A", "B", "C"], required=True),
        "Prerekvizita": st.column_config.TextColumn("Prerekvizita (Návaznost)", disabled=True)
    }
)

if not upravena_data.equals(df_filtrovano):
    df.update(upravena_data)
    df.to_csv(SOUBOR, index=False, encoding="utf-8")
    st.rerun()

st.divider()

# ---------------------------------------------------------
# ZOBRAZENÍ TABULKY S BAREVNÝM ODLIŠENÍM
# ---------------------------------------------------------
def barva_stavu(val):
    if val == 'Splněno':
        return 'color: #2e7d32; font-weight: bold;'
    elif val == 'Nesplněno':
        return 'color: #d32f2f; font-weight: bold;'
    elif val == 'Zapsáno':
        return 'color: #ed6c02; font-weight: bold;'
    elif val == 'Nezačato':
        return 'color: #0288d1;'
    return ''

st.write(f"### 📗 Přehledný barevný náhled předmětů ({len(df_filtrovano)} zobrazeno)")
stylovana_data = df_filtrovano.style.map(barva_stavu, subset=['Stav'])
st.dataframe(stylovana_data, use_container_width=True)

st.divider()

# ---------------------------------------------------------
# 1. SOUHRNNÁ TABULKA KREDITŮ PODLE ROČNÍKŮ
# ---------------------------------------------------------
st.write("### 📊 Souhrnná tabulka mého kreditového plánu (Po Ročnících)")

prehled_rocniky = []
for r in [1, 2, 3, 4]:
    df_r = df[df['Muj_Plan_Rocnik'] == r]
    splneno_r = df_r[df_r['Stav'] == 'Splněno']['Kredity'].sum()
    zapsano_r = df_r[df_r['Stav'] == 'Zapsáno']['Kredity'].sum()
    nezacato_r = df_r[df_r['Stav'].isin(['Nezačato', 'Nesplněno'])]['Kredity'].sum()
    celkem_r = df_r['Kredity'].sum()
    
    prehled_rocniky.append({
        "Plánovaný Ročník": f"{r}. ročník",
        "Počet předmětů": f"{len(df_r)} x",
        "Hotovo (Splněno)": f"{splneno_r} kr.",
        "Aktuálně Zapsáno": f"{zapsano_r} kr.",
        "Zbývá splnit / Nezačato": f"{nezacato_r} kr.",
        "Celkem kreditů": f"{celkem_r} kr."
    })

col_s1, col_s2 = st.columns([2, 1])
with col_s1:
    st.dataframe(pd.DataFrame(prehled_rocniky), use_container_width=True)
with col_s2:
    st.bar_chart(df.groupby('Muj_Plan_Rocnik')['Kredity'].sum())

st.divider()

# ---------------------------------------------------------
# 2. SOUHRNNÁ TABULKA: ROZPAD PODLE SEMESTRŮ (ZS / LS)
# ---------------------------------------------------------
st.write("### 🗓️ Detailní rozpad podle Semestrů (ZS / LS)")

prehled_semestry = []
for r in [1, 2, 3, 4]:
    for sem in ["ZS", "LS"]:
        df_rs = df[(df['Muj_Plan_Rocnik'] == r) & (df['Semestr'] == sem)]
        splneno_s = df_rs[df_rs['Stav'] == 'Splněno']['Kredity'].sum()
        zapsano_s = df_rs[df_rs['Stav'] == 'Zapsáno']['Kredity'].sum()
        nezacato_s = df_rs[df_rs['Stav'].isin(['Nezačato', 'Nesplněno'])]['Kredity'].sum()
        celkem_s = df_rs['Kredity'].sum()
        
        prehled_semestry.append({
            "Ročník a Semestr": f"{r}. ročník - {sem}",
            "Počet předmětů": f"{len(df_rs)} x",
            "Splněno": f"{splneno_s} kr.",
            "Zapsáno": f"{zapsano_s} kr.",
            "Nezačato / Chybí": f"{nezacato_s} kr.",
            "Celkem kreditů": f"{celkem_s} kr."
        })

df_sem_summary = pd.DataFrame(prehled_semestry)

col_sem1, col_sem2 = st.columns([2, 1])

with col_sem1:
    st.dataframe(df_sem_summary, use_container_width=True)

with col_sem2:
    df['Rocnik_Semestr'] = df['Muj_Plan_Rocnik'].astype(str) + ". roč - " + df['Semestr']
    st.bar_chart(df.groupby('Rocnik_Semestr')['Kredity'].sum())
csv_data = df.to_csv(index=False).encode('utf-8')

st.sidebar.download_button(
    label="📥 Stáhnout aktuální plán (CSV)",
    data=csv_data,
    file_name="studium_data.csv",
    mime="text/csv",
    help="Stáhne aktuální verzi souboru se všemi úpravami"
)