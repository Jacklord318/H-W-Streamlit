// HazenWilliamsApp.tsx
import { useState } from "react";
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  Node,
  Edge,
  MarkerType,
} from "reactflow";
import "reactflow/dist/style.css";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import * as XLSX from "xlsx";
import { useEffect } from "react";
import { read, utils } from "xlsx";

const edgeStyle = { stroke: "#555", strokeWidth: 2 };

const initialNodes: Node[] = [
  { id: "R1", position: { x: 300, y: 0 }, data: { elevation: 500 }, type: "default" },
  { id: "A", position: { x: 300, y: 100 }, data: { elevation: 455 }, type: "default" },
  { id: "B", position: { x: 0, y: 100 }, data: { elevation: 448 }, type: "default" },
  { id: "C", position: { x: 0, y: 550 }, data: { elevation: 442 }, type: "default" },
  { id: "D", position: { x: 300, y: 550 }, data: { elevation: 438 }, type: "default" },
  { id: "E", position: { x: 620, y: 550 }, data: { elevation: 432 }, type: "default" },
  { id: "F", position: { x: 620, y: 100 }, data: { elevation: 445 }, type: "default" },
];

function calcularVelocidad(Q: number, D: number): number {
  const area = Math.PI * Math.pow(D / 2, 2);
  return Q / area;
}

function calcularPerdidaHazenWilliams(Q: number, L: number, D: number, C: number): number {
  const v = 0.849 * Math.pow(C, -1.85) * Math.pow(Q, 1.85) / Math.pow(D, 4.87);
  return L * v;
}

function sugerirDiametro(Q: number, velocidadObjetivo = 1): number {
  const area = Q / velocidadObjetivo;
  return 2 * Math.sqrt(area / Math.PI);
}

export default function HazenWilliamsApp() {
  const [nodes, setNodes] = useState<Node[]>(initialNodes);
  const [edges, setEdges] = useState<Edge[]>([]);
  const [longitud, setLongitud] = useState(350);
  const [diametro, setDiametro] = useState(0.2);
  const [caudal, setCaudal] = useState(0.01);
  const [C, setC] = useState(140);
  const [perdida, setPerdida] = useState<number | null>(null);
  const [velocidad, setVelocidad] = useState<number | null>(null);
  const [sugerido, setSugerido] = useState<number | null>(null);

  const handleCalcular = () => {
    const hf = calcularPerdidaHazenWilliams(caudal, longitud, diametro, C);
    const v = calcularVelocidad(caudal, diametro);
    const sugerido = sugerirDiametro(caudal);

    const edgeColor = v < 0.9 || v > 1.1 ? "#e11d48" : "#10b981";

    const newEdges = [
      {
        id: "tramo-prueba",
        source: "A",
        target: "B",
        label: `${v.toFixed(2)} m/s` + (v < 0.9 || v > 1.1 ? ` ⚠` : ""),
        style: { stroke: edgeColor, strokeWidth: 3 },
        markerEnd: { type: MarkerType.ArrowClosed },
      },
    ];

    setEdges(newEdges);
    setPerdida(hf);
    setVelocidad(v);
    setSugerido(sugerido);

    // Calcular presión en todos los nodos
    const nodoReferencia = nodes.find((n) => n.id === "R1");
    const zReferencia = nodoReferencia?.data?.elevation || 0;
    const H = 500; // Presión total en R1 en m.c.a.

    const nuevosNodos = nodes.map((n) => {
      const z = n.data?.elevation || 0;
      const presion = H - (zReferencia - z); // presión en m.c.a.
      return {
        ...n,
        data: {
          ...n.data,
          label: `${n.id}\n(${z} msnm)\n${presion.toFixed(1)} m.c.a.`,
        },
      };
    });
    setNodes(nuevosNodos);
  };

  return (
    <div className="max-w-6xl mx-auto p-4 grid gap-4">
      <Card>
        <CardContent className="p-4">
          <h2 className="text-lg font-bold mb-4">Visualización de Red Hidráulica</h2>
          <div className="h-[600px]">
            <ReactFlow nodes={nodes} edges={edges} fitView>
              <MiniMap />
              <Controls />
              <Background gap={12} size={1} />
            </ReactFlow>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="p-4 grid gap-4">
          <h2 className="text-lg font-bold mb-2">Cálculo de Pérdida por Hazen-Williams</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <Label>Longitud (m)</Label>
              <Input type="number" value={longitud} onChange={(e) => setLongitud(Number(e.target.value))} />
            </div>
            <div>
              <Label>Diámetro (m)</Label>
              <Input type="number" step="0.01" value={diametro} onChange={(e) => setDiametro(Number(e.target.value))} />
            </div>
            <div>
              <Label>Caudal (m³/s)</Label>
              <Input type="number" step="0.001" value={caudal} onChange={(e) => setCaudal(Number(e.target.value))} />
            </div>
            <div>
              <Label>Coef. C</Label>
              <Input type="number" value={C} onChange={(e) => setC(Number(e.target.value))} />
            </div>
          </div>
          <Button onClick={handleCalcular} className="mt-4">Calcular pérdida</Button>
          {perdida !== null && (
            <p className="mt-2">Pérdida por fricción: <strong>{perdida.toFixed(3)} m</strong></p>
          )}
          {velocidad !== null && (
            <p className="mt-1">Velocidad del flujo: <strong>{velocidad.toFixed(3)} m/s</strong></p>
          )}
          {sugerido !== null && (
            <p className="mt-1">Diámetro económico sugerido: <strong>{sugerido.toFixed(3)} m</strong></p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
