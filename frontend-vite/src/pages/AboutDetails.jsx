import Navbar from "../components/Navbar";
import Card from "../components/Card";
import { useNavigate } from "react-router-dom";

export default function AboutDetails() {
  const navigate = useNavigate();

  return (
    <>
      <Navbar />

      <div className="page space-y-8">
        {/* 🔙 BACK */}
        <button onClick={() => navigate("/about")} className="text-blue-600">
          ← Back
        </button>

        {/* TITLE */}
        <h2 className="text-3xl font-semibold">About ReviewGuard</h2>

        {/* 🔹 OVERVIEW */}
        <Card>
          <h3 className="font-semibold mb-2">Overview</h3>
          <p className="text-sm text-gray-600">
            ReviewGuard is an AI-based system that detects fake product reviews.
            It analyzes review text and ratings to classify them as genuine or
            fake. The goal is to help users trust reviews and make better
            decisions.
          </p>
        </Card>

        {/* 🔹 PIPELINE */}
        <Card>
          <h3 className="font-semibold mb-3">Processing Pipeline</h3>
          <div className="text-sm text-gray-600 space-y-1">
            <p>• Collect reviews from product pages</p>
            <p>• Clean and preprocess the data</p>
            <p>• Combine text and rating information</p>
            <p>• Apply AI model for classification</p>
            <p>• Generate results and insights</p>
          </div>
        </Card>

        {/* 🔹 ARCHITECTURE */}
        <Card>
          <h3 className="font-semibold mb-4">System Architecture</h3>

          <img
            src="/system flowchart.png"
            alt="System Architecture"
            className="w-[400px] mx-auto rounded-xl border"
          />

          <p className="text-sm text-gray-600 mt-3 text-center">
            Modular design for better scalability and performance.
          </p>
        </Card>

        {/* 🔹 MODELS */}
        <Card>
          <h3 className="font-semibold mb-2">Models & Performance</h3>
          <p className="text-sm text-gray-600">
            Different models like Logistic Regression, SVM, Random Forest, and
            DistilBERT were tested. RoBERTa performed best with around 96%
            F1-score, providing accurate and reliable predictions.
          </p>
        </Card>

        {/* 🔹 FEATURES */}
        <Card>
          <h3 className="font-semibold mb-2">Key Features</h3>
          <ul className="text-sm text-gray-600 list-disc ml-5 space-y-1">
            <li>Real-time review analysis</li>
            <li>AI-based fake detection</li>
            <li>Clear trust score and insights</li>
            <li>Fast and responsive interface</li>
            <li>Easy to use for all users</li>
          </ul>
        </Card>

        {/* 🔹 USE CASE */}
        <Card>
          <h3 className="font-semibold mb-2">Use Cases</h3>
          <p className="text-sm text-gray-600">
            Helps online shoppers verify reviews before buying. Useful for
            researchers studying fake review patterns. Supports businesses in
            maintaining review authenticity.
          </p>
        </Card>

        {/* 🔹 WHY */}
        <Card>
          <h3 className="font-semibold mb-2">Why ReviewGuard?</h3>
          <ul className="text-sm text-gray-600 list-disc ml-5 space-y-1">
            <li>Reduces confusion caused by fake reviews</li>
            <li>Improves trust in online shopping</li>
            <li>Saves time by analyzing reviews instantly</li>
            <li>Detects patterns not visible to humans</li>
            <li>Provides simple and clear insights</li>
          </ul>
        </Card>

        {/* 🔹 LIMITATIONS */}
        <Card>
          <h3 className="font-semibold mb-2">Limitations</h3>
          <ul className="text-sm text-gray-600 list-disc ml-5 space-y-1">
            <li>Currently supports limited platforms (mainly Flipkart)</li>
            <li>
              Depends on website structure — scraping may break if UI changes
            </li>
            <li>Limited behavioral features (only text + rating used)</li>
            <li>May misclassify short or ambiguous reviews</li>
            <li>Struggles with sarcasm or mixed sentiment reviews</li>
            <li>Model performance depends on training dataset quality</li>
            <li>Real-time scraping can be slow for large datasets</li>
            <li>No explainability — users cannot see why a review is fake</li>
          </ul>
        </Card>

        {/* 🔹 FUTURE */}
        <Card>
          <h3 className="font-semibold mb-2">Future Improvements</h3>
          <ul className="text-sm text-gray-600 list-disc ml-5 space-y-1">
            <li>Add support for multiple platforms (Amazon, Myntra, etc.)</li>
            <li>
              Include behavioral signals (review frequency, user patterns)
            </li>
            <li>Implement Explainable AI (show why a review is fake)</li>
            <li>Use model ensemble for better accuracy</li>
            <li>Optimize scraping speed and performance</li>
            <li>Deploy system on cloud for scalability</li>
            <li>Build browser extension for real-time detection</li>
            <li>Add multilingual support for regional languages</li>
          </ul>
        </Card>
      </div>
    </>
  );
}
