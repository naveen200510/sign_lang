import { useState, useRef, useEffect } from "react";


import Header from "./components/Header";
import CameraFeed from "./components/CameraFeed";
import TranslationCard from "./components/TranslationCard";
import ConfidenceBar from "./components/ConfidenceBar";
import Controls from "./components/Controls";
import HistoryPanel from "./components/HistoryPanel";
import StatusPanel from "./components/StatusPanel";

function App() {

  useEffect(() => {
  return () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
  };
}, []);

  const intervalRef = useRef(null);
  const [translation, setTranslation] = useState(
    "Press Start to begin translation"
  );

  const [cameraOn, setCameraOn] = useState(true);

  const [confidence, setConfidence] = useState(92);

  const [history, setHistory] = useState([]);

  const [isProcessing, setIsProcessing] = useState(false);

  const handleStart = async () => {

  if (intervalRef.current) return;

  setIsProcessing(true);
  setTranslation("Starting camera...");

  try {

    await fetch(
      "http://127.0.0.1:5000/start",
      {
        method: "POST"
      }
    );

    intervalRef.current = setInterval(async () => {

      const response = await fetch(
        "http://127.0.0.1:5000/latest_prediction"
      );

      const data = await response.json();

      if (data.translation) {

        setTranslation(data.translation);

        setConfidence(
          Math.round(data.confidence * 100)
        );

        setHistory(prev => {

          if (prev[0] === data.translation)
            return prev;

          return [
            data.translation,
            ...prev
          ];

        });

      }

    }, 300);

  } catch (error) {

    console.error(error);

    setTranslation("Backend Error");

  }

};

const handleStop = async () => {

  clearInterval(intervalRef.current);
  intervalRef.current = null;

  await fetch(
    "http://127.0.0.1:5000/stop",
    {
      method: "POST"
    }
  );

  setIsProcessing(false);
  setTranslation("Translation Stopped");
};

  const handleSpeak = () => {
    const speech =
      new SpeechSynthesisUtterance(translation);

    speechSynthesis.speak(speech);
  };

  return (
    <div className="min-h-screen bg-gray-100 text-gray-900">
      <Header />

      <main className="max-w-7xl mx-auto grid lg:grid-cols-2 gap-6 p-6">
        <CameraFeed
          cameraOn={cameraOn}
          setCameraOn={setCameraOn}
        />

        <div className="space-y-4">
          <TranslationCard text={translation} />

          <StatusPanel
            cameraOn={cameraOn}
            translation={translation}
            isProcessing={isProcessing}
          />

          <ConfidenceBar confidence={confidence} />

          <Controls
            onStart={handleStart}
            onStop={handleStop}
            onSpeak={handleSpeak}
          />

          <HistoryPanel history={history} />
        </div>
      </main>
    </div>
  );
}

export default App;