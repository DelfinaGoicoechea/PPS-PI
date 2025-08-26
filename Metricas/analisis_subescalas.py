import os
import re
import pandas as pd


def _extract_phase_parts(phase_value: str):
    """Extrae numero de fase y etapa (PRE/POST) desde valores como 'FASE 2 PRE'.
    Devuelve (fase_numero:int, etapa:str) o (None, None) si no coincide.
    """
    if pd.isna(phase_value):
        return None, None
    text = str(phase_value).strip()
    match = re.search(r"FASE\s*(\d+)\s*(PRE|POST)", text, flags=re.IGNORECASE)
    if not match:
        return None, None
    fase_num = int(match.group(1))
    etapa = match.group(2).upper()
    return fase_num, etapa




def _identify_subscale_columns(df: pd.DataFrame):
    """Identifica columnas de subescalas/metricas numericas a agregar.
    Excluye identificadores y columnas auxiliares de fase.
    """
    exclude = {"Participante", "Fase", "Fase_Numero", "Etapa"}
    candidate_cols = [c for c in df.columns if c not in exclude]

    numeric_cols = []
    for col in candidate_cols:
        # Intentar convertir a numerico para verificar
        coerced = pd.to_numeric(df[col], errors="coerce")
        if coerced.notna().any():
            numeric_cols.append(col)
    return numeric_cols


def _coerce_numeric_inplace(df: pd.DataFrame, columns: list[str]):
    for c in columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")


