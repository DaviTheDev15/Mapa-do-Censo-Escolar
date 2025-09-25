import json
import subprocess
import sys
from helpers.logging import logger
from helpers.database import db     
from helpers.application import app
from models.UF import UF
from models.Mesorregiao import Mesorregiao
from models.Microrregiao import Microrregiao
from models.Municipio import Municipio
from models.InstituicaoEnsino import InstituicaoEnsino


EXTRATORES = [
    "UFExtrator.py",
    "MesorregiaoExtrator.py",
    "MicrorregiaoExtrator.py",
    "MunicipioExtrator.py",
]


def run_script(script_name):
    print(f"Executando {script_name}...")
    result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Erro ao executar {script_name}:\n{result.stderr}")
        sys.exit(1)
    print(result.stdout)


with app.app_context():
    print("Tabelas já estão criadas!")


for script in EXTRATORES:
    run_script(script)


try:
    with open("instituicoes2023.json", "r", encoding="utf-8") as f:
        instituicoes = json.load(f)
except FileNotFoundError:
    logger.error("Arquivo instituicoes2023.json não encontrado.")
    exit(1)


with app.app_context():
    try:
        for inst in instituicoes:
            for campo in [
                'QT_MAT_BAS', 'QT_MAT_EJA', 'QT_MAT_ESP',
                'QT_MAT_FUND', 'QT_MAT_INF', 'QT_MAT_MED', 'QT_MAT_PROF'
            ]:
                inst[campo] = inst.get(campo) or 0


        chaves_existentes = set(
            db.session.query(
                InstituicaoEnsino.NU_ANO_CENSO,
                InstituicaoEnsino.CO_ENTIDADE
            ).all()
        )


        to_insert = []
        to_update = []


        for inst in instituicoes:
            chave = (inst['NU_ANO_CENSO'], inst['CO_ENTIDADE'])
            if chave in chaves_existentes:
                to_update.append(inst)
            else:
                to_insert.append(inst)


        if to_insert:
            print(f"Inserindo {len(to_insert)} instituições novas...")
            db.session.bulk_insert_mappings(InstituicaoEnsino, to_insert)

        if to_update:
            print(f"Atualizando {len(to_update)} instituições existentes...")
            db.session.bulk_update_mappings(InstituicaoEnsino, to_update)

        db.session.commit()
        print("Instituições inseridas/atualizadas com sucesso via bulk operations.")

    except Exception:
        db.session.rollback()
        logger.exception("Erro ao persistir instituições no banco com ORM")
