from helpers.application import app, api
from helpers.database import db
from helpers.CORS import cors

from resources.InstituicaoResource import (
    InstituicoesResource,
    InstituicaoResource,
    InstituicaoAnoResource,
    MatriculasPorEstadoResource
)
from resources.IndexResource import IndexResource
from resources.UFResource import UFsResource, UFResource
from resources.MesorregiaoResource import MesorregioesResource, MesorregiaoResource
from resources.MicrorregiaoResource import MicrorregioesResource, MicrorregiaoResource
from resources.MunicipioResource import MunicipiosResource, MunicipioResource

cors.init_app(app)

api.add_resource(IndexResource, '/')
api.add_resource(InstituicoesResource, "/instituicoes")
api.add_resource(InstituicaoResource, "/instituicoes/<int:CO_ENTIDADE>/<int:NU_ANO_CENSO>")
api.add_resource(InstituicaoAnoResource, "/instituicoes/<int:NU_ANO_CENSO>")
api.add_resource(MatriculasPorEstadoResource, "/matriculas-por-estado")
api.add_resource(UFsResource, "/ufs")
api.add_resource(UFResource, '/ufs/<int:CO_UF>')
api.add_resource(MesorregioesResource, '/mesorregioes')
api.add_resource(MesorregiaoResource, '/mesorregioes/<int:CO_MESORREGIAO>')
api.add_resource(MicrorregioesResource, '/microrregioes')
api.add_resource(MicrorregiaoResource, '/microrregioes/<int:CO_MICRORREGIAO>')
api.add_resource(MunicipiosResource, '/municipios')
api.add_resource(MunicipioResource, '/municipios/<int:CO_MUNICIPIO>')

if __name__ == "__main__":
    app.run(debug=True)
