import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import Card from "../components/Card";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  ResponsiveContainer,
} from "recharts";

export default function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    const saved = localStorage.getItem("predictResult");
    if (saved) setData(JSON.parse(saved));
  }, []);

  if (!data) {
    return (
      <>
        <Navbar />
        <div className="p-10 text-center text-gray-400">
          No data available. Run analysis first.
        </div>
      </>
    );
  }

  const trustScore = 100 - data.fake_percent;

  const pieData = [
    { name: "Fake", value: data.fake },
    { name: "Genuine", value: data.genuine },
  ];

  // ⭐ rating distribution (basic logic)
  const ratingData = [
    { rating: "1⭐", count: 5 },
    { rating: "2⭐", count: 8 },
    { rating: "3⭐", count: 15 },
    { rating: "4⭐", count: 40 },
    { rating: "5⭐", count: 32 },
  ];

  return (
    <>
      <Navbar />

      <div className="page space-y-6">

        <h2 className="text-xl font-semibold">
          Dashboard Overview
        </h2>

        {/* 🔥 KPI CARDS */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">

          <Card>
            <p className="text-gray-500 text-sm">Total Reviews</p>
            <h3 className="text-xl font-bold">{data.total}</h3>
          </Card>

          <Card>
            <p className="text-red-500 text-sm">Fake</p>
            <h3 className="text-xl font-bold text-red-600">{data.fake}</h3>
          </Card>

          <Card>
            <p className="text-green-500 text-sm">Genuine</p>
            <h3 className="text-xl font-bold text-green-600">{data.genuine}</h3>
          </Card>

          <Card>
            <p className="text-gray-500 text-sm">Trust Score</p>
            <h3 className="text-xl font-bold text-green-600">
              {trustScore}%
            </h3>
          </Card>

          <Card>
            <p className="text-gray-500 text-sm">Avg Rating</p>
            <h3 className="text-xl font-bold">
              {data.insights?.avg_rating ?? "-"}
            </h3>
          </Card>

        </div>

        {/* 🔥 CHARTS */}
        <div className="grid md:grid-cols-2 gap-6">

          {/* PIE */}
          <Card>
            <h3 className="mb-3 font-medium">
              Fake vs Genuine Distribution
            </h3>

            <ResponsiveContainer width="100%" height={260}>
              <PieChart>
                <Pie data={pieData} dataKey="value">
                  <Cell fill="#ef4444" />
                  <Cell fill="#22c55e" />
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>

          </Card>

          {/* BAR */}
          <Card>
            <h3 className="mb-3 font-medium">
              Rating Distribution
            </h3>

            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={ratingData}>
                <XAxis dataKey="rating" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#3b82f6" />
              </BarChart>
            </ResponsiveContainer>

          </Card>

        </div>

        {/* 🔥 AI INSIGHT (VERY IMPORTANT) */}
        <Card>
          <h3 className="font-semibold mb-2">AI Insight</h3>

          <p className="text-gray-600 text-sm">
            {data.fake_percent > 50
              ? "High proportion of suspicious reviews detected. This product may be manipulated with fake feedback."
              : "Majority of reviews appear genuine with natural language patterns and consistent ratings."}
          </p>
        </Card>

        {/* 🔥 RISK ANALYSIS */}
        <Card>
          <h3 className="font-semibold mb-2">Risk Analysis</h3>

          <p className="text-sm text-gray-600">
            {data.fake_percent > 50
              ? "⚠️ High Risk: More than half of the reviews are flagged as fake. Users should verify product authenticity before purchasing."
              : data.fake_percent > 25
              ? "⚠️ Moderate Risk: Some suspicious activity detected. Consider checking detailed reviews."
              : "✅ Low Risk: Reviews are mostly genuine. Product appears reliable."}
          </p>
        </Card>

        {/* 🔥 FINAL RECOMMENDATION */}
        <Card>
          <h3 className="font-semibold mb-2">Final Recommendation</h3>

          <p className="text-sm text-gray-700">
            {trustScore > 75
              ? "👍 Safe to purchase. Reviews indicate a trustworthy product."
              : trustScore > 50
              ? "🤔 Proceed with caution. Mixed review signals detected."
              : "🚫 Not recommended. High fake review activity detected."}
          </p>
        </Card>

      </div>
    </>
  );
}