def _read_results_files(resultados_dir: str, base_name: str):
    """Lee archivo *_promedios.csv para la base dada."""
    path = os.path.join(resultados_dir, f"{base_name}_promedios.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"No existe el archivo de promedios: {path}")
    return pd.read_csv(path)


def _prepare_dataframe(df_unified: pd.DataFrame):
    """Normaliza columnas del archivo unico y asegura 'Media_Global'."""
    df = df_unified.copy()

    # Agregar fase descompuesta
    phases = df["Fase"].apply(_extract_phase_parts)
    df["Fase_Numero"] = phases.apply(lambda x: x[0])
    df["Etapa"] = phases.apply(lambda x: x[1])

    # Filtrar filas con fase parseada correctamente
    df = df[pd.notna(df["Fase_Numero"]) & pd.notna(df["Etapa"])].copy()
    df["Fase_Numero"] = df["Fase_Numero"].astype(int)
    df["Etapa"] = df["Etapa"].astype(str)
    return df


def _format_phase_label(fase_num, etapa: str):
    return f"{int(fase_num)} - {etapa.upper()}"


def calcular_estadisticas_por_fase(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Calcula media y desviacion estandar por subescala y fase (PRE/POST).
    Retorna dos DataFrames en formato ancho: (medias, desviaciones).
    """
    subscale_cols = _identify_subscale_columns(df)
    _coerce_numeric_inplace(df, subscale_cols)

    agrupado = df.groupby(["Fase_Numero", "Etapa"], dropna=False)[subscale_cols]
    mean_df = agrupado.mean().round(2).reset_index()
    std_df = agrupado.std(ddof=1).round(2).reset_index()

    # Etiqueta de fase "X - PRE/POST"
    mean_df["Fase"] = mean_df.apply(lambda r: _format_phase_label(r["Fase_Numero"], r["Etapa"]), axis=1)
    std_df["Fase"] = std_df.apply(lambda r: _format_phase_label(r["Fase_Numero"], r["Etapa"]), axis=1)

    medias = mean_df[["Fase", *subscale_cols]].copy()
    desvios = std_df[["Fase", *subscale_cols]].copy()
    medias.insert(0, "Medida", "Media")
    desvios.insert(0, "Medida", "DE")
    return medias, desvios


def calcular_diferencias_post_pre(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula diferencias de medias POST - PRE por subescala dentro de la misma fase.
    Retorna formato ancho con columnas de subescalas y fila por fase.
    """
    subscale_cols = _identify_subscale_columns(df)
    _coerce_numeric_inplace(df, subscale_cols)

    # Promedios por fase y etapa en una tabla pivote
    mean_df = df.groupby(["Fase_Numero", "Etapa"], dropna=False)[subscale_cols].mean()
    pivot = mean_df.unstack("Etapa")  # columnas multinivel: (subescala, PRE/POST)

    filas = []
    for fase_num, row in pivot.iterrows():
        # Saltar si falta PRE o POST
        if (subscale_cols[0], "PRE") not in row.index or (subscale_cols[0], "POST") not in row.index:
            continue
        dif = (row.xs("POST", level=1, axis=0) - row.xs("PRE", level=1, axis=0)).round(2)
        out = {"Medida": "Diferencia", "Fase": _format_phase_label(fase_num, "POST")}
        for col in subscale_cols:
            out[col] = float(dif[col]) if pd.notna(dif[col]) else pd.NA
        filas.append(out)

    return pd.DataFrame(filas)


def guardar_resultados(resultados_dir: str, base_name: str, df_media: pd.DataFrame, df_de: pd.DataFrame, df_diff: pd.DataFrame):
    os.makedirs(resultados_dir, exist_ok=True)
    combinado = pd.concat([df_media, df_de, df_diff], ignore_index=True)

    # Ordenar: primero PRE y luego POST por fase dentro de cada Medida
    # Extraer numero de fase y etapa desde columna Fase (ej: "2 - PRE")
    fase_num = combinado["Fase"].str.extract(r"^(\d+)\s*-\s*(PRE|POST)$", expand=True)
    combinado["_fase_num"] = pd.to_numeric(fase_num[0], errors="coerce").fillna(-1).astype(int)
    combinado["_etapa"] = fase_num[1].fillna("")
    etapa_order = {"PRE": 0, "POST": 1}
    combinado["_etapa_ord"] = combinado["_etapa"].map(etapa_order).fillna(9).astype(int)
    medida_order = {"Media": 0, "DE": 1, "Diferencia": 2}
    combinado["_medida_ord"] = combinado["Medida"].map(medida_order).fillna(9).astype(int)

    combinado = combinado.sort_values(by=["_medida_ord", "_fase_num", "_etapa_ord", "Fase"]).reset_index(drop=True)
    combinado = combinado.drop(columns=["_fase_num", "_etapa", "_etapa_ord", "_medida_ord"])

    out_path = os.path.join(resultados_dir, f"{base_name}_analisis.csv")
    combinado.to_csv(out_path, index=False, encoding="utf-8")
    print(f"Guardado: {out_path}")


def _listar_bases_disponibles(resultados_dir: str):
    if not os.path.exists(resultados_dir):
        return []
    bases = []
    for f in os.listdir(resultados_dir):
        if f.endswith("_promedios.csv"):
            bases.append(f.replace("_promedios.csv", ""))
    return sorted(bases)


def procesar_base(resultados_dir: str, base_name: str):
    df_unified = _read_results_files(resultados_dir, base_name)
    df = _prepare_dataframe(df_unified)
    df_media, df_de = calcular_estadisticas_por_fase(df)
    df_diff = calcular_diferencias_post_pre(df)
    guardar_resultados(resultados_dir, base_name, df_media, df_de, df_diff)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    datos_dir = os.path.join(script_dir, "Datos_autocompasion")
    resultados_dir = os.path.join(datos_dir, "Resultados")

    bases = _listar_bases_disponibles(resultados_dir)
    if not bases:
        print("No se encontraron archivos *_promedios.csv en la carpeta de resultados.")
        return

    if len(bases) == 1:
        seleccion = bases[0]
    else:
        print("Bases disponibles:")
        for i, b in enumerate(bases, 1):
            print(f"  {i}. {b}")
        try:
            choice = input("Seleccione una base por numero (o presione Enter para cancelar): ").strip()
            if not choice:
                print("Cancelado por el usuario.")
                return
            idx = int(choice)
            if 1 <= idx <= len(bases):
                seleccion = bases[idx - 1]
            else:
                print("Seleccion invalida.")
                return
        except Exception:
            print("Seleccion invalida.")
            return

    print(f"Procesando base: {seleccion}")
    try:
        procesar_base(resultados_dir, seleccion)
    except Exception as e:
        print(f"Error procesando {seleccion}: {e}")


if __name__ == "__main__":
    main()


