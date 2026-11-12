#!/usr/bin/env python3
"""Prueba las contrasenas de un CSV contra un archivo ZIP local."""

import argparse
import csv
import sys
import zipfile
from pathlib import Path


def passwords_from_csv(csv_path: Path, column: str):
    with csv_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        if not reader.fieldnames or column not in reader.fieldnames:
            available = ", ".join(reader.fieldnames or [])
            raise ValueError(
                f'No se encontro la columna "{column}". Columnas disponibles: {available}'
            )

        seen = set()
        for row in reader:
            password = (row.get(column) or "").strip()
            if password and password not in seen:
                seen.add(password)
                yield password


def password_is_valid(archive: zipfile.ZipFile, password: str) -> bool:
    encrypted_file = next(
        (
            info
            for info in archive.infolist()
            if not info.is_dir() and info.flag_bits & 0x1
        ),
        None,
    )
    if encrypted_file is None:
        raise ValueError("El ZIP no contiene archivos cifrados.")

    try:
        with archive.open(encrypted_file, pwd=password.encode("utf-8")) as member:
            member.read(1)
    except RuntimeError as error:
        if "password" in str(error).lower() or "encrypted" in str(error).lower():
            return False
        raise

    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Prueba contrasenas de un CSV contra un ZIP sin extraerlo."
    )
    parser.add_argument("zip_path", type=Path, help="Ruta al archivo ZIP")
    parser.add_argument("csv_path", type=Path, help="Ruta al CSV de contrasenas")
    parser.add_argument(
        "--column",
        default="Password",
        help='Nombre de la columna del CSV (predeterminado: "Password")',
    )
    args = parser.parse_args()

    try:
        with zipfile.ZipFile(args.zip_path) as archive:
            for attempt, password in enumerate(
                passwords_from_csv(args.csv_path, args.column), start=1
            ):
                if password_is_valid(archive, password):
                    print(f"Contrasena encontrada en el intento {attempt}: {password}")
                    return 0
    except (OSError, ValueError, zipfile.BadZipFile, zipfile.LargeZipFile) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2

    print("No se encontro una contrasena valida en el CSV.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
