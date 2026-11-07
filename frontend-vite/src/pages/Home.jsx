// import { useNavigate } from "react-router-dom";

// export default function Home() {
//   const navigate = useNavigate();

//   return (
//     <div className="min-h-screen">
//       {/* NAVBAR */}
//       <div className="sticky top-0 bg-white/80 backdrop-blur-md border-b px-10 py-4 flex justify-between">
//         <h1 className="font-semibold">ReviewGuard</h1>

//         <div className="flex gap-4">
//           <button onClick={() => navigate("/predict")} className="nav-item">
//             Predict
//           </button>

//           <button onClick={() => navigate("/models")} className="nav-item">
//             Models
//           </button>

//           <button onClick={() => navigate("/About")} className="nav-item">
//             About
//           </button>

//           <button onClick={() => navigate("/login")} className="nav-item">
//             Login
//           </button>
//         </div>
//       </div>

//       {/* HERO */}
//       <div
//         className="
//   flex flex-col items-center justify-center
//   text-center px-6 py-20
// "
//       >
//         {/* TITLE */}
//         <h1
//           className="
//     text-6xl md:text-7xl font-semibold tracking-tight
//     bg-gradient-to-r from-blue-600 to-indigo-600
//     text-transparent bg-clip-text
//     animate-fade-in
//   "
//         >
//           Detect Fake Reviews
//         </h1>

//         {/* SUBTITLE */}
//         <p
//           className="
//     mt-6 text-lg text-gray-600 max-w-2xl
//     animate-fade-in delay-100
//   "
//         >
//           AI-powered system that analyzes product reviews and identifies fake,
//           spam, and manipulated feedback instantly.
//         </p>

//         {/* BUTTONS */}
//         <div className="mt-10 flex gap-4 animate-fade-in delay-200">
//           <button
//             onClick={() => navigate("/predict")}
//             className="
//         px-8 py-3 rounded-xl
//         bg-blue-600 text-white font-medium

//         hover:bg-blue-700 hover:scale-105
//         active:scale-95

//         transition-all duration-200
//       "
//           >
//             Try Now
//           </button>

//           <button
//             onClick={() => navigate("/signup")}
//             className="
//         px-8 py-3 rounded-xl
//         border border-gray-300 font-medium

//         hover:bg-gray-100 hover:scale-105
//         active:scale-95

//         transition-all duration-200
//       "
//           >
//             Get Started
//           </button>
//         </div>
//       </div>

//       {/* FEATURES */}
//       <div className="grid md:grid-cols-3 gap-6 px-10 pb-18">
//         <div className="card">
//           <h3 className="font-semibold">AI Detection</h3>
//           <p className="text-gray-600">Detect fake patterns.</p>
//         </div>

//         <div className="card">
//           <h3 className="font-semibold">Model Comparison</h3>
//           <p className="text-gray-600">Compare ML models.</p>
//         </div>

//         <div className="card">
//           <h3 className="font-semibold">Explainable AI</h3>
//           <p className="text-gray-600">Understand decisions.</p>
//         </div>
//       </div>
//     </div>
//   );
// }

import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";

export default function Home() {
  const navigate = useNavigate();

  const [showIntro, setShowIntro] = useState(true);

  // ✅ Show intro only first time
  useEffect(() => {
    const seen = localStorage.getItem("seenIntro");

    if (!seen) {
      setTimeout(() => {
        setShowIntro(false);
        localStorage.setItem("seenIntro", "true");
      }, 2000);
    } else {
      setShowIntro(false);
    }
  }, []);

  // ✅ INTRO SCREEN
  if (showIntro) {
    return (
      <div className="h-screen flex flex-col items-center justify-center bg-white">

        <h1 className="
          text-5xl font-bold
          bg-gradient-to-r from-blue-600 to-purple-600
          text-transparent bg-clip-text
          animate-fadeScale
        ">
          ReviewGuard
        </h1>

        <p className="mt-4 text-gray-500 animate-fadeScale delay-1">
          AI Fake Review Detection
        </p>

        <p className="mt-6 text-sm text-gray-400 animate-pulse">
          Loading...
        </p>

      </div>
    );
  }

  return (
    <div className="min-h-screen relative overflow-hidden">

      {/* 🌈 BACKGROUND */}
      <div className="absolute inset-0 bg-animated opacity-10"></div>

      {/* NAVBAR */}
      <div className="relative z-10  top-0 bg-white/80 backdrop-blur-md border-b px-10 py-4 flex justify-between">
        <h1 className="font-semibold">ReviewGuard</h1>

        <div className="flex sticky gap-4">
          <button onClick={() => navigate("/predict")} className="nav-item">
            Predict
          </button>

          <button onClick={() => navigate("/models")} className="nav-item">
            Models
          </button>

          <button onClick={() => navigate("/about")} className="nav-item">
            About
          </button>

          <button onClick={() => navigate("/login")} className="nav-item">
            Login
          </button>
        </div>
      </div>

      {/* HERO */}
      <div className="relative z-10 flex flex-col items-center justify-center text-center px-6 py-24">

        {/* TITLE */}
        <h1
          className="
            text-5xl md:text-6xl font-bold tracking-tight
            bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600
            text-transparent bg-clip-text
            animate-fadeScale
          "
        >
          Detect Fake Reviews
        </h1>

        {/* SUBTITLE */}
        <p
          className="
            mt-6 text-lg text-gray-600 max-w-2xl
            animate-fadeScale delay-1
          "
        >
          AI-powered system that analyzes product reviews and identifies fake,
          spam, and manipulated feedback instantly.
        </p>

        {/* BUTTONS */}
        <div className="mt-10 flex gap-4 animate-fadeScale delay-2">

          <button
            onClick={() => navigate("/predict")}
            className="
              px-8 py-3 rounded-xl
              bg-blue-600 text-white font-medium

              hover:bg-blue-700 hover:scale-110
              active:scale-95

              shadow-md hover:shadow-xl

              transition-all duration-300
            "
          >
            Try Now
          </button>

          <button
            onClick={() => navigate("/signup")}
            className="
              px-8 py-3 rounded-xl
              border border-gray-300 font-medium

              hover:bg-gray-100 hover:scale-110
              active:scale-95

              transition-all duration-300
            "
          >
            Get Started
          </button>

        </div>
      </div>

      {/* FEATURES (NO ANIMATION — CLEAN UI) */}
      <div className="relative z-10 grid md:grid-cols-3 gap-6 px-10 pb-20">

        <div className="card">
          <h3 className="font-semibold">AI Detection</h3>
          <p className="text-gray-600">Detect fake patterns.</p>
        </div>

        <div className="card">
          <h3 className="font-semibold">Model Comparison</h3>
          <p className="text-gray-600">Compare ML models.</p>
        </div>

        <div className="card">
          <h3 className="font-semibold">Explainable AI</h3>
          <p className="text-gray-600">Understand decisions.</p>
        </div>

      </div>

    </div>
  );
}