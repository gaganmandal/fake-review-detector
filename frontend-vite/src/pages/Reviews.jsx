// import { useEffect, useState } from "react";
// import Navbar from "../components/Navbar";

// export default function Reviews() {
//   const [reviews, setReviews] = useState([]);
//   const [filter, setFilter] = useState("all");

//   useEffect(() => {
//     const data = JSON.parse(localStorage.getItem("reviewsData"));
//     if (data) setReviews(data);
//   }, []);

//   const filtered =
//     filter === "all"
//       ? reviews
//       : reviews.filter(r =>
//           filter === "fake" ? r.label === 1 : r.label === 0
//         );

//   return (
//     <>
//       <Navbar />

//       <div className="page">
//         <h2 className="text-xl font-semibold mb-6">
//           All Reviews & Predictions
//         </h2>

//         {/* FILTER */}
//         <div className="mb-4 flex gap-3">
//           <button onClick={() => setFilter("all")} className="nav-item">
//             All
//           </button>
//           <button onClick={() => setFilter("fake")} className="nav-item text-red-500">
//             Fake
//           </button>
//           <button onClick={() => setFilter("real")} className="nav-item text-green-600">
//             Genuine
//           </button>
//         </div>

//         {/* TABLE */}
//         <div className="card overflow-auto">
//           <table className="w-full text-sm">

//             <thead className="bg-gray-50">
//               <tr>
//                 <th className="p-3 text-left">Review</th>
//                 <th className="p-3">Label</th>
//                 <th className="p-3">Rating</th>
//                 <th className="p-3">Verified</th>
//               </tr>
//             </thead>

//             <tbody>
//               {filtered.map((r, i) => (
//                 <tr key={i} className="border-t">

//                   <td className="p-3 text-left max-w-xl">
//                     {r.review}
//                   </td>

//                   <td className="p-3 text-center">
//                     <span
//                       className={`px-3 py-1 rounded-full text-xs font-medium ${
//                         r.label === 1
//                           ? "bg-red-100 text-red-600"
//                           : "bg-green-100 text-green-600"
//                       }`}
//                     >
//                       {r.label === 1 ? "Fake" : "Genuine"}
//                     </span>
//                   </td>

//                   <td className="p-3 text-center">
//                     {r.rating ?? "-"}
//                   </td>

//                   <td className="p-3 text-center">
//                     {r.verified ? "✅" : "❌"}
//                   </td>

//                 </tr>
//               ))}
//             </tbody>

//           </table>
//         </div>
//       </div>
//     </>
//   );
// }

import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";

export default function Reviews() {
  const [reviews, setReviews] = useState([]);
  const [filter, setFilter] = useState("all");
  const [page, setPage] = useState(1);

  const perPage = 10;

  useEffect(() => {
    const data = localStorage.getItem("reviewsData");
    if (data) setReviews(JSON.parse(data));
  }, []);

  // 🔹 FILTER
  const filtered =
    filter === "all"
      ? reviews
      : reviews.filter(r =>
          filter === "fake" ? r.label === 1 : r.label === 0
        );

  // 🔹 PAGINATION
  const start = (page - 1) * perPage;
  const paginated = filtered.slice(start, start + perPage);

  return (
    <>
      <Navbar />

      <div className="page">

        <h2 className="text-xl font-semibold mb-6">
          All Reviews & Predictions
        </h2>

        {/* 🔹 FILTER BUTTONS */}
        <div className="mb-4 flex gap-3">
          <button onClick={() => { setFilter("all"); setPage(1); }} className="nav-item">
            All
          </button>

          <button onClick={() => { setFilter("fake"); setPage(1); }} className="nav-item text-red-500">
            Fake
          </button>

          <button onClick={() => { setFilter("real"); setPage(1); }} className="nav-item text-green-600">
            Genuine
          </button>
        </div>

        {/* 🔹 TABLE */}
        <div className="card overflow-auto">
          <table className="w-full text-sm">

            <thead className="bg-gray-50">
              <tr>
                <th className="p-3 text-left">Review</th>
                <th className="p-3">Label</th>
                <th className="p-3">Rating</th>
                <th className="p-3">Verified</th>
              </tr>
            </thead>

            <tbody>
              {paginated.map((r, i) => (
                <tr key={i} className="border-t">

                  {/* REVIEW */}
                  <td className="p-3 text-left max-w-xl">
                    {r.review}
                  </td>

                  {/* LABEL */}
                  <td className="p-3 text-center">
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-medium ${
                        r.label === 1
                          ? "bg-red-100 text-red-600"
                          : "bg-green-100 text-green-600"
                      }`}
                    >
                      {r.label === 1 ? "Fake" : "Genuine"}
                    </span>
                  </td>

                  {/* RATING */}
                  <td className="p-3 text-center">
                    {r.rating ?? "-"}
                  </td>

                  {/* VERIFIED */}
                  <td className="p-3 text-center">
                    {r.verified ? "✅" : "❌"}
                  </td>

                </tr>
              ))}
            </tbody>

          </table>
        </div>

        {/* 🔹 PAGINATION */}
        <div className="flex justify-center mt-6 gap-3">

          <button
            onClick={() => setPage(p => Math.max(p - 1, 1))}
            className="nav-item"
          >
            ← Prev
          </button>

          <span className="px-3 py-1 text-sm">
            Page {page}
          </span>

          <button
            onClick={() =>
              setPage(p =>
                start + perPage < filtered.length ? p + 1 : p
              )
            }
            className="nav-item"
          >
            Next →
          </button>

        </div>

      </div>
    </>
  );
}