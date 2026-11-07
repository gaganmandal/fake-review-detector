// import { useState } from "react";
// import Navbar from "../components/Navbar";
// import Card from "../components/Card";
// import Button from "../components/Button";
// import axios from "axios";

// import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";

// export default function Predict() {
//   const [url, setUrl] = useState("");
//   const [result, setResult] = useState(null);
//   const [loading, setLoading] = useState(false);

//   const analyze = async () => {
//     if (!url) return;

//     setLoading(true);

//     try {
//       const res = await axios.post("http://localhost:8000/analyze", { url });
//       setResult(res.data);
//       localStorage.setItem("reviewsData", JSON.stringify(res.data.reviews));
//     } catch (err) {
//       console.log(err);
//     }

//     setLoading(false);
//   };

//   const pieData = result
//     ? [
//         { name: "Fake", value: result.fake_percent },
//         { name: "Genuine", value: 100 - result.fake_percent },
//       ]
//     : [];

//   return (
//     <>
//       <Navbar />

//       {/* FULL SCREEN LOCK */}
//       <div className="h-[calc(100vh-60px)] overflow-hidden">
//         {/* SPLIT SCREEN */}
//         <div className="grid md:grid-cols-2 h-full">
//           {/* 🔥 LEFT PANEL (STICKY) */}
//           <div className="border-r bg-white flex items-start justify-center">
//             <div className="w-full max-w-xl p-6 sticky top-6">
//                <Card className="space-y-4">

//         <input
//           type="text"
//           className="w-full p-3 border rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none"
//           placeholder="Paste Flipkart product URL..."
//           onChange={(e) => setUrl(e.target.value)}
//         />

//         {loading && (
//           <p className="text-blue-600 text-sm animate-pulse">
//             Analyzing reviews...
//           </p>
//         )}

//         <Button onClick={analyze} disabled={loading}>
//           {loading ? "Analyzing..." : "Analyze"}
//         </Button>

//       </Card>
//             </div>
//           </div>

//           {/* 🔥 RIGHT PANEL (SCROLLABLE + ANIMATED) */}
//           {/* 🔥 RIGHT PANEL */}
//   <div className="bg-gray-50 h-full overflow-y-auto px-8 py-6">

//     {!result && !loading && (
//       <div className="flex items-center justify-center h-full text-gray-400">
//         <p>No analysis yet. Enter a URL to begin.</p>
//       </div>
//     )}

//     {result && (
//       <div className="max-w-xl mx-auto space-y-6">

//         {/* HEADER */}
//         <div className="flex justify-between items-center sticky top-0 bg-gray-50 py-2 z-10">
//           <h2 className="text-xl font-bold">Analysis Result</h2>

//           <span
//             className={`px-4 py-1 rounded-full text-white text-sm ${
//               result.fake_percent > 50
//                 ? "bg-red-500"
//                 : "bg-green-500"
//             }`}
//           >
//             {result.fake_percent > 50 ? "Fake" : "Genuine"}
//           </span>
//         </div>

//         {/* DONUT */}
//         <Card>
//           <h3 className="font-semibold mb-4">Review Distribution</h3>

//           <div className="h-60 relative flex items-center justify-center">

//             <ResponsiveContainer>
//               <PieChart>
//                 <Pie
//                   data={pieData}
//                   dataKey="value"
//                   innerRadius={65}
//                   outerRadius={95}
//                 >
//                   <Cell fill="#ef4444" />
//                   <Cell fill="#22c55e" />
//                 </Pie>
//                 <Tooltip />
//               </PieChart>
//             </ResponsiveContainer>

//             <div className="absolute text-center">
//               <p className="text-xs text-gray-500">Trust</p>
//               <h2 className="text-xl font-bold text-green-500">
//                 {100 - result.fake_percent}%
//               </h2>
//             </div>

//           </div>
//         </Card>

//         {/* METRICS */}
//         <div className="grid grid-cols-2 gap-4">

//           <Card>
//             <p className="text-sm text-gray-500">Fake %</p>
//             <h3 className="text-xl font-bold text-red-500">
//               {result.fake_percent}%
//             </h3>
//           </Card>

