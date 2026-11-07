// import Input from "../components/Input";
// import Button from "../components/Button";
// import { useNavigate } from "react-router-dom";

// export default function Signup() {
//   const navigate = useNavigate();

//   return (
//     <div className="h-screen flex items-center justify-center bg-blue-50">

//       <div className="card w-96">

//         <h2 className="text-center text-2xl font-semibold mb-6">
//           Create Account
//         </h2>

//         <Input placeholder="Name" />
//         <Input placeholder="Email" />
//         <Input placeholder="Password" />

//         <Button onClick={() => navigate("/predict")}>
//           Signup
//         </Button>

//         <p className="text-center mt-4 cursor-pointer text-blue-600"
//            onClick={() => navigate("/login")}>
//           Back to Login
//         </p>

//       </div>
//     </div>
//   );
// }

import { useNavigate } from "react-router-dom";
import { useState } from "react";

export default function Signup() {
  const navigate = useNavigate();
  const [active, setActive] = useState("");

  return (
    <div className="min-h-screen flex bg-gray-50">

      {/* LEFT */}
      <div className="hidden md:flex w-1/2 items-center justify-center px-16">
        <div className="max-w-md">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Join the Future of Review Analysis
          </h1>
          <p className="text-gray-500 text-lg">
            Create your account and start detecting fake reviews using AI.
          </p>
        </div>
      </div>

      {/* RIGHT */}
      <div className="w-full md:w-1/2 flex items-center justify-center px-6">

        {/* CARD */}
        <div className="w-full max-w-sm bg-white p-8 rounded-2xl shadow-xl border border-gray-100
                        transform transition-all duration-500 hover:scale-105">

          <h2 className="text-2xl font-semibold mb-2">Create account</h2>
          <p className="text-gray-500 text-sm mb-6">
            Get started in seconds
          </p>

          {/* NAME */}
          <input
            type="text"
            placeholder="Full name"
            onFocus={() => setActive("name")}
            className={`w-full mb-4 px-4 py-3 border rounded-xl outline-none transition-all
              ${
                active === "name"
                  ? "border-blue-500 ring-2 ring-blue-200 shadow-md scale-105"
                  : "border-gray-300"
              }`}
          />

          {/* EMAIL */}
          <input
            type="email"
            placeholder="Email"
            onFocus={() => setActive("email")}
            className={`w-full mb-4 px-4 py-3 border rounded-xl outline-none transition-all
              ${
                active === "email"
                  ? "border-blue-500 ring-2 ring-blue-200 shadow-md scale-105"
                  : "border-gray-300"
              }`}
          />

          {/* PASSWORD */}
          <input
            type="password"
            placeholder="Password"
            onFocus={() => setActive("password")}
            className={`w-full mb-5 px-4 py-3 border rounded-xl outline-none transition-all
              ${
                active === "password"
                  ? "border-blue-500 ring-2 ring-blue-200 shadow-md scale-105"
                  : "border-gray-300"
              }`}
          />

          <button
            onClick={() => navigate("/predict")}
            className="w-full bg-blue-600 text-white py-3 rounded-xl
                       hover:bg-blue-700 transform hover:scale-105 active:scale-95 transition"
          >
            Signup
          </button>

          <p className="text-center mt-6 text-sm text-gray-600">
            Already have an account?{" "}
            <button
              onClick={() => navigate("/login")}
              className="text-blue-600 font-medium hover:underline"
            >
              Login
            </button>
          </p>

        </div>
      </div>
    </div>
  );
}