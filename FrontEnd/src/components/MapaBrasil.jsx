import React, { useState, useEffect } from "react";
import {
  ComposableMap,
  Geographies,
  Geography,
} from "react-simple-maps";
import { scaleLinear } from "d3-scale";
import "./MapaBrasil.css";

const BRAZIL_TOPOJSON =
  "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson";

const estadosSiglaNome = {
  AC: "Acre", AL: "Alagoas", AP: "Amapá", AM: "Amazonas", BA: "Bahia", CE: "Ceará",
  DF: "Distrito Federal", ES: "Espírito Santo", GO: "Goiás", MA: "Maranhão",
  MT: "Mato Grosso", MS: "Mato Grosso do Sul", MG: "Minas Gerais", PA: "Pará",
  PB: "Paraíba", PR: "Paraná", PE: "Pernambuco", PI: "Piauí", RJ: "Rio de Janeiro",
  RN: "Rio Grande do Norte", RS: "Rio Grande do Sul", RO: "Rondônia", RR: "Roraima",
  SC: "Santa Catarina", SP: "São Paulo", SE: "Sergipe", TO: "Tocantins"
};

export default function MapaBrasil() {
  const [anoSelecionado, setAnoSelecionado] = useState(2023);
  const [matriculasData, setMatriculasData] = useState({});
  const [hoveredEstado, setHoveredEstado] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:5000/matriculas-por-estado?ano=${anoSelecionado}`)
      .then((res) => {
        if (!res.ok) throw new Error("Erro ao buscar dados da API");
        return res.json();
      })
      .then((data) => setMatriculasData(data))
      .catch((err) => {
        console.error(err);
        setMatriculasData({});
      });
  }, [anoSelecionado]);

  const dadosAno = matriculasData || {};
  const valores = Object.values(dadosAno);
  const maxMatriculas = valores.length > 0 ? Math.max(...valores) : 0;

  const colorScale = scaleLinear()
    .domain([0, maxMatriculas || 1])
    .range(["#ef9a9a", "#d32f2f"]);

  return (
    <div className="mapa-container">
      <div className="ano-seletor">
        <label htmlFor="ano" className="ano-label">
          Selecione o ano:
        </label>
        <select
          id="ano"
          value={anoSelecionado}
          onChange={(e) => setAnoSelecionado(Number(e.target.value))}
          className="ano-select"
        >
          <option value={2023}>2023</option>
          <option value={2024}>2024</option>
        </select>
      </div>

      <div className="mapa-info-container">
        <ComposableMap
          projection="geoMercator"
          projectionConfig={{ scale: 850, center: [-54, -15] }}
          width={700}
          height={700}
          className="mapa-svg"
        >
          <Geographies geography={BRAZIL_TOPOJSON}>
            {({ geographies }) =>
              geographies.map((geo) => {
                const sigla =
                  geo.properties.sigla || geo.properties.UF || geo.id;
                const valor = dadosAno[sigla] || 0;

                return (
                  <Geography
                    key={geo.rsmKey}
                    geography={geo}
                    fill={colorScale(valor)}
                    stroke="#fff"
                    strokeWidth={0.5}
                    onMouseEnter={() => setHoveredEstado({ sigla, valor })}
                    onMouseLeave={() => setHoveredEstado(null)}
                    className="estado"
                    style={{
                      default: { outline: "none" },
                      hover: { outline: "none", cursor: "pointer", opacity: 0.8 },
                      pressed: { outline: "none" },
                    }}
                  />
                );
              })
            }
          </Geographies>
        </ComposableMap>
        <div className="info-box">
          {hoveredEstado ? (
            <>
              <span className="info-titulo">
                {estadosSiglaNome[hoveredEstado.sigla] || hoveredEstado.sigla}
              </span>
              <span className="info-texto">
                Matrículas: {hoveredEstado.valor.toLocaleString()}
              </span>
            </>
          ) : (
            "Passe o mouse\nsobre um estado"
          )}
        </div>
      </div>
    </div>
  );
}
