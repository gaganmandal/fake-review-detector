import Navbar from "../components/Navbar";
import Card from "../components/Card";
import { useNavigate } from "react-router-dom";

export default function About() {
  const navigate = useNavigate();

  return (
    <>
      <Navbar />

      <div className="page space-y-8">
        {/* 🔥 HERO */}
        <div className="text-center space-y-3">
          <h1 className="text-3xl font-bold">
            AI-Powered Fake Review Detection
          </h1>

          <p className="text-gray-600 max-w-2xl mx-auto">
            ReviewGuard helps users identify fake and misleading product reviews
            using advanced AI models like RoBERTa, enabling smarter and more
            confident purchasing decisions.
          </p>

          {/* BUTTON */}
          <button
            onClick={() => navigate("/about/details")}
            className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition"
          >
            Learn More →
          </button>
        </div>

        {/* 🔥 FEATURES */}
        <div className="grid md:grid-cols-3 gap-4">
          <Card>
            <h3 className="font-semibold mb-2">🔍 Smart Detection</h3>
            <p className="text-sm text-gray-600">
              Instantly classify reviews as fake or genuine using AI.
            </p>
          </Card>

          <Card>
            <h3 className="font-semibold mb-2">⚡ Real-Time Analysis</h3>
            <p className="text-sm text-gray-600">
              Analyze reviews directly from live product pages.
            </p>
          </Card>

          <Card>
            <h3 className="font-semibold mb-2">📊 Insightful Results</h3>
            <p className="text-sm text-gray-600">
              Get fake percentage, trust score, and detailed insights.
            </p>
          </Card>
        </div>

        {/* 🔥 WHY */}
        <Card>
          <h3 className="font-semibold mb-3">Why ReviewGuard?</h3>

          <ul className="text-sm text-gray-600 space-y-2 list-disc ml-5">
            <li>Fake reviews mislead users and create confusion.</li>
            <li>Helps users make safe and confident buying decisions.</li>
            <li>Saves time by quickly analyzing large numbers of reviews.</li>
            <li>
              Identifies hidden patterns that are hard to detect manually.
            </li>
            <li>Improves trust in online shopping platforms.</li>
            <li>Provides clear insights instead of raw data.</li>
          </ul>
        </Card>
      </div>
    </>
  );
}