//           <Card>
//             <p className="text-sm text-gray-500">Trust Score</p>
//             <h3 className="text-xl font-bold text-green-500">
//               {100 - result.fake_percent}%
//             </h3>
//           </Card>

//         </div>

//         {/* SUMMARY */}
//         <Card>
//           <h3 className="font-semibold mb-2">AI Insight</h3>
//           <p className="text-gray-600 text-sm">
//             {result.fake_percent > 50
//               ? "Detected suspicious patterns in reviews."
//               : "Reviews appear genuine and natural."}
//           </p>
//         </Card>

//         {/* RECOMMENDATION */}
//         <Card>
//           <h3 className="font-semibold mb-2">Recommendation</h3>
//           <p className="text-gray-600 text-sm">
//             {result.fake_percent > 50
//               ? "Be cautious before purchasing."
//               : "This product seems trustworthy."}
//           </p>
//         </Card>

//       </div>
//     )}

//   </div>
//         </div>
//       </div>
//     </>
//   );
// }

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import Card from "../components/Card";
import Button from "../components/Button";
import axios from "axios";
import { Turnstile } from "@marsidev/react-turnstile";

import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";

export default function Predict() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [turnstileToken, setTurnstileToken] = useState("");

  const navigate = useNavigate();

  // ✅ restore data on reload
  useEffect(() => {
    const saved = localStorage.getItem("predictResult");
    if (saved) setResult(JSON.parse(saved));
  }, []);

  const analyze = async () => {
    if (!url || !turnstileToken) {
      alert("Please complete the security verification first.");
      return;
    }

    setLoading(true);

    // clear old
    localStorage.removeItem("predictResult");
    localStorage.removeItem("reviewsData");

    try {
      // const res = await axios.post("http://localhost:8000/analyze", { url });
      const res = await axios.post(
        `${import.meta.env.VITE_API_URL || "http://localhost:8000"}/analyze`,
        { url, turnstileToken },
      );

      setResult(res.data);

      // ✅ save
      localStorage.setItem("predictResult", JSON.stringify(res.data));
      localStorage.setItem("reviewsData", JSON.stringify(res.data.reviews));
    } catch (err) {
      console.log(err);
    }

    setLoading(false);
  };

  const pieData = result
    ? [
        { name: "Fake", value: result.fake_percent },
        { name: "Genuine", value: 100 - result.fake_percent },
      ]
    : [];

  return (
    <>
      <Navbar />

      <div className="h-[calc(100vh-60px)] overflow-hidden">
        <div className="grid md:grid-cols-2 h-full">
          {/* LEFT */}
          <div className="border-r bg-white flex items-start justify-center">
            <div className="w-full max-w-xl p-6 sticky top-6">
              <Card className="space-y-4">
                <input
                  type="text"
                  className="w-full p-3 border rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none"
                  placeholder="Paste Flipkart product URL..."
                  onChange={(e) => setUrl(e.target.value)}
                />
                <Turnstile
                  siteKey={import.meta.env.VITE_TURNSTILE_SITE_KEY}
                  onSuccess={(token) => setTurnstileToken(token)}
                  onExpire={() => setTurnstileToken("")}
                  onError={() => setTurnstileToken("")}
                />

                {loading && (
                  <p className="text-blue-600 text-sm animate-pulse">
                    Analyzing reviews...
                  </p>
                )}

                <Button onClick={analyze} disabled={loading || !turnstileToken}>
                  {loading ? "Analyzing..." : "Analyze"}
                </Button>
              </Card>
              {/* ✅ SHOW AFTER RESULT */}
              {result && (
                <div className="flex px-2 py-2 gap-3 mt-2">
                  <button
                    onClick={() => {
                      const el = document.getElementById("reviewsBtn");
                      el.classList.add("scale-95");
                      setTimeout(() => navigate("/reviews"), 150);
                    }}
                    id="reviewsBtn"
                    className="
                      px-4 py-2 text-sm rounded-lg
                      bg-gray-800 text-white
                      transition-all duration-150
                      hover:scale-105 hover:bg-gray-900
                      hover:shadow-gray-400
                      active:scale-95
                      shadow-md hover:shadow-lg
                    "
                  >
                    Reviews →
                  </button>

                  <button
                    onClick={() => {
                      const el = document.getElementById("dashboardBtn");
                      el.classList.add("scale-95");
                      setTimeout(() => navigate("/dashboard"), 150);
                    }}
                    id="dashboardBtn"
                    className="
                      px-4 py-2 text-sm rounded-lg
                      bg-green-600 text-white
                      transition-all duration-150
                      hover:scale-105 hover:bg-green-700
                      hover:shadow-green-300
                      active:scale-95
                      shadow-md hover:shadow-lg
                    "
                  >
                    Dashboard →
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* RIGHT */}
          <div className="bg-gray-50 h-full overflow-y-auto px-8 py-6">
            {!result && !loading && (
              <div className="flex items-center justify-center h-full text-gray-400">
                <p>No analysis yet. Enter a URL to begin.</p>
              </div>
            )}

            {result && (
              <div className="max-w-xl mx-auto space-y-6">
                {/* HEADER */}
                <div className="flex justify-between items-center sticky top-0 bg-gray-50 py-2 z-10">
                  <h2 className="text-xl font-bold">Analysis Result</h2>

                  <span
                    className={`px-4 py-1 rounded-full text-white text-sm ${
                      result.fake_percent > 50 ? "bg-red-500" : "bg-green-500"
                    }`}
                  >
                    {result.fake_percent > 50 ? "Fake" : "Genuine"}
                  </span>
                </div>

                {/* 🔥 DONUT + STATS */}
                <Card>
                  <h3 className="font-semibold mb-4">Review Distribution</h3>

                  <div className="flex items-center justify-between">
                    {/* DONUT LEFT */}
                    <div className="w-1/2 h-60 relative">
                      <ResponsiveContainer>
                        <PieChart>
                          <Pie
                            data={pieData}
                            dataKey="value"
                            innerRadius={60}
                            outerRadius={90}
                          >
                            <Cell fill="#ef4444" />
                            <Cell fill="#22c55e" />
                          </Pie>
                          <Tooltip />
                        </PieChart>
                      </ResponsiveContainer>

                      <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <p className="text-xs text-gray-500">Trust</p>
                        <h2 className="text-xl font-bold text-green-600">
                          {100 - result.fake_percent}%
                        </h2>
                      </div>
                    </div>

                    {/* 📊 STATS RIGHT */}
                    <div className="w-1/2 space-y-3">
                      <div className="flex justify-between">
                        <span className="text-gray-500">Total Reviews</span>
                        <span className="font-semibold">{result.total}</span>
                      </div>

                      <div className="flex justify-between">
                        <span className="text-red-500">Fake</span>
                        <span className="font-semibold text-red-600">
                          {result.fake}
                        </span>
                      </div>

                      <div className="flex justify-between">
                        <span className="text-green-600">Genuine</span>
                        <span className="font-semibold text-green-600">
                          {result.genuine}
                        </span>
                      </div>
                    </div>
                  </div>
                </Card>

                {/* METRICS */}
                <div className="grid grid-cols-2 gap-4">
                  <Card>
                    <p className="text-sm text-gray-500">Fake %</p>
                    <h3 className="text-xl font-bold text-red-500">
                      {result.fake_percent}%
                    </h3>
                  </Card>

                  <Card>
                    <p className="text-sm text-gray-500">Trust Score</p>
                    <h3 className="text-xl font-bold text-green-600">
                      {100 - result.fake_percent}%
                    </h3>
                  </Card>
                </div>

                {/* SUMMARY */}
                <Card>
                  <h3 className="font-semibold mb-2">AI Insight</h3>
                  <p className="text-gray-600 text-sm">
                    {result.fake_percent > 50
                      ? "Detected suspicious patterns in reviews."
                      : "Reviews appear genuine and natural."}
                  </p>
                </Card>

                {/* RECOMMENDATION */}
                <Card>
                  <h3 className="font-semibold mb-2">Recommendation</h3>
                  <p className="text-gray-600 text-sm">
                    {result.fake_percent > 50
                      ? "Be cautious before purchasing."
                      : "This product seems trustworthy."}
                  </p>
                </Card>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
}
