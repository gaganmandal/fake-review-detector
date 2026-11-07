import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  Cell,
} from "recharts";

export default function Models() {
  const [models, setModels] = useState([]);

  useEffect(() => {
    // fetch("http://localhost:8000/model-accuracy")
    fetch(`${import.meta.env.VITE_API_URL || "http://localhost:8000"}/model-accuracy`)
      .then((res) => res.json())
      .then((data) => setModels(data));
  }, []);

  // ✅ Find best model (highest accuracy)
  const bestModel = models.length
    ? models.reduce((max, m) => (m.Accuracy > max.Accuracy ? m : max))
    : null;

  return (
    <>
      <Navbar />

      <div className="page">
        {/* TITLE */}
        <h2 className="text-xl font-semibold mb-6 tracking-tight">
          Model Performance Comparison
        </h2>

        {/* BEST MODEL BADGE */}
        {bestModel && (
          <div className="mb-4 text-green-600 font-medium">
            🏆 Best Model: {bestModel.Model} (
            {(bestModel.Accuracy * 100).toFixed(1)}%)
          </div>
        )}

        {/* TABLE */}
        <div className="card mb-8 overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-gray-50">
              <tr className="text-gray-500 text-left">
                <th className="p-4">Model</th>
                <th className="p-4">Accuracy</th>
                <th className="p-4">Precision</th>
                <th className="p-4">Recall</th>
                <th className="p-4">F1 Score</th>
              </tr>
            </thead>

            <tbody>
              {models.map((m, i) => (
                <tr
                  key={i}
                  className="border-t hover:bg-blue-50 transition duration-200 group"
                >
                  <td className="p-4 font-medium group-hover:text-blue-600 transition">
                    {m.Model}
                  </td>

                  <td className="p-4 group-hover:text-blue-600 transition">
                    {(m.Accuracy * 100).toFixed(1)}%
                  </td>

                  <td className="p-4 group-hover:text-blue-600 transition">
                    {(m.Precision * 100).toFixed(1)}%
                  </td>

                  <td className="p-4 group-hover:text-blue-600 transition">
                    {(m.Recall * 100).toFixed(1)}%
                  </td>

                  <td className="p-4 group-hover:text-blue-600 transition">
                    {(m["F1 Score"] * 100).toFixed(1)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* BAR CHART */}
        <div className="card">
          <h3 className="text-md font-medium mb-4 text-gray-700">
            Accuracy Comparison
          </h3>

          <ResponsiveContainer width="100%" height={320}>
            <BarChart data={models}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />

              <XAxis
                dataKey="Model"
                interval={0} // ✅ show all labels
                angle={-20} // ✅ tilt labels (important)
                textAnchor="end"
                height={80} // ✅ space for long names
                tick={{ fill: "#6b7280", fontSize: 12 }}
              />

              <YAxis />

              <Tooltip />

              <Bar dataKey="Accuracy">
                {models.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={
                      bestModel && entry.Model === bestModel.Model
                        ? "#22c55e"
                        : "#3b82f6"
                    }
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </>
  );
}
