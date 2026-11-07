// import Input from "../components/Input";
// import Button from "../components/Button";
// import { useNavigate } from "react-router-dom";

// export default function Login() {
//   const navigate = useNavigate();

//   return (
//     <div className="h-screen flex items-center justify-center bg-blue-50">

//       <div className="card w-96">

//         <h2 className="text-center text-2xl font-semibold mb-6">
//           Sign in
//         </h2>

//         <Input placeholder="Email" />
//         <Input type="password" placeholder="Password" />

//         <Button onClick={() => navigate("/predict")}>
//           Login
//         </Button>

//         <p className="text-center mt-4 cursor-pointer text-blue-600"
//            onClick={() => navigate("/signup")}>
//           Create Account
//         </p>

//       </div>
//     </div>
//   );
// }

import { useNavigate } from "react-router-dom";
import { useState } from "react";

export default function Login() {
  const navigate = useNavigate();
  const [active, setActive] = useState("");

  return (
    <div className="min-h-screen flex bg-gray-50">

      {/* LEFT */}
      <div className="hidden md:flex w-1/2 items-center justify-center px-16">
        <div className="max-w-md">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Detect Fake Reviews Instantly
          </h1>
          <p className="text-gray-500 text-lg">
            AI-powered system to analyze reviews and detect fake ones.
          </p>
        </div>
      </div>

      {/* RIGHT */}
      <div className="w-full md:w-1/2 flex items-center justify-center px-6">

        {/* CARD */}
        <div className="w-full max-w-sm bg-white p-8 rounded-2xl shadow-xl border border-gray-100
                        transform transition-all duration-500 hover:scale-105">

          <h2 className="text-2xl font-semibold mb-2">Sign in</h2>
          <p className="text-gray-500 text-sm mb-6">
            Enter your details to continue
          </p>

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

          <div className="text-right text-sm mb-5 text-gray-500 cursor-pointer hover:text-black">
            Forgot password?
          </div>

          <button
            onClick={() => navigate("/predict")}
            className="w-full bg-blue-600 text-white py-3 rounded-xl
                       hover:bg-blue-700 transform hover:scale-105 active:scale-95 transition"
          >
            Login
          </button>

          <p className="text-center mt-6 text-sm text-gray-600">
            Don’t have an account?{" "}
            <button
              onClick={() => navigate("/signup")}
              className="text-blue-600 font-medium hover:underline"
            >
              Sign up
            </button>
          </p>

        </div>
      </div>
    </div>
  );
